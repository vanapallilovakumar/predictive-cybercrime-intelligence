# PRAHARI & CYBER SAFELY: Predictive Cybercrime Cash-Out Forecasting & Citizen Protection
## Document 02: Technical Requirements Document (TRD)

---

### 1. Architectural Topology & Dual-Portal Design

PRAHARI & Cyber Safely is engineered as a **Two-Tier Pure-Python System** integrated with **Supabase Cloud (PostgreSQL, PostGIS, Supabase Auth Email OTP, and Supabase Storage)**.

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│                                   PRESENTATION TIER                                    │
│   Streamlit Web Application (Port 8501)                                                │
│   ├── [Citizen Portal: "Cyber Safely"]                                                 │
│   │   ├── Authentication: Supabase Native Email OTP Login                              │
│   │   ├── Phishing Link Scanner: Real-time fraud URL check & safety awareness          │
│   │   ├── Crime Reporting: Form with victim bank details & receipt/screenshot upload   │
│   │   ├── Status Tracker: Real-time case tracking by reference number                  │
│   │   └── Safety Guidance: Interactive DOs/DONTs cards & 1930 Golden Hour advice       │
│   │                                                                                    │
│   └── [Investigator Portal: "PRAHARI Command"]                                         │
│       ├── Command Dashboard: 4 KPIs, 24h withdrawal pattern, district risk, anomalies  │
│       ├── Hotspots Map: Interactive Uber H3 Hexagonal Grid (Res 7/8)                   │
│       ├── Alerts Queue: Actionable leads, status updates, 1-click Bank Freeze Notice   │
│       └── Scenario Selector: Active Mule Surge vs Digital Arrest Corridor             │
└───────────────────────────────────────────▲────────────────────────────────────────────┘
                                            │ HTTP REST (JSON)
                                            │ requests / httpx
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                             APPLICATION & AI SERVICE TIER                              │
│   FastAPI Microservice (Port 8000)                                                     │
│   ├── /api/v1/cyber-safely/scan-link     (Hybrid Phishing & Fraud Link Scanner)        │
│   ├── /api/v1/cyber-safely/report-crime  (Citizen crime intake & storage dispatch)     │
│   ├── /api/v1/cyber-safely/track/{ref}   (Public case status lookup)                   │
│   ├── /api/v1/command/*                  (KPI aggregations, charts, anomalies)         │
│   ├── /api/v1/hotspots                   (H3 spatio-temporal binning & cell scoring)   │
│   ├── /api/v1/alerts                     (Ranked alert queue & reason codes)           │
│   └── /api/v1/scenarios                  (Deterministic demo scenario manager)         │
│                                                                                        │
│   AI & Security Inference Engine (In-Memory serialized .pkl models + Threat Engine)   │
│   ├── Model 1: Gradient Boosting (Cell Cash-Out Probability for next 6h)               │
│   ├── Model 2: DBSCAN (Mule Syndicate Spatio-Temporal Clustering)                      │
│   ├── Model 3: Isolation Forest (Late-Night & Velocity Anomaly Detector)               │
│   ├── Threat Scanner: Heuristic Lexical Rules + Google Safe Browsing / VirusTotal API  │
│   └── Reason Code Synthesizer (Plain-English investigative rationale)                  │
└───────────────────────────────────────────▲────────────────────────────────────────────┘
                                            │ Supabase Python SDK
                                            │ supabase-py
┌───────────────────────────────────────────▼────────────────────────────────────────────┐
│                               PERSISTENCE & CLOUD TIER                                 │
│   Supabase Cloud Platform                                                              │
│   ├── PostgreSQL 15 + PostGIS            (Relational & spatial database)               │
│   │   ├── complaints                     (NCRP cases, victim accounts, status)         │
│   │   ├── cashout_nodes                  (ATMs, CSP kiosks, bank branches, H3 indices) │
│   │   ├── spatial_forecasts              (Versioned cell scores, probabilities)        │
│   │   ├── alerts                         (Actionable leads, status, reason codes)      │
│   │   └── scenarios                      (Pre-computed demo scenario records)          │
│   │                                                                                    │
│   ├── Supabase Auth                      (Native Email OTP sign-in / verification)     │
│   └── Supabase Storage                   (Bucket: 'complaint-evidence' for screenshots)│
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

### 2. "Cyber Safely" Phishing & Fraud Link Analysis Subsystem

The Phishing Scanner protects citizens **before** they enter personal details or transfer money. It utilizes a **Hybrid Detection Architecture**:

```
Suspicious URL Input (e.g. "http://sbi-reward-kyc.top/claim-bonus.apk")
                              │
               ┌──────────────┴──────────────┐
               ▼                             ▼
   [ Layer 1: Python Heuristics ]    [ Layer 2: Threat API Check ]
   • Brand Impersonation Regex       • Google Safe Browsing v4
     (sbi, hdfc, pnb, paytm, etc.)   • VirusTotal URL Lookup
   • Suspicious TLD Detection          (Async query with 2s timeout)
     (.top, .xyz, .site, .vip, .tk)                  │
   • Malicious APK Extension                         │
   • IP Address Host Detection                       │
   • High Domain Entropy                             │
               │                                     │
               └──────────────┬──────────────────────┘
                              ▼
                 [ Threat Fusion Engine ]
                              │
         ┌────────────────────┼────────────────────┐
         ▼                    ▼                    ▼
   MALICIOUS_PHISHING      SUSPICIOUS             SAFE
   (Score: 0.85 - 1.0)  (Score: 0.40 - 0.84)   (Score: < 0.40)
         │
         ▼
   Streamlit Warning Banner:
   "⚠️ DANGER: Malicious Phishing Website Detected!
    This link is impersonating State Bank of India to steal net banking credentials.
    Do NOT enter OTP or download APK files from this site."
```

#### 2.1 Layer 1: Python Rule-Based & Lexical Features
* **Brand Impersonation Matching:** Regex patterns detecting Indian bank and payment brands in domain or path where the base domain is not official:
  `r"(sbi|statebank|hdfc|icici|punjabnational|pnb|paytm|phonepe|gpay|yono)"` combined with non-official second-level domains.
* **Suspicious Top-Level Domains (TLDs):** Flags free/cheap TLDs heavily abused by cyber fraudsters (`.top`, `.xyz`, `.club`, `.tk`, `.site`, `.vip`, `.buzz`, `.fit`).
* **APK Download Lure:** Flags URLs pointing directly to Android `.apk` package files, a common vector for remote access trojans (RATs) and fake loan apps.
* **IP-as-Host:** Identifies URLs using raw IP addresses (e.g. `http://192.168.1.10/login`) instead of registered domains.

#### 2.2 Layer 2: External Threat Intelligence Integration
* Evaluates domain reputations against Google Safe Browsing Lookup API (or VirusTotal API).
* If external API key is absent or network fails, Layer 1 provides immediate, zero-lag offline detection.

---

### 3. Supabase Auth & Storage Technical Integration

#### 3.1 Citizen Authentication via Native Email OTP
* **Sign-in Request:**
  ```python
  from supabase import Client

  def request_citizen_otp(supabase: Client, email: str):
      """Requests a 6-digit verification code sent to the citizen's email."""
      return supabase.auth.sign_in_with_otp({"email": email})
  ```
* **Verify OTP Request:**
  ```python
  def verify_citizen_otp(supabase: Client, email: str, token: str):
      """Verifies the 6-digit OTP code and returns authenticated session."""
      return supabase.auth.verify_otp({"email": email, "token": token, "type": "email"})
  ```

#### 3.2 Citizen Evidence Upload via Supabase Storage
* **Bucket Name:** `complaint-evidence` (Public Read / Authenticated Write, or Service Key upload).
* **Storage Path Pattern:** `evidence/{reference_no}/{filename}`
* **Upload Implementation:**
  ```python
  def upload_complaint_evidence(supabase: Client, reference_no: str, file_bytes: bytes, filename: str, content_type: str):
      file_path = f"evidence/{reference_no}/{filename}"
      supabase.storage.from_("complaint-evidence").upload(
          path=file_path,
          file=file_bytes,
          file_options={"content-type": content_type}
      )
      return supabase.storage.from_("complaint-evidence").get_public_url(file_path)
  ```

---

### 4. FastAPI REST API Endpoints Specification

#### 4.1 Citizen Portal Endpoints ("Cyber Safely")

* **`POST /api/v1/cyber-safely/scan-link`**
  * **Request Body:**
    ```json
    {"url": "http://sbi-reward-kyc.top/claim-bonus"}
    ```
  * **Response:**
    ```json
    {
      "url": "http://sbi-reward-kyc.top/claim-bonus",
      "verdict": "MALICIOUS_PHISHING",
      "threat_score": 0.92,
      "risk_factors": [
        "Brand impersonation detected: State Bank of India ('sbi')",
        "High-risk untrusted top-level domain: '.top'",
        "Suspicious credential harvesting keywords: 'kyc', 'bonus'"
      ],
      "safety_guidance": "DO NOT open this link or enter bank account numbers, passwords, or OTPs. Official SBI portals only use 'onlinesbi.sbi' or 'sbi.co.in'."
    }
    ```

* **`POST /api/v1/cyber-safely/report-crime`**
  * **Request Body (Multipart Form or JSON with Storage URL):**
    ```json
    {
      "typology": "OTP fraud",
      "loss_amount_inr": 148000,
      "victim_name": "Rohan Sharma",
      "victim_email": "rohan@example.com",
      "victim_account_no": "XXXXXX1290",
      "victim_bank_name": "State Bank of India",
      "victim_district": "Pune",
      "beneficiary_bank": "Bank of India",
      "beneficiary_account": "XXXXXX4921",
      "reported_district": "Deoghar",
      "incident_timestamp": "2026-09-12T17:30:00Z",
      "description": "Caller claimed to be bank officer, requested OTP for card update",
      "evidence_urls": ["https://xyz.supabase.co/storage/v1/object/public/complaint-evidence/..."]
    }
    ```
  * **Response:**
    ```json
    {
      "success": true,
      "reference_no": "NCRP/2026/000188",
      "tracking_status": "Under Review",
      "assigned_officer": "Inspector Vikram (Cyber Cell)",
      "message": "Complaint successfully registered. Our AI forecasting system has alerted patrol units to likely cash-out points."
    }
    ```

* **`GET /api/v1/cyber-safely/track/{reference_no}`**
  * **Response:**
    ```json
    {
      "reference_no": "NCRP/2026/000181",
      "typology": "UPI fraud",
      "loss_amount_inr": 148000,
      "filing_date": "2026-09-12T15:30:00Z",
      "tracking_status": "Action in Progress",
      "assigned_officer": "Inspector Vikram (State Cyber Crime Police Station)",
      "status_notes": "Patrol alerted to Deoghar Bus Stand ATM corridor; Bank Freeze Notice issued to Bank of India."
    }
    ```

#### 4.2 Investigator Command Endpoints ("PRAHARI Command")
*(Maintains all existing endpoints from v1.0)*
* `GET /health`
* `GET /api/v1/scenarios` & `POST /api/v1/scenarios/{id}/activate`
* `GET /api/v1/command/stats`
* `GET /api/v1/command/timing-pattern`
* `GET /api/v1/command/district-risk`
* `GET /api/v1/command/typology-mix`
* `GET /api/v1/command/anomalies`
* `GET /api/v1/hotspots?window_hours=6`
* `GET /api/v1/alerts`
* `PATCH /api/v1/alerts/{alert_id}/status`

---

### 5. AI Spatio-Temporal Modeling Architecture

*(Preserved exactly from v1.0)*
* **Model 1 (Gradient Boosting):** Forecasts probability $P(\text{cash-out} \in \text{next 6h})$ per H3 cell.
* **Model 2 (DBSCAN Clustering):** Groups multi-ATM mule hopping runs using spatio-temporal distance.
* **Model 3 (Isolation Forest):** Flags late-night freeze evasion and loss amounts $> 2.1\times$ standard deviation.
* **Reason Code Synthesizer:** Produces plain-English justifications for court-defensible actions.
