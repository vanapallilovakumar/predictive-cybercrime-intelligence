# PRAHARI & CYBER SAFELY: Predictive Cybercrime Cash-Out Forecasting & Citizen Protection
## Document 06: Implementation Plan & Step-by-Step Build Guide

---

### 1. Updated Repository Layout & Architecture

```
predictive cybercrime/
├── docs/                                    # Architectural & Requirement Specifications (v2.0)
│   ├── 01_product_requirements_document.md
│   ├── 02_technical_requirements_document.md
│   ├── 03_workflow_and_app_flow.md
│   ├── 04_ui_ux_specification.md
│   ├── 05_backend_schema_and_supabase.md
│   └── 06_implementation_plan.md
│
├── backend/                                 # FastAPI Backend & Intelligence Services
│   ├── __init__.py
│   ├── app.py                               # FastAPI REST API route definitions
│   ├── config.py                            # Pydantic settings & environment management
│   ├── db.py                                # Supabase Auth, Storage & DB client helpers
│   ├── models.py                            # Pydantic schemas (Request/Response validation)
│   ├── cyber_safely/                        # Citizen Safety Subsystem
│   │   ├── __init__.py
│   │   ├── scanner.py                       # Hybrid Phishing & Fraud Link Threat Scanner
│   │   └── guidance.py                      # Typology DOs/DONTs & 1930 Golden Hour guide
│   ├── ml_pipeline/                         # Spatio-Temporal AI Subsystem
│   │   ├── __init__.py
│   │   ├── features.py                      # Spatio-temporal feature extraction & H3 binning
│   │   ├── train.py                         # One-command model training script
│   │   ├── inference.py                     # Inference engine & reason code synthesizer
│   │   └── weights/                         # Serialized model weights (.pkl)
│   │       ├── hotspot_model.pkl
│   │       └── anomaly_model.pkl
│   └── data/
│       └── mock_scenarios.json              # Local fallback offline presentation data
│
├── frontend/                                # Pure-Python Streamlit Web Dashboard
│   ├── app.py                               # Main launcher & portal router (Citizen vs Command)
│   ├── theme.py                             # Custom CSS injector (Dark console + Citizen card theme)
│   ├── api_client.py                        # HTTP client consuming FastAPI endpoints
│   ├── citizen/                             # Citizen Portal Screens ("Cyber Safely")
│   │   ├── login_view.py                    # Supabase Native Email OTP Login Card
│   │   ├── link_scanner_view.py             # Phishing & Fraud Link Checker
│   │   ├── report_crime_view.py             # Complaint intake form & receipt file uploader
│   │   ├── track_status_view.py             # Reference number status lookup & simple badge
│   │   └── safety_guidance_view.py          # Typology DOs/DONTs & Golden Hour advisory
│   └── command/                             # Police Investigator Screens ("PRAHARI Command")
│       ├── overview_view.py                 # KPIs, 24h withdrawal pattern, district risk
│       ├── hotspots_view.py                 # Interactive Uber H3 Hexagonal Risk Map
│       └── alerts_view.py                   # Prioritized alerts, triage & Bank Freeze Advisory
│
├── requirements.txt                         # Consolidated Python dependencies
├── run_prahari.py                           # 1-Command Launcher (starts FastAPI + Streamlit)
└── README.md                                # Master project documentation
```

---

### 2. Consolidated Dependencies (`requirements.txt`)

```text
# Web Frameworks & Server
fastapi>=0.110.0,<1.0.0
uvicorn[standard]>=0.28.0,<1.0.0
pydantic>=2.6.0,<3.0.0
pydantic-settings>=2.2.0,<3.0.0
requests>=2.31.0,<3.0.0
httpx>=0.27.0,<1.0.0
python-multipart>=0.0.9

# Frontend & Visualization (Pure Python)
streamlit>=1.32.0,<2.0.0
streamlit-folium>=0.17.0,<1.0.0
folium>=0.15.0,<1.0.0
altair>=5.2.0,<6.0.0
plotly>=5.19.0,<6.0.0

# Geospatial & Spatial Indexing
h3>=3.7.6,<4.0.0
shapely>=2.0.0,<3.0.0
geopandas>=0.14.0,<1.0.0

# Machine Learning & Analytics
scikit-learn>=1.4.0,<2.0.0
pandas>=2.2.0,<3.0.0
numpy>=1.26.0,<2.0.0
joblib>=1.3.2,<2.0.0

# Database, Auth & Storage
supabase>=2.4.0,<3.0.0
python-dotenv>=1.0.1,<2.0.0
```

---

### 3. Phishing Link Threat Scanner (`backend/cyber_safely/scanner.py`)

