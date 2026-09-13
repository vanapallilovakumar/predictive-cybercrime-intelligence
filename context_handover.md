# CONTEXT HANDOVER — PRAHARI & Cyber Safely MVP
**⚠️ RULE: This document is the single source of truth for all agents continuing work on this project. Before making any decision, reading code, or writing a single line — read this file in full. Do not assume, override, or contradict what is written here.**

---

## Project Identity
| Field | Value |
|---|---|
| **Project Name** | PRAHARI & Cyber Safely |
| **Hackathon** | Smart India Hackathon (SIH) 2026 |
| **Problem Statement** | SIH26184 — Ministry of Home Affairs (MHA) |
| **Team** | TRACE X |
| **Stage** | MVP — Backend complete, Frontend pending |
| **Handover Date** | 2026-09-13 |

---

## What This System Does
A dual-portal predictive cybercrime platform:

1. **Cyber Safely (Citizen Portal)** — Citizens can verify suspicious links before clicking, file cybercrime complaints with evidence upload, and track their case through a 4-stage restitution status badge.
2. **PRAHARI Command (Police Portal)** — Law enforcement gets a dark tactical console with live KPIs, a predictive Uber H3 hexagonal hotspot map, alert triage, and 1-click Section 91 BNSS/CrPC Bank Freeze Notice generation.

---

## Current Build State

### ✅ DONE — Backend (FastAPI)
All files exist and are complete:

| File | Status | Notes |
|---|---|---|
| [`backend/__init__.py`](./backend/__init__.py) | ✅ Done | Package init |
| [`backend/config.py`](./backend/config.py) | ✅ Done | Pydantic settings, reads `.env` |
| [`backend/models.py`](./backend/models.py) | ✅ Done | All Pydantic request/response schemas |
| [`backend/db.py`](./backend/db.py) | ✅ Done | Hybrid Supabase + local JSON persistence |
| [`backend/app.py`](./backend/app.py) | ✅ Done | FastAPI with all 20 REST endpoints |
| [`backend/data/mock_scenarios.json`](./backend/data/mock_scenarios.json) | ✅ Done | Full seed dataset (complaints, nodes, alerts, forecasts) |
| [`backend/cyber_safely/__init__.py`](./backend/cyber_safely/__init__.py) | ✅ Done | Package init |
| [`backend/cyber_safely/scanner.py`](./backend/cyber_safely/scanner.py) | ✅ Done | Hybrid phishing threat scanner |
| [`backend/cyber_safely/guidance.py`](./backend/cyber_safely/guidance.py) | ✅ Done | Golden Hour + typology safety guidance |
| [`backend/ml_pipeline/__init__.py`](./backend/ml_pipeline/__init__.py) | ✅ Done | Package init |
| [`backend/ml_pipeline/features.py`](./backend/ml_pipeline/features.py) | ✅ Done | H3 conversion, temporal features |
| [`backend/ml_pipeline/train.py`](./backend/ml_pipeline/train.py) | ✅ Done | Training script (HistGBT + IsolationForest) |
| [`backend/ml_pipeline/inference.py`](./backend/ml_pipeline/inference.py) | ✅ Done | Probability scoring + reason code synthesis |
| [`requirements.txt`](./requirements.txt) | ✅ Done | All deps installed on host machine |
| [`.env`](./.env) | ✅ Done | MOCK_AUTH=True, demo OTP=123456 |

### ❌ NOT YET BUILT — Frontend (Streamlit)
These files **do not exist yet** and are the primary next task:

| File | Priority | Notes |
|---|---|---|
| `frontend/__init__.py` | P1 | Package init |
| `frontend/theme.py` | P1 | CSS injector — dark navy theme |
| `frontend/api_client.py` | P1 | HTTP wrapper to FastAPI on port 8000 |
| `frontend/app.py` | P1 | Main Streamlit router — portal switcher |
| `frontend/citizen/login_view.py` | P1 | Mock Email OTP login (no real Supabase needed) |
| `frontend/citizen/link_scanner_view.py` | P1 | URL input + red/green result banner |
| `frontend/citizen/report_crime_view.py` | P1 | 4-section intake form + file upload |
| `frontend/citizen/track_status_view.py` | P1 | Ref number → 4-stage status badge |
| `frontend/citizen/safety_guidance_view.py` | P1 | Golden Hour + typology cards |
| `frontend/command/overview_view.py` | P1 | KPIs, 24h chart, district bars, anomalies |
| `frontend/command/hotspots_view.py` | P1 | Folium H3 hexagonal map |
| `frontend/command/alerts_view.py` | P1 | Alert queue + freeze notice |
| `run_prahari.py` | P1 | Single-command launcher |

