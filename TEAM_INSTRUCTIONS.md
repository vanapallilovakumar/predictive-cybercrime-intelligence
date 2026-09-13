# PRAHARI & Cyber Safely — Team Instructions

**Project:** PRAHARI & Cyber Safely  
**Team:** TRACE X  
**Hackathon:** Smart India Hackathon 2026  
**Problem Statement:** SIH26184 — Ministry of Home Affairs  
**Runtime:** Python 3.14 on Windows  
**Application type:** Streamlit frontend + FastAPI backend  

This file is the operational guide for the team. It explains how to install, run, demonstrate, develop, test, and troubleshoot the MVP.

---

## 1. Product Overview

PRAHARI & Cyber Safely is a dual-portal predictive cybercrime platform:

### Cyber Safely — Citizen Portal

Citizens can:

- Sign in using mock email OTP authentication.
- Check suspicious links before opening them.
- File cybercrime complaints.
- Upload screenshots, transaction receipts, or PDFs.
- Receive an NCRP-style tracking reference.
- Track investigation and restitution status.
- Read typology-specific safety guidance.
- Call the 1930 National Cyber Crime Helpline during the Golden Hour.

### PRAHARI Command — Investigator Portal

Investigators can:

- View active complaints and financial loss at risk.
- Monitor open alerts and cash-out nodes.
- Review 24-hour cash-out timing patterns.
- Inspect district-level risk.
- Review typology distribution and anomalies.
- View predictive H3 hotspot cells.
- Triage alerts.
- Generate Section 91 BNSS / CrPC bank freeze notices.
- Move alerts through the workflow:

```text
OPEN → DISPATCHED → ACKNOWLEDGED → RESOLVED
```

Alert status changes synchronize with the corresponding citizen complaint:

| Alert status | Citizen-facing status |
|---|---|
| `OPEN` | `Under Review` |
| `DISPATCHED` | `Investigation Active` |
| `ACKNOWLEDGED` | `Criminal Traced` |
| `RESOLVED` | `Returned to Victim` |

The system is a decision-support prototype. It does not automatically freeze bank accounts, dispatch police, or determine guilt. Human investigators and bank nodal officers must validate every lead.

---

## 2. Repository Layout

```text
predictive cybercrime/
├── backend/
│   ├── app.py                         FastAPI routes
│   ├── config.py                      Environment configuration
│   ├── db.py                          Supabase/local persistence and business logic
│   ├── models.py                      Pydantic request/response schemas
│   ├── cyber_safely/
│   │   ├── scanner.py                 Phishing and fraud URL scanner
│   │   └── guidance.py                Golden Hour and typology guidance
│   ├── ml_pipeline/
│   │   ├── features.py                H3 and temporal feature engineering
│   │   ├── inference.py               Probability, anomaly, and reason-code logic
│   │   ├── train.py                   Optional model training script
│   │   └── weights/                   Optional generated model files
│   └── data/
│       ├── mock_scenarios.json        Local live demo dataset
│       └── evidence/                  Local evidence uploads
├── frontend/
│   ├── app.py                         Streamlit router and global navigation
│   ├── api_client.py                  FastAPI client with offline fallbacks
│   ├── theme.py                       Dark tactical theme
│   ├── citizen/                       Citizen portal views
│   └── command/                       Investigator portal views
├── docs/                              Product and technical specifications
├── requirements.txt                   Python dependencies
├── .env                               Local runtime configuration
├── run_prahari.py                     Starts backend and frontend together
├── README.md                          Project summary
└── TEAM_INSTRUCTIONS.md               This guide
```

---

## 3. Prerequisites

Install the following before running the project:

- Windows 10 or Windows 11
- Python 3.14
- Git, if cloning or managing the repository
- Internet access for the first dependency installation

Check the Python version:

```powershell
python --version
```

The expected version is Python 3.14 or a compatible 3.x release supported by the installed packages.

---

## 4. First-Time Installation

Open PowerShell and move to the project directory:

```powershell
cd "C:\Users\Lova kumar\OneDrive\Desktop\predictive cybercrime"
```

### 4.1 Recommended virtual environment

Create a virtual environment:

