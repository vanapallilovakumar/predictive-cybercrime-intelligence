import json
import os
from pathlib import Path
from typing import Any, Dict, Optional

import requests

BASE_URL = os.getenv("BACKEND_API_URL", "http://127.0.0.1:8000")
_DATA_PATH = Path(__file__).resolve().parents[1] / "backend" / "data" / "mock_scenarios.json"


def _data() -> Dict[str, Any]:
    try:
        return json.loads(_DATA_PATH.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return {}


def _request(method: str, path: str, **kwargs: Any) -> Optional[Any]:
    try:
        response = requests.request(method, f"{BASE_URL}{path}", timeout=4, **kwargs)
        response.raise_for_status()
        return response.json()
    except (requests.RequestException, ValueError):
        return None


def get(path: str, fallback: Any = None) -> Any:
    result = _request("GET", path)
    return fallback if result is None else result


def post(path: str, payload: Optional[Dict[str, Any]] = None, files: Any = None) -> Any:
    kwargs: Dict[str, Any] = {"json": payload} if files is None else {"data": payload or {}, "files": files}
    return _request("POST", path, **kwargs)


def patch(path: str, payload: Dict[str, Any]) -> Any:
    return _request("PATCH", path, json=payload)


def request_otp(email: str) -> Any:
    return post(
        "/api/v1/cyber-safely/auth/request-otp",
        {"email": email},
    ) or {
        "success": True,
        "message": f"Demo OTP generated for {email}. Use code '123456' to log in.",
        "token": "123456",
    }


def verify_otp(email: str, otp: str) -> Any:
    result = post("/api/v1/cyber-safely/auth/verify-otp", {"email": email, "otp": otp})
    if result is not None:
        return result
    if otp == "123456":
        return {
            "success": True,
            "message": "Authentication successful (offline demo access).",
            "token": "offline_demo_token",
            "user": {"email": email, "role": "citizen", "name": email.split("@")[0].replace(".", " ").title()},
        }
    return {"success": False, "message": "Invalid demo OTP."}


def scan_link(url: str) -> Any:
    result = post("/api/v1/cyber-safely/scan-link", {"url": url})
    if result is not None:
        return result
    from backend.cyber_safely.scanner import scan_url

    return scan_url(url)


def report_crime(payload: Dict[str, Any], uploaded_file: Any = None) -> Any:
    if uploaded_file is None:
        return post("/api/v1/cyber-safely/report-crime", payload)
    files = {"evidence": (uploaded_file.name, uploaded_file.getvalue(), uploaded_file.type)}
    return post("/api/v1/cyber-safely/report-crime-multipart", payload, files=files)


def track(reference_no: str) -> Any:
    result = get(f"/api/v1/cyber-safely/track/{reference_no}")
    if result:
        return result
    for complaint in _data().get("complaints", []):
        if complaint.get("reference_no", "").upper() == reference_no.strip().upper():
            return {
                "reference_no": complaint.get("reference_no"),
                "typology": complaint.get("typology"),
                "loss_amount_inr": complaint.get("loss_amount_inr", 0),
                "victim_bank_name": complaint.get("victim_bank_name", "Not Disclosed"),
                "victim_account_no": complaint.get("victim_account_no", "XXXXXX0000"),
                "filing_date": complaint.get("filing_date", "Recently"),
                "tracking_status": complaint.get("tracking_status", "Under Review"),
                "assigned_officer": complaint.get("assigned_officer", "Inspector Vikram"),
                "status_notes": complaint.get("status_notes", "Under active review."),
                "status_step": complaint.get("status_step", 1),
            }
    return None


def guidance() -> Any:
    result = get("/api/v1/cyber-safely/guidance")
    if result:
        return result
    from backend.cyber_safely.guidance import GOLDEN_HOUR_ADVISORY, TYPOLOGY_GUIDANCE

    return {"golden_hour": GOLDEN_HOUR_ADVISORY, "typologies": TYPOLOGY_GUIDANCE}


def command_stats() -> Dict[str, Any]:
    data = _data()
    complaints = data.get("complaints", [])
    alerts = data.get("alerts", [])
    forecasts = data.get("spatial_forecasts", [])
    return get(
        "/api/v1/command/stats",
        {
            "active_complaints": len(complaints),
            "loss_at_risk_inr": sum(float(c.get("loss_amount_inr", 0)) for c in complaints),
            "open_alerts": sum(a.get("status") in ("OPEN", "DISPATCHED") for a in alerts),
            "forecast_points": len(forecasts),
            "monitored_nodes": len(data.get("cashout_nodes", [])),
            "mean_confidence_pct": int(sum(f.get("probability_pct", 0) for f in forecasts) / len(forecasts)) if forecasts else 0,
        },
    )


def command_list(endpoint: str, key: str, fallback: Any = None) -> Any:
    data = _data()
    complaints = data.get("complaints", [])
    forecasts = data.get("spatial_forecasts", [])
    typology_counts: Dict[str, int] = {}
    for complaint in complaints:
        typology = complaint.get("typology", "Other")
        typology_counts[typology] = typology_counts.get(typology, 0) + 1
    total = len(complaints)
    district_values: Dict[str, Dict[str, Any]] = {}
    for forecast in forecasts:
        district = forecast.get("district", "Unknown")
        candidate = {
            "district": district,
            "probability_pct": int(forecast.get("probability_pct", 0)),
            "tier": forecast.get("risk_tier", "NORMAL"),
        }
        if district not in district_values or candidate["probability_pct"] > district_values[district]["probability_pct"]:
            district_values[district] = candidate
    defaults = {
        "timing-pattern": data.get("timing_pattern", []),
        "district-risk": sorted(district_values.values(), key=lambda item: item["probability_pct"], reverse=True),
        "typology-mix": [
            {"typology": typology, "count": count, "pct": int(count / total * 100) if total else 0}
            for typology, count in sorted(typology_counts.items(), key=lambda item: item[1], reverse=True)
        ],
        "anomalies": data.get("anomalies", []),
        "hotspots": data.get("spatial_forecasts", []),
        "alerts": data.get("alerts", []),
        "recent-complaints": complaints[:15],
    }
    return get(endpoint, defaults.get(key, fallback))


def generate_advisory(alert_id: str) -> Any:
    return post(f"/api/v1/alerts/{alert_id}/generate-advisory")


def update_alert(alert_id: str, status: str, notes: str = "") -> Any:
    return patch(f"/api/v1/alerts/{alert_id}/status", {"status": status, "notes": notes})


def scenarios() -> Any:
    return get("/api/v1/scenarios", _data().get("scenarios", []))


def activate_scenario(scenario_id: str) -> Any:
    return post(f"/api/v1/scenarios/{scenario_id}/activate") or {"success": True, "active_scenario": scenario_id}
