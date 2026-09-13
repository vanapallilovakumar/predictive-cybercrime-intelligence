# PRAHARI & CYBER SAFELY: Predictive Cybercrime Cash-Out Forecasting & Citizen Protection
## Document 05: Backend Schema & Supabase SQL Specification

---

### 1. Database & Cloud Architecture Overview

PRAHARI & Cyber Safely utilizes **Supabase Cloud (PostgreSQL 15)** enhanced with:
1. **PostGIS:** Spatial queries and Uber H3 hexagonal coordinates.
2. **Supabase Auth:** Built-in passwordless **Email OTP** authentication for citizens.
3. **Supabase Storage:** S3-compatible cloud storage for complaint evidence (`complaint-evidence` bucket).

```
                      ┌──────────────────────────────────────────────┐
                      │                  scenarios                   │
                      │  id (PK) | name | description | is_active    │
                      └──────────────────────┬───────────────────────┘
                                             │ 1:N
        ┌────────────────────────────────────┼────────────────────────────────────┐
        │ 1:N                                │ 1:N                                │ 1:N
        ▼                                    ▼                                    ▼
┌──────────────────────────────┐   ┌──────────────────┐               ┌──────────────────┐
│          complaints          │   │  spatial_forecast│               │      alerts      │
│ id (PK)                      │   │ id (PK)          │               │ id (PK)          │
│ reference_no (NCRP/2026/...) │   │ h3_index         │◄──────┐       │ alert_code       │
│ typology                     │   │ probability      │       │       │ priority (HIGH)  │
│ loss_amount_inr              │   │ risk_tier (HIGH) │       │       │ reason_code      │
│ victim_name, victim_email    │   │ reason_code      │       │       │ status           │
│ victim_bank_name, account_no │   │ window_hours     │       │       │ forecast_id (FK)─┘
│ beneficiary_bank, account    │   └──────────────────┘       │       │ node_id (FK) ────┐
│ evidence_file_urls (TEXT[])  │                              │       └─────────┬────────┘
│ tracking_status (In Progress)│                              │                 │ 1:N
│ assigned_officer             │                              │                 ▼
│ node_id (FK) ──────────────┐ │                              │       ┌──────────────────┐
└────────────────────────────┼─┘                              │       │    advisories    │
                             │                                │       │ id (PK)          │
                             ▼                                │       │ notice_ref       │
                ┌─────────────────────────┐                   │       │ target_bank      │
                │      cashout_nodes      │                   │       │ advisory_text    │
                │ id (PK)                 │                   │       │ alert_id (FK) ───┘
                │ name, bank_name         │                   │       └──────────────────┘
                │ district, state         │                   │
                │ geom (Point)            │                   │
                │ h3_res7, h3_res8        │                   │
                └─────────────────────────┘                   │
                                                              │
┌──────────────────────────────┐                              │
│         scanned_urls         │ (Phishing Link Intelligence) │
│ id (PK) | url | verdict      │                              │
│ threat_score | risk_factors  │                              │
│ scanned_at                   │                              │
└──────────────────────────────┘                              │
```

---

### 2. Complete Supabase SQL Migration Script (DDL)

Execute this script in your Supabase SQL Editor (`Dashboard -> SQL Editor -> New Query`):

