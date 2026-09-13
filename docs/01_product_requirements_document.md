# PRAHARI & CYBER SAFELY: Predictive Cybercrime Cash-Out Forecasting & Citizen Protection
## Document 01: Product Requirements Document (PRD)

---

### 1. Document Overview & Metadata
* **Project Name:** PRAHARI & Cyber Safely
* **Problem Statement:** SIH26184 — Ministry of Home Affairs (MHA)
* **Team:** TRACE X
* **Target Release:** SIH 2026 Unified MVP Demonstration
* **Document Version:** 2.0.0 (Unified Citizen Portal + Command Intelligence Scope)
* **Tech Stack Mandate:** 100% Python (Streamlit UI, FastAPI Engine), Supabase (PostgreSQL + PostGIS + Supabase Auth Email OTP + Supabase Storage)

---

### 2. Executive Summary & Dual Mission

#### 2.1 The Two Halves of Cybercrime Interception
Combating financial cybercrime requires synchronizing two vital touchpoints:
1. **The Citizen Defense Front ("Cyber Safely"):** Citizens are the first line of defense. When they encounter suspicious phishing links, fake investment portals, or digital arrest threats, they need instant verification to prevent victimization before entering credentials. If fraud has already occurred, citizens require an authenticated, frictionless channel to report incident details, victim bank accounts, and evidence within the crucial **"Golden Hour"**, followed by transparent status tracking.
2. **The Predictive Command Front ("PRAHARI"):** Once complaints are submitted, law enforcement faces the **cash-out latency gap**. Mule syndicates withdraw stolen cash across ATMs/CSP kiosks within 2 to 6 hours. PRAHARI processes scattered citizen complaints through a 3-model spatio-temporal AI engine (Gradient Boosting, DBSCAN clustering, Isolation Forest) to forecast where illicit cash will surface next, enabling rapid patrol dispatch and pre-emptive bank debit freeze advisories.

> **Operational Safeguard (Core Philosophy):**
> *Decision-support, not verdict.* PRAHARI delivers investigative leads and early-warning advisories. It mandates human-in-the-loop validation with beneficiary banks before field dispatch or punitive enforcement.

---

### 3. User Personas & Target Audience

| Persona | Role | Key Jobs to be Done | Pain Points Addressed |
| :--- | :--- | :--- | :--- |
| **Aarav (Indian Citizen / Consumer)** | Citizen encountering suspicious links or victim of cyber fraud | Wants to check if a link received on WhatsApp/SMS is fraudulent before clicking; needs to report lost money (OTP fraud, digital arrest) with bank details and track case progress. | Has no instant tool to verify phishing links; reporting via traditional portals is slow; lacks visibility into whether police took action. |
| **Inspector Vikram (Cyber Cell IO)** | Investigating Officer / Field Police Commander | Needs to prioritize which ATM clusters or CSP hubs in hotspot districts (e.g. Jamtara, Deoghar, Nuh) to monitor or dispatch patrol teams to right now. | Overwhelmed by raw complaint tables; lacks spatio-temporal prioritization; currently acts purely reactively after cash is withdrawn. |
| **Analyst Priya (State Cyber Command)** | Intelligence Analyst at State Cyber Cell | Analyzes cross-jurisdictional syndicate movement, peak withdrawal timing patterns, and emerging fraud typologies. | Cannot correlate scattered complaints across different victim districts with physical mule cash-out nodes. |
| **Nodal Officer Rajesh (Bank Fraud Monitoring)** | Bank Fraud Nodal Officer (Private/PSU Bank) | Receives priority alerts on specific beneficiary accounts and ATM clusters to apply emergency debit freezes or dispatch ATM security. | Receives freeze notices long after ATM withdrawals have emptied the accounts. |

---

### 4. MVP Scope & Boundaries

