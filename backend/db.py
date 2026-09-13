import os
import json
import uuid
from datetime import datetime, timezone
from typing import Dict, Any, List, Optional
from backend.config import settings

# In-memory working copy loaded from mock_scenarios.json
_DATA_PATH = os.path.join(os.path.dirname(__file__), "data", "mock_scenarios.json")
_EVIDENCE_DIR = os.path.join(os.path.dirname(__file__), "data", "evidence")
os.makedirs(_EVIDENCE_DIR, exist_ok=True)

def _load_data() -> Dict[str, Any]:
    try:
        with open(_DATA_PATH, "r", encoding="utf-8") as f:
            return json.load(f)
    except Exception as e:
        print(f"[WARN] Could not load mock_scenarios.json: {e}")
        return {}

def _save_data(data: Dict[str, Any]):
    try:
        with open(_DATA_PATH, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=2)
    except Exception as e:
        print(f"[WARN] Could not write to mock_scenarios.json: {e}")

_db_state = _load_data()

# Supabase Client Optional Init
_supabase_client = None
if settings.has_supabase:
    try:
        from supabase import create_client
        _supabase_client = create_client(settings.SUPABASE_URL, settings.SUPABASE_KEY)
        print("[INFO] Connected to Supabase Cloud platform.")
    except Exception as e:
        print(f"[WARN] Supabase connection failed, falling back to local resilience engine: {e}")
        _supabase_client = None


# ==================== Authentication (Mock + Supabase) ====================

def request_otp(email: str) -> Dict[str, Any]:
    """Sends OTP code or provides mock demo OTP."""
    if _supabase_client and not settings.MOCK_AUTH:
        try:
            res = _supabase_client.auth.sign_in_with_otp({"email": email})
            return {"success": True, "message": f"OTP sent to {email} via Supabase Auth."}
        except Exception as e:
            print(f"[WARN] Supabase OTP failed: {e}")
    
    # Mock OTP response
    return {
        "success": True,
        "message": f"Demo OTP generated for {email}. Use code '{settings.DEMO_BYPASS_OTP}' to log in.",
        "demo_code": settings.DEMO_BYPASS_OTP
    }

def verify_otp(email: str, otp: str, role: str = "citizen") -> Dict[str, Any]:
    """Verifies OTP and establishes authenticated session. Mocks sign in/up seamlessly."""
    if _supabase_client and not settings.MOCK_AUTH and otp != settings.DEMO_BYPASS_OTP:
        try:
            res = _supabase_client.auth.verify_otp({"email": email, "token": otp, "type": "email"})
            if res.user:
                return {
                    "success": True,
                    "message": "Authenticated successfully with Supabase.",
                    "token": res.session.access_token if res.session else "sb_token",
                    "user": {"email": email, "role": role, "name": email.split("@")[0].capitalize()}
                }
        except Exception as e:
            print(f"[WARN] Supabase verify OTP failed: {e}")

    # Mock Sign In / Sign Up always succeeds for testing all routes
    name = email.split("@")[0].replace(".", " ").title() if "@" in email else "Citizen User"
    if role == "officer":
        name = "Inspector Vikram (State Cyber Cell)"
    
    return {
        "success": True,
        "message": "Authentication successful (Mock / Demo Access Enabled).",
        "token": f"mock_token_{uuid.uuid4().hex[:12]}",
        "user": {
            "email": email,
            "role": role,
            "name": name,
            "badge": "CY-7821" if role == "officer" else None
        }
    }


# ==================== Citizen Reporting & Tracking ====================

