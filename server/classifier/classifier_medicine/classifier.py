import logging
import os
from pathlib import Path
import torch
from peft import PeftModel
from transformers import AutoModelForCausalLM, AutoTokenizer


os.environ["CUDA_VISIBLE_DEVICES"] = "4"

EVAL_BATCH_SIZE = 2

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)

def _init_model():
    logger.info('Medicine classifier inizializing started')

    current_dir = Path(__file__).parent
    model_path = current_dir / "checkpoint-488"
    prompt_path = current_dir / "medicine_input_prompt.txt"

    if not model_path.exists():
        raise FileNotFoundError(f"Model directory {model_path} not found")
    
    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file {prompt_path} not found")

    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    torch.manual_seed(42)
    try:
        tokenizer = AutoTokenizer.from_pretrained(model_path)
        tokenizer.pad_token = tokenizer.eos_token  # важно для генерации
        base_model = AutoModelForCausalLM.from_pretrained("Qwen/Qwen2.5-0.5B-Instruct")
        model = PeftModel.from_pretrained(base_model, model_path)
        model.to(device)
        model.eval()
    except Exception as e:
        raise RuntimeError(f"Model loading failed: {e}")

    with open(prompt_path, "r") as f:
        classifier_prompt = f.read()

    logger.info('Medicine classifier inizializing ended')
    return model, tokenizer, classifier_prompt, device

model, tokenizer, classifier_prompt, device = _init_model()


def check_medicine(prompt: str) -> str|None:
    formatted_prompt = classifier_prompt.replace("{prompt}", str(prompt))
    tokenized_input = tokenizer(formatted_prompt, return_tensors="pt").to(device)

    with torch.no_grad():
        generated_ids = model.generate(
            **tokenized_input,
            max_new_tokens=1,
            do_sample=False, 
            temperature=None,
            top_p=None,
            top_k=None, 
            num_beams=1,      
            pad_token_id=tokenizer.pad_token_id
        )

    generated_text = tokenizer.decode(generated_ids[0], skip_special_tokens=True)
    answer = generated_text.replace(formatted_prompt, '').strip()
    
    if not answer:
        return None
    return "Medicine" if answer == "Yes" else None
