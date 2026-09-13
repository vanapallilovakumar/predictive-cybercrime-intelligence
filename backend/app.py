import os
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional, List

from backend.config import settings
from backend.models import (
    URLScanRequest, URLScanResponse,
    CrimeReportRequest, CrimeReportResponse,
    ComplaintTrackingResponse,
    OTPRequest, OTPVerifyRequest, AuthResponse,
    CommandStatsResponse, TimingPatternPoint,
    DistrictRiskItem, TypologyMixItem, AnomalyFeedItem,
    HotspotCellResponse, AlertItemResponse, AlertStatusUpdate,
    AdvisoryResponse, ScenarioItem
)
from backend import db
from backend.cyber_safely import scanner
from backend.cyber_safely.guidance import GOLDEN_HOUR_ADVISORY, TYPOLOGY_GUIDANCE

app = FastAPI(
    title="Prahari • Cyber Saver API",
    version="2.0.0",
    description="Prahari • Cyber Saver Predictive Intelligence API (SIH26184)"
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {
        "message": "Welcome to Prahari API - Cyber Saver",
        "docs_url": "/docs",
        "health_check": "/health"
    }

@app.get("/health")
def health_check():
    return {
        "status": "online",
        "service": "Prahari • Cyber Saver Engine",
        "version": "2.0.0",
        "has_supabase": settings.has_supabase,
        "mock_auth": settings.MOCK_AUTH
    }


# ==================== Citizen Portal Endpoints ====================

@app.post("/api/v1/cyber-safely/auth/request-otp", response_model=AuthResponse)
def request_otp_endpoint(req: OTPRequest):
    result = db.request_otp(req.email)
    return AuthResponse(
        success=result["success"],
        message=result["message"],
        token=result.get("demo_code")
    )

@app.post("/api/v1/cyber-safely/auth/verify-otp", response_model=AuthResponse)
def verify_otp_endpoint(req: OTPVerifyRequest):
    result = db.verify_otp(req.email, req.otp, role="citizen")
    return AuthResponse(
        success=result["success"],
        message=result["message"],
        token=result.get("token"),
        user=result.get("user")
    )

@app.post("/api/v1/cyber-safely/scan-link", response_model=URLScanResponse)
def scan_link_endpoint(req: URLScanRequest):
    if not req.url:
        raise HTTPException(status_code=400, detail="URL cannot be empty.")
    result = scanner.scan_url(req.url)
    return URLScanResponse(**result)

@app.post("/api/v1/cyber-safely/report-crime", response_model=CrimeReportResponse)
def report_crime_endpoint(req: CrimeReportRequest):
    res = db.save_complaint(req.model_dump())
    return CrimeReportResponse(**res)

@app.post("/api/v1/cyber-safely/report-crime-multipart", response_model=CrimeReportResponse)
async def report_crime_multipart(
    typology: str = Form(...),
    loss_amount_inr: float = Form(...),
    victim_name: str = Form("Anonymous Citizen"),
    victim_email: str = Form(...),
    victim_account_no: str = Form("XXXXXX0000"),
    victim_bank_name: str = Form("Not Disclosed"),
    victim_district: str = Form(...),
    beneficiary_bank: str = Form(...),
    beneficiary_account: str = Form(...),
    reported_district: str = Form(...),
    incident_timestamp: str = Form(...),
    description: Optional[str] = Form(""),
    evidence: Optional[UploadFile] = File(None)
):
    evidence_bytes = None
    filename = None
    if evidence:
        evidence_bytes = await evidence.read()
        filename = evidence.filename
        
    report_dict = {
        "typology": typology,
        "loss_amount_inr": loss_amount_inr,
        "victim_name": victim_name,
        "victim_email": victim_email,
        "victim_account_no": victim_account_no,
        "victim_bank_name": victim_bank_name,
        "victim_district": victim_district,
        "beneficiary_bank": beneficiary_bank,
        "beneficiary_account": beneficiary_account,
        "reported_district": reported_district,
        "incident_timestamp": incident_timestamp,
        "description": description or ""
    }
    res = db.save_complaint(report_dict, evidence_bytes=evidence_bytes, filename=filename)
    return CrimeReportResponse(**res)

@app.get("/api/v1/cyber-safely/track/{reference_no:path}", response_model=ComplaintTrackingResponse)
def track_complaint_endpoint(reference_no: str):
    complaint = db.get_complaint_by_ref(reference_no)
    if not complaint:
        raise HTTPException(status_code=404, detail=f"Complaint reference '{reference_no}' not found.")
        
    return ComplaintTrackingResponse(
        reference_no=complaint["reference_no"],
        typology=complaint["typology"],
        loss_amount_inr=complaint["loss_amount_inr"],
        victim_bank_name=complaint.get("victim_bank_name", "Not Disclosed"),
        victim_account_no=complaint.get("victim_account_no", "XXXXXX0000"),
        filing_date=complaint.get("filing_date", "Recently"),
        tracking_status=complaint.get("tracking_status", "Under Review"),
        assigned_officer=complaint.get("assigned_officer", "Inspector Vikram (State Cyber Cell)"),
        status_notes=complaint.get("status_notes", "Under active review."),
        status_step=complaint.get("status_step", 1)
    )

@app.get("/api/v1/cyber-safely/guidance")
def get_guidance():
    return {
        "golden_hour": GOLDEN_HOUR_ADVISORY,
        "typologies": TYPOLOGY_GUIDANCE
    }


# ==================== Command Center Endpoints ====================

@app.get("/api/v1/command/stats", response_model=CommandStatsResponse)
def get_stats_endpoint():
    return CommandStatsResponse(**db.get_command_stats())

@app.get("/api/v1/command/timing-pattern", response_model=List[TimingPatternPoint])
def get_timing_endpoint():
    return [TimingPatternPoint(**p) for p in db.get_timing_pattern()]

@app.get("/api/v1/command/district-risk", response_model=List[DistrictRiskItem])
def get_district_risk_endpoint():
    return [DistrictRiskItem(**d) for d in db.get_district_risk()]

@app.get("/api/v1/command/typology-mix", response_model=List[TypologyMixItem])
def get_typology_mix_endpoint():
    return [TypologyMixItem(**t) for t in db.get_typology_mix()]

@app.get("/api/v1/command/anomalies", response_model=List[AnomalyFeedItem])
def get_anomalies_endpoint():
    return [AnomalyFeedItem(**a) for a in db.get_anomalies()]

@app.get("/api/v1/command/recent-complaints")
def get_recent_complaints_endpoint():
    return db.get_recent_complaints(limit=15)

@app.get("/api/v1/hotspots", response_model=List[HotspotCellResponse])
def get_hotspots_endpoint():
    return [HotspotCellResponse(**h) for h in db.get_hotspots()]

@app.get("/api/v1/alerts", response_model=List[AlertItemResponse])
def get_alerts_endpoint():
    return [AlertItemResponse(**a) for a in db.get_alerts()]

@app.patch("/api/v1/alerts/{alert_id}/status", response_model=AlertItemResponse)
def update_alert_endpoint(alert_id: str, req: AlertStatusUpdate):
    updated = db.update_alert_status(alert_id, req.status, notes=req.notes or "")
    if not updated:
        raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found.")
    return AlertItemResponse(**updated)

@app.post("/api/v1/alerts/{alert_id}/generate-advisory", response_model=AdvisoryResponse)
def generate_advisory_endpoint(alert_id: str):
    adv = db.generate_freeze_advisory(alert_id)
    if not adv:
        raise HTTPException(status_code=404, detail=f"Alert '{alert_id}' not found.")
    return AdvisoryResponse(**adv)

@app.get("/api/v1/scenarios", response_model=List[ScenarioItem])
def get_scenarios_endpoint():
    return [ScenarioItem(**s) for s in db.get_scenarios()]

@app.post("/api/v1/scenarios/{scenario_id}/activate")
def activate_scenario_endpoint(scenario_id: str):
    db.set_active_scenario(scenario_id)
    return {"success": True, "active_scenario": scenario_id}