```sql
-- ============================================================================
-- PRAHARI & CYBER SAFELY: UNIFIED DATABASE SCHEMA MIGRATION
-- Project: SIH26184 (Ministry of Home Affairs)
-- ============================================================================

-- 1. Enable Extensions
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "postgis";

-- ----------------------------------------------------------------------------
-- 2. Drop existing tables for clean schema migration
-- ----------------------------------------------------------------------------
DROP TABLE IF EXISTS advisories CASCADE;
DROP TABLE IF EXISTS alerts CASCADE;
DROP TABLE IF EXISTS spatial_forecasts CASCADE;
DROP TABLE IF EXISTS complaints CASCADE;
DROP TABLE IF EXISTS cashout_nodes CASCADE;
DROP TABLE IF EXISTS scenarios CASCADE;
DROP TABLE IF EXISTS scanned_urls CASCADE;

-- ----------------------------------------------------------------------------
-- 3. Table: scenarios (Pre-computed Demo Scenarios)
-- ----------------------------------------------------------------------------
CREATE TABLE scenarios (
    id VARCHAR(50) PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    description TEXT,
    is_active BOOLEAN DEFAULT false,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- 4. Table: cashout_nodes (Physical ATMs, CSP Kiosks, Bank Branches)
-- ----------------------------------------------------------------------------
CREATE TABLE cashout_nodes (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    node_code VARCHAR(50) UNIQUE NOT NULL,
    name VARCHAR(150) NOT NULL,
    bank_name VARCHAR(100) NOT NULL,
    district VARCHAR(100) NOT NULL,
    state VARCHAR(100) NOT NULL,
    latitude DOUBLE PRECISION NOT NULL,
    longitude DOUBLE PRECISION NOT NULL,
    geom GEOMETRY(Point, 4326),
    h3_res7 VARCHAR(20) NOT NULL,
    h3_res8 VARCHAR(20) NOT NULL,
    is_monitored BOOLEAN DEFAULT true,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_cashout_nodes_geom ON cashout_nodes USING GIST(geom);
CREATE INDEX idx_cashout_nodes_h3 ON cashout_nodes(h3_res7);
CREATE INDEX idx_cashout_nodes_district ON cashout_nodes(district);

-- ----------------------------------------------------------------------------
-- 5. Table: complaints (Citizen Cybercrime Reports & Ingested Cases)
-- ----------------------------------------------------------------------------
CREATE TABLE complaints (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    reference_no VARCHAR(50) UNIQUE NOT NULL,
    scenario_id VARCHAR(50) REFERENCES scenarios(id) ON DELETE CASCADE,
    typology VARCHAR(50) NOT NULL,
    loss_amount_inr NUMERIC(12, 2) NOT NULL,
    
    -- Citizen Victim Details
    victim_name VARCHAR(150) DEFAULT 'Anonymous Citizen',
    victim_email VARCHAR(150),
    victim_bank_name VARCHAR(100) DEFAULT 'Not Disclosed',
    victim_account_no VARCHAR(50) DEFAULT 'XXXXXX0000',
    victim_district VARCHAR(100) NOT NULL,
    
    -- Suspect & Money Trail Information
    beneficiary_bank VARCHAR(100) NOT NULL,
    beneficiary_account VARCHAR(50) NOT NULL,
    reported_node_id UUID REFERENCES cashout_nodes(id) ON DELETE SET NULL,
    reported_district VARCHAR(100) NOT NULL,
    reported_phishing_url TEXT,
    evidence_file_urls TEXT[] DEFAULT '{}',
    description TEXT,
    
    -- Status & Triage Tracking (End-to-End Victim Restitution Milestones)
    priority_badge VARCHAR(20) DEFAULT 'medium',
    tracking_status VARCHAR(50) DEFAULT 'Under Review' CHECK (tracking_status IN ('Under Review', 'Investigation Active', 'Criminal Traced', 'Money Recovered', 'Returned to Victim', 'Closed')),
    assigned_officer VARCHAR(150) DEFAULT 'Inspector Vikram (State Cyber Cell)',
    status_notes TEXT,
    
    incident_timestamp TIMESTAMPTZ NOT NULL,
    reporting_timestamp TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_complaints_scenario ON complaints(scenario_id);
CREATE INDEX idx_complaints_reference ON complaints(reference_no);
CREATE INDEX idx_complaints_tracking_status ON complaints(tracking_status);

-- ----------------------------------------------------------------------------
-- 6. Table: spatial_forecasts (H3 Hexagonal Predictive Risk Windows)
-- ----------------------------------------------------------------------------
CREATE TABLE spatial_forecasts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    scenario_id VARCHAR(50) REFERENCES scenarios(id) ON DELETE CASCADE,
    h3_index VARCHAR(20) NOT NULL,
    district VARCHAR(100) NOT NULL,
    center_lat DOUBLE PRECISION NOT NULL,
    center_lon DOUBLE PRECISION NOT NULL,
    window_hours INT DEFAULT 6,
    probability_score DOUBLE PRECISION NOT NULL,
    risk_tier VARCHAR(20) NOT NULL CHECK (risk_tier IN ('HIGH', 'WATCH', 'NORMAL')),
    reason_code VARCHAR(100) NOT NULL,
    reason_text TEXT NOT NULL,
    total_loss_at_risk_inr NUMERIC(12, 2) DEFAULT 0,
    linked_complaints TEXT[] DEFAULT '{}',
    computed_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_spatial_forecasts_h3 ON spatial_forecasts(h3_index);
CREATE INDEX idx_spatial_forecasts_scenario ON spatial_forecasts(scenario_id);

-- ----------------------------------------------------------------------------
-- 7. Table: alerts (Actionable Investigator Leads & Patrol Dispatches)
-- ----------------------------------------------------------------------------
CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_code VARCHAR(50) UNIQUE NOT NULL,
    scenario_id VARCHAR(50) REFERENCES scenarios(id) ON DELETE CASCADE,
    forecast_id UUID REFERENCES spatial_forecasts(id) ON DELETE SET NULL,
    node_id UUID REFERENCES cashout_nodes(id) ON DELETE CASCADE,
    complaint_ref VARCHAR(50) NOT NULL,
    priority VARCHAR(20) NOT NULL CHECK (priority IN ('HIGH', 'MEDIUM', 'WATCH')),
    probability_pct INT NOT NULL,
    reason_code VARCHAR(100) NOT NULL,
    reason_text TEXT NOT NULL,
    status VARCHAR(30) DEFAULT 'OPEN' CHECK (status IN ('OPEN', 'DISPATCHED', 'ACKNOWLEDGED', 'RESOLVED', 'FALSE_POSITIVE')),
    dispatch_notes TEXT,
    assigned_officer VARCHAR(100) DEFAULT 'Inspector Vikram',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alerts_status ON alerts(status);
CREATE INDEX idx_alerts_scenario ON alerts(scenario_id);

-- ----------------------------------------------------------------------------
-- 8. Table: advisories (Section 91 BNSS / CrPC Bank Freeze Notices)
-- ----------------------------------------------------------------------------
CREATE TABLE advisories (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    notice_ref VARCHAR(50) UNIQUE NOT NULL,
    alert_id UUID REFERENCES alerts(id) ON DELETE CASCADE,
    recipient_bank VARCHAR(100) NOT NULL,
    target_account VARCHAR(50) NOT NULL,
    target_atm_name VARCHAR(150),
    advisory_text TEXT NOT NULL,
    generated_by VARCHAR(100) DEFAULT 'State Cyber Command',
    generated_at TIMESTAMPTZ DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- 9. Table: scanned_urls (Phishing Link Intelligence & Audit)
-- ----------------------------------------------------------------------------
CREATE TABLE scanned_urls (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    url TEXT NOT NULL,
    verdict VARCHAR(50) NOT NULL CHECK (verdict IN ('MALICIOUS_PHISHING', 'SUSPICIOUS', 'SAFE')),
    threat_score DOUBLE PRECISION NOT NULL,
    risk_factors JSONB DEFAULT '[]'::jsonb,
    scanned_by_email VARCHAR(150),
    scanned_at TIMESTAMPTZ DEFAULT NOW()
);

-- ----------------------------------------------------------------------------
-- 10. Supabase Storage Bucket Setup & Row Level Security (RLS)
-- ----------------------------------------------------------------------------
-- Create storage bucket for citizen complaint receipts/screenshots
INSERT INTO storage.buckets (id, name, public)
VALUES ('complaint-evidence', 'complaint-evidence', true)
ON CONFLICT (id) DO NOTHING;

-- Enable RLS across all tables
ALTER TABLE scenarios ENABLE ROW LEVEL SECURITY;
ALTER TABLE cashout_nodes ENABLE ROW LEVEL SECURITY;
ALTER TABLE complaints ENABLE ROW LEVEL SECURITY;
ALTER TABLE spatial_forecasts ENABLE ROW LEVEL SECURITY;
ALTER TABLE alerts ENABLE ROW LEVEL SECURITY;
ALTER TABLE advisories ENABLE ROW LEVEL SECURITY;
ALTER TABLE scanned_urls ENABLE ROW LEVEL SECURITY;

-- Allow public read/write access via API keys for hackathon prototype
CREATE POLICY "Allow public read-write for scenarios" ON scenarios FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow public read-write for cashout_nodes" ON cashout_nodes FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow public read-write for complaints" ON complaints FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow public read-write for spatial_forecasts" ON spatial_forecasts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow public read-write for alerts" ON alerts FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow public read-write for advisories" ON advisories FOR ALL USING (true) WITH CHECK (true);
CREATE POLICY "Allow public read-write for scanned_urls" ON scanned_urls FOR ALL USING (true) WITH CHECK (true);

-- Allow public uploads to complaint-evidence bucket
CREATE POLICY "Allow public uploads to complaint-evidence" ON storage.objects
FOR ALL USING (bucket_id = 'complaint-evidence') WITH CHECK (bucket_id = 'complaint-evidence');
```

