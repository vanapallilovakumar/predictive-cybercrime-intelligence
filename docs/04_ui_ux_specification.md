# PRAHARI & CYBER SAFELY: Predictive Cybercrime Cash-Out Forecasting & Citizen Protection
## Document 04: UI/UX Specification Document

---

### 1. Dual-Portal User Experience Design System

PRAHARI & Cyber Safely features two distinct yet harmonized user interfaces:
1. **The Citizen Safety Portal ("Cyber Safely"):** Clean, approachable, reassuring, and accessible to non-technical citizens. Designed to prevent panic, provide instant link security awareness, and streamline crime reporting.
2. **The Intelligence Command Console ("PRAHARI Command"):** High-contrast, data-dense dark tactical console for cyber police investigators and bank nodal fraud analysts.

---

### 2. Global Shell & Navigation Architecture

```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ [P] PRAHARI & CYBER SAFELY      [🛡️ Citizen Safety]    [⚡ Command Center]  [👤 Logout] │
└────────────────────────────────────────────────────────────────────────────────────────┘
```
* **Top Navigation Bar:**
  * **Brand Mark:** Dark shield badge with cyan letter **P**, accompanied by **PRAHARI & Cyber Safely**.
  * **Portal Selector Pills:** Allows seamless switching between the public citizen front and the authorized police command console.
  * **Session Indicator:** Shows active citizen email or officer badge ID (`Inspector Vikram`).

---

### 3. Citizen Portal UI Wireframes ("Cyber Safely")

#### 3.1 Screen C-1: Email OTP Login Modal / Card
```
┌─────────────────────────────────────────────────────────┐
│                    🛡️ CYBER SAFELY                       │
│              Citizen Protection & Reporting             │
│                                                         │
│  Enter your email to sign in or file an urgent report:  │
│  ┌───────────────────────────────────────────────────┐  │
│  │ rohan.sharma@example.com                          │  │
│  └───────────────────────────────────────────────────┘  │
│  [ Send Login Code (OTP) ]                              │
│                                                         │
│  Enter 6-Digit Code sent to your inbox:                 │
│  ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐ ┌───┐                    │
│  │ 5 │ │ 8 │ │ 2 │ │ 9 │ │ 1 │ │ 4 │                    │
│  └───┘ └───┘ └───┘ └───┘ └───┘ └───┘                    │
│  [ Verify Code & Enter Portal ]                         │
│                                                         │
│  🔒 Powered by Supabase Secure Authentication           │
└─────────────────────────────────────────────────────────┘
```

---

#### 3.2 Screen C-2: Phishing Link Scanner ("Cyber Safely Awareness")
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 🔍 PHISHING & FRAUD LINK CHECKER                                                       │
│ Received a suspicious link on SMS or WhatsApp? Check if it is fake before clicking!    │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Enter Website Link:                                                                    │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ http://sbi-reward-kyc.top/claim-bonus.apk                                          │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
│ [ ⚡ Analyze Link Security ]                                                           │
│                                                                                        │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ 🚨 HIGH-RISK FAKE / PHISHING LINK DETECTED                                          │ │
│ │                                                                                    │ │
│ │ • Impersonation: Deceptive website pretending to be State Bank of India ('sbi').   │ │
│ │ • High-Risk Domain: Registered under untrusted extension (.top).                   │ │
│ │ • Malicious File: Attempts to download an unauthorized Android application (.apk).  │ │
│ │                                                                                    │ │
│ │ 🛡️ SAFETY ADVICE FOR YOU:                                                          │ │
│ │ 1. DO NOT open this website or fill any forms.                                     │ │
│ │ 2. Official banks NEVER use .top, .xyz, or .site domains.                          │ │
│ │ 3. NEVER enter your Net Banking Password, ATM PIN, or OTP on unverified links.     │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