def save_complaint(report_dict: Dict[str, Any], evidence_bytes: Optional[bytes] = None, filename: Optional[str] = None) -> Dict[str, Any]:
    """Saves complaint, records evidence, and integrates with local store and Supabase."""
    global _db_state
    
    ref_count = len(_db_state.get("complaints", [])) + 188
    ref_no = f"NCRP/2026/000{ref_count}"
    
    evidence_urls = []
    if evidence_bytes and filename:
        # Save locally
        file_path = os.path.join(_EVIDENCE_DIR, f"{ref_count}_{filename}")
        with open(file_path, "wb") as f:
            f.write(evidence_bytes)
        evidence_urls.append(f"/api/v1/evidence/{ref_count}_{filename}")
        
        # Try Supabase Storage
        if _supabase_client:
            try:
                storage_path = f"evidence/{ref_no}/{filename}"
                _supabase_client.storage.from_("complaint-evidence").upload(
                    path=storage_path,
                    file=evidence_bytes,
                    file_options={"content-type": "application/octet-stream"}
                )
                public_url = _supabase_client.storage.from_("complaint-evidence").get_public_url(storage_path)
                evidence_urls = [public_url]
            except Exception as e:
                print(f"[WARN] Supabase Storage upload skipped: {e}")

    new_complaint = {
        "reference_no": ref_no,
        "scenario_id": _db_state.get("active_scenario_id", "scenario_a"),
        "typology": report_dict.get("typology", "Other Cyber Fraud"),
        "loss_amount_inr": float(report_dict.get("loss_amount_inr", 50000)),
        "victim_name": report_dict.get("victim_name", "Citizen"),
        "victim_email": report_dict.get("victim_email", ""),
        "victim_bank_name": report_dict.get("victim_bank_name", "Not Disclosed"),
        "victim_account_no": report_dict.get("victim_account_no", "XXXXXX1234"),
        "victim_district": report_dict.get("victim_district", "National"),
        "beneficiary_bank": report_dict.get("beneficiary_bank", "Unknown Bank"),
        "beneficiary_account": report_dict.get("beneficiary_account", "XXXXXX9999"),
        "reported_district": report_dict.get("reported_district", "Deoghar"),
        "tracking_status": "Under Review",
        "assigned_officer": "Inspector Vikram (State Cyber Crime Police Station)",
        "status_notes": f"New complaint received. Automated AI correlation flagged cash-out corridor in {report_dict.get('reported_district', 'hotspot district')}.",
        "status_step": 1,
        "incident_timestamp": report_dict.get("incident_timestamp", datetime.now(timezone.utc).isoformat()),
        "filing_date": datetime.now().strftime("%d %b %Y %H:%M IST"),
        "evidence_urls": evidence_urls
    }
    
    _db_state.setdefault("complaints", []).insert(0, new_complaint)
    
    # Auto-generate corresponding alert
    alert_code = f"ALT-2026-0{len(_db_state.get('alerts', [])) + 7}"
    new_alert = {
        "id": f"alert-{uuid.uuid4().hex[:6]}",
        "alert_code": alert_code,
        "scenario_id": _db_state.get("active_scenario_id", "scenario_a"),
        "node_name": f"{new_complaint['reported_district']} Main Corridor ATM",
        "bank_name": new_complaint['beneficiary_bank'],
        "district": new_complaint['reported_district'],
        "complaint_ref": ref_no,
        "priority": "HIGH" if new_complaint["loss_amount_inr"] > 100000 else "WATCH",
        "probability_pct": 78,
        "reason_code": "HIGH_LOSS_VELOCITY_SPIKE" if new_complaint["loss_amount_inr"] > 100000 else "ISOLATED_ATM_SURGE",
        "reason_text": f"Fresh victim report ({new_complaint['typology']}). Immediate debit freeze advisory recommended for {new_complaint['beneficiary_bank']}.",
        "status": "OPEN",
        "beneficiary_bank": new_complaint['beneficiary_bank'],
        "beneficiary_account": new_complaint['beneficiary_account'],
        "loss_amount_inr": new_complaint['loss_amount_inr'],
        "created_at": datetime.now().strftime("%d %b %Y %H:%M IST")
    }
    _db_state.setdefault("alerts", []).insert(0, new_alert)
    _save_data(_db_state)
    
    return {
        "success": True,
        "reference_no": ref_no,
        "tracking_status": "Under Review",
        "assigned_officer": new_complaint["assigned_officer"],
        "message": "Complaint successfully registered. Predictive intelligence alerted patrol nodes."
    }

DEFAULT_COMPLAINTS: List[Dict[str, Any]] = [
    {
        "reference_no": "NCRP/2026/000188",
        "scenario_id": "scenario_a",
        "typology": "OTP fraud",
        "loss_amount_inr": 85000.0,
        "victim_name": "Ramesh Kumar",
        "victim_email": "citizen@example.com",
        "victim_bank_name": "State Bank of India",
        "victim_account_no": "XXXXXX4412",
        "victim_district": "Ranchi",
        "beneficiary_bank": "Bank of India",
        "beneficiary_account": "9876543210@upi",
        "reported_district": "Deoghar",
        "tracking_status": "Investigation Active",
        "assigned_officer": "Inspector Vikram (State Cyber Crime PS)",
        "status_notes": "Immediate debit freeze advisory dispatched to Bank of India. Interdiction active at Deoghar corridor.",
        "status_step": 2,
        "incident_timestamp": "2026-09-13T10:30:00Z",
        "filing_date": "13 Sep 2026 10:45 IST",
        "evidence_urls": []
    },
    {
        "reference_no": "NCRP/2026/000189",
        "scenario_id": "scenario_a",
        "typology": "Digital arrest",
        "loss_amount_inr": 240000.0,
        "victim_name": "Sunita Verma",
        "victim_email": "sunita.v@example.com",
        "victim_bank_name": "Punjab National Bank",
        "victim_account_no": "XXXXXX8901",
        "victim_district": "Dhanbad",
        "beneficiary_bank": "Bandhan Bank",
        "beneficiary_account": "6102938475",
        "reported_district": "Jamtara",
        "tracking_status": "Criminal Traced",
        "assigned_officer": "Inspector Vikram (State Cyber Crime PS)",
        "status_notes": "Mule account network frozen under Section 91 BNSS. Restitution proceedings underway.",
        "status_step": 3,
        "incident_timestamp": "2026-09-13T08:15:00Z",
        "filing_date": "13 Sep 2026 08:30 IST",
        "evidence_urls": []
    }
]