```powershell
python -m venv .venv
```

Activate it:

```powershell
.\.venv\Scripts\Activate.ps1
```

If PowerShell blocks activation, use the current shell process only:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\.venv\Scripts\Activate.ps1
```

Confirm that the prompt shows `(.venv)`.

### 4.2 Install dependencies

```powershell
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

The main packages are:

- FastAPI and Uvicorn
- Streamlit
- Requests and HTTPX
- Folium and Streamlit-Folium
- Pandas, NumPy, and scikit-learn
- H3
- Supabase client

If dependencies are already installed globally, the virtual environment is still recommended for consistent judging and team development.

---

## 5. Environment Configuration

The project includes a local `.env` configured for mock demo mode:

```env
SUPABASE_URL=
SUPABASE_KEY=

FASTAPI_HOST=127.0.0.1
FASTAPI_PORT=8000
STREAMLIT_PORT=8501

MOCK_AUTH=True
DEMO_BYPASS_OTP=123456
```

### 5.1 Recommended hackathon/demo configuration

Keep the Supabase fields empty and use:

```env
MOCK_AUTH=True
DEMO_BYPASS_OTP=123456
```

This configuration:

- Does not require a real Supabase project.
- Accepts any valid-looking email address.
- Uses OTP `123456`.
- Reads and writes local demo data.
- Stores uploaded evidence locally.
- Allows the judging flow to work without external services.

### 5.2 Optional Supabase configuration

For cloud testing, set:

```env
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your-anon-or-service-key
MOCK_AUTH=False
```

Before enabling this mode:

1. Create a Supabase project.
2. Apply the schema and policies in `docs/05_backend_schema_and_supabase.md`.
3. Create or verify the `complaint-evidence` storage bucket.
4. Enable email OTP authentication.
5. Confirm the credentials are not committed to Git.

The backend still attempts to fall back to local resilience behavior if cloud initialization fails.

---

## 6. Starting the Complete Application

Always launch from the project root because backend imports expect the root on `sys.path`.

```powershell
cd "C:\Users\Lova kumar\OneDrive\Desktop\predictive cybercrime"
python run_prahari.py
```

The launcher starts:

| Service | URL |
|---|---|
| FastAPI backend | http://127.0.0.1:8000 |
| Swagger API docs | http://127.0.0.1:8000/docs |
| Streamlit frontend | http://localhost:8501 |

The launcher:

1. Starts Uvicorn on port `8000`.
2. Waits briefly for the backend.
3. Starts Streamlit on port `8501`.
4. Keeps both services running.
5. Stops both child processes when `Ctrl+C` is pressed.

Do not close the PowerShell window while demonstrating the application.

---

## 7. Starting Services Separately

Separate startup is useful while debugging.

### Backend only

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

### Frontend only

Open a second PowerShell window, move to the root, and run:

```powershell
python -m streamlit run frontend/app.py --server.port 8501 --server.headless true
```

The frontend uses API fallback data when the backend is unavailable, but live complaint submission, alert updates, and tracking updates require the backend.

---

## 8. Login Instructions

1. Open <http://localhost:8501>.
2. Enter any email address, for example:

   ```text
   demo@tracex.example
   ```

3. Select **Send Login Code (OTP)**.
4. Enter:

   ```text
   123456
   ```

5. Select **Verify & Enter Portal**.

The same session can access both portals. There is no real role restriction in the MVP because the judging flow requires the command console to be accessible during a single demonstration.

---

## 9. Recommended Judging Demonstration

Use this sequence for the cleanest end-to-end story.

### Step 1 — Citizen login

Log in with any email and OTP `123456`.

### Step 2 — Detect a malicious link

Open **Citizen Safety → Check Suspicious Link** and paste:

```text
http://sbi-reward-kyc.top/claim-bonus.apk
```

Expected result:

- Verdict: `MALICIOUS_PHISHING`
- Red danger banner
- SBI impersonation warning
- High-risk `.top` domain warning
- APK download warning
- Credential and OTP safety guidance

### Step 3 — Check an official domain

Paste:

```text
https://onlinesbi.sbi
```

Expected result:

- Verdict: `SAFE`
- Green safe banner
- Official SBI domain recognition

### Step 4 — Submit a complaint

Open **Citizen Safety → Report Cybercrime** and use values similar to:

| Field | Demo value |
|---|---|
| Typology | `OTP fraud` |
| Amount | `148000` |
| Name | `Rohan Sharma` |
| Victim bank | `State Bank of India` |
| Victim account | `XXXXXX1290` |
| Victim district | `Pune` |
| Beneficiary bank | `Bank of India` |
| Beneficiary account | `XXXXXX4921` |
| Reported district | `Deoghar` |
| Description | `Caller claimed to be a bank officer and requested an OTP for KYC update.` |

Optionally upload a PNG, JPG, JPEG, or PDF.

Expected result:

- Complaint success message
- New reference number in the format `NCRP/2026/XXXXXX`
- New alert generated in the command queue
- Golden Hour reminder to call `1930`

### Step 5 — Track the seeded case

Open **Citizen Safety → Track Complaint** and enter:

```text
NCRP/2026/000181
```

Expected result:

- Status: `Investigation Active`
- Assigned officer: Inspector Vikram
- Deoghar ATM patrol note
- Four-stage progress display

### Step 6 — Show safety guidance

Open **Citizen Safety → Safety Guidance**.

Show:

- Golden Hour advisory
- 1930 helpline
- Cybercrime.gov.in portal
- OTP and KYC fraud guidance
- Digital arrest guidance
- Part-time job and Telegram task guidance
- Fake loan application guidance

### Step 7 — Switch to Command Center

Use the sidebar portal selector and choose **Command Center**.

### Step 8 — Show overview intelligence

Open **Overview** and demonstrate:

- Active complaints
- Total loss at risk
- Open alerts
- Monitored cash-out nodes
- Mean confidence
- 24-hour cash-out timing chart
- District risk bars
- Next opening windows
- Typology mix
- Anomalies
- Recent complaints

### Step 9 — Switch simulation scenarios

Use the **Simulation scenario** selector to show:

- Active Mule Surge
- Digital Arrest Corridor
- Baseline Calm State

Select **Activate scenario** when demonstrating scenario-control capability.

### Step 10 — Show H3 hotspots

Open **Hotspots**.

Use the forecast horizon selector:

- Next 2 hours
- Next 4 hours
- Next 6 hours

Explain the map:

- Red hexagons are `HIGH`.
- Amber hexagons are `WATCH`.
- Slate hexagons are `NORMAL`.
- Clicking a cell reveals district, probability, reason code, linked complaints, and money at risk in the table below.

### Step 11 — Generate a bank freeze notice

Open **Alerts**.

Expand:

```text
ALT-2026-001
```

Select **Generate Sec 91 Notice**.

Expected result:

- Notice reference such as `BNSS-91-FROZEN/2026/2026-001`
- Recipient bank
- Target account
- Full Section 91 BNSS / CrPC emergency debit freeze advisory

### Step 12 — Dispatch the alert

Select **Mark DISPATCHED**.

Expected result:

- Alert status becomes `DISPATCHED`.
- Corresponding citizen complaint becomes `Investigation Active`.
- Citizen tracking reflects the updated investigation note.

Continue the demo if needed:

```text
DISPATCHED → ACKNOWLEDGED → RESOLVED
```

The final `RESOLVED` state maps to `Returned to Victim`.

---

## 10. Important Seeded References

The local demo dataset includes these references:

| Reference | Typology | District | Loss | Status |
|---|---|---:|---:|---|
| `NCRP/2026/000181` | UPI fraud | Deoghar | ₹1,48,000 | Investigation Active |
| `NCRP/2026/000182` | Investment scam | Jamtara | ₹6,20,000 | Investigation Active |
| `NCRP/2026/000183` | Digital arrest | Nuh | ₹2,55,000 | Under Review |
| `NCRP/2026/000184` | Loan app extortion | Mathura | ₹92,000 | Returned to Victim |
| `NCRP/2026/000185` | Job fraud | Giridih | ₹1,75,000 | Investigation Active |
| `NCRP/2026/000186` | OTP fraud | Bharatpur | ₹66,000 | Under Review |