```python
# backend/cyber_safely/scanner.py
import re
import math
from urllib.parse import urlparse
from typing import Dict, Any, List

SUSPICIOUS_TLDS = {".top", ".xyz", ".club", ".site", ".vip", ".buzz", ".fit", ".tk", ".ml", ".ga"}
BANK_BRANDS = ["sbi", "statebank", "hdfc", "icici", "pnb", "punjabnational", "paytm", "phonepe", "yono"]
FRAUD_KEYWORDS = ["kyc", "reward", "bonus", "claim", "lottery", "parttime", "job", "free", "login", "verify"]

def calculate_entropy(s: str) -> float:
    prob = [float(s.count(c)) / len(s) for c in dict.fromkeys(list(s))]
    return -sum([p * math.log(p) / math.log(2.0) for p in prob]) if s else 0.0

def scan_url(url: str) -> Dict[str, Any]:
    url = url.strip()
    if not url.startswith(("http://", "https://")):
        url = "http://" + url
        
    parsed = urlparse(url)
    domain = parsed.netloc.lower()
    path = parsed.path.lower()
    
    risk_factors: List[str] = []
    score = 0.0
    
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
            # Check if domain is legitimate official bank
            official = any(domain.endswith(f".{brand}.co.in") or domain.endswith(f".{brand}.bank") or domain.endswith(f".{brand}.com") for b in [brand])
            if not official:
                score += 0.45
                risk_factors.append(f"Deceptive impersonation of financial brand: '{brand.upper()}'")
                break
                
    # 4. Check APK Download
    if path.endswith(".apk") or ".apk" in url:
        score += 0.40
        risk_factors.append("Direct download link for Android application package (.apk) detected")
        
    # 5. Check Fraud Keywords
    keyword_hits = [kw for kw in FRAUD_KEYWORDS if kw in domain or kw in path]
    if len(keyword_hits) >= 2:
        score += 0.30
        risk_factors.append(f"Contains multiple credential harvesting keywords: {keyword_hits}")
        
    # Cap score
    score = min(score, 1.0)
    
    if score >= 0.70:
        verdict = "MALICIOUS_PHISHING"
        guidance = "DO NOT open this website or fill any forms. This link is identified as a fake phishing portal designed to steal banking credentials."
    elif score >= 0.40:
        verdict = "SUSPICIOUS"
        guidance = "Proceed with extreme caution. This domain exhibits high-risk patterns. Verify with official bank customer care before entering details."
    else:
        verdict = "SAFE"
        guidance = "No overt malicious patterns detected. Always verify that your browser displays a secure connection (https://)."
        
    return {
        "url": url,
        "verdict": verdict,
        "threat_score": round(score, 2),
        "risk_factors": risk_factors,
        "safety_guidance": guidance
    }
```

---

### 4. Step-by-Step Build Roadmap

#### Phase 1: Supabase Configuration
1. Open [supabase.com](https://supabase.com) and navigate to your project.
2. In **SQL Editor**, execute the DDL script from [docs/05_backend_schema_and_supabase.md](docs/05_backend_schema_and_supabase.md).
3. In **Authentication -> Providers -> Email**, ensure Email OTP is enabled.
4. In **Storage**, confirm bucket `complaint-evidence` is created and public.
5. In `.env`:
   ```env
   SUPABASE_URL="https://your-project.supabase.co"
   SUPABASE_KEY="your-anon-key"
   FASTAPI_HOST="127.0.0.1"
   FASTAPI_PORT=8000
   STREAMLIT_PORT=8501
   ```

#### Phase 2: Machine Learning Model Serialization
1. Run `python backend/ml_pipeline/train.py` to generate `hotspot_model.pkl` and `anomaly_model.pkl` in `backend/ml_pipeline/weights/`.

#### Phase 3: FastAPI Backend Services
1. Implement route handlers in `backend/app.py`:
   * `/api/v1/cyber-safely/scan-link` (calling `scanner.scan_url`)
   * `/api/v1/cyber-safely/report-crime` (saving complaint to Supabase and triggering ML re-scoring)
   * `/api/v1/cyber-safely/track/{ref}` (fetching status and assigned officer)
   * `/api/v1/command/*` and `/api/v1/hotspots` (serving predictive command intelligence)

#### Phase 4: Streamlit Dual-Portal Frontend
1. Scaffold `frontend/app.py` with the portal switcher in the header:
   * **Citizen Tab:** Renders Email OTP Login, Phishing Link Scanner, Complaint Reporting Form, Status Tracker, and Safety Guidance.
   * **Command Tab:** Renders the dark command center (KPIs, Recharts-styled charts, H3 Hexagonal Folium Map, and Alert Triage with Section 91 Bank Freeze Notices).

#### Phase 5: End-to-End Testing & Master Demo Runner
1. Launch both services using `python run_prahari.py`.
2. Follow the Verification Checklist below to test all workflows.

---

### 5. Verification & Testing Checklist

| Step | Action | Expected Result | Pass/Fail |
| :--- | :--- | :--- | :--- |
| **1. Email OTP** | Enter email on Citizen Portal | Receives 6-digit OTP code in email; entering code authenticates session | [ ] |
| **2. Phishing Scan (Fake)** | Paste `http://sbi-reward-kyc.top/claim.apk` | Shows Crimson Banner: `MALICIOUS_PHISHING`, flags SBI impersonation & APK | [ ] |
| **3. Phishing Scan (Safe)** | Paste `https://onlinesbi.sbi` | Shows Green Banner: `SAFE`, no malicious patterns detected | [ ] |
| **4. Crime Reporting** | Fill form (Typology: OTP Fraud, ₹1,48,000) & attach PNG | Saves to Supabase Storage; generates `NCRP/2026/XXXXXX` reference | [ ] |
| **5. AI Pipeline Sync** | Check PRAHARI Command Console | Newly reported complaint triggers immediate H3 hex recalculation & High Alert | [ ] |
| **6. Bank Advisory** | Click `Generate Freeze Advisory` in Command | Formats Section 91 BNSS legal freeze notice to beneficiary bank | [ ] |
| **7. Officer Status Update**| Update status to `Action in Progress` | Alert record in Supabase updates with officer notes | [ ] |
| **8. Citizen Tracking** | Enter Ref No on `Track Complaint Status` | Displays Simple Status Badge: `Action in Progress` with assigned officer | [ ] |
| **9. Golden Hour Guide** | Open `Safety Guidance` | Displays 1930 Helpline callout and DOs/DONTs cards | [ ] |
