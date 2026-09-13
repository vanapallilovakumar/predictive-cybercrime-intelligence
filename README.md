# PRAHARI & CYBER SAFELY: Predictive Cybercrime Intelligence & Citizen Protection
> **Smart India Hackathon (SIH 2026)** | Problem Statement ID: **SIH26184** (Ministry of Home Affairs)  
> **Team Name:** TRACE X  
> **Core Concept:** A Spatio-Temporal AI Early-Warning System Forecasting Illicit Cash-Outs Combined with Citizen Threat Prevention & Reporting.

---

## Complete MVP Documentation Suite (v2.0)

All 6 architectural and implementation blueprints have been compiled for building the unified MVP:

1. **[Product Requirements Document (PRD)](docs/01_product_requirements_document.md)**
   * Dual mission: Citizen front ("Cyber Safely") for phishing prevention and crime reporting + Law enforcement front ("PRAHARI Command") for predictive cash-out forecasting.
   * User personas, MVP scope boundaries, and functional requirements for both portals.
2. **[Technical Requirements Document (TRD)](docs/02_technical_requirements_document.md)**
   * Two-Tier 100% Python architecture (Streamlit + FastAPI), Uber H3 hexagonal binning, 3-model AI pipeline (Gradient Boosting, DBSCAN, Isolation Forest), Hybrid Phishing Link Scanner engine, and Supabase Auth Email OTP & Storage integration.
3. **[Workflow & Application Flow](docs/03_workflow_and_app_flow.md)**
   * End-to-end intelligence lifecycle, Mermaid sequence and state diagrams, detailed step-by-step citizen & investigator walkthroughs, and cross-system status synchronization.
4. **[UI/UX Specification](docs/04_ui_ux_specification.md)**
   * Dual-Portal layout wireframes: Citizen Protection UI (OTP login card, phishing scanner with red warning banners, crime intake form, simple status badge tracking, safety guidance) + Police Command Console (dark tactical theme matching reference dashboard).
5. **[Backend Schema & Supabase SQL](docs/05_backend_schema_and_supabase.md)**
   * Supabase PostgreSQL + PostGIS schema, `complaint-evidence` storage bucket setup, complete copy-paste DDL script, RLS policies, seed dataset, and Python client integration code.
6. **[Implementation Plan & Build Guide](docs/06_implementation_plan.md)**
   * Clean repository file structure, `requirements.txt`, phishing scanner code (`scanner.py`), model training script (`train.py`), one-command launcher (`run_prahari.py`), and a verification testing checklist.

---

## Tech Stack Summary

* **Frontend:** 100% Python via **Streamlit** (with `streamlit-folium` / `pydeck` for H3 risk maps). Zero JavaScript required.
* **Backend API:** **FastAPI** + **Uvicorn** (asynchronous REST API).
* **Database & Cloud:** **Supabase Cloud** (PostgreSQL 15 with **PostGIS**, **Supabase Auth Email OTP**, and **Supabase Storage** for complaint receipts).
* **AI & Security Engine:** **scikit-learn** (`HistGradientBoostingClassifier`, `DBSCAN`, `IsolationForest`), **uber-h3** (`h3-py`), **pandas**, and a **Python Phishing Threat Scanner**.