Important alerts:

```text
ALT-2026-001 — Deoghar Bus Stand ATM — HIGH — 77%
ALT-2026-002 — Nuh Tauru Chowk ATM — HIGH — 71%
ALT-2026-003 — Jamtara Main Road ATM Cluster — HIGH — 71%
```

---

## 11. API Endpoints

The backend exposes the following main routes.

### Health

```text
GET /health
```

### Authentication

```text
POST /api/v1/cyber-safely/auth/request-otp
POST /api/v1/cyber-safely/auth/verify-otp
```

### Citizen portal

```text
POST /api/v1/cyber-safely/scan-link
POST /api/v1/cyber-safely/report-crime
POST /api/v1/cyber-safely/report-crime-multipart
GET  /api/v1/cyber-safely/track/{reference_no}
GET  /api/v1/cyber-safely/guidance
```

The tracking route accepts slash-containing references such as:

```text
/api/v1/cyber-safely/track/NCRP/2026/000181
```

### Command portal

```text
GET   /api/v1/command/stats
GET   /api/v1/command/timing-pattern
GET   /api/v1/command/district-risk
GET   /api/v1/command/typology-mix
GET   /api/v1/command/anomalies
GET   /api/v1/command/recent-complaints
GET   /api/v1/hotspots
GET   /api/v1/alerts
PATCH /api/v1/alerts/{alert_id}/status
POST  /api/v1/alerts/{alert_id}/generate-advisory
GET   /api/v1/scenarios
POST  /api/v1/scenarios/{scenario_id}/activate
```

Swagger is available at:

```text
http://127.0.0.1:8000/docs
```

---

## 12. Local Data and Persistence

When Supabase is not configured, the backend uses:

```text
backend/data/mock_scenarios.json
```

This file is live read/write demo state. The backend updates it when:

- A complaint is submitted.
- Evidence metadata is saved.
- An alert status changes.
- A scenario is activated.

Uploaded evidence is stored under:

```text
backend/data/evidence/
```

Do not use real victim information. Only use synthetic demo data.

---

## 13. Resetting the Demo Dataset

Before an important judging run, restore the original demo data from version control if the repository is clean and the seed file is tracked:

```powershell
git restore -- backend/data/mock_scenarios.json
```

If the file contains intentional team changes, do not restore it blindly. First inspect the diff:

```powershell
git diff -- backend/data/mock_scenarios.json
```

Local evidence files can be removed individually after inspecting the directory:

```powershell
Get-ChildItem "backend\data\evidence"
```

Do not delete the entire project directory or broad parent directories.

---

## 14. Development Workflow

### Before changing code

1. Read `context_handover.md` if present.
2. Read the relevant documents in `docs/`.
3. Check the current worktree:

   ```powershell
   git status --short
   ```

4. Avoid changing the backend contract unless a bug is confirmed.

### Frontend changes

Frontend screens are organized by responsibility:

- `frontend/citizen/` for citizen workflows.
- `frontend/command/` for investigator workflows.
- `frontend/api_client.py` for API calls and fallback behavior.
- `frontend/theme.py` for shared styling.
- `frontend/app.py` for routing and session state.

### Backend changes

The backend is already complete for the MVP. Only change it when:

- An endpoint is broken.
- A response does not match the frontend contract.
- A demonstrated workflow cannot complete.
- A bug directly affects persistence or status synchronization.

Preserve:

- FastAPI route paths.
- Pydantic response shapes.
- Mock OTP `123456`.
- Local JSON fallback.
- H3 v4 compatibility through `geo_to_h3_safe()`.

### H3 compatibility

The installed H3 package may use the v4 API. Use:

```python
h3.latlng_to_cell(lat, lng, resolution)
```

or the existing project wrapper:

```python
from backend.ml_pipeline.features import geo_to_h3_safe
```

Do not introduce direct calls to the removed v3-only API `h3.geo_to_h3()` when the wrapper can be reused.

---

## 15. Validation Commands

Run these checks after code changes:

### Compile Python files

```powershell
python -m compileall -q backend frontend run_prahari.py
```

### Import the backend

