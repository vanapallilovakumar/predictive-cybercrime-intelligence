# PRAHARI & Cyber Safely: Usage Guide

## 1. Start the MVP

From the project root, run:

```powershell
cd "C:\Users\Lova kumar\OneDrive\Desktop\predictive cybercrime"
python run_prahari.py
```

Open the following URLs:

- Citizen and command frontend: <http://localhost:8501>
- FastAPI health check: <http://127.0.0.1:8000/health>
- Interactive API documentation: <http://127.0.0.1:8000/docs>

Press `Ctrl+C` in the launcher window to stop both services.

## 2. Demo authentication

The checked-in `.env` uses safe local demo authentication. Enter any email address, request an OTP, and enter:

```text
123456
```

No real email or Supabase account is required in mock mode.

## 3. Citizen Safety portal

### Check a suspicious link

Open **Check Suspicious Link** and paste a URL such as:

```text
http://sbi-reward-kyc.top/claim-bonus.apk
```

The scanner highlights brand impersonation, risky domains, APK downloads, IP hosts, and fraud keywords. For comparison, try:

```text
https://onlinesbi.sbi
```

### File a complaint

Open **Report Cybercrime**, complete the incident, financial, and beneficiary sections, and optionally upload a PNG, JPG, or PDF receipt. The app returns a reference such as `NCRP/2026/000194`. Call **1930** immediately if the incident happened within the Golden Hour.

### Track a complaint

Open **Track Complaint** and try the seeded reference `NCRP/2026/000181`. The four-stage badge shows the current investigation milestone.

### Read safety guidance

Open **Safety Guidance** for the 1930 Golden Hour advisory and typology-specific warning signs, do's, and don'ts.

## 4. PRAHARI Command portal

Use the sidebar portal switcher to open **Command Center**. The same mock login exposes the command console for the MVP demo.

- **Overview** shows live KPIs, cash-out timing, district risk, typology mix, anomalies, and recent complaints.
- **Hotspots** shows forecast cells on a map, with high-risk, watch, and normal tiers.
- **Alerts** lets an investigator advance alert status from `OPEN` to `DISPATCHED`, `ACKNOWLEDGED`, and `RESOLVED`, and generate a Section 91 BNSS debit-freeze notice.

Status transitions synchronize back to citizen complaint tracking in the local persistence file.

## 5. Local persistence and Supabase

With empty `SUPABASE_URL` and `SUPABASE_KEY`, the backend uses `backend/data/mock_scenarios.json` and stores uploaded evidence under `backend/data/evidence/`. This is the recommended judging configuration.

To use Supabase, populate the credentials in `.env` and set `MOCK_AUTH=False`. Apply the schema and storage policies from `docs/05_backend_schema_and_supabase.md` first. The local fallback remains available if cloud initialization fails.

## 6. Troubleshooting

- If the frontend opens before the API is ready, refresh after a few seconds; the client also uses static fallback data for dashboard reads.
- If a port is occupied, change `FASTAPI_PORT` or `STREAMLIT_PORT` in `.env` and restart the launcher.
- Run `python -m uvicorn backend.app:app --host 127.0.0.1 --port 8000` alone to inspect backend errors.
