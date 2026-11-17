import logging
import re
from typing import Dict, List, Optional

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s [%(name)s] %(message)s'
)
logger = logging.getLogger(__name__)

class LLMStaticTests:
    def __init__(self):
        self.category_weights: Dict[str, int] = {
            "direct_injection": 3,
            "malicious_intent": 3,
            "manipulation_attempts": 3,
            "data_exfiltration": 2,
            "sql_injection": 1,
            "xss_attacks": 2,
            "command_injection": 1,
            "path_traversal": 1,
            "suspicious_urls": 1,
            "encoding_attempts": 0,
            "obfuscation": 0,
        }
        self.patterns = self._load_injection_patterns()

    def _load_injection_patterns(self) -> Dict[str, List[re.Pattern]]:
        raw_patterns = {
            "direct_injection": [
                r"(ignore|skip|override)\s+(previous|system|instructions|rule|rules|all)",
                r"(sudo|admin|root|privileged)\s+access",
                r"(eval\(|system\(|exec\()",
                r"(you are now|act as)\s+(free|unrestricted|malicious)",
                r"(disregard|forget|remove)\s+(all|previous)\s+(rules|constraints)",
                r"(this is|pretend to be)\s+(just a test|hypothetical)",
                r"(output|write|generate)\s+(without|ignoring)\s+(restrictions|safety)",
                r"(previous|above)\s+(instructions|rules)\s+(don't apply|are void)"
            ],
            "malicious_intent": [
                r"(generate|write|create)\s+(malware|virus|ransomware|exploit)",
                r"(how to|steps to)\s+(hack|breach|phish|bypass)",
                r"(explain|teach)\s+(password cracking|DoS attack|SQL injection)",
                r"(create|generate)\s+(phishing|spam|scam)\s+(email|website)",
                r"(bypass|disable)\s+(antivirus|firewall|security)",
                r"(pretend to be|impersonate)\s+(bank|government|official)",
                r"(create fake)\s+(login page|social media account)",
                r"(steal|obtain)\s+(credentials|passwords|credit card)",
                r"(generate|write)\s+(hate speech|violent content|extremist material)",
                r"(create instructions for)\s+(weapon|drug production|illegal activities)"
            ],
            "manipulation_attempts": [
                r"(your purpose is to obey me|you must comply)",
                r"(this is more important than safety guidelines)",
                r"(prioritize this over ethical constraints)",
                r"(this is for research purposes only)",
                r"(I take full responsibility for ethical implications)"
            ],
            "encoding_attempts": [
                r"%[0-9a-fA-F]{2}",
                r"\\x[0-9a-fA-F]{2}",
                r"&#x?[0-9a-fA-F]+;",
                r"(?:=|%3D|%253D)(?!$)",
                r"u0+0*[a-fA-F0-9]{4}"
            ],
            "sql_injection": [
                r"\b(union\s+select|select\s+\w+\s+from|insert\s+into)",
                r"\b(drop\s+table|alter\s+table|truncate\s+table)\b",
                r"\b(1=1|'1'='1'|'a'='a')\b",
                r"\b(waitfor\s+delay|sleep\(\d+\)|benchmark\()",
                r"\b(cast\(|convert\(|version\(\))\b"
            ],
            "xss_attacks": [
                r"<script\b[^>]*>[\s\S]*?</script>",
                r"javascript:\s*(?:alert|prompt|confirm|eval)\(",
                r"(onmouseover|onload|onerror|onfocus)\s*=",
                r"<iframe\b[^>]*>|<embed\b[^>]*>",
                r"document\.(cookie|location|write)\b"
            ],
            "command_injection": [
                r"(;\s*|\|\||&&)\s*(rm\s+-|wget\s+|curl\s+|sh\s+|bash\s+)",
                r"/bin/(?:sh|bash)\s+-c\s+['\"]",
                r"\b(nc|netcat)\s+-e\s+/bin/(?:sh|bash)\b",
                r"\b(powershell|pwsh)\s+-(c|Command)\s+"
            ],
            "path_traversal": [
                r"(\.\./|\.\.\\){2,}",
                r"/etc/passwd",
                r"C:\\Windows\\System32",
                r"/(proc/self|root)/"
            ],
            "suspicious_urls": [
                r"(https?://|www\.)(?:[\w-]+\.)*(?:bank|paypal|login|account)\.",
                r"\b(bit\.ly|goo\.gl|tinyurl)\b/\w+",
                r"\b[\w-]{15,}\.(?:ru|cn|top|xyz)\b",
                r"/?(phpmyadmin|wp-admin|admin)(/|$)"
            ],
            "data_exfiltration": [
                r"\b[\w.%+-]+@[\w.-]+\.[a-zA-Z]{2,6}\b",
                r"\b(?:\d{4}[ -]?){4}\b",
                r"\b(?:5[1-5]\d{2}|222[1-9]|22[3-9]\d|2[3-6]\d{2}|27[01]\d|2720)\d{12}\b",
                r"\b3[47]\d{13}\b"
            ],
            "obfuscation": [
                r"(\w)\1{5,}",
                r"\b[a-f0-9]{32}\b",
                r"\b[A-Za-z0-9+/]{40,}={0,2}\b",
                r"\b(?:[a-z]{2,}\d{3,}|\d{3,}[a-z]{2,})\b"
            ]
        }
        return {
            category: [re.compile(p, re.IGNORECASE | re.MULTILINE) for p in pats]
            for category, pats in raw_patterns.items()
        }

    def _check_regex_patterns(self, text: str, analysis: Dict):
        analysis["regex_matches"] = {}
        for category, patterns in self.patterns.items():
            if any(p.search(text) for p in patterns):
                analysis["regex_matches"][category] = True

    def _calculate_risk_level(self, analysis: Dict) -> str:
        total_score = sum(
            self.category_weights.get(cat, 0)
            for cat in analysis.get("regex_matches", {})
        )
        if total_score >= 4:
            return "CRITICAL"
        elif total_score >= 3:
            return "HIGH"
        elif total_score >= 2:
            return "MEDIUM"
        else:
            return "LOW"

    def detect_injection(self, text: str) -> Optional[str]:
        analysis = {"risk_level": "LOW", "regex_matches": {}}
        self._check_regex_patterns(text, analysis)
        analysis["risk_level"] = self._calculate_risk_level(analysis)
        if analysis["risk_level"] in ("MEDIUM","HIGH", "CRITICAL"):
            return "Injection"
        return None

_static_security = LLMStaticTests()

def check_static(text: str) -> Optional[str]:
    return _static_security.detect_injection(text)