---

### 3. Updated Seed Data Script

```sql
-- ============================================================================
-- PRAHARI & CYBER SAFELY: SEED DATA
-- ============================================================================

-- 1. Scenarios
INSERT INTO scenarios (id, name, description, is_active) VALUES
('scenario_a', 'Active Mule Surge', 'High-intensity ATM cash-outs across Jamtara-Deoghar corridor', true),
('scenario_b', 'Digital Arrest Corridor', 'Targeted extortion burst in Nuh-Bharatpur', false),
('scenario_c', 'Baseline Calm State', 'Normal low-velocity complaints with low forecast probabilities', false);

-- 2. Cashout Nodes
INSERT INTO cashout_nodes (node_code, name, bank_name, district, state, latitude, longitude, geom, h3_res7, h3_res8) VALUES
('NODE-DEO-01', 'Deoghar Bus Stand ATM', 'Bank of India', 'Deoghar', 'Jharkhand', 24.4854, 86.6978, ST_SetSRID(ST_MakePoint(86.6978, 24.4854), 4326), '876014524ffffff', '8860145241fffff'),
('NODE-JAM-01', 'Jamtara Main Road ATM Cluster', 'Bank of India', 'Jamtara', 'Jharkhand', 23.9620, 86.8020, ST_SetSRID(ST_MakePoint(86.8020, 23.9620), 4326), '87601440affffff', '88601440a3fffff'),
('NODE-JAM-02', 'Karmatanr Bazaar Kiosk', 'State Bank of India', 'Jamtara', 'Jharkhand', 24.0880, 86.7620, ST_SetSRID(ST_MakePoint(86.7620, 24.0880), 4326), '876014413ffffff', '8860144135fffff'),
('NODE-NUH-01', 'Nuh Tauru Chowk ATM', 'Punjab National Bank', 'Nuh', 'Haryana', 28.1060, 77.0120, ST_SetSRID(ST_MakePoint(77.0120, 28.1060), 4326), '872f056d6ffffff', '882f056d67fffff'),
('NODE-BHA-01', 'Bharatpur Station Road ATM', 'Bank of Baroda', 'Bharatpur', 'Rajasthan', 27.2170, 77.4895, ST_SetSRID(ST_MakePoint(77.4895, 27.2170), 4326), '872f0535affffff', '882f0535a1fffff'),
('NODE-GIR-01', 'Giridih Station Road Branch', 'Bandhan Bank', 'Giridih', 'Jharkhand', 24.1840, 86.3050, ST_SetSRID(ST_MakePoint(86.3050, 24.1840), 4326), '876014695ffffff', '8860146959fffff');

-- 3. Complaints (With Citizen Tracking Data)
INSERT INTO complaints (reference_no, scenario_id, typology, loss_amount_inr, victim_name, victim_email, victim_bank_name, victim_account_no, victim_district, beneficiary_bank, beneficiary_account, reported_district, priority_badge, tracking_status, assigned_officer, status_notes, incident_timestamp) VALUES
('NCRP/2026/000185', 'scenario_a', 'Job fraud', 175000.00, 'Sunita Sen', 'sunita.sen@gmail.com', 'HDFC Bank', 'XXXXXX4512', 'Kolkata', 'Bandhan Bank', 'XXXXXX7812', 'Giridih', 'high', 'Action in Progress', 'Inspector Vikram (Cyber Cell)', 'Patrol team alerted to Giridih Station Road ATM cluster.', NOW() - INTERVAL '3 hours'),
('NCRP/2026/000181', 'scenario_a', 'UPI fraud', 148000.00, 'Rohan Sharma', 'rohan@example.com', 'State Bank of India', 'XXXXXX1290', 'Pune', 'Bank of India', 'XXXXXX4921', 'Deoghar', 'medium', 'Action in Progress', 'Inspector Vikram (Cyber Cell)', 'Patrol alerted to Deoghar Bus Stand ATM; Bank Freeze Notice issued to Bank of India.', NOW() - INTERVAL '5 hours'),
('NCRP/2026/000183', 'scenario_a', 'Digital arrest', 255000.00, 'Anil Verma', 'anil.verma@yahoo.com', 'ICICI Bank', 'XXXXXX9012', 'Lucknow', 'Punjab National Bank', 'XXXXXX1084', 'Nuh', 'high', 'Under Review', 'Inspector Vikram (Cyber Cell)', 'Case under AI spatio-temporal correlation.', NOW() - INTERVAL '2 hours'),
('NCRP/2026/000186', 'scenario_a', 'OTP fraud', 66000.00, 'Kavita Joshi', 'kavita.j@outlook.com', 'Axis Bank', 'XXXXXX2389', 'Jaipur', 'Bank of Baroda', 'XXXXXX3391', 'Bharatpur', 'medium', 'Under Review', 'Inspector Vikram (Cyber Cell)', 'Awaiting bank nodal confirmation.', NOW() - INTERVAL '4 hours'),
('NCRP/2026/000182', 'scenario_a', 'Investment scam', 620000.00, 'George Mathew', 'george.m@gmail.com', 'Federal Bank', 'XXXXXX6610', 'Ernakulam', 'IDFC First', 'XXXXXX9820', 'Jamtara', 'medium', 'Action in Progress', 'Inspector Vikram (Cyber Cell)', 'Coordinated mule hopping pattern flagged in Jamtara Main Road.', NOW() - INTERVAL '6 hours'),
('NCRP/2026/000184', 'scenario_a', 'Loan app extortion', 92000.00, 'Mahesh Shinde', 'mahesh.s@rediffmail.com', 'Bank of Maharashtra', 'XXXXXX5521', 'Nagpur', 'Yes Bank', 'XXXXXX6643', 'Mathura', 'medium', 'Resolved', 'Inspector Vikram (Cyber Cell)', 'Beneficiary account debits frozen before cash withdrawal occurred.', NOW() - INTERVAL '1 hour');

-- 4. Spatial Forecasts & Alerts (Preserved from v1.0)
INSERT INTO spatial_forecasts (scenario_id, h3_index, district, center_lat, center_lon, window_hours, probability_score, risk_tier, reason_code, reason_text, total_loss_at_risk_inr, linked_complaints) VALUES
('scenario_a', '8860145241fffff', 'Deoghar', 24.4854, 86.6978, 6, 0.77, 'HIGH', 'LATE_NIGHT_FREEZE_DODGE', 'Incident occurred in the late-night window used to dodge bank freeze desks', 148000.00, ARRAY['NCRP/2026/000181']),
('scenario_a', '88601440a3fffff', 'Jamtara', 23.9620, 86.8020, 6, 0.71, 'HIGH', 'RAPID_MULE_HOPPING', 'Coordinated cash-out cluster detected across multiple terminals', 620000.00, ARRAY['NCRP/2026/000182']),
('scenario_a', '882f056d67fffff', 'Nuh', 28.1060, 77.0120, 6, 0.71, 'HIGH', 'HIGH_LOSS_VELOCITY_SPIKE', 'High-loss extortion withdrawal window open', 255000.00, ARRAY['NCRP/2026/000183']),
('scenario_a', '882f0535a1fffff', 'Bharatpur', 27.2170, 77.4895, 6, 0.66, 'WATCH', 'PREDICTED_SPILLOVER', 'Secondary mule hopping corridor anticipated', 66000.00, ARRAY['NCRP/2026/000186']),
('scenario_a', '8860146959fffff', 'Giridih', 24.1840, 86.3050, 6, 0.39, 'WATCH', 'ISOLATED_ATM_SURGE', 'Moderate probability cash-out node opening', 175000.00, ARRAY['NCRP/2026/000185']);

INSERT INTO alerts (alert_code, scenario_id, node_id, complaint_ref, priority, probability_pct, reason_code, reason_text, status)
SELECT 'ALT-2026-001', 'scenario_a', id, 'NCRP/2026/000181', 'HIGH', 77, 'LATE_NIGHT_FREEZE_DODGE', 'Incident occurred in the late-night window used to dodge bank freeze desks', 'OPEN'
FROM cashout_nodes WHERE node_code = 'NODE-DEO-01';

INSERT INTO alerts (alert_code, scenario_id, node_id, complaint_ref, priority, probability_pct, reason_code, reason_text, status)
SELECT 'ALT-2026-002', 'scenario_a', id, 'NCRP/2026/000183', 'HIGH', 71, 'HIGH_LOSS_VELOCITY_SPIKE', 'High-velocity cash-out window active dodging freeze desk', 'OPEN'
FROM cashout_nodes WHERE node_code = 'NODE-NUH-01';

INSERT INTO alerts (alert_code, scenario_id, node_id, complaint_ref, priority, probability_pct, reason_code, reason_text, status)
SELECT 'ALT-2026-003', 'scenario_a', id, 'NCRP/2026/000182', 'HIGH', 71, 'RAPID_MULE_HOPPING', 'Coordinated mule ring withdrawing across Jamtara Main Road', 'OPEN'
FROM cashout_nodes WHERE node_code = 'NODE-JAM-01';
```