#### 3.3 Screen C-3: Report a Cybercrime Form (`/intake`)
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 📝 LODGE OFFICIAL CYBERCRIME COMPLAINT                                                 │
│ Report financial fraud immediately to trigger AI cash-out forecasting & bank freezes.   │
├────────────────────────────────────────────────────┬───────────────────────────────────┤
│ 1. INCIDENT DETAILS                                │ 2. FINANCIAL LOSS & BANK DETAILS  │
│ Typology:                                          │ Amount Lost (INR):                │
│ [ OTP Fraud                            ▼ ]         │ [ ₹ 1,48,000                    ] │
│ Date & Time of Incident:                           │ Your Bank Name (Victim Bank):     │
│ [ 12/09/2026, 17:30 IST                📅 ]         │ [ State Bank of India           ] │
│ Your District / City:                              │ Your Account Number (Last 4 Dig): │
│ [ Pune                                 ]           │ [ XXXXXX1290                    ] │
├────────────────────────────────────────────────────┼───────────────────────────────────┤
│ 3. SUSPECT / BENEFICIARY INFORMATION               │ 4. UPLOAD EVIDENCE & RECEIPTS     │
│ Suspect Bank (where money went):                   │ Attach Screenshot / PDF Receipt:  │
│ [ Bank of India                        ▼ ]         │ ┌───────────────────────────────┐ │
│ Suspect Account / UPI ID (if available):           │ │ [ 📎 Drag & Drop Files Here ] │ │
│ [ XXXXXX4921 / paytm-mule@okaxis       ]           │ │ Max size: 10MB (PNG, JPG, PDF)│ │
│ Suspect Branch / ATM Location (if known):          │ └───────────────────────────────┘ │
│ [ Deoghar, Jharkhand                   ]           │ Attached: fake_sms_screenshot.png │
├────────────────────────────────────────────────────┴───────────────────────────────────┤
│ ⚠️ Golden Hour Notice: If this incident happened within the last 2 hours, also dial    │
│    the 1930 Cyber Fraud Helpline immediately.                                          │
│                                                                                        │
│ [ 🚀 Submit Official Complaint to Live Intelligence Engine ]                          │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

#### 3.4 Screen C-4: Track Complaint Status (End-to-End Restitution Progress)
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 🔎 TRACK YOUR CYBERCRIME COMPLAINT                                                     │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ Enter Complaint Reference: [ NCRP/2026/000181             ]  [ 🔍 Check Status ]       │
│                                                                                        │
│ ┌────────────────────────────────────────────────────────────────────────────────────┐ │
│ │ Case Reference: NCRP/2026/000181                         Filing Date: 12 Sep 2026  │
│ │ Category:       UPI Fraud                                Amount Lost: ₹1,48,000    │
│ │ Victim Bank:    State Bank of India (A/C: XXXXXX1290)                              │
│ │                                                                                    │ │
│ │ CURRENT RESOLUTION STATUS:                                                         │ │
│ │ ┌────────────────────────────────────────────────────────────────────────────────┐ │ │
│ │ │ 🟢 MONEY RECOVERED & RETURNED TO VICTIM ACCOUNT                                │ │ │
│ │ └────────────────────────────────────────────────────────────────────────────────┘ │ │
│ │                                                                                    │ │
│ │ [✓] 1. Complaint Lodged & Assigned to Investigation Officer                        │ │
│ │ [✓] 2. Investigation & AI Hotspot Interception Active                              │ │
│ │ [✓] 3. Criminal Located & Stolen Funds Frozen (Sec 91 BNSS Bank Freeze)            │ │
│ │ [✓] 4. Money Successfully Re-Credited to Your Bank Account (Restitution Complete)  │ │
│ │                                                                                    │ │
│ │ Assigned Police Unit:  Inspector Vikram (State Cyber Crime Police Station)         │ │
│ │ Final Police Remark:   Patrol intercepted cash mule at Deoghar Bus Stand ATM.     │ │
│ │                        ₹1,48,000 reversed from beneficiary bank to victim account. │ │
│ └────────────────────────────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────────────────────────┘
```

---

#### 3.5 Screen C-5: Safety Guidance & 1930 Golden Hour Advisory
```
┌────────────────────────────────────────────────────────────────────────────────────────┐
│ 🛡️ CYBER SAFETY GUIDANCE & PREVENTION                                                  │
├────────────────────────────────────────────────────────────────────────────────────────┤
│ 🚨 THE "GOLDEN HOUR" RULE                                                              │
│ If you lost money in a cyber fraud, reporting within the FIRST 2 HOURS gives an 80%+   │
│ chance of freezing the money before cash-out. Dial 1930 Helpline immediately!          │
├──────────────────────────┬──────────────────────────┬──────────────────────────────────┤
│ 📱 OTP & KYC FRAUDS      │ ⚖️ DIGITAL ARREST SCAMS  │ 💼 FAKE PART-TIME JOBS           │
│ • Bank staff NEVER ask   │ • Police / CBI NEVER do  │ • Legitimate companies NEVER     │
│   for OTPs on the phone. │   arrests via Skype or   │   charge registration fees.      │
│ • Never install AnyDesk  │   WhatsApp video calls.  │ • Do not send money to unlock    │
│   or QuickSupport apps.  │ • Never transfer funds   │   "Telegram task earnings".      │
│ • Verify SMS sender IDs. │   to "security accounts".│ • Block suspicious recruitment   │
└──────────────────────────┴──────────────────────────┴──────────────────────────────────┘
```

---

### 4. Investigator Command Console UI ("PRAHARI Command")

The Command Console maintains the exact high-contrast dark layout, typography, and color tokens from Document 04 v1.0 and the reference HTML:
* **Background Canvas:** `#0b0f19` (dark navy)
* **Panel Containers:** `#111827` (slate-900 with `#1f2937` border)
* **Top Metric Bar:** 4 live KPIs (Active complaints, Open alerts, Monitored cash-out nodes, Mean confidence %).
* **Analytical Visualizations:** Withdrawal timing pattern line chart, District risk index progress bars, Typology mix horizontal bars, Anomalies feed, Next windows opening list.
* **Recent Complaints Table:** Live feed of both synthetic scenario records and newly submitted citizen complaints.
* **Interactive Hotspots Map:** Uber H3 hexagonal tiles (Res 7/8) with risk tiers (Crimson Red, Amber, Slate) and side drawer inspection.
* **Alerts Queue:** One-click Section 91 BNSS Bank Freeze Notice generation.