### ❌ NOT YET BUILT — User-Facing Docs
| File | Priority | Notes |
|---|---|---|
| `docs/HOW_TO_USE.md` | P1 | Complete usage guide requested by user |

---

## Tech Stack (Frozen — Do Not Change)
```
Frontend:   Streamlit 1.63+ (100% Python, zero JS)
Backend:    FastAPI 0.141+ on Uvicorn (Port 8000)
Maps:       streamlit-folium + Folium (Leaflet / H3 hex polygons)
Charts:     Altair 6 / Plotly 7
AI Models:  scikit-learn (HistGradientBoostingClassifier, IsolationForest, DBSCAN)
Geo:        h3 4.5.0 (WARNING: uses new API — latlng_to_cell, NOT geo_to_h3)
Database:   Supabase (live) OR backend/data/mock_scenarios.json (local fallback)
Python:     3.14 on Windows
Auth:       MOCKED — any email + OTP "123456" grants full access
```

> [!CAUTION]
> **h3 version 4.x API Breaking Change:** The installed library is `h3==4.5.0`. In h3 v4, the function is `h3.latlng_to_cell(lat, lng, res)` NOT `h3.geo_to_h3(lat, lng, res)`. The `features.py` file already handles this with `geo_to_h3_safe()`. Always use that wrapper.

---

## Authentication — Mock Mode (Key Decision)

Auth is **fully mocked**. The user explicitly asked for this. Here is the contract:

1. **Any email** + **OTP `123456`** → authenticated citizen session.
2. **Any email** + **OTP `123456`** + role `"officer"` param → authenticated officer session with `Inspector Vikram` identity.
3. Real Supabase OTP is only triggered if `MOCK_AUTH=False` in `.env` AND `SUPABASE_URL`/`SUPABASE_KEY` are set.
4. **The frontend should never block any route behind real authentication.** All tabs — Citizen and Command — are accessible after the mock login.

The mock is implemented in [`backend/db.py`](./backend/db.py) → `verify_otp()`.

---

## All FastAPI REST Endpoints

Base URL: `http://127.0.0.1:8000`

### Health
| Method | Path | Description |
|---|---|---|
| GET | `/health` | System status + Supabase connectivity |

### Citizen Auth
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/cyber-safely/auth/request-otp` | Send OTP (mocked: returns demo code `123456`) |
| POST | `/api/v1/cyber-safely/auth/verify-otp` | Verify OTP (mocked: any email + `123456` works) |

### Citizen Cyber Safely
| Method | Path | Description |
|---|---|---|
| POST | `/api/v1/cyber-safely/scan-link` | Phishing link scanner — returns MALICIOUS_PHISHING / SUSPICIOUS / SAFE |
| POST | `/api/v1/cyber-safely/report-crime` | JSON complaint submission |
| POST | `/api/v1/cyber-safely/report-crime-multipart` | Multipart with evidence file upload |
| GET | `/api/v1/cyber-safely/track/{reference_no}` | 4-stage complaint tracking by ref no |
| GET | `/api/v1/cyber-safely/guidance` | Golden Hour advisory + typology safety cards |

### PRAHARI Command Intelligence
| Method | Path | Description |
|---|---|---|
| GET | `/api/v1/command/stats` | 4 KPI metrics (complaints, alerts, nodes, mean confidence) |
| GET | `/api/v1/command/timing-pattern` | 24-hour cash-out timing series |
| GET | `/api/v1/command/district-risk` | District max-probability list |
| GET | `/api/v1/command/typology-mix` | Crime type breakdown |
| GET | `/api/v1/command/anomalies` | Statistical anomaly feed |
| GET | `/api/v1/command/recent-complaints` | Recent 15 complaints table |
| GET | `/api/v1/hotspots` | Uber H3 hexagonal cell predictions |
| GET | `/api/v1/alerts` | Prioritized alert queue |
| PATCH | `/api/v1/alerts/{alert_id}/status` | Update alert status (OPEN→DISPATCHED→ACKNOWLEDGED→RESOLVED) |
| POST | `/api/v1/alerts/{alert_id}/generate-advisory` | Generate Section 91 BNSS Bank Freeze Notice |
| GET | `/api/v1/scenarios` | List all demo scenarios |
| POST | `/api/v1/scenarios/{scenario_id}/activate` | Switch active scenario |

### Interactive Docs
FastAPI auto-generates: `http://127.0.0.1:8000/docs` (Swagger UI)

---

## Persistence Architecture

```
.env has SUPABASE_URL/KEY set?
    YES → Live Supabase PostgreSQL, Auth OTP, Storage
    NO  → backend/data/mock_scenarios.json (local JSON store)
```