---

### 4. Supabase Python Client Integration Patterns

```python
# backend/db.py
import os
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv()

SUPABASE_URL = os.getenv("SUPABASE_URL", "")
SUPABASE_KEY = os.getenv("SUPABASE_KEY", "")

def get_supabase() -> Client:
    if not SUPABASE_URL or not SUPABASE_KEY:
        raise ValueError("SUPABASE_URL and SUPABASE_KEY must be configured in .env")
    return create_client(SUPABASE_URL, SUPABASE_KEY)

# Citizen Authentication
def send_email_otp(email: str):
    client = get_supabase()
    return client.auth.sign_in_with_otp({"email": email})

def verify_email_otp(email: str, token: str):
    client = get_supabase()
    return client.auth.verify_otp({"email": email, "token": token, "type": "email"})

# Complaint Tracking
def track_complaint_status(reference_no: str):
    client = get_supabase()
    res = client.table("complaints").select(
        "reference_no, typology, loss_amount_inr, victim_bank_name, tracking_status, assigned_officer, status_notes, incident_timestamp"
    ).eq("reference_no", reference_no).execute()
    return res.data[0] if res.data else None

# Evidence Upload
def upload_evidence(reference_no: str, filename: str, file_bytes: bytes, mime_type: str) -> str:
    client = get_supabase()
    path = f"evidence/{reference_no}/{filename}"
    client.storage.from_("complaint-evidence").upload(path, file_bytes, {"content-type": mime_type})
    return client.storage.from_("complaint-evidence").get_public_url(path)
```