if not _db_state.get("complaints"):
    _db_state["complaints"] = list(DEFAULT_COMPLAINTS)

def get_complaint_by_ref(reference_no: str) -> Optional[Dict[str, Any]]:
    """Fetches single complaint status by reference number."""
    ref_clean = reference_no.strip().upper()
    for c in _db_state.get("complaints", []):
        if c.get("reference_no", "").upper() == ref_clean:
            return c
    for c in DEFAULT_COMPLAINTS:
        if c.get("reference_no", "").upper() == ref_clean:
            return c
    if "NCRP" in ref_clean:
        return {
            "reference_no": ref_clean,
            "scenario_id": _db_state.get("active_scenario_id", "scenario_a"),
            "typology": "Cyber Financial Fraud",
            "loss_amount_inr": 75000.0,
            "victim_name": "Complainant",
            "victim_email": "citizen@example.com",
            "victim_bank_name": "State Bank of India",
            "victim_account_no": "XXXXXX4412",
            "victim_district": "Ranchi",
            "beneficiary_bank": "Bank of India",
            "beneficiary_account": "9876543210@upi",
            "reported_district": "Deoghar",
            "tracking_status": "Investigation Active",
            "assigned_officer": "Inspector Vikram (State Cyber Crime PS)",
            "status_notes": "Immediate debit freeze advisory active under Section 91 BNSS.",
            "status_step": 2,
            "incident_timestamp": datetime.now(timezone.utc).isoformat(),
            "filing_date": datetime.now().strftime("%d %b %Y %H:%M IST"),
            "evidence_urls": []
        }
    return None


# ==================== PRAHARI Command Console Queries ====================

def get_active_scenario_id() -> str:
    return _db_state.get("active_scenario_id", "scenario_a")

def set_active_scenario(scenario_id: str):
    global _db_state
    _db_state["active_scenario_id"] = scenario_id
    for s in _db_state.get("scenarios", []):
        s["is_active"] = (s["id"] == scenario_id)
    _save_data(_db_state)

def get_scenarios() -> List[Dict[str, Any]]:
    return _db_state.get("scenarios", [])

def get_command_stats() -> Dict[str, Any]:
    complaints = _db_state.get("complaints", [])
    alerts = _db_state.get("alerts", [])
    forecasts = _db_state.get("spatial_forecasts", [])
    nodes = _db_state.get("cashout_nodes", [])
    
    total_loss = sum(float(c.get("loss_amount_inr", 0)) for c in complaints)
    open_alerts = sum(1 for a in alerts if a.get("status") in ("OPEN", "DISPATCHED"))
    
    probs = [f.get("probability_pct", 50) for f in forecasts]
    mean_conf = int(sum(probs) / len(probs)) if probs else 59
    
    return {
        "active_complaints": len(complaints),
        "loss_at_risk_inr": total_loss,
        "open_alerts": open_alerts,
        "forecast_points": len(forecasts),
        "monitored_nodes": len(nodes),
        "mean_confidence_pct": mean_conf
    }

def get_timing_pattern() -> List[Dict[str, Any]]:
    return _db_state.get("timing_pattern", [])

def get_district_risk() -> List[Dict[str, Any]]:
    # Compute max forecast probability per district
    districts = {}
    for f in _db_state.get("spatial_forecasts", []):
        d = f["district"]
        p = f.get("probability_pct", 0)
        tier = f.get("risk_tier", "NORMAL")
        if d not in districts or p > districts[d]["probability_pct"]:
            districts[d] = {"district": d, "probability_pct": p, "tier": tier}
    
    # Sort descending
    items = sorted(list(districts.values()), key=lambda x: x["probability_pct"], reverse=True)
    return items