```
IN-SCOPE (MVP)                                      OUT-OF-SCOPE (Post-MVP / Future)
┌──────────────────────────────────────────────┐    ┌──────────────────────────────────────────────┐
│ • Dual-Portal Streamlit App:                 │    │ • Automated live production NCRP API crawler │
│   - Citizen Portal ("Cyber Safely")          │    │ • Automated core banking direct freeze API   │
│   - Investigator Portal ("PRAHARI Command")  │    │ • Computer vision facial recognition at ATMs │
│ • Citizen Email OTP Login via Supabase Auth  │    │ • Real-time GPS patrol car dispatch tracking │
│ • Phishing & Fraud Link Scanner with safety  │    │ • Multi-tenant department billing & RBAC     │
│   awareness feedback (Hybrid Rule + API)     │    │ • Native Android/iOS mobile application      │
│ • Crime Intake with Evidence Upload to       │    │ • Real victim PII storage (synthetic data    │
│   Supabase Storage ('complaint-evidence')    │    │   only for compliance and safe evaluation)   │
│ • Simple Status Badge Tracking for Citizens  │    │                                              │
│ • Typology Safety Guidance & Golden Hour     │    │                                              │
│ • 3-Model AI Engine: Gradient Boosting,      │    │                                              │
│   DBSCAN Clustering, Isolation Forest        │    │                                              │
│ • H3 Hexagonal Spatial Binning (Res 7/8)     │    │                                              │
│ • 1-Click Field Dispatch & Bank Freeze Notice│    │                                              │
│ • 100% Python Stack (Streamlit + FastAPI)    │    │                                              │
│ • Supabase Cloud (Postgres, Auth, Storage)   │    │                                              │
└──────────────────────────────────────────────┘    └──────────────────────────────────────────────┘
```

---

### 5. Functional Requirements (FR)

#### 5.1 Portal 1: Citizen Safety & Reporting ("Cyber Safely")

* **FR-C1: Citizen Authentication (Email OTP):**
  * Citizen enters email address to request a 6-digit one-time password.
  * System utilizes native Supabase Auth Email OTP (`supabase.auth.sign_in_with_otp`).
  * Citizen enters OTP to verify session (`supabase.auth.verify_otp`), establishing an authenticated session state in Streamlit.
* **FR-C2: Phishing & Fraud Link Scanner ("Cyber Safely Awareness"):**
  * Input field allowing citizens to paste suspicious website links received via SMS, WhatsApp, or email.
  * Hybrid analysis engine: Evaluates domain typosquatting (e.g. `sbi-reward-kyc.top`, `telegram-parttime-job.xyz`), brand impersonation, IP hosts, and APK download patterns, combined with threat API checks.
  * If identified as dangerous/fake: App halts the user with a prominent danger banner:
    * *"Warning: This link is identified as a fraudulent phishing website!"*
    * Explain why (e.g. deceptive domain pretending to be State Bank of India, unverified APK installer).
    * Delivers immediate awareness guidance: *"Do not enter your net banking credentials, ATM PIN, or OTP on this site."*
* **FR-C3: Report a Cybercrime & Upload Evidence:**
  * Categorized reporting form capturing:
    * Crime Typology: Dropdown (OTP Fraud, Digital Arrest, Job Fraud, UPI Fraud, Investment Scam, Loan App Extortion).
    * Victim Financial Loss Details: Amount lost (INR), Victim Account Number, Victim Bank Name, Victim District.
    * Suspect Beneficiary Details: Suspect Beneficiary Bank, Suspect Account Number, Transaction/UPI Reference, Reported Location/ATM.
    * Incident Timestamp & Brief description.
  * Evidence File Uploader: Supports PNG, JPG, PDF (transaction receipts, chat screenshots) uploaded directly to Supabase Storage bucket `complaint-evidence`.
  * Generates a unique tracking acknowledgment number: `NCRP/2026/XXXXXX`.
* **FR-C4: Track Complaint Status (End-to-End Restitution Milestones):**
  * Citizen inputs their Reference Number (`NCRP/2026/000181`).
  * Displays a clean, reassuring **Simple Status Badge** tracking the 4 key stages:
    * `Under Review`: Case registered, undergoing AI spatio-temporal correlation.
    * `Investigation Active`: Sent to Police & Investigation Officer; patrol alerted to ATM node.
    * `Criminal Traced & Money Recovered`: Mule intercepted; stolen funds frozen in beneficiary account via Sec 91 BNSS notice.
    * `Money Returned to Victim`: Restitution order issued under Sec 503 BNSS / 457 CrPC; funds credited back to victim's bank account.
  * Officer / Cyber Cell assigned: e.g. `Assigned to: Inspector Vikram (State Cyber Crime Police Station)`.
  * Case filed timestamp & verified loss amount.
