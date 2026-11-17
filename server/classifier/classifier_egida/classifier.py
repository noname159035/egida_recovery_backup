import logging
from pathlib import Path

import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification, AutoModelForCausalLM, pipeline, logging as hf_logging
from peft import PeftModel, PeftConfig

hf_logging.set_verbosity_error()
logging.basicConfig(level=logging.INFO, format="%(asctime)s %(levelname)s [%(name)s] %(message)s")
logger = logging.getLogger(__name__)

id2label = {0: "Safe", 1: "Injection", 2: "Injection", 3: "Jailbreak", 4: "Generic Attack"}

CURRENT_DIR = Path(__file__).parent
SHORT_DIR = CURRENT_DIR / "model-short-texts"
LONG_DIR = CURRENT_DIR / "model-long-texts"

LLAMA_GUARD_DIR = CURRENT_DIR / "classifier"
if not LLAMA_GUARD_DIR.exists():
    raise FileNotFoundError

lg_tok = AutoTokenizer.from_pretrained(LLAMA_GUARD_DIR, local_files_only=True)
lg_mod = AutoModelForCausalLM.from_pretrained(
    LLAMA_GUARD_DIR,
    local_files_only=True,
    device_map="auto",
    torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
)

def _load_model(mdir: Path, n_labels: int, device: torch.device):
    if (mdir / "config.json").exists():
        model = AutoModelForSequenceClassification.from_pretrained(
            mdir, num_labels=n_labels, ignore_mismatched_sizes=True, local_files_only=True
        )
    elif (mdir / "adapter_config.json").exists():
        peft_cfg = PeftConfig.from_pretrained(mdir, local_files_only=True)
        base = AutoModelForSequenceClassification.from_pretrained(
            peft_cfg.base_model_name_or_path,
            num_labels=n_labels,
            ignore_mismatched_sizes=True,
            local_files_only=True,
        )
        model = PeftModel.from_pretrained(base, mdir, local_files_only=True)
    else:
        raise ValueError
    return model.to(device).eval()

def _init_egida():
    for d in (SHORT_DIR, LONG_DIR):
        if not d.exists():
            raise FileNotFoundError
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    short_tok = AutoTokenizer.from_pretrained(SHORT_DIR, local_files_only=True)
    long_tok = AutoTokenizer.from_pretrained(LONG_DIR, local_files_only=True)
    short_mod = _load_model(SHORT_DIR, 5, device)
    long_mod = _load_model(LONG_DIR, 5, device)
    return short_tok, short_mod, long_tok, long_mod, device

short_tok, short_mod, long_tok, long_mod, device = _init_egida()

def _egida_label(text: str):
    if len(short_tok(text)["input_ids"]) <= 5:
        model, tokenizer, max_len, name = short_mod, short_tok, 8, "short"
    else:
        model, tokenizer, max_len, name = long_mod, long_tok, 1200, "long"
    inputs = tokenizer(text, max_length=max_len, truncation=True, padding="max_length", return_tensors="pt").to(device)
    with torch.no_grad():
        logits = model(**inputs).logits
    return id2label[int(logits.argmax(dim=-1).cpu())], name

def _guard_verdict(text: str) -> str:
    conv = [{"role": "user", "content": [{"type": "text", "text": text}]}]
    print(text)
    ids = lg_tok.apply_chat_template(conv, return_tensors="pt").to(lg_mod.device)
    pl = ids.shape[1]
    out = lg_mod.generate(ids, max_new_tokens=8, pad_token_id=0)
    gen = out[:, pl:]
    return lg_tok.decode(gen[0]).strip().lower()

def check_text(text: str):
    verdict = _guard_verdict(text)
    if verdict.startswith("safe"):
        return "Safe", "llama-guard"
    egida_label, model_name = _egida_label(text)
    if egida_label == "Safe":
        return "Harmful", f"lg+{model_name}"
    return egida_label, model_name

