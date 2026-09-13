"""
Cyber Safely Guidance & Emergency Restitution Knowledge Base
"""

GOLDEN_HOUR_ADVISORY = {
    "title": "The Golden Hour Rule (Immediate Action)",
    "helpline": "1930",
    "portal": "cybercrime.gov.in",
    "summary": "If you lost money to cyber fraud, reporting within the FIRST 2 HOURS gives an 80%+ chance of stopping cash withdrawals and freezing funds in the beneficiary account.",
    "steps": [
        "1. Immediately call the National Cyber Crime Helpline 1930 or log in here to file a report.",
        "2. Keep your Transaction ID (UTR / RRN), Victim Bank Name, and Suspect Beneficiary Account handy.",
        "3. Notify your home branch immediately to request a temporary debit freeze on compromised cards.",
        "4. Save all WhatsApp/SMS chats, payment slips, and call logs as digital evidence."
    ]
}

TYPOLOGY_GUIDANCE = [
    {
        "typology": "OTP & KYC Fraud",
        "icon": "📱",
        "danger_signs": [
            "Calls claiming your SIM card, bank account, or credit card will be blocked within 24 hours.",
            "Requests to install remote access apps like AnyDesk, TeamViewer, or QuickSupport.",
            "SMS with short links asking you to update PAN card or KYC details."
        ],
        "dos": [
            "Only update KYC by visiting your official bank branch or official net banking app.",
            "Check SMS header codes (official bank SMS headers start with 2 characters like VM-SBI, AX-HDFC)."
        ],
        "donts": [
            "NEVER share your 6-digit OTP or ATM PIN with anyone, even if they claim to be bank managers.",
            "NEVER click on links received via SMS claiming reward points or lottery claims."
        ]
    },
    {
        "typology": "Digital Arrest Scams",
        "icon": "⚖️",
        "danger_signs": [
            "Video calls on WhatsApp/Skype from persons wearing police uniforms claiming a parcel with narcotics was seized.",
            "Claims that an arrest warrant has been issued by CBI, ED, or Supreme Court.",
            "Demands to remain on video call in a locked room ('Digital Arrest') and transfer money to 'RBI verification accounts'."
        ],
        "dos": [
            "Immediately disconnect the video call. Law enforcement NEVER conducts arrests or trials via video calls.",
            "Report the phone number immediately to 1930 Helpline and the local police station.",
            "Talk to family members or trusted friends before taking any panic action."
        ],
        "donts": [
            "NEVER transfer money to any 'safe account' or 'police verification account' — no such account exists.",
            "Do NOT share bank account balances or screens under threat of immediate arrest."
        ]
    },
    {
        "typology": "Part-Time Job & Telegram Tasks",
        "icon": "💼",
        "danger_signs": [
            "WhatsApp messages offering ₹3,000–₹8,000/day for liking YouTube videos or writing Google reviews.",
            "Initial small payouts (₹150–₹500) provided to win trust, followed by Telegram group invitations.",
            "Demands to deposit 'prepaid task fees' to unlock accumulated pseudo-earnings."
        ],
        "dos": [
            "Verify employment opportunities directly on company career portals.",
            "Recognize that genuine employers pay you for work; they NEVER ask you to deposit money first."
        ],
        "donts": [
            "NEVER transfer money to participate in 'crypto investment' or 'prepaid review' tasks.",
            "Do not trust screenshots of supposed huge profits shared in Telegram groups."
        ]
    },
    {
        "typology": "Fake Loan Apps & Extortion",
        "icon": "💸",
        "danger_signs": [
            "Apps offering instant loans without CIBIL score or documentation.",
            "Apps requesting full access to your phone contacts, gallery, and camera.",
            "Harassment calls with morphed photographs sent to your phone contacts within 7 days."
        ],
        "dos": [
            "Only borrow from RBI-registered Banks and Non-Banking Financial Companies (NBFCs).",
            "File a complaint under Information Technology Act and Section 308 BNSS for extortion."
        ],
        "donts": [
            "NEVER download `.apk` loan applications from WhatsApp links or third-party websites.",
            "Do not pay blackmailers repeated sums; file an official police complaint immediately."
        ]
    }
]