The `mock_scenarios.json` is a **live read-write file**. When new complaints or alert status changes happen, `db.py` writes changes back to this file using `_save_data()`. It contains:
- `scenarios[]` — 3 demo scenarios (scenario_a/b/c)
- `cashout_nodes[]` — 6 physical ATM nodes
- `complaints[]` — 6 seed complaints (NCRP/2026/000181 through 000186)
- `spatial_forecasts[]` — 6 H3 hex cell predictions
- `alerts[]` — 6 actionable alerts
- `timing_pattern[]` — 24h series
- `anomalies[]` — 3 anomaly feed items

**Demo Reference Numbers (pre-seeded):**
- `NCRP/2026/000181` → Rohan Sharma, UPI fraud, ₹1,48,000, Deoghar — Status: Investigation Active
- `NCRP/2026/000182` → George Mathew, Investment scam, ₹6,20,000, Jamtara — Status: Investigation Active
- `NCRP/2026/000183` → Anil Verma, Digital arrest, ₹2,55,000, Nuh — Status: Under Review
- `NCRP/2026/000184` → Mahesh Shinde, Loan app, ₹92,000, Mathura — Status: Returned to Victim ✅
- `NCRP/2026/000185` → Sunita Sen, Job fraud, ₹1,75,000, Giridih — Status: Investigation Active
- `NCRP/2026/000186` → Kavita Joshi, OTP fraud, ₹66,000, Bharatpur — Status: Under Review

---

## UI Design System (Frozen)

Dark tactical theme — do **not** deviate from these values:

```python
# Palette
BACKGROUND   = "#0b0f19"   # Dark navy canvas
PANEL        = "#111827"   # Panel cards
BORDER       = "#1f2937"   # Card borders
DANGER       = "#ef4444"   # RED — High risk, phishing, malicious
AMBER        = "#f59e0b"   # AMBER — Watch tier alerts
SUCCESS      = "#22c55e"   # GREEN — Safe, resolved, returned to victim
PRIMARY      = "#3b82f6"   # BLUE — Active, investigation
TEXT_MUTED   = "#94a3b8"   # Muted labels, micro-caps
```

**Risk Tier Colors:**
- `HIGH` → Crimson red (`#ef4444`)
- `WATCH` → Amber (`#f59e0b`)
- `NORMAL` → Slate (`#64748b`)

**Status Step Colors:**
- Step 1 "Under Review" → 🟡 Yellow
- Step 2 "Investigation Active" → 🟠 Orange
- Step 3 "Criminal Traced / Money Recovered" → 🔵 Blue
- Step 4 "Returned to Victim" → 🟢 Green

---

## Frontend Architecture To Build

```
frontend/
├── __init__.py
├── app.py              ← Main Streamlit router (global nav + portal switcher)
├── theme.py            ← CSS injector (dark navy theme as above)
├── api_client.py       ← requests wrapper to http://127.0.0.1:8000
├── citizen/
│   ├── __init__.py
│   ├── login_view.py          ← Mock OTP login card (any email + 123456)
│   ├── link_scanner_view.py   ← Phishing URL scanner
│   ├── report_crime_view.py   ← 4-section intake + file upload
│   ├── track_status_view.py   ← Ref no → 4-stage status badge
│   └── safety_guidance_view.py ← Golden Hour + typology cards
└── command/
    ├── __init__.py
    ├── overview_view.py  ← KPIs, charts, anomalies, recent complaints
    ├── hotspots_view.py  ← Folium H3 map (streamlit-folium)
    └── alerts_view.py    ← Alert triage + Sec 91 freeze notice
```

**Global Navigation Layout:**
```
[P] PRAHARI & CYBER SAFELY | [🛡️ Citizen Safety]  [⚡ Command Center]  [👤 {user_name}]
```
- Switching portal does NOT require re-login. Session is persistent.
- Citizens can see Citizen tabs. Officers (same mock login) can toggle to Command.
- No real RBAC — both portals are accessible after any login.

---

## run_prahari.py (To Build)

The launcher must:
1. Start FastAPI via `uvicorn backend.app:app --host 127.0.0.1 --port 8000` as a subprocess
2. Start Streamlit via `python -m streamlit run frontend/app.py --server.port 8501` as a subprocess
3. Print URLs to console with a 2-second delay between launching each
4. Handle Ctrl+C to gracefully kill both subprocesses
5. Use `--no-browser` flag on Streamlit so it doesn't auto-open during judging if not needed

```python
# run_prahari.py skeleton
import subprocess, sys, time, signal, os

def launch():
    api_proc = subprocess.Popen([sys.executable, "-m", "uvicorn", "backend.app:app", "--host", "127.0.0.1", "--port", "8000"])
    time.sleep(2)
    st_proc = subprocess.Popen([sys.executable, "-m", "streamlit", "run", "frontend/app.py", "--server.port", "8501"])
    ...
```

---

## Key Constraints & Rules for Continuing Agents

