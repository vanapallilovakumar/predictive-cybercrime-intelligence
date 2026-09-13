import re
import math
from urllib.parse import urlparse
from typing import Dict, Any, List

SUSPICIOUS_TLDS = {".top", ".xyz", ".club", ".site", ".vip", ".buzz", ".fit", ".tk", ".ml", ".ga", ".work", ".live", ".cfd"}
BANK_BRANDS = ["sbi", "statebank", "hdfc", "icici", "pnb", "punjabnational", "paytm", "phonepe", "yono", "axis", "kotak", "canara", "bob"]
FRAUD_KEYWORDS = ["kyc", "reward", "bonus", "claim", "lottery", "parttime", "job", "free", "login", "verify", "update", "arrest", "refund"]

# Official domains for brands to avoid false positives
OFFICIAL_DOMAINS = {
    "sbi": ["onlinesbi.sbi", "sbi.co.in", "bank.sbi"],
    "statebank": ["onlinesbi.sbi", "sbi.co.in", "bank.sbi"],
    "hdfc": ["hdfcbank.com", "hdfc.com"],
    "icici": ["icicibank.com"],
    "pnb": ["pnbindia.in"],
    "punjabnational": ["pnbindia.in"],
    "paytm": ["paytm.com"],
    "phonepe": ["phonepe.com"],
    "yono": ["sbionline.sbi", "sbi.co.in", "onlinesbi.sbi"],
    "axis": ["axisbank.com"],
    "kotak": ["kotak.com"],
    "canara": ["canarabank.com"],
    "bob": ["bankofbaroda.in"]
}

def calculate_entropy(s: str) -> float:
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob]) if s else 0.0

def scan_url(url: str) -> Dict[str, Any]:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
        
    parsed = urlparse(url)
    domain = (parsed.netloc or "").lower()
    path = (parsed.path or "").lower()
    query = (parsed.query or "").lower()
    
    risk_factors: List[str] = []
    score = 0.0
    
    # Check if this is an official verified domain
    for brand, legit_domains in OFFICIAL_DOMAINS.items():
        if any(domain == legit or domain.endswith("." + legit) for legit in legit_domains):
            return {
                "url": url,
                "verdict": "SAFE",
                "threat_score": 0.05,
                "risk_factors": ["Verified legitimate official financial institution domain."],
                "safety_guidance": f"Official domain verified for {brand.upper()}. Always ensure your browser connection is secure."
            }

    # 1. Check IP Host
    if re.match(r"^\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}(:\d+)?$", domain):
        score += 0.50
        risk_factors.append("URL uses raw IP address instead of registered domain name")
        
    # 2. Check Suspicious TLD
    for tld in SUSPICIOUS_TLDS:
        if domain.endswith(tld):
            score += 0.35
            risk_factors.append(f"Registered under high-risk untrusted top-level domain: '{tld}'")
            break
            
    # 3. Check Brand Impersonation
    for brand in BANK_BRANDS:
        if brand in domain or brand in path:
            score += 0.45
            risk_factors.append(f"Deceptive impersonation of financial brand: '{brand.upper()}'")
            break
                
    # 4. Check APK Download Lure
    if path.endswith(".apk") or ".apk" in url:
        score += 0.40
        risk_factors.append("Direct download link for Android application package (.apk) detected")
        
    # 5. Check Fraud Keywords
    keyword_hits = [kw for kw in FRAUD_KEYWORDS if kw in domain or kw in path or kw in query]
    if len(keyword_hits) >= 2:
        score += 0.30
        risk_factors.append(f"Contains multiple credential harvesting keywords: {keyword_hits}")
    elif len(keyword_hits) == 1:
        score += 0.15
        risk_factors.append(f"Contains suspicious keywords: {keyword_hits}")
        
    # 6. Check High Entropy
    ent = calculate_entropy(domain)
    if ent > 3.8 and len(domain) > 15:
        score += 0.20
        risk_factors.append(f"Unusually high domain entropy ({ent:.2f}), typical of algorithmically generated scam domains")
        
    # Cap score between 0.0 and 1.0
    score = min(score, 1.0)
    
    if score >= 0.65:
        verdict = "MALICIOUS_PHISHING"
        guidance = "DO NOT open this website or fill any forms. This link is identified as a fake phishing portal designed to steal banking credentials, OTPs, or install malicious APK software."
    elif score >= 0.35:
        verdict = "SUSPICIOUS"
        guidance = "Proceed with extreme caution. This domain exhibits high-risk patterns. Verify with official bank customer care before entering any personal details."
    else:
        verdict = "SAFE"
        guidance = "No overt malicious patterns detected. Always verify that your browser displays a secure connection (https://) before entering passwords."
        
    return {
        "url": url,
        "verdict": verdict,
        "threat_score": round(score, 2),
        "risk_factors": risk_factors if risk_factors else ["No prominent threat indicators detected."],
        "safety_guidance": guidance
    }