```powershell
python -c "from backend.app import app; print(len(app.routes))"
```

### Start the backend

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

In another PowerShell window:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

### Test the phishing scanner

```powershell
python -c "from backend.cyber_safely.scanner import scan_url; print(scan_url('http://sbi-reward-kyc.top/claim-bonus.apk'))"
```

Expected verdict:

```text
MALICIOUS_PHISHING
```

### Test Streamlit startup

```powershell
python -m streamlit run frontend/app.py --server.headless true --server.port 8501
```

Then open:

```text
http://localhost:8501
```

---

## 16. Troubleshooting

### The frontend says the backend is unavailable

Check whether port `8000` is running:

```powershell
Invoke-RestMethod http://127.0.0.1:8000/health
```

If it fails, start the backend manually:

```powershell
python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000
```

### Port 8000 or 8501 is already in use

Change the ports in `.env`:

```env
FASTAPI_PORT=8001
STREAMLIT_PORT=8502
```

Restart both services.

### The login does not proceed

Use:

```text
Any email containing @
OTP: 123456
```

Verify that `.env` contains:

```env
MOCK_AUTH=True
DEMO_BYPASS_OTP=123456
```

### A seeded reference returns not found

Confirm the exact reference, including all slashes:

```text
NCRP/2026/000181
```

Confirm the backend is running the current code and restart Uvicorn after route changes.

### The map is blank

Check:

1. `folium` is installed.
2. `streamlit-folium` is installed.
3. The hotspot endpoint returns data:

   ```powershell
   Invoke-RestMethod http://127.0.0.1:8000/api/v1/hotspots
   ```

4. The browser has loaded the Streamlit page completely.

### Upload fails

Use only:

```text
PNG, JPG, JPEG, PDF
```

In local mode, evidence is written to:

```text
backend/data/evidence/
```

### Supabase errors appear

For judging, empty Supabase credentials and `MOCK_AUTH=True` are recommended. Do not put real keys in source files or commit them.

### Streamlit shows stale data

Streamlit reruns the script after widget interaction. If necessary:

1. Use the app refresh button.
2. Restart Streamlit.
3. Restart the complete launcher.

---

## 17. Team Safety and Data Rules

- Use synthetic names, accounts, email addresses, and transaction records only.
- Never upload real victim documents.
- Never commit `.env` credentials.
- Never expose Supabase service-role keys in frontend code.
- Treat scanner results as awareness guidance, not a definitive legal or security verdict.
- Treat hotspot predictions as investigative leads, not proof of criminal activity.
- Validate all bank freeze actions with the authorized bank nodal officer.
- Do not commit generated evidence files or Python bytecode.

---

## 18. Demo Talking Points

Use these concise explanations during judging:

### Why two portals?

Citizens need immediate protection and transparent reporting, while cyber investigators need predictive intelligence and prioritized intervention. The two views close the loop from victim report to possible cash-out interception.

### Why H3?

H3 converts geographic locations into consistent hexagonal cells. This allows complaints, ATMs, forecasts, and alerts to be compared spatially without exposing exact operational details in every visualization.

### Why local fallback?

The hackathon demo must remain usable if the network or Supabase is unavailable. Local JSON persistence keeps the primary workflows demonstrable while preserving the same API contract.

### Why the 1930 reminder?

Cyber-fraud recovery is time-sensitive. Reporting quickly increases the chance that beneficiary accounts can be frozen before the money is withdrawn or moved.

### Why human-in-the-loop?

PRAHARI is decision support. A prediction should prioritize investigation and bank coordination; it should never automatically make a legal determination or punitive action.

---

## 19. Quick Start Card

```powershell
cd "C:\Users\Lova kumar\OneDrive\Desktop\predictive cybercrime"
.\.venv\Scripts\Activate.ps1
python run_prahari.py
```

Then open:

```text
http://localhost:8501
```

Login:

```text
Email: any email address
OTP:   123456
```

Best first demo link:

```text
http://sbi-reward-kyc.top/claim-bonus.apk
```

Best seeded tracking reference:

```text
NCRP/2026/000181
```

Best seeded alert:

```text
ALT-2026-001
```