> [!IMPORTANT]
> **RULE 1 — This document is the source of truth.** Any instruction here overrides assumptions from docs/, README.md, or general knowledge.

> [!IMPORTANT]
> **RULE 2 — Do not change the backend.** The FastAPI backend in `backend/` is complete. Only create frontend files and `run_prahari.py` unless a bug must be fixed.

> [!IMPORTANT]
> **RULE 3 — Mock auth must unlock all routes.** Every Streamlit page — citizen and command — must be accessible after login with any email and OTP `123456`. Never add route guards that block access.

> [!IMPORTANT]
> **RULE 4 — h3 v4 API only.** Use `h3.latlng_to_cell(lat, lng, res)` NOT `h3.geo_to_h3()`. Use `geo_to_h3_safe()` from `backend/ml_pipeline/features.py`.

> [!WARNING]
> **RULE 5 — Python 3.14 on Windows.** Avoid packages that have no Python 3.14 Windows wheel (e.g., `geopandas` was excluded for this reason). All packages in `requirements.txt` are pre-verified to install successfully.

> [!WARNING]
> **RULE 6 — Streamlit script must be run from project root.** Always run: `python run_prahari.py` from `C:/Users/Lova kumar/OneDrive/Desktop/predictive cybercrime/`. Imports like `from backend.config import settings` depend on the project root being on `sys.path`.

> [!NOTE]
> **RULE 7 — No external CSS/JS.** This is a 100% Python Streamlit application. All styling goes through `st.markdown(..., unsafe_allow_html=True)` inside `frontend/theme.py`.

> [!NOTE]
> **RULE 8 — Fallback safety.** All API calls from `frontend/api_client.py` must catch connection errors and return fallback static data so the UI never crashes, even if the backend is starting up.

---

## How to Start the App (After Building Frontend)

```powershell
# Step 1: Navigate to project root
cd "C:\Users\Lova kumar\OneDrive\Desktop\predictive cybercrime"

# Step 2: Launch both services with one command
python run_prahari.py

# URLs
# Backend API:   http://127.0.0.1:8000
# Swagger Docs:  http://127.0.0.1:8000/docs
# Frontend:      http://localhost:8501
```

---

## Demo Flow (Hackathon Judging Sequence)

Follow this exact order to impress evaluators:

1. **Citizen login** → Any email + OTP `123456` → Authenticated
2. **Phishing scan** → Paste `http://sbi-reward-kyc.top/claim-bonus.apk` → Red danger banner ✅
3. **Safe scan** → Paste `https://onlinesbi.sbi` → Green safe banner ✅
4. **File complaint** → OTP Fraud, ₹1,48,000, Bank of India beneficiary, Deoghar district → Get `NCRP/2026/00XXXX`
5. **Track complaint** → Enter `NCRP/2026/000181` → Shows `🟠 Investigation Active` badge
6. **Safety guidance** → Show Golden Hour 1930 helpline + typology cards
7. **Switch to Command Center** → Toggle to `⚡ Command Center`
8. **Overview** → Live KPIs + 24h withdrawal chart + district risk bars
9. **Hotspot Map** → H3 hexagons over Deoghar (77%), Jamtara (71%), Nuh (71%)
10. **Triage alert** → Click `ALT-2026-001` → Generate Sec 91 BNSS Freeze Notice → Copy advisory text
11. **Update status** → Set alert to `DISPATCHED` → Verify citizen portal now shows `🟠 Investigation Active`

---

## File Sizes & Reference (As of Handover)

```
backend/app.py              201 lines   — FastAPI all endpoints
backend/db.py               ~250 lines  — Hybrid persistence + auth
backend/models.py           ~130 lines  — Pydantic schemas
backend/config.py           ~20 lines   — Settings
backend/cyber_safely/scanner.py  ~90 lines   — Phishing scanner
backend/cyber_safely/guidance.py ~90 lines   — Safety guidance data
backend/ml_pipeline/features.py  ~55 lines   — Feature engineering
backend/ml_pipeline/inference.py ~130 lines  — Scoring + reason codes
backend/ml_pipeline/train.py     ~60 lines   — Training script
backend/data/mock_scenarios.json ~400 lines  — Seed data (live read-write)
```

---

## Contact / Continuation Instructions

This handover was created by Antigravity (Google DeepMind agent) on 2026-09-13. The user is **Lova Kumar**, Team TRACE X. The agent conversation ID is `ee19090a-fb84-449e-9642-86900d8b7df1`.

**The next agent's immediate task list:**
1. Build all `frontend/` files listed above
2. Build `run_prahari.py`
3. Build `docs/HOW_TO_USE.md` (user explicitly requested this — full command guide)
4. Verify end-to-end by running `python run_prahari.py` and walking through the demo flow above