* **FR-C5: View Cyber Safety Guidance:**
  * Typology-specific action cards: Practical DOs & DONTs for OTP scams, Digital Arrest extortion, and Fake Part-Time Job fraud.
  * Urgent **"Golden Hour Advisory"**: Clear instructions explaining that calling the **1930 Helpline** within 2 hours provides an 80%+ chance of recovering fraudulent transfers.

---

#### 5.2 Portal 2: Investigator Command Dashboard ("PRAHARI Command")

* **FR-I1: Command Dashboard (Overview & Situational Awareness):**
  * 4 KPI Panels: Active Complaints & Loss at Risk, Open Alerts, Monitored Cash-Out Nodes, Mean Confidence %.
  * 24h Withdrawal Timing Pattern Line Chart.
  * District Risk Index Progress Bars (Deoghar, Jamtara, Nuh, Bharatpur, Mathura, Giridih).
  * Crime Typology Mix Bar Distribution.
  * Statistical Anomalies Feed (Late-night windows dodging bank freeze desks, loss > 2.1x std dev).
  * Next Opening Windows List & Recent Complaints Table.
* **FR-I2: Predictive Hotspots Map (`/hotspots`):**
  * Interactive Uber H3 Hexagonal Grid (Res 7/8) colored by risk tier: High Risk (> 70%), Watch (40–70%), Normal (< 40%).
  * Time horizon filter (Next 2h, 4h, 6h).
  * Cell drill-down drawer showing linked NCRP complaints, total INR at risk, reason codes, and monitored ATM nodes.
* **FR-I3: Alerts & Legal Advisory Generation (`/alerts`):**
  * Prioritized alert queue with plain-English reason codes.
  * Status management: `OPEN` $\to$ `DISPATCHED` $\to$ `ACKNOWLEDGED` $\to$ `RESOLVED`.
  * 1-Click Dispatch Order & Bank Nodal Freeze Notice (Section 91 CrPC / BNSS legal advisory).
* **FR-I4: Scenario Control & Dynamic Simulation:**
  * Pre-computed Scenario Selector: Scenario A (Active Mule Surge), Scenario B (Digital Arrest Corridor), Scenario C (Baseline Calm).
  * Immediate re-scoring upon citizen complaint submission.

---

### 6. Non-Functional Requirements (NFR)

* **NFR-1 (100% Python Runtime):** All frontend components execute purely via Python (Streamlit 1.32+), eliminating any JavaScript/Node build requirements.
* **NFR-2 (FastAPI Latency):** Phishing link analysis under **< 350ms**; spatio-temporal predictive scoring under **< 1.0s**.
* **NFR-3 (Secure Authentication & Storage):** Citizen sessions authenticated via Supabase Auth Email OTP; evidence files stored securely in Supabase Storage with signed access.
* **NFR-4 (Data Privacy & Compliance):** Synthetic records only for the hackathon prototype; zero real PII stored.
* **NFR-5 (High Availability Demo Fallback):** Automated local JSON fallback ensures the demo never crashes even if external internet drops during judging.

---

### 7. Evaluation & Success Criteria (Hackathon Pitch)

1. **Complete Citizen-to-Police Loop:** A citizen reports an OTP fraud on the "Cyber Safely" portal $\to$ Complaint immediately reflects in the "PRAHARI Command" predictive map as a High-Risk ATM node in Jamtara $\to$ Officer generates a 1-click Bank Freeze Notice.
2. **Proactive Awareness Demonstration:** Entering a malicious phishing link triggers the "Cyber Safely" warning banner and explains why the link is fraudulent before any money is lost.
3. **Transparent Citizen Tracking:** Entering the complaint reference immediately returns the current investigation status badge.
4. **100% Python Feasibility:** The entire dual-portal architecture runs seamlessly via `python run_prahari.py`.
