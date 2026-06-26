"""
AI Medical Diagnosis System — Premium Streamlit Frontend
=========================================================
Author  : Senior UI/UX Engineer
Backend : FastAPI (unchanged — only the frontend is redesigned)
"""

# =============================================================
# 1. IMPORTS
# =============================================================

import os
import datetime

import requests
import streamlit as st
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

# ----- env -----
load_dotenv()
API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")


# =============================================================
# 2. CSS — Design System
# =============================================================

def inject_css():
    st.markdown(
        """
        <style>
        /* ── Google Fonts ───────────────────────────────── */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&family=DM+Serif+Display&display=swap');

        /* ── Reset / Base ───────────────────────────────── */
        html, body, [class*="css"] {
            font-family: 'Inter', sans-serif;
        }

        /* Hide Streamlit chrome */
        #MainMenu, footer, header { visibility: hidden; }
        .block-container { padding: 0 !important; }

        /* ── Color tokens ───────────────────────────────── */
        :root {
            --bg:        #F7F8FC;
            --surface:   #FFFFFF;
            --border:    #E8EAF0;
            --text:      #1A1D2E;
            --muted:     #6B7080;
            --accent:    #2563EB;
            --accent-lt: #EEF3FF;
            --accent-dk: #1D4ED8;
            --green:     #059669;
            --green-lt:  #ECFDF5;
            --red:       #DC2626;
            --red-lt:    #FEF2F2;
            --amber:     #D97706;
            --amber-lt:  #FFFBEB;
            --radius-sm: 8px;
            --radius-md: 14px;
            --radius-lg: 20px;
            --shadow-sm: 0 1px 3px rgba(0,0,0,.06), 0 1px 2px rgba(0,0,0,.04);
            --shadow-md: 0 4px 12px rgba(0,0,0,.08);
            --shadow-lg: 0 16px 40px rgba(0,0,0,.10);
        }

        /* ── Page background ─────────────────────────────── */
        .stApp { background: var(--bg); }

        /* ── Sidebar ─────────────────────────────────────── */
        [data-testid="stSidebar"] {
            background: var(--surface) !important;
            border-right: 1px solid var(--border);
        }
        [data-testid="stSidebar"] * { color: var(--text) !important; }

        /* ── Typography helpers ──────────────────────────── */
        .display-title {
            font-family: 'DM Serif Display', serif;
            font-size: 3rem;
            line-height: 1.15;
            color: var(--text);
            letter-spacing: -0.02em;
        }
        .section-title {
            font-size: 1.15rem;
            font-weight: 600;
            color: var(--text);
            margin: 0 0 4px;
        }
        .label {
            font-size: 0.78rem;
            font-weight: 500;
            text-transform: uppercase;
            letter-spacing: .06em;
            color: var(--muted);
        }

        /* ── Cards ───────────────────────────────────────── */
        .card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 24px 28px;
            box-shadow: var(--shadow-sm);
        }
        .card-hover {
            transition: box-shadow .2s, transform .2s;
        }
        .card-hover:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-2px);
        }

        /* ── Feature cards (landing) ─────────────────────── */
        .feature-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 28px 24px;
            text-align: center;
            box-shadow: var(--shadow-sm);
            transition: box-shadow .2s, transform .2s;
            height: 100%;
        }
        .feature-card:hover {
            box-shadow: var(--shadow-md);
            transform: translateY(-3px);
        }
        .feature-icon {
            font-size: 2.2rem;
            margin-bottom: 14px;
        }
        .feature-title {
            font-size: 1rem;
            font-weight: 600;
            color: var(--text);
            margin-bottom: 6px;
        }
        .feature-desc {
            font-size: 0.85rem;
            color: var(--muted);
            line-height: 1.55;
        }

        /* ── Hero gradient strip ─────────────────────────── */
        .hero-wrap {
            background: linear-gradient(135deg, #1e40af 0%, #2563eb 45%, #3b82f6 100%);
            border-radius: var(--radius-lg);
            padding: 56px 52px;
            color: #fff;
            position: relative;
            overflow: hidden;
        }
        .hero-wrap::after {
            content: '';
            position: absolute;
            right: -60px; top: -80px;
            width: 320px; height: 320px;
            background: rgba(255,255,255,.06);
            border-radius: 50%;
        }
        .hero-title {
            font-family: 'DM Serif Display', serif;
            font-size: 2.6rem;
            line-height: 1.2;
            margin: 0 0 12px;
        }
        .hero-sub {
            font-size: 1.05rem;
            opacity: .85;
            max-width: 480px;
            line-height: 1.6;
        }
        .badge {
            display: inline-block;
            background: rgba(255,255,255,.18);
            border: 1px solid rgba(255,255,255,.3);
            border-radius: 100px;
            padding: 4px 14px;
            font-size: 0.78rem;
            font-weight: 500;
            margin-bottom: 18px;
            backdrop-filter: blur(4px);
        }

        /* ── Auth card ───────────────────────────────────── */
        .auth-card {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-lg);
            padding: 40px 44px;
            max-width: 460px;
            margin: 0 auto;
            box-shadow: var(--shadow-lg);
        }
        .auth-title {
            font-size: 1.55rem;
            font-weight: 700;
            color: var(--text);
            margin-bottom: 4px;
        }
        .auth-sub {
            font-size: 0.88rem;
            color: var(--muted);
            margin-bottom: 28px;
        }

        /* ── Streamlit input overrides ───────────────────── */
        /* Wrapper containers */
        [data-baseweb="input"], [data-baseweb="textarea"] {
            background: #ffffff !important;
            border-radius: var(--radius-sm) !important;
            border: 1.5px solid var(--border) !important;
        }
        /* Actual input elements — text must be dark */
        input[type="text"], input[type="password"], textarea,
        [data-baseweb="input"] input, [data-baseweb="textarea"] textarea {
            background: #ffffff !important;
            color: #1A1D2E !important;
            border: none !important;
            border-radius: var(--radius-sm) !important;
            font-size: 0.92rem !important;
            transition: border-color .15s !important;
            caret-color: #1A1D2E !important;
        }
        /* Placeholder text */
        input::placeholder, textarea::placeholder {
            color: #9CA3AF !important;
            opacity: 1 !important;
        }
        /* Focus ring on the wrapper */
        [data-baseweb="input"]:focus-within,
        [data-baseweb="textarea"]:focus-within {
            border-color: var(--accent) !important;
            box-shadow: 0 0 0 3px rgba(37,99,235,.12) !important;
        }
        /* ── Select / dropdown — force white bg + dark text ── */
        [data-baseweb="select"],
        [data-baseweb="select"] > div,
        [data-baseweb="select"] [data-baseweb="select-control"],
        [data-baseweb="select"] [class*="valueContainer"],
        [data-baseweb="select"] [class*="singleValue"],
        [data-baseweb="select"] [class*="placeholder"] {
            background: #ffffff !important;
            background-color: #ffffff !important;
            color: #1A1D2E !important;
        }
        /* The inner input inside select */
        [data-baseweb="select"] input {
            color: #1A1D2E !important;
            background: transparent !important;
        }
        /* Dropdown menu list */
        [data-baseweb="menu"],
        [data-baseweb="menu"] ul,
        [data-baseweb="menu"] li {
            background: #ffffff !important;
            color: #1A1D2E !important;
        }
        [data-baseweb="menu"] li:hover {
            background: #EEF3FF !important;
        }
        /* Input labels */
        label[data-testid="stWidgetLabel"] p,
        label[data-testid="stWidgetLabel"],
        .stTextInput label, .stSelectbox label, .stTextArea label {
            color: #374151 !important;
            font-size: 0.85rem !important;
            font-weight: 500 !important;
        }
        /* General paragraph / text inside app — ensure dark */
        .stMarkdown p,
        .stMarkdown li,
        .stMarkdown h1, .stMarkdown h2, .stMarkdown h3,
        .stMarkdown strong, .stMarkdown em,
        [data-testid="stMarkdownContainer"] p,
        [data-testid="stMarkdownContainer"] li,
        [data-testid="stMarkdownContainer"] h1,
        [data-testid="stMarkdownContainer"] h2,
        [data-testid="stMarkdownContainer"] h3 {
            color: #1A1D2E !important;
        }

        /* ── Buttons ─────────────────────────────────────── */
        .stButton > button {
            border-radius: var(--radius-sm) !important;
            font-weight: 600 !important;
            font-size: 0.9rem !important;
            padding: 0.55rem 1.4rem !important;
            transition: all .15s ease !important;
            letter-spacing: .01em !important;
        }
        /* Primary — blue */
        .stButton.primary > button,
        div[data-testid="stButton"] button[kind="primary"] {
            background: var(--accent) !important;
            color: #fff !important;
            border: none !important;
        }
        div[data-testid="stButton"] button[kind="primary"]:hover {
            background: var(--accent-dk) !important;
            box-shadow: 0 4px 12px rgba(37,99,235,.35) !important;
        }
        /* Secondary */
        div[data-testid="stButton"] button[kind="secondary"] {
            background: var(--surface) !important;
            color: var(--accent) !important;
            border: 1.5px solid var(--accent) !important;
        }

        /* ── Alert overrides ─────────────────────────────── */
        [data-testid="stAlert"] {
            border-radius: var(--radius-sm) !important;
            border: none !important;
            font-size: 0.88rem !important;
        }

        /* ── Metric cards ────────────────────────────────── */
        [data-testid="stMetric"] {
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius-md);
            padding: 18px 22px;
            box-shadow: var(--shadow-sm);
        }
        [data-testid="stMetricLabel"] { color: var(--muted) !important; font-size: 0.8rem !important; }
        [data-testid="stMetricValue"] { font-size: 1.9rem !important; font-weight: 700 !important; }

        /* ── Expanders ───────────────────────────────────── */
        [data-testid="stExpander"] {
            background: var(--surface) !important;
            border: 1px solid var(--border) !important;
            border-radius: var(--radius-md) !important;
            box-shadow: var(--shadow-sm);
            margin-bottom: 10px;
        }
        [data-testid="stExpander"] summary {
            font-weight: 600 !important;
            font-size: 0.93rem !important;
            padding: 14px 18px !important;
        }

        /* ── Divider ─────────────────────────────────────── */
        hr { border-color: var(--border) !important; }

        /* ── Chat messages — white bg, dark text ────────── */
        [data-testid="stChatMessage"] {
            background: #ffffff !important;
            border: 1px solid #E8EAF0 !important;
            border-radius: 14px !important;
            padding: 20px 24px !important;
            color: #1A1D2E !important;
        }
        /* Text nodes inside chat — dark color, NO background override */
        [data-testid="stChatMessage"] p,
        [data-testid="stChatMessage"] li,
        [data-testid="stChatMessage"] ol,
        [data-testid="stChatMessage"] ul,
        [data-testid="stChatMessage"] h1,
        [data-testid="stChatMessage"] h2,
        [data-testid="stChatMessage"] h3,
        [data-testid="stChatMessage"] strong,
        [data-testid="stChatMessage"] em,
        [data-testid="stChatMessage"] code {
            color: #1A1D2E !important;
        }
        /* Only reset background on the markdown container, not every element */
        [data-testid="stChatMessage"] [data-testid="stMarkdownContainer"] {
            background: transparent !important;
        }
        /* Expander content text */
        [data-testid="stExpander"] p,
        [data-testid="stExpander"] li,
        [data-testid="stExpander"] span,
        [data-testid="stExpander"] strong {
            color: #1A1D2E !important;
        }

        /* ── Scrollbar ───────────────────────────────────── */
        ::-webkit-scrollbar { width: 6px; }
        ::-webkit-scrollbar-track { background: transparent; }
        ::-webkit-scrollbar-thumb { background: var(--border); border-radius: 3px; }

        /* ── Toast notification — light theme ────────────── */
        [data-testid="stToast"] {
            background: #ffffff !important;
            border: 1px solid #E8EAF0 !important;
            border-radius: 10px !important;
            box-shadow: 0 4px 20px rgba(0,0,0,.10) !important;
            color: #1A1D2E !important;
        }
        [data-testid="stToast"] p,
        [data-testid="stToast"] span,
        [data-testid="stToast"] div,
        [data-testid="stToast"] li {
            color: #1A1D2E !important;
            background: transparent !important;
        }
        [data-testid="stToast"] button svg { fill: #6B7080 !important; }

        /* ── Page wrapper ────────────────────────────────── */
        .page-wrap {
            max-width: 1040px;
            margin: 0 auto;
            padding: 40px 32px 80px;
        }

        /* ── Suggestion chips ────────────────────────────── */
        .chips {
            display: flex;
            flex-wrap: wrap;
            gap: 8px;
            margin-bottom: 14px;
        }
        .chip {
            background: var(--accent-lt);
            color: var(--accent);
            border: 1px solid #bfdbfe;
            border-radius: 100px;
            padding: 5px 14px;
            font-size: 0.8rem;
            font-weight: 500;
            cursor: pointer;
            transition: background .15s;
        }
        .chip:hover { background: #dbeafe; }
        /* Style chip st.buttons as pill-shaped suggestion tags */
        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button {
            background: #EEF3FF !important;
            color: #2563EB !important;
            border: 1px solid #bfdbfe !important;
            border-radius: 100px !important;
            padding: 4px 12px !important;
            font-size: 0.78rem !important;
            font-weight: 500 !important;
            white-space: nowrap !important;
            overflow: hidden !important;
            text-overflow: ellipsis !important;
            width: 100% !important;
        }
        div[data-testid="stHorizontalBlock"] div[data-testid="stButton"] button:hover {
            background: #dbeafe !important;
            box-shadow: none !important;
        }

        /* ── Status pills ────────────────────────────────── */
        .pill {
            display: inline-flex;
            align-items: center;
            gap: 5px;
            border-radius: 100px;
            padding: 3px 12px;
            font-size: 0.78rem;
            font-weight: 500;
        }
        .pill-green { background: var(--green-lt); color: var(--green); }
        .pill-blue  { background: var(--accent-lt); color: var(--accent); }

        /* ── Profile card in sidebar ─────────────────────── */
        .profile-card {
            background: linear-gradient(135deg, var(--accent-lt), #fff);
            border: 1px solid #bfdbfe;
            border-radius: var(--radius-md);
            padding: 18px 16px;
            text-align: center;
            margin-bottom: 20px;
        }
        .profile-avatar {
            width: 56px; height: 56px;
            background: var(--accent);
            border-radius: 50%;
            display: flex; align-items: center; justify-content: center;
            font-size: 1.4rem; color: #fff;
            margin: 0 auto 10px;
            font-weight: 700;
        }
        .profile-name {
            font-weight: 700; font-size: 1rem; color: var(--text);
        }
        .profile-role {
            font-size: 0.78rem; color: var(--muted); margin-top: 2px;
        }

        /* ── Diagnosis result ────────────────────────────── */
        .result-section {
            border-left: 3px solid var(--accent);
            padding-left: 14px;
            margin-bottom: 18px;
        }
        .result-label {
            font-size: 0.72rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: .07em;
            color: var(--accent);
            margin-bottom: 4px;
        }

        /* ── Upload zone ─────────────────────────────────── */
        [data-testid="stFileUploader"] {
            border-radius: var(--radius-md) !important;
        }
        [data-testid="stFileUploader"] > div {
            border: 2px dashed var(--border) !important;
            border-radius: var(--radius-md) !important;
            background: var(--bg) !important;
            transition: border-color .15s !important;
        }
        [data-testid="stFileUploader"] > div:hover {
            border-color: var(--accent) !important;
        }

        /* ── Tabs ────────────────────────────────────────── */
        [data-testid="stTabs"] [data-baseweb="tab"] {
            font-weight: 500 !important;
            font-size: 0.9rem !important;
            padding: 10px 20px !important;
        }
        [data-testid="stTabs"] [aria-selected="true"] {
            color: var(--accent) !important;
            font-weight: 700 !important;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )


# =============================================================
# 3. SESSION STATE
# =============================================================

def init_session():
    defaults = {
        "logged_in": False,
        "username": "",
        "role": "",
        "auth": None,
        "docs": [],
        "diagnosis_result": None,
        "q_input": "",   # shared key with text_area widget
        "auth_tab": "login",      # "login" | "signup"
    }
    for k, v in defaults.items():
        if k not in st.session_state:
            st.session_state[k] = v


# =============================================================
# 4. API HELPER FUNCTIONS  (unchanged from original)
# =============================================================

def signup_user(username, password, role):
    try:
        response = requests.post(
            f"{API_URL}/auth/signup",
            json={"username": username, "password": password, "role": role},
        )
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"detail": str(e)}


def authenticate_user(username, password):
    try:
        response = requests.get(
            f"{API_URL}/auth/login",
            auth=HTTPBasicAuth(username, password),
        )
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"detail": str(e)}


def upload_report(auth, files):
    try:
        files_data = [
            ("files", (f.name, f.getvalue(), f.type)) for f in files
        ]
        response = requests.post(
            f"{API_URL}/reports/upload", auth=auth, files=files_data
        )
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"detail": str(e)}


def get_diagnosis(auth, doc_id, question):
    try:
        response = requests.post(
            f"{API_URL}/diagnosis/from_report",
            auth=auth,
            data={"doc_id": doc_id, "question": question},
        )
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"detail": str(e)}


def get_doctor_diagnosis(auth, patient_name):
    try:
        response = requests.get(
            f"{API_URL}/diagnosis/by_patient_name",
            auth=auth,
            params={"patient_name": patient_name},
        )
        return response.status_code, response.json()
    except requests.exceptions.RequestException as e:
        return 500, {"detail": str(e)}


# =============================================================
# 5. SIDEBAR
# =============================================================

def render_sidebar():
    """Authenticated sidebar with profile card, nav links, and logout."""
    with st.sidebar:
        # ── Logo / Brand ──────────────────────────────────────
        st.markdown(
            """
            <div style="display:flex;align-items:center;gap:10px;
                        padding:24px 8px 20px;">
                <span style="font-size:1.6rem;">🩺</span>
                <span style="font-family:'DM Serif Display',serif;
                             font-size:1.25rem;color:var(--text);">
                    MediAI
                </span>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Profile card ──────────────────────────────────────
        initials = (st.session_state.username[:2] or "?").upper()
        role_label = (
            "🩻 Doctor" if st.session_state.role == "doctor" else "🧑 Patient"
        )
        st.markdown(
            f"""
            <div class="profile-card">
                <div class="profile-avatar">{initials}</div>
                <div class="profile-name">{st.session_state.username}</div>
                <div class="profile-role">{role_label}</div>
                <div style="margin-top:10px;">
                    <span class="pill pill-green">● Active</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # ── Uploaded reports list (patients only) ─────────────
        if st.session_state.role == "patient" and st.session_state.docs:
            st.markdown(
                "<div class='label' style='padding:0 4px 8px;'>Uploaded Reports</div>",
                unsafe_allow_html=True,
            )
            for doc in st.session_state.docs:
                st.markdown(
                    f"""
                    <div style="display:flex;align-items:center;gap:8px;
                                padding:8px 10px;border-radius:8px;
                                background:var(--bg);margin-bottom:6px;
                                border:1px solid var(--border);font-size:.82rem;">
                        <span>📄</span>
                        <span style="color:var(--text);font-weight:500;
                                     overflow:hidden;text-overflow:ellipsis;
                                     white-space:nowrap;">{doc['filename']}</span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )

        st.markdown("<br>", unsafe_allow_html=True)
        st.divider()

        # ── Logout ────────────────────────────────────────────
        if st.button("← Log Out", use_container_width=True):
            for k in ["logged_in", "username", "role", "auth", "docs",
                      "diagnosis_result", "question"]:
                st.session_state[k] = (
                    False if k == "logged_in" else ([] if k == "docs" else "")
                )
            st.session_state.auth = None
            st.session_state.diagnosis_result = None
            st.rerun()

        st.markdown(
            "<div style='padding:16px 4px 0;font-size:.75rem;color:var(--muted);'>"
            "MediAI © 2025 · All rights reserved"
            "</div>",
            unsafe_allow_html=True,
        )


# =============================================================
# 6. LANDING PAGE
# =============================================================

def landing_page():
    """Public-facing hero + features shown before authentication."""
    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    # ── Hero ──────────────────────────────────────────────────
    st.markdown(
        """
        <div class="hero-wrap">
            <div class="badge">✦ Powered by Groq Llama 3.3 &amp; Gemini</div>
            <div class="hero-title">Your medical records,<br>understood instantly.</div>
            <div class="hero-sub">
                Upload any lab report or clinical document and get a clear,
                AI-generated diagnosis in seconds — reviewed and accessible
                by your doctor from anywhere.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Feature cards ─────────────────────────────────────────
    features = [
        ("🔒", "Secure Uploads", "End-to-end encrypted PDF storage with instant vector indexing via Pinecone."),
        ("🤖", "AI-powered Diagnosis", "Ask questions in plain English and get structured answers from your reports."),
        ("👨‍⚕️", "Doctor Dashboard", "Doctors can review any patient's diagnosis history in one clean view."),
        ("📋", "Full Medical History", "Every question and answer is stored chronologically for future reference."),
    ]

    cols = st.columns(4, gap="small")
    for col, (icon, title, desc) in zip(cols, features):
        with col:
            st.markdown(
                f"""
                <div class="feature-card">
                    <div class="feature-icon">{icon}</div>
                    <div class="feature-title">{title}</div>
                    <div class="feature-desc">{desc}</div>
                </div>
                """,
                unsafe_allow_html=True,
            )

    st.markdown("<br><br>", unsafe_allow_html=True)

    # ── CTA ───────────────────────────────────────────────────
    st.markdown(
        """
        <div style="text-align:center;padding:40px 20px;
                    background:var(--surface);border:1px solid var(--border);
                    border-radius:var(--radius-lg);box-shadow:var(--shadow-sm);">
            <div style="font-family:'DM Serif Display',serif;font-size:1.7rem;
                        color:var(--text);margin-bottom:8px;">
                Ready to get started?
            </div>
            <div style="color:var(--muted);font-size:.9rem;margin-bottom:24px;">
                Create a free account or log in to access your dashboard.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Inline auth tab buttons
    c1, c2, c3 = st.columns([2, 1, 2])
    with c2:
        if st.button("Get Started →", type="primary", use_container_width=True):
            st.session_state.auth_tab = "login"
            st.session_state.show_auth = True
            st.rerun()

    st.markdown("</div>", unsafe_allow_html=True)


# =============================================================
# 7. LOGIN PAGE
# =============================================================

def login_page():
    """Centered login — narrow column keeps inputs compact."""
    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        st.markdown(
            """
            <div style="text-align:center;padding:48px 0 28px;">
                <span style="font-size:2.4rem;">🩺</span>
                <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;
                            color:var(--text);margin-top:8px;">
                    Welcome back
                </div>
                <div style="color:var(--muted);font-size:.88rem;margin-top:4px;">
                    Log in to access your MediAI dashboard.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        username = st.text_input("Username", placeholder="your_username", key="li_user")
        password = st.text_input("Password", type="password", placeholder="\u2022\u2022\u2022\u2022\u2022\u2022\u2022\u2022", key="li_pass")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        login_btn = st.button("Log In", type="primary", key="li_btn")
        st.markdown(
            "<p style='font-size:.83rem;color:var(--muted);margin:10px 0 2px;'>"
            "Don't have an account?</p>",
            unsafe_allow_html=True,
        )
        switch = st.button("Create one \u2192", key="li_to_signup")
        if login_btn:
            if not username or not password:
                st.warning("Please enter both username and password.")
            else:
                with st.spinner("Authenticating\u2026"):
                    status, response = authenticate_user(username, password)
                if status == 200:
                    st.session_state.logged_in = True
                    st.session_state.username = username
                    st.session_state.role = response["role"]
                    st.session_state.auth = HTTPBasicAuth(username, password)
                    st.toast(f"Welcome back, {username}! \U0001f44b", icon="\u2705")
                    st.rerun()
                else:
                    st.error(response.get("detail", "Invalid credentials. Please try again."))
        if switch:
            st.session_state.auth_tab = "signup"
            st.rerun()


# =============================================================
# 8. SIGNUP PAGE
# =============================================================

def signup_page():
    """Centered signup — narrow column keeps inputs compact."""
    _, col, _ = st.columns([1, 1.6, 1])
    with col:
        st.markdown(
            """
            <div style="text-align:center;padding:48px 0 28px;">
                <span style="font-size:2.4rem;">🩺</span>
                <div style="font-family:'DM Serif Display',serif;font-size:1.8rem;
                            color:var(--text);margin-top:8px;">
                    Create your account
                </div>
                <div style="color:var(--muted);font-size:.88rem;margin-top:4px;">
                    Free to use. No credit card required.
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )
        username = st.text_input("Username", placeholder="choose_a_username", key="su_user")
        password = st.text_input("Password", type="password", placeholder="min. 8 characters", key="su_pass")
        role = st.selectbox("I am a\u2026", ["patient", "doctor"], key="su_role")
        st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)
        signup_btn = st.button("Create Account", type="primary", key="su_btn")
        st.markdown(
            "<p style='font-size:.83rem;color:var(--muted);margin:10px 0 2px;'>"
            "Already have an account?</p>",
            unsafe_allow_html=True,
        )
        switch = st.button("Log in \u2192", key="su_to_login")
        if signup_btn:
            if not username or not password:
                st.warning("All fields are required.")
            elif len(password) < 6:
                st.warning("Password must be at least 6 characters.")
            else:
                with st.spinner("Creating account\u2026"):
                    status, response = signup_user(username, password, role)
                if status == 200:
                    st.success("Account created! You can now log in.")
                    st.session_state.auth_tab = "login"
                    st.rerun()
                else:
                    st.error(response.get("detail", "Signup failed. Please try again."))
        if switch:
            st.session_state.auth_tab = "login"
            st.rerun()


# =============================================================
# 9. PATIENT DASHBOARD — UPLOAD SECTION
# =============================================================

def upload_section():
    """Drag-and-drop upload with progress and success feedback."""
    st.markdown(
        """
        <div class='section-title'>Upload Reports</div>
        <div style='color:var(--muted);font-size:.85rem;margin-bottom:16px;'>
            Upload PDF medical reports to ask AI questions about them.
        </div>
        """,
        unsafe_allow_html=True,
    )

    uploaded_files = st.file_uploader(
        "Drop PDFs here or click to browse",
        type=["pdf"],
        accept_multiple_files=True,
        label_visibility="visible",
    )

    if uploaded_files:
        st.markdown(
            f"<div style='color:var(--muted);font-size:.82rem;margin:8px 0;'>"
            f"{len(uploaded_files)} file(s) selected</div>",
            unsafe_allow_html=True,
        )

        if st.button("⬆  Upload Reports", type="primary"):
            progress = st.progress(0, text="Uploading…")
            with st.spinner(""):
                status, response = upload_report(st.session_state.auth, uploaded_files)

            progress.progress(100, text="Done")

            if status == 200:
                st.session_state.docs = response
                st.toast("Reports uploaded successfully!", icon="📄")
                st.rerun()
            else:
                st.error(response.get("detail", "Upload failed."))


# =============================================================
# 10. PATIENT DASHBOARD — DIAGNOSIS SECTION
# =============================================================

SUGGESTED_QUESTIONS = [
    "What is the overall diagnosis?",
    "Explain any abnormal values.",
    "Summarise the key findings.",
    "Are there any urgent concerns?",
    "What follow-up tests are recommended?",
]


def diagnosis_section():
    """Report selector + AI question input + diagnosis output."""
    if not st.session_state.docs:
        st.info("Upload at least one report to start asking questions.")
        return

    st.markdown("<div class='section-title'>AI Diagnosis</div>", unsafe_allow_html=True)
    st.markdown("<div style='height:4px'></div>", unsafe_allow_html=True)

    # ── Report selector ───────────────────────────────────────
    options = {
        f"{doc['filename']}  ·  {doc['doc_id'][:8]}…": doc["doc_id"]
        for doc in st.session_state.docs
    }
    selected_label = st.selectbox("Select a report", list(options.keys()))
    doc_id = options[selected_label]

    st.markdown("<div style='height:8px'></div>", unsafe_allow_html=True)

    # ── Suggested questions (clickable — writes directly into widget key) ───
    st.markdown("<div class='label' style='margin-bottom:8px;'>Suggested questions</div>", unsafe_allow_html=True)
    chip_cols = st.columns(len(SUGGESTED_QUESTIONS))
    for i, q in enumerate(SUGGESTED_QUESTIONS):
        with chip_cols[i]:
            if st.button(q, key=f"chip_{i}"):
                # Write directly into the text_area widget key so it shows immediately
                st.session_state["q_input"] = q

    # ── Question input ────────────────────────────────────────
    # No value= argument — let the key manage state entirely
    question = st.text_area(
        "Your question",
        placeholder="e.g. What does my HbA1c level indicate?",
        height=100,
        key="q_input",
    )

    if st.button("🔍  Generate Diagnosis", type="primary"):
        if not question.strip():
            st.warning("Please enter a question before generating.")
        else:
            with st.spinner("Analysing your report…"):
                status, result = get_diagnosis(
                    st.session_state.auth, doc_id, question
                )

            if status == 200:
                # Normalise — some backends return the text directly in different keys
                if not result.get("diagnosis"):
                    result["diagnosis"] = (
                        result.get("result")
                        or result.get("answer")
                        or result.get("text")
                        or str(result)
                    )
                st.session_state.diagnosis_result = result
                # question is already stored in st.session_state["q_input"]
                st.toast("Diagnosis ready!", icon="🩺")
            else:
                st.error(result.get("detail", "Generation failed."))

    # ── Diagnosis output ──────────────────────────────────────
    if st.session_state.diagnosis_result:
        result = st.session_state.diagnosis_result
        diagnosis_text = result.get("diagnosis") or ""
        st.markdown("<br>", unsafe_allow_html=True)

        # Render as a plain white card — avoids Streamlit dark-theme interference
        st.markdown(
            """
            <div style="background:#ffffff;border:1.5px solid #E8EAF0;
                        border-radius:14px;padding:24px 28px;
                        box-shadow:0 2px 8px rgba(0,0,0,.06);">
                <div style="display:flex;align-items:center;gap:10px;
                            margin-bottom:16px;padding-bottom:14px;
                            border-bottom:1px solid #E8EAF0;">
                    <span style="font-size:1.4rem;">🩺</span>
                    <span style="font-size:0.72rem;font-weight:700;
                                 text-transform:uppercase;letter-spacing:.08em;
                                 color:#2563EB;">Diagnosis Result</span>
                </div>
            </div>
            """,
            unsafe_allow_html=True,
        )

        # Diagnosis text in a clean container
        with st.container():
            st.markdown(
                f"<div style='background:#ffffff;padding:0 0 8px;'></div>",
                unsafe_allow_html=True,
            )
            # Write text line by line so Streamlit renders each as normal text
            for line in (diagnosis_text or "").split("\n"):
                if line.strip():
                    st.write(line)

        if result.get("sources"):
            st.markdown(
                "<div style='margin-top:12px;font-size:0.78rem;font-weight:600;"
                "text-transform:uppercase;letter-spacing:.06em;color:#6B7080;"
                "margin-bottom:6px;'>Sources</div>",
                unsafe_allow_html=True,
            )
            for src in result["sources"]:
                st.markdown(
                    f"<span style='display:inline-block;background:#EEF3FF;"
                    f"color:#2563EB;border:1px solid #bfdbfe;border-radius:100px;"
                    f"padding:3px 12px;font-size:0.78rem;margin:2px;'>📎 {src}</span>",
                    unsafe_allow_html=True,
                )

        st.markdown("<div style='height:12px'></div>", unsafe_allow_html=True)
        if st.button("📋  Copy Diagnosis"):
            st.code(diagnosis_text, language="")


# =============================================================
# 11. PATIENT DASHBOARD — MAIN
# =============================================================

def patient_dashboard():
    """Full patient view: welcome banner + tabs for Upload / Diagnose."""
    render_sidebar()

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    # ── Welcome banner ────────────────────────────────────────
    st.markdown(
        f"""
        <div class="hero-wrap" style="padding:36px 44px;">
            <div class="badge">Patient Portal</div>
            <div class="hero-title" style="font-size:2rem;">
                Hello, {st.session_state.username} 👋
            </div>
            <div class="hero-sub" style="font-size:.93rem;">
                Upload your medical reports and get an AI-powered diagnosis
                in seconds.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Metric strip ──────────────────────────────────────────
    m1, m2, m3 = st.columns(3)
    m1.metric("Reports Uploaded", len(st.session_state.docs))
    m2.metric("Diagnoses Generated",
              1 if st.session_state.diagnosis_result else 0)
    m3.metric("AI Model", "Llama 3.3")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Tabs: Upload | Diagnose ───────────────────────────────
    tab_upload, tab_diagnose = st.tabs(["📂  Upload Reports", "🔍  AI Diagnosis"])

    with tab_upload:
        st.markdown("<br>", unsafe_allow_html=True)
        upload_section()

    with tab_diagnose:
        st.markdown("<br>", unsafe_allow_html=True)
        diagnosis_section()

    st.markdown("</div>", unsafe_allow_html=True)


# =============================================================
# 12. DOCTOR DASHBOARD
# =============================================================

def doctor_dashboard():
    """Doctor view: search patients and review diagnosis history."""
    render_sidebar()

    st.markdown('<div class="page-wrap">', unsafe_allow_html=True)

    # ── Welcome banner ────────────────────────────────────────
    st.markdown(
        f"""
        <div class="hero-wrap" style="padding:36px 44px;">
            <div class="badge">Doctor Portal</div>
            <div class="hero-title" style="font-size:2rem;">
                Welcome, Dr. {st.session_state.username} 🩻
            </div>
            <div class="hero-sub" style="font-size:.93rem;">
                Search any patient by username to review their full
                diagnosis history.
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Patient search ────────────────────────────────────────
    st.markdown(
        "<div class='section-title'>Patient Search</div>",
        unsafe_allow_html=True,
    )

    col_inp, col_btn = st.columns([5, 1])
    with col_inp:
        patient_name = st.text_input(
            "Patient username",
            placeholder="e.g. john_doe",
            label_visibility="collapsed",
        )
    with col_btn:
        search = st.button("Search", type="primary", use_container_width=True)

    if search:
        if not patient_name.strip():
            st.warning("Enter a patient username to search.")
        else:
            with st.spinner("Fetching records…"):
                status, data = get_doctor_diagnosis(
                    st.session_state.auth, patient_name
                )

            if status == 200:
                if not data:
                    st.info(f"No diagnosis history found for **{patient_name}**.")
                else:
                    # ── Results header ────────────────────────
                    st.markdown(
                        f"""
                        <div style="display:flex;align-items:center;gap:10px;
                                    margin:20px 0 14px;">
                            <span class='pill pill-green'>
                                {len(data)} record(s) found
                            </span>
                            <span style='color:var(--muted);font-size:.83rem;'>
                                for patient "{patient_name}"
                            </span>
                        </div>
                        """,
                        unsafe_allow_html=True,
                    )

                    # ── Expandable record cards ───────────────
                    for i, item in enumerate(data, 1):
                        label = (
                            f"#{i} · {item.get('question', 'Diagnosis')[:60]}"
                        )
                        with st.expander(label, expanded=(i == 1)):
                            r1, r2 = st.columns([1, 2])
                            with r1:
                                st.markdown(
                                    f"""
                                    <div class='label'>Patient</div>
                                    <div style='font-weight:600;margin-bottom:12px;'>
                                        {item.get('patient_name', patient_name)}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )
                                if item.get("timestamp"):
                                    st.markdown(
                                        f"""
                                        <div class='label'>Date</div>
                                        <div style='font-size:.85rem;color:var(--muted);'>
                                            {item.get('timestamp', '—')}
                                        </div>
                                        """,
                                        unsafe_allow_html=True,
                                    )
                            with r2:
                                st.markdown(
                                    f"""
                                    <div class='label'>Question asked</div>
                                    <div style='font-size:.9rem;font-weight:500;
                                                margin-bottom:12px;'>
                                        {item.get('question', '—')}
                                    </div>
                                    """,
                                    unsafe_allow_html=True,
                                )

                            st.markdown("<div class='label'>Diagnosis</div>", unsafe_allow_html=True)
                            st.markdown(item.get("diagnosis", "—"))
            else:
                st.error(data.get("detail", "Unable to fetch records."))

    st.markdown("</div>", unsafe_allow_html=True)


# =============================================================
# 13. MAIN FUNCTION — Router
# =============================================================

def main():
    st.set_page_config(
        page_title="MediAI — AI Medical Diagnosis",
        page_icon="🩺",
        layout="wide",
        initial_sidebar_state="auto",
    )
    inject_css()
    init_session()

    # ── Unauthenticated flow ──────────────────────────────────
    if not st.session_state.logged_in:
        # Show landing unless user clicked "Get Started"
        if not st.session_state.get("show_auth", False):
            # Render landing with a sidebar nav for Login / Sign up
            with st.sidebar:
                st.markdown(
                    """
                    <div style="display:flex;align-items:center;gap:10px;
                                padding:24px 8px 20px;">
                        <span style="font-size:1.6rem;">🩺</span>
                        <span style="font-family:'DM Serif Display',serif;
                                     font-size:1.25rem;color:var(--text);">
                            MediAI
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                nav = st.radio(
                    "Navigation",
                    ["🏠 Home", "🔑 Log In", "✨ Sign Up"],
                    label_visibility="collapsed",
                )
                if nav == "🔑 Log In":
                    st.session_state.auth_tab = "login"
                    st.session_state.show_auth = True
                    st.rerun()
                elif nav == "✨ Sign Up":
                    st.session_state.auth_tab = "signup"
                    st.session_state.show_auth = True
                    st.rerun()

            landing_page()

        else:
            # Auth pages
            with st.sidebar:
                st.markdown(
                    """
                    <div style="display:flex;align-items:center;gap:10px;
                                padding:24px 8px 20px;">
                        <span style="font-size:1.6rem;">🩺</span>
                        <span style="font-family:'DM Serif Display',serif;
                                     font-size:1.25rem;color:var(--text);">
                            MediAI
                        </span>
                    </div>
                    """,
                    unsafe_allow_html=True,
                )
                nav = st.radio(
                    "Auth",
                    ["🔑 Log In", "✨ Sign Up", "← Back to Home"],
                    label_visibility="collapsed",
                    index=0 if st.session_state.auth_tab == "login" else 1,
                )
                if nav == "← Back to Home":
                    st.session_state.show_auth = False
                    st.rerun()
                elif nav == "🔑 Log In":
                    st.session_state.auth_tab = "login"
                elif nav == "✨ Sign Up":
                    st.session_state.auth_tab = "signup"

            if st.session_state.auth_tab == "login":
                login_page()
            else:
                signup_page()

        return

    # ── Authenticated flow ────────────────────────────────────
    if st.session_state.role == "patient":
        patient_dashboard()
    elif st.session_state.role == "doctor":
        doctor_dashboard()


if __name__ == "__main__":
    main()