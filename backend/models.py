from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any

# ==================== Citizen / Cyber Safely Models ====================

class URLScanRequest(BaseModel):
    url: str

class URLScanResponse(BaseModel):
    url: str
    verdict: str
    threat_score: float
    risk_factors: List[str]
    safety_guidance: str

class CrimeReportRequest(BaseModel):
    typology: str
    loss_amount_inr: float
    victim_name: str = "Anonymous Citizen"
    victim_email: str
    victim_account_no: str = "XXXXXX0000"
    victim_bank_name: str = "Not Disclosed"
    victim_district: str
    beneficiary_bank: str
    beneficiary_account: str
    reported_district: str
    incident_timestamp: str
    description: str = ""
    evidence_urls: List[str] = []

class CrimeReportResponse(BaseModel):
    success: bool
    reference_no: str
    tracking_status: str
    assigned_officer: str
    message: str

class ComplaintTrackingResponse(BaseModel):
    reference_no: str
    typology: str
    loss_amount_inr: float
    victim_bank_name: str
    victim_account_no: str
    filing_date: str
    tracking_status: str
    assigned_officer: str
    status_notes: str
    status_step: int  # 1: Under Review, 2: Investigation Active, 3: Money Recovered, 4: Returned to Victim

class OTPRequest(BaseModel):
    email: str

class OTPVerifyRequest(BaseModel):
    email: str
    otp: str

class AuthResponse(BaseModel):
    success: bool
    message: str
    token: Optional[str] = None
    user: Optional[Dict[str, Any]] = None

# ==================== PRAHARI Command Console Models ====================

class CommandStatsResponse(BaseModel):
    active_complaints: int
    loss_at_risk_inr: float
    open_alerts: int
    forecast_points: int
    monitored_nodes: int
    mean_confidence_pct: int

class TimingPatternPoint(BaseModel):
    hour: str
    cashouts: int

class DistrictRiskItem(BaseModel):
    district: str
    probability_pct: int
    tier: str

class TypologyMixItem(BaseModel):
    typology: str
    count: int
    pct: int

class AnomalyFeedItem(BaseModel):
    id: str
    title: str
    severity: str
    timestamp: str
    description: str

class HotspotCellResponse(BaseModel):
    h3_index: str
    district: str
    center_lat: float
    center_lon: float
    probability_pct: int
    risk_tier: str  # HIGH, WATCH, NORMAL
    reason_code: str
    reason_text: str
    total_loss_at_risk_inr: float
    linked_complaints: List[str]
    atm_nodes: List[str]

class AlertItemResponse(BaseModel):
    id: str
    alert_code: str
    scenario_id: str
    node_name: str
    bank_name: str
    district: str
    complaint_ref: str
    priority: str
    probability_pct: int
    reason_code: str
    reason_text: str
    status: str  # OPEN, DISPATCHED, ACKNOWLEDGED, RESOLVED
    beneficiary_bank: str
    beneficiary_account: str
    loss_amount_inr: float
    created_at: str

class AlertStatusUpdate(BaseModel):
    status: str
    notes: Optional[str] = ""

class AdvisoryResponse(BaseModel):
    notice_ref: str
    alert_code: str
    recipient_bank: str
    target_account: str
    advisory_text: str
    generated_at: str

class ScenarioItem(BaseModel):
    id: str
    name: str
    description: str
    is_active: bool