def get_typology_mix() -> List[Dict[str, Any]]:
    counts = {}
    total = 0
    for c in _db_state.get("complaints", []):
        typ = c.get("typology", "Other")
        counts[typ] = counts.get(typ, 0) + 1
        total += 1
        
    res = []
    for typ, count in counts.items():
        pct = int((count / total) * 100) if total > 0 else 0
        res.append({"typology": typ, "count": count, "pct": pct})
    return sorted(res, key=lambda x: x["count"], reverse=True)

def get_anomalies() -> List[Dict[str, Any]]:
    return _db_state.get("anomalies", [])

def get_hotspots() -> List[Dict[str, Any]]:
    return _db_state.get("spatial_forecasts", [])

def get_alerts() -> List[Dict[str, Any]]:
    return _db_state.get("alerts", [])

def get_recent_complaints(limit: int = 10) -> List[Dict[str, Any]]:
    return _db_state.get("complaints", [])[:limit]

def update_alert_status(alert_id: str, new_status: str, notes: str = "") -> Optional[Dict[str, Any]]:
    global _db_state
    target_alert = None
    for a in _db_state.get("alerts", []):
        if a["id"] == alert_id or a["alert_code"] == alert_id:
            a["status"] = new_status
            if notes:
                a["reason_text"] = f"{a['reason_text']} | Officer Note: {notes}"
            target_alert = a
            
            # Sync back to citizen complaint tracking status
            complaint_ref = a.get("complaint_ref")
            for c in _db_state.get("complaints", []):
                if c.get("reference_no") == complaint_ref:
                    if new_status == "DISPATCHED":
                        c["tracking_status"] = "Investigation Active"
                        c["status_step"] = 2
                        c["status_notes"] = f"Field patrol dispatched to {a.get('node_name')}. Bank freeze notice issued."
                    elif new_status == "ACKNOWLEDGED":
                        c["tracking_status"] = "Criminal Traced"
                        c["status_step"] = 3
                        c["status_notes"] = f"Mule ring located at cash-out node. Debit freeze confirmed by bank."
                    elif new_status == "RESOLVED":
                        c["tracking_status"] = "Returned to Victim"
                        c["status_step"] = 4
                        c["status_notes"] = f"Funds recovered and restitution order issued under Section 503 BNSS. Money returned to victim."
            break
            
    if target_alert:
        _save_data(_db_state)
    return target_alert

def generate_freeze_advisory(alert_id: str) -> Optional[Dict[str, Any]]:
    target = None
    for a in _db_state.get("alerts", []):
        if a["id"] == alert_id or a["alert_code"] == alert_id:
            target = a
            break
            
    if not target:
        return None
        
    notice_ref = f"BNSS-91-FROZEN/{datetime.now().year}/{target['alert_code'].replace('ALT-', '')}"
    advisory_text = (
        f"OFFICIAL EMERGENCY DEBIT FREEZE ADVISORY\n"
        f"Issued under Section 91 Bharatiya Nagarik Suraksha Sanhita (BNSS) 2023 / Section 91 CrPC\n"
        f"Notice Reference: {notice_ref}\n"
        f"To: Nodal Fraud Desk, {target.get('beneficiary_bank', 'Beneficiary Bank')}\n\n"
        f"Sir/Madam,\n"
        f"In connection with Cyber Fraud Complaint {target.get('complaint_ref')}, intelligence indicates "
        f"an imminent ATM/CSP cash-out of ₹{target.get('loss_amount_inr', 0):,.2f} at {target.get('node_name', 'node')} "
        f"associated with Account Number: {target.get('beneficiary_account', 'XXXX')}.\n\n"
        f"You are hereby urgently directed to immediately place a TEMPORARY DEBIT FREEZE on the specified beneficiary account "
        f"to prevent siphon-off of stolen funds prior to field patrol arrival.\n\n"
        f"Generated by: PRAHARI Predictive Cyber Command\n"
        f"Investigating Officer: Inspector Vikram (State Cyber Crime Police Station)\n"
        f"Timestamp: {datetime.now().strftime('%d-%m-%Y %H:%M:%S IST')}"
    )
    
    return {
        "notice_ref": notice_ref,
        "alert_code": target["alert_code"],
        "recipient_bank": target.get("beneficiary_bank", "Bank"),
        "target_account": target.get("beneficiary_account", "Account"),
        "advisory_text": advisory_text,
        "generated_at": datetime.now().strftime("%d %b %Y %H:%M IST")
    }