---

### 5. Streamlit Theme & Component Injector (`frontend/theme.py`)

```python
# frontend/theme.py
import streamlit as st

def apply_unified_theme(mode: str = "citizen"):
    """
    Applies custom styling. 
    mode="citizen": Clean, approachable, modern dark styling.
    mode="command": High-contrast tactical command center styling.
    """
    st.markdown("""
    <style>
    /* Global Base */
    .stApp {
        background-color: #0b0f19;
        color: #f8fafc;
        font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, sans-serif;
    }
    
    /* Reusable Card Panel */
    .prahari-card {
        background-color: #111827;
        border: 1px solid #1f2937;
        border-radius: 8px;
        padding: 1.25rem;
        margin-bottom: 1rem;
    }
    
    /* Phishing Danger Banner */
    .phishing-danger {
        background: rgba(239, 68, 68, 0.12);
        border: 1px solid #ef4444;
        border-radius: 8px;
        padding: 1.25rem;
        color: #fecaca;
        margin-top: 1rem;
    }
    
    /* Phishing Safe Banner */
    .phishing-safe {
        background: rgba(34, 197, 94, 0.12);
        border: 1px solid #22c55e;
        border-radius: 8px;
        padding: 1.25rem;
        color: #bbf7d0;
        margin-top: 1rem;
    }
    
    /* Status Badges */
    .badge-progress {
        background: rgba(245, 158, 11, 0.2);
        color: #f59e0b;
        border: 1px solid #f59e0b;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    .badge-resolved {
        background: rgba(34, 197, 94, 0.2);
        color: #22c55e;
        border: 1px solid #22c55e;
        padding: 4px 12px;
        border-radius: 9999px;
        font-weight: 700;
        font-size: 0.85rem;
        display: inline-block;
    }
    
    /* Micro-caps */
    .label-caps {
        font-size: 0.7rem;
        text-transform: uppercase;
        letter-spacing: 0.08em;
        font-weight: 600;
        color: #94a3b8;
    }
    </style>
    """, unsafe_allow_html=True)
```
