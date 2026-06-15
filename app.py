import streamlit as st
import os
import pandas as pd
import plotly.graph_objects as go
from dotenv import load_dotenv

# Import utilities
from utils.parser import parse_resume
from utils.analyzer import analyze_resume_vs_jd, generate_career_guidance
from utils.interview import generate_interview_questions, evaluate_mock_interview
from utils.rewriter import (
    rewrite_resume,
    generate_cover_letter,
    generate_linkedin_profile,
    generate_salary_insights,
    analyze_persona,
    score_resume_breakdown,
)

# Load environment variables
load_dotenv()

# ───────────────────────────── PAGE CONFIG ─────────────────────────────────────
st.set_page_config(
    page_title="Resume Intelligence Platform",
    page_icon="🔥",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ───────────────────────────── PREMIUM FUTURISTIC CSS ──────────────────────────
st.markdown("""
<style>
/* ══════════════════════════════════════════════════════════════
   CAREERFORGE AI — Premium Futuristic Dashboard Theme
   Inspired by Linear, Stripe, Notion, Apple design language
   ══════════════════════════════════════════════════════════════ */

@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800;900&family=Outfit:wght@300;400;500;600;700;800;900&family=JetBrains+Mono:wght@400;500;600&display=swap');

/* ── Root Variables ──────────────────────────────────────────── */
:root {
    --bg-primary: #0B1020;
    --bg-secondary: #1A103D;
    --bg-tertiary: #2D1B69;
    --accent-pink: #FF4FD8;
    --accent-purple: #8B5CF6;
    --accent-blue: #6366F1;
    --accent-cyan: #22D3EE;
    --accent-green: #34D399;
    --accent-amber: #FBBF24;
    --accent-red: #F87171;
    --text-primary: #FFFFFF;
    --text-secondary: #B8BFD3;
    --text-muted: #6B7294;
    --glass-bg: rgba(255, 255, 255, 0.04);
    --glass-bg-hover: rgba(255, 255, 255, 0.07);
    --glass-border: rgba(255, 255, 255, 0.08);
    --glass-border-hover: rgba(255, 255, 255, 0.15);
    --glass-blur: 20px;
    --radius-sm: 12px;
    --radius-md: 16px;
    --radius-lg: 20px;
    --radius-xl: 24px;
    --shadow-glow-purple: 0 0 60px rgba(139, 92, 246, 0.15);
    --shadow-glow-pink: 0 0 60px rgba(255, 79, 216, 0.12);
    --shadow-card: 0 8px 40px rgba(0, 0, 0, 0.4);
    --shadow-card-hover: 0 16px 60px rgba(0, 0, 0, 0.5);
    --transition-smooth: all 0.35s cubic-bezier(0.4, 0, 0.2, 1);
}

/* ── Global Resets ───────────────────────────────────────────── */
html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif !important;
    color: var(--text-primary);
}
h1, h2, h3, h4, h5, h6 {
    font-family: 'Outfit', -apple-system, sans-serif !important;
    font-weight: 700;
    letter-spacing: -0.5px;
    color: var(--text-primary) !important;
}
p, span, div, li {
    color: var(--text-secondary);
}

/* ── Main Background ────────────────────────────────────────── */
.stApp {
    background: linear-gradient(145deg, #0B1020 0%, #12082E 30%, #1A103D 55%, #150D30 80%, #0B1020 100%) !important;
    background-attachment: fixed !important;
}
.stApp::before {
    content: '';
    position: fixed;
    top: -50%;
    left: -50%;
    width: 200%;
    height: 200%;
    background:
        radial-gradient(ellipse at 20% 20%, rgba(139, 92, 246, 0.08) 0%, transparent 50%),
        radial-gradient(ellipse at 80% 80%, rgba(255, 79, 216, 0.06) 0%, transparent 50%),
        radial-gradient(ellipse at 50% 50%, rgba(99, 102, 241, 0.04) 0%, transparent 60%);
    pointer-events: none;
    z-index: 0;
    animation: ambientFloat 25s ease-in-out infinite alternate;
}
@keyframes ambientFloat {
    0% { transform: translate(0, 0) rotate(0deg); }
    50% { transform: translate(-2%, 1%) rotate(1deg); }
    100% { transform: translate(1%, -1%) rotate(-0.5deg); }
}

/* ── Sidebar ─────────────────────────────────────────────────── */
section[data-testid="stSidebar"] {
    background: linear-gradient(180deg, #0D0B1E 0%, #130F2B 40%, #1A103D 100%) !important;
    border-right: 1px solid rgba(139, 92, 246, 0.12) !important;
    box-shadow: 4px 0 30px rgba(0, 0, 0, 0.3);
}
section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--text-primary) !important;
}

/* ── Streamlit Widgets Override ───────────────────────────────── */
.stTextInput > div > div > input,
.stTextArea > div > div > textarea,
.stSelectbox > div > div {
    background: rgba(255, 255, 255, 0.03) !important;
    border: 1px solid rgba(255, 255, 255, 0.08) !important;
    border-radius: var(--radius-sm) !important;
    color: var(--text-primary) !important;
    font-family: 'Inter', sans-serif !important;
    transition: var(--transition-smooth) !important;
}
.stTextInput > div > div > input:focus,
.stTextArea > div > div > textarea:focus {
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 0 2px rgba(139, 92, 246, 0.2) !important;
}

/* ── Buttons ─────────────────────────────────────────────────── */
.stButton > button {
    background: linear-gradient(135deg, var(--accent-purple), var(--accent-pink)) !important;
    color: white !important;
    border: none !important;
    border-radius: var(--radius-sm) !important;
    font-family: 'Inter', sans-serif !important;
    font-weight: 600 !important;
    font-size: 0.9rem !important;
    letter-spacing: 0.3px !important;
    padding: 0.6rem 1.5rem !important;
    transition: var(--transition-smooth) !important;
    box-shadow: 0 4px 20px rgba(139, 92, 246, 0.3) !important;
}
.stButton > button:hover {
    transform: translateY(-2px) !important;
    box-shadow: 0 8px 30px rgba(139, 92, 246, 0.45) !important;
}
.stButton > button:active {
    transform: translateY(0) !important;
}

/* ── Download Button ─────────────────────────────────────────── */
.stDownloadButton > button {
    background: rgba(255, 255, 255, 0.04) !important;
    border: 1px solid rgba(139, 92, 246, 0.3) !important;
    color: var(--accent-purple) !important;
    border-radius: var(--radius-sm) !important;
    font-weight: 600 !important;
    transition: var(--transition-smooth) !important;
}
.stDownloadButton > button:hover {
    background: rgba(139, 92, 246, 0.1) !important;
    border-color: var(--accent-purple) !important;
    box-shadow: 0 0 20px rgba(139, 92, 246, 0.2) !important;
    transform: translateY(-1px) !important;
}

/* ── Tabs ─────────────────────────────────────────────────────── */
.stTabs [data-baseweb="tab-list"] {
    background: rgba(255, 255, 255, 0.02);
    border-radius: var(--radius-md);
    padding: 6px;
    gap: 4px;
    border: 1px solid rgba(255, 255, 255, 0.04);
}
.stTabs [data-baseweb="tab"] {
    border-radius: var(--radius-sm);
    padding: 10px 18px;
    font-family: 'Outfit', sans-serif !important;
    font-weight: 500;
    font-size: 0.85rem;
    color: var(--text-muted) !important;
    transition: var(--transition-smooth);
}
.stTabs [aria-selected="true"] {
    background: rgba(139, 92, 246, 0.12) !important;
    color: var(--text-primary) !important;
    border-bottom-color: var(--accent-purple) !important;
}

/* ── Expanders ───────────────────────────────────────────────── */
.streamlit-expanderHeader {
    background: rgba(255, 255, 255, 0.03) !important;
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--glass-border) !important;
    font-family: 'Inter', sans-serif !important;
}

/* ── Progress Bar ────────────────────────────────────────────── */
.stProgress > div > div > div {
    background: linear-gradient(90deg, var(--accent-purple), var(--accent-pink)) !important;
    border-radius: 10px !important;
}

/* ── Alerts ───────────────────────────────────────────────────── */
.stAlert {
    border-radius: var(--radius-sm) !important;
    border: 1px solid var(--glass-border) !important;
    backdrop-filter: blur(10px) !important;
}

/* ════════════════════════════════════════════════════════════════
   CUSTOM COMPONENT CLASSES
   ════════════════════════════════════════════════════════════════ */

/* ── Hero Section ────────────────────────────────────────────── */
.hero-wrapper {
    position: relative;
    text-align: center;
    padding: 2rem 1rem 1rem 1rem;
    margin-bottom: 0.5rem;
}
.hero-glow {
    position: absolute;
    top: 50%;
    left: 50%;
    transform: translate(-50%, -50%);
    width: 500px;
    height: 200px;
    background: radial-gradient(ellipse, rgba(139, 92, 246, 0.15), transparent 70%);
    filter: blur(40px);
    pointer-events: none;
    z-index: 0;
}
.hero-badge {
    position: relative;
    z-index: 1;
    display: inline-block;
    background: linear-gradient(135deg, rgba(139, 92, 246, 0.12), rgba(255, 79, 216, 0.08));
    border: 1px solid rgba(139, 92, 246, 0.25);
    color: var(--accent-purple);
    padding: 0.35rem 1.2rem;
    border-radius: 24px;
    font-size: 0.72rem;
    font-weight: 600;
    letter-spacing: 1.5px;
    text-transform: uppercase;
    margin-bottom: 1rem;
}
.hero-title {
    position: relative;
    z-index: 1;
    font-family: 'Outfit', sans-serif;
    font-size: 3.2rem;
    font-weight: 900;
    background: linear-gradient(135deg, #FFFFFF 0%, #C4B5FD 25%, #FF4FD8 50%, #8B5CF6 75%, #22D3EE 100%);
    background-size: 200% 200%;
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    letter-spacing: -1.5px;
    line-height: 1.1;
    margin-bottom: 0.5rem;
    animation: gradientShift 8s ease-in-out infinite alternate;
}
@keyframes gradientShift {
    0% { background-position: 0% 50%; }
    100% { background-position: 100% 50%; }
}
.hero-subtitle {
    position: relative;
    z-index: 1;
    color: var(--text-muted);
    font-size: 1rem;
    font-weight: 400;
    margin-bottom: 1.5rem;
    letter-spacing: 0.5px;
    line-height: 1.6;
}

/* ── Glass Card ──────────────────────────────────────────────── */
.glass-card {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-lg);
    padding: 2rem;
    box-shadow: var(--shadow-card);
    transition: var(--transition-smooth);
    position: relative;
    overflow: hidden;
}
.glass-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(255,255,255,0.1), transparent);
}
.glass-card:hover {
    background: var(--glass-bg-hover);
    border-color: var(--glass-border-hover);
    box-shadow: var(--shadow-card-hover);
    transform: translateY(-4px);
}

/* ── Glass Card Variant: Glow ────────────────────────────────── */
.glass-card-glow {
    background: var(--glass-bg);
    backdrop-filter: blur(var(--glass-blur));
    -webkit-backdrop-filter: blur(var(--glass-blur));
    border: 1px solid rgba(139, 92, 246, 0.15);
    border-radius: var(--radius-lg);
    padding: 2rem;
    box-shadow: var(--shadow-card), var(--shadow-glow-purple);
    transition: var(--transition-smooth);
    position: relative;
    overflow: hidden;
}
.glass-card-glow::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.4), transparent);
}
.glass-card-glow:hover {
    border-color: rgba(139, 92, 246, 0.3);
    box-shadow: var(--shadow-card-hover), 0 0 80px rgba(139, 92, 246, 0.2);
    transform: translateY(-4px);
}

/* ── Score Display ───────────────────────────────────────────── */
.score-container {
    text-align: center;
    padding: 1rem 0;
}
.score-value {
    font-family: 'Outfit', sans-serif;
    font-size: 5.5rem;
    font-weight: 900;
    line-height: 1;
    margin: 0.3rem 0;
    letter-spacing: -3px;
}
.score-label {
    font-family: 'Inter', sans-serif;
    font-size: 0.78rem;
    font-weight: 600;
    letter-spacing: 2px;
    text-transform: uppercase;
    color: var(--text-muted);
    margin-bottom: 0.3rem;
}
.score-sublabel {
    font-family: 'Inter', sans-serif;
    font-size: 0.95rem;
    font-weight: 600;
    letter-spacing: 0.5px;
}

/* ── Section Header ──────────────────────────────────────────── */
.section-hdr {
    display: flex;
    align-items: center;
    gap: 0.6rem;
    font-family: 'Outfit', sans-serif;
    font-size: 1.1rem;
    font-weight: 600;
    color: var(--text-primary);
    padding-bottom: 0.7rem;
    margin-bottom: 1rem;
    border-bottom: 1px solid rgba(255,255,255,0.06);
    position: relative;
}
.section-hdr::after {
    content: '';
    position: absolute;
    bottom: -1px;
    left: 0;
    width: 60px;
    height: 2px;
    background: linear-gradient(90deg, var(--accent-purple), var(--accent-pink));
    border-radius: 2px;
}

/* ── Skill Pills ─────────────────────────────────────────────── */
.pill {
    display: inline-flex;
    align-items: center;
    gap: 0.3rem;
    padding: 0.35rem 0.9rem;
    border-radius: 24px;
    font-size: 0.8rem;
    font-weight: 500;
    font-family: 'Inter', sans-serif;
    margin: 0.2rem;
    transition: var(--transition-smooth);
    cursor: default;
}
.pill:hover {
    transform: scale(1.06);
}
.pill-tech {
    background: rgba(34, 211, 238, 0.08);
    color: var(--accent-cyan);
    border: 1px solid rgba(34, 211, 238, 0.18);
}
.pill-tech:hover {
    background: rgba(34, 211, 238, 0.14);
    box-shadow: 0 0 15px rgba(34, 211, 238, 0.15);
}
.pill-soft {
    background: rgba(139, 92, 246, 0.08);
    color: #C4B5FD;
    border: 1px solid rgba(139, 92, 246, 0.18);
}
.pill-soft:hover {
    background: rgba(139, 92, 246, 0.14);
    box-shadow: 0 0 15px rgba(139, 92, 246, 0.15);
}
.pill-gap {
    background: rgba(248, 113, 113, 0.08);
    color: var(--accent-red);
    border: 1px solid rgba(248, 113, 113, 0.18);
}
.pill-gap:hover {
    background: rgba(248, 113, 113, 0.14);
}
.pill-demand {
    background: rgba(52, 211, 153, 0.08);
    color: var(--accent-green);
    border: 1px solid rgba(52, 211, 153, 0.18);
}
.pill-demand:hover {
    background: rgba(52, 211, 153, 0.14);
    box-shadow: 0 0 15px rgba(52, 211, 153, 0.15);
}

/* ── Insight Cards ───────────────────────────────────────────── */
.insight-card {
    background: rgba(255, 255, 255, 0.02);
    border-left: 3px solid;
    padding: 0.9rem 1.2rem;
    border-radius: 0 var(--radius-sm) var(--radius-sm) 0;
    margin-bottom: 0.6rem;
    font-size: 0.9rem;
    line-height: 1.6;
    color: var(--text-secondary);
    transition: var(--transition-smooth);
}
.insight-card:hover {
    background: rgba(255, 255, 255, 0.04);
    transform: translateX(4px);
}
.insight-purple { border-left-color: var(--accent-purple); }
.insight-pink   { border-left-color: var(--accent-pink); }
.insight-cyan   { border-left-color: var(--accent-cyan); }
.insight-green  { border-left-color: var(--accent-green); }
.insight-amber  { border-left-color: var(--accent-amber); }
.insight-red    { border-left-color: var(--accent-red); }

/* ── Letter Block ────────────────────────────────────────────── */
.letter-block {
    background: rgba(255, 255, 255, 0.02);
    border: 1px solid rgba(255, 255, 255, 0.04);
    border-radius: var(--radius-md);
    padding: 1.5rem 1.8rem;
    margin-bottom: 0.8rem;
    font-size: 0.93rem;
    line-height: 1.8;
    color: var(--text-secondary);
    transition: var(--transition-smooth);
}
.letter-block:hover {
    border-color: rgba(139, 92, 246, 0.12);
    background: rgba(255, 255, 255, 0.03);
}

/* ── Bullet Rewrite ──────────────────────────────────────────── */
.bullet-new {
    background: rgba(52, 211, 153, 0.04);
    border: 1px solid rgba(52, 211, 153, 0.1);
    border-radius: var(--radius-sm);
    padding: 0.85rem 1.2rem 0.85rem 2.5rem;
    margin-bottom: 0.5rem;
    font-size: 0.88rem;
    line-height: 1.65;
    color: var(--text-secondary);
    position: relative;
    transition: var(--transition-smooth);
}
.bullet-new::before {
    content: '✦';
    position: absolute;
    left: 1rem;
    top: 0.85rem;
    color: var(--accent-green);
    font-size: 0.75rem;
}
.bullet-new:hover {
    background: rgba(52, 211, 153, 0.07);
    border-color: rgba(52, 211, 153, 0.2);
    transform: translateX(4px);
}

/* ── Persona Card ────────────────────────────────────────────── */
.persona-card {
    background: linear-gradient(145deg, rgba(139, 92, 246, 0.06), rgba(255, 79, 216, 0.04));
    border: 1px solid rgba(139, 92, 246, 0.15);
    border-radius: var(--radius-xl);
    padding: 2.5rem;
    text-align: center;
    margin-bottom: 1.5rem;
    position: relative;
    overflow: hidden;
}
.persona-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    right: 0;
    height: 1px;
    background: linear-gradient(90deg, transparent, rgba(139, 92, 246, 0.4), rgba(255, 79, 216, 0.3), transparent);
}
.persona-title {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    background: linear-gradient(135deg, #C4B5FD, #FF4FD8);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    margin-bottom: 0.8rem;
}
.persona-desc {
    color: var(--text-secondary);
    font-size: 0.95rem;
    line-height: 1.7;
    margin: 0.8rem auto;
    max-width: 600px;
}
.persona-style-badge {
    display: inline-block;
    background: rgba(139, 92, 246, 0.1);
    border: 1px solid rgba(139, 92, 246, 0.25);
    color: #C4B5FD;
    padding: 0.4rem 1.4rem;
    border-radius: 24px;
    font-size: 0.82rem;
    font-weight: 600;
    margin-top: 0.8rem;
    letter-spacing: 0.5px;
}

/* ── Salary Range ────────────────────────────────────────────── */
.salary-display {
    font-family: 'Outfit', sans-serif;
    font-size: 2.5rem;
    font-weight: 800;
    background: linear-gradient(135deg, var(--accent-green), var(--accent-cyan));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    background-clip: text;
    text-align: center;
    margin: 0.5rem 0;
    letter-spacing: -1px;
}
.demand-badge {
    display: inline-block;
    padding: 0.4rem 1.4rem;
    border-radius: 24px;
    font-size: 0.8rem;
    font-weight: 600;
    text-transform: uppercase;
    letter-spacing: 1px;
}
.demand-very-high {
    background: rgba(52, 211, 153, 0.1);
    color: var(--accent-green);
    border: 1px solid rgba(52, 211, 153, 0.25);
}
.demand-high {
    background: rgba(34, 211, 238, 0.1);
    color: var(--accent-cyan);
    border: 1px solid rgba(34, 211, 238, 0.25);
}
.demand-moderate {
    background: rgba(251, 191, 36, 0.1);
    color: var(--accent-amber);
    border: 1px solid rgba(251, 191, 36, 0.25);
}
.demand-lower {
    background: rgba(248, 113, 113, 0.1);
    color: var(--accent-red);
    border: 1px solid rgba(248, 113, 113, 0.25);
}

/* ── LinkedIn Section ────────────────────────────────────────── */
.linkedin-headline {
    background: rgba(10, 102, 194, 0.06);
    border: 1px solid rgba(10, 102, 194, 0.15);
    border-radius: var(--radius-md);
    padding: 1.3rem 1.5rem;
    font-size: 1.05rem;
    font-weight: 600;
    color: #93C5FD;
    margin-bottom: 1rem;
    position: relative;
}
.linkedin-headline::before {
    content: 'in';
    position: absolute;
    top: -8px;
    right: 16px;
    background: rgba(10, 102, 194, 0.2);
    color: #60A5FA;
    padding: 2px 8px;
    border-radius: 6px;
    font-size: 0.7rem;
    font-weight: 700;
}

/* ── Stat Mini Cards ─────────────────────────────────────────── */
.stat-mini {
    background: var(--glass-bg);
    border: 1px solid var(--glass-border);
    border-radius: var(--radius-md);
    padding: 1.2rem;
    text-align: center;
    transition: var(--transition-smooth);
}
.stat-mini:hover {
    border-color: var(--glass-border-hover);
    transform: translateY(-2px);
}
.stat-mini-value {
    font-family: 'Outfit', sans-serif;
    font-size: 2rem;
    font-weight: 800;
    line-height: 1;
    margin-bottom: 0.3rem;
}
.stat-mini-label {
    font-size: 0.72rem;
    font-weight: 500;
    color: var(--text-muted);
    text-transform: uppercase;
    letter-spacing: 1px;
}
</style>
""", unsafe_allow_html=True)


# ───────────────────────────── SESSION STATE ───────────────────────────────────
defaults = {
    "resume_text": "",
    "jd_text": "",
    "analysis_result": None,
    "career_guidance": None,
    "interview_active": False,
    "interview_questions": [],
    "current_question_idx": 0,
    "qa_history": [],
    "interview_feedback": None,
    "rewritten_resume": None,
    "score_breakdown": None,
    "cover_letter": None,
    "linkedin_profile": None,
    "salary_insight": None,
    "persona": None,
}
for k, v in defaults.items():
    if k not in st.session_state:
        st.session_state[k] = v


# ───────────────────────────── SIDEBAR ─────────────────────────────────────────
st.sidebar.markdown("### ⚙️ Configuration")

gemini_api_key = st.sidebar.text_input(
    "Gemini API Key",
    value=os.getenv("GOOGLE_API_KEY", ""),
    type="password",
    help="Your Google Gemini API key. Set in `.env` as GOOGLE_API_KEY to auto-populate.",
)

model_name = st.sidebar.selectbox(
    "AI Model",
    options=["gemini-2.5-flash", "gemini-2.5-pro"],
    index=0,
    help="Flash = fast. Pro = deeper analysis.",
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 Resume & Job Description")

sample_option = st.sidebar.selectbox(
    "Quick-Load Sample",
    options=["Custom Upload / Paste", "Software Engineer Sample", "Product Manager Sample"],
    index=0,
)

sample_resume, sample_jd = "", ""
if sample_option == "Software Engineer Sample":
    try:
        with open("samples/resume_swe.txt", "r") as f:
            sample_resume = f.read()
        with open("samples/jd_swe.txt", "r") as f:
            sample_jd = f.read()
    except FileNotFoundError:
        st.sidebar.warning("Sample files not found.")
elif sample_option == "Product Manager Sample":
    try:
        with open("samples/resume_pm.txt", "r") as f:
            sample_resume = f.read()
        with open("samples/jd_pm.txt", "r") as f:
            sample_jd = f.read()
    except FileNotFoundError:
        st.sidebar.warning("Sample files not found.")

uploaded_file = st.sidebar.file_uploader(
    "Upload Resume (PDF, DOCX, TXT)",
    type=["pdf", "docx", "doc", "txt"],
    disabled=(sample_option != "Custom Upload / Paste"),
)

if sample_option == "Custom Upload / Paste":
    if uploaded_file is not None:
        try:
            st.session_state.resume_text = parse_resume(uploaded_file)
            st.sidebar.success("✅ Resume parsed!")
        except Exception as e:
            st.sidebar.error(f"Error parsing resume: {e}")
    else:
        st.session_state.resume_text = ""
else:
    st.session_state.resume_text = sample_resume
    st.sidebar.success(f"✅ Loaded {sample_option}")

if sample_option == "Custom Upload / Paste":
    jd_input = st.sidebar.text_area(
        "Target Job Description",
        height=180,
        placeholder="Paste the full job description here…",
    )
    st.session_state.jd_text = jd_input
else:
    st.sidebar.text_area(
        "Target Job Description",
        value=sample_jd,
        height=180,
        disabled=True,
    )
    st.session_state.jd_text = sample_jd

st.sidebar.markdown("---")
st.sidebar.markdown(
    '<p style="text-align:center;color:#6B7294;font-size:0.72rem;letter-spacing:0.5px;">'
    "Powered by Google Gemini · Built with Streamlit</p>",
    unsafe_allow_html=True,
)


# ───────────────────────────── HERO HEADER ─────────────────────────────────────
st.markdown("""
<div class="hero-wrapper">
    <div class="hero-glow"></div>
    <div class="hero-badge">✦ AI-POWERED CAREER INTELLIGENCE</div>
    <div class="hero-title">CareerForge AI</div>
    <div class="hero-subtitle">
        Resume analysis · ATS optimization · Mock interviews · Cover letters · LinkedIn branding · Salary intelligence
    </div>
</div>
""", unsafe_allow_html=True)

if not gemini_api_key:
    st.warning("⚠️ Please provide your Gemini API Key in the sidebar to begin.")
    st.stop()


# ───────────────────────────── TAB LAYOUT ──────────────────────────────────────
tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
    "📊 Resume Analysis",
    "✍️ Resume Rewriter",
    "💬 Mock Interview",
    "📈 Performance Report",
    "📝 Cover Letter",
    "🔗 LinkedIn Optimizer",
    "💰 Salary & Career",
])


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 1 — RESUME ANALYSIS & ATS MATCH
# ═══════════════════════════════════════════════════════════════════════════════
with tab1:
    st.header("Resume Analysis & ATS Compatibility")

    col_left, col_right = st.columns([1, 2])

    with col_left:
        analyze_btn = st.button("🚀 Analyze Resume", type="primary", use_container_width=True)

        if analyze_btn:
            if not st.session_state.resume_text:
                st.error("Upload / load a resume in the sidebar first.")
            elif not st.session_state.jd_text:
                st.error("Enter / load a job description in the sidebar first.")
            else:
                with st.spinner("Running deep resume analysis…"):
                    try:
                        analysis = analyze_resume_vs_jd(
                            st.session_state.resume_text,
                            st.session_state.jd_text,
                            gemini_api_key,
                            model_name,
                        )
                        st.session_state.analysis_result = analysis
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

                with st.spinner("Generating score breakdown…"):
                    try:
                        breakdown = score_resume_breakdown(
                            st.session_state.resume_text,
                            st.session_state.jd_text,
                            gemini_api_key,
                            model_name,
                        )
                        st.session_state.score_breakdown = breakdown
                    except Exception as e:
                        st.warning(f"Score breakdown unavailable: {e}")
                if st.session_state.analysis_result:
                    st.success("✅ Analysis complete!")

        if st.session_state.analysis_result:
            score = st.session_state.analysis_result.match_percentage
            if score >= 80:
                color, glow, level = "#22D3EE", "rgba(34,211,238,0.2)", "Excellent Fit"
            elif score >= 60:
                color, glow, level = "#FBBF24", "rgba(251,191,36,0.2)", "Moderate Fit"
            else:
                color, glow, level = "#F87171", "rgba(248,113,113,0.2)", "Needs Work"

            st.markdown(f"""
            <div class="glass-card-glow" style="text-align:center;">
                <div class="score-label">ATS MATCH SCORE</div>
                <div class="score-value" style="background:linear-gradient(135deg,{color},#8B5CF6);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;">{score}%</div>
                <div class="score-sublabel" style="color:{color};">{level}</div>
            </div>
            """, unsafe_allow_html=True)

            # Radar Chart
            if st.session_state.score_breakdown:
                bd = st.session_state.score_breakdown
                cats = ["Technical\nMatch", "Soft\nSkills", "Formatting", "Action\nVerbs", "Metrics\nUsage", "ATS\nFriendly"]
                vals = [bd.technical_match, bd.soft_skills_score, bd.formatting_score,
                        bd.action_verbs_score, bd.metrics_usage_score, bd.ats_friendliness]
                vals_c = vals + [vals[0]]
                cats_c = cats + [cats[0]]

                fig = go.Figure()
                # Fill area
                fig.add_trace(go.Scatterpolar(
                    r=vals_c, theta=cats_c, fill="toself",
                    fillcolor="rgba(139,92,246,0.1)",
                    line=dict(color="#8B5CF6", width=2.5),
                    marker=dict(size=7, color="#FF4FD8", line=dict(width=2, color="#8B5CF6")),
                    name="Score",
                ))
                fig.update_layout(
                    polar=dict(
                        bgcolor="rgba(0,0,0,0)",
                        radialaxis=dict(
                            visible=True, range=[0, 100],
                            gridcolor="rgba(255,255,255,0.05)",
                            tickfont=dict(size=8, color="#6B7294"),
                            linecolor="rgba(255,255,255,0.03)",
                        ),
                        angularaxis=dict(
                            gridcolor="rgba(255,255,255,0.04)",
                            tickfont=dict(size=9, color="#B8BFD3", family="Inter"),
                            linecolor="rgba(255,255,255,0.04)",
                        ),
                    ),
                    showlegend=False,
                    paper_bgcolor="rgba(0,0,0,0)",
                    plot_bgcolor="rgba(0,0,0,0)",
                    margin=dict(l=50, r=50, t=25, b=25),
                    height=280,
                )
                st.plotly_chart(fig, use_container_width=True)

                # Mini stat cards
                st.markdown(f"""
                <div style="display:grid;grid-template-columns:1fr 1fr;gap:0.5rem;margin-top:0.5rem;">
                    <div class="stat-mini">
                        <div class="stat-mini-value" style="color:#22D3EE;">{bd.technical_match}</div>
                        <div class="stat-mini-label">Technical</div>
                    </div>
                    <div class="stat-mini">
                        <div class="stat-mini-value" style="color:#8B5CF6;">{bd.ats_friendliness}</div>
                        <div class="stat-mini-label">ATS Score</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

                st.caption(bd.score_rationale)
        else:
            st.info("Load a resume + JD in the sidebar, then click **Analyze Resume**.")

    with col_right:
        if st.session_state.analysis_result:
            result = st.session_state.analysis_result

            st.markdown('<div class="section-hdr">🔍 Identified Skills</div>', unsafe_allow_html=True)
            c1, c2 = st.columns(2)
            with c1:
                st.markdown("**Technical Skills**")
                if result.technical_skills:
                    html = "".join(f'<span class="pill pill-tech">{s}</span>' for s in result.technical_skills)
                    st.markdown(html, unsafe_allow_html=True)
                else:
                    st.write("_None identified._")
            with c2:
                st.markdown("**Soft Skills & Leadership**")
                if result.soft_skills:
                    html = "".join(f'<span class="pill pill-soft">{s}</span>' for s in result.soft_skills)
                    st.markdown(html, unsafe_allow_html=True)
                else:
                    st.write("_None identified._")

            st.markdown("---")
            st.markdown('<div class="section-hdr">⚠️ Missing Skills & Gaps</div>', unsafe_allow_html=True)
            if result.skills_gaps:
                for gap in result.skills_gaps:
                    st.markdown(f'<div class="insight-card insight-red">❌ <strong>{gap}</strong></div>', unsafe_allow_html=True)
            else:
                st.success("🎉 No significant gaps found!")

            st.markdown("---")
            st.markdown('<div class="section-hdr">💡 ATS Optimization Tips</div>', unsafe_allow_html=True)
            if result.ats_suggestions:
                for tip in result.ats_suggestions:
                    st.markdown(f'<div class="insight-card insight-purple">📌 {tip}</div>', unsafe_allow_html=True)
        else:
            st.markdown("""
            ### Ready to optimize your resume?
            1. **Load** your resume and a job description in the sidebar.
            2. Click **Analyze Resume** to get your ATS score, radar breakdown, skill gaps, and tips.
            """)


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 2 — AI RESUME REWRITER
# ═══════════════════════════════════════════════════════════════════════════════
with tab2:
    st.header("✍️ AI Resume Rewriter")
    st.write("Transform your resume bullets into powerful, ATS-optimized statements with metrics and strong action verbs.")

    if not st.session_state.resume_text or not st.session_state.jd_text:
        st.info("Load a resume and job description in the sidebar to use the rewriter.")
    else:
        if st.button("🔄 Rewrite My Resume", type="primary", use_container_width=True):
            with st.spinner("AI is rewriting your resume with optimized bullets…"):
                try:
                    rewritten = rewrite_resume(
                        st.session_state.resume_text,
                        st.session_state.jd_text,
                        gemini_api_key,
                        model_name,
                    )
                    st.session_state.rewritten_resume = rewritten
                    st.success("✅ Resume rewritten!")
                except Exception as e:
                    st.error(f"Rewrite failed: {e}")

        if st.session_state.rewritten_resume:
            rw = st.session_state.rewritten_resume

            st.markdown('<div class="section-hdr">📋 Professional Summary</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="letter-block">{rw.summary_statement}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-hdr">✦ Rewritten Experience Bullets</div>', unsafe_allow_html=True)
            for bullet in rw.rewritten_bullets:
                st.markdown(f'<div class="bullet-new">{bullet}</div>', unsafe_allow_html=True)

            st.markdown("---")
            st.markdown('<div class="section-hdr">🔧 What We Improved</div>', unsafe_allow_html=True)
            for imp in rw.key_improvements:
                st.markdown(f'<div class="insight-card insight-green">✅ {imp}</div>', unsafe_allow_html=True)

            full_text = f"PROFESSIONAL SUMMARY\n{'='*50}\n{rw.summary_statement}\n\n"
            full_text += f"EXPERIENCE\n{'='*50}\n"
            for b in rw.rewritten_bullets:
                full_text += f"• {b}\n"
            st.download_button(
                "📥 Download Rewritten Resume (.txt)",
                data=full_text,
                file_name="Rewritten_Resume.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 3 — INTERACTIVE MOCK INTERVIEW
# ═══════════════════════════════════════════════════════════════════════════════
with tab3:
    st.header("💬 AI Mock Interview")
    st.write("Simulate a realistic interview tailored to your profile and target role.")

    if not st.session_state.resume_text or not st.session_state.jd_text:
        st.info("Set up a resume and job description in the sidebar first.")
    else:
        if not st.session_state.interview_active:
            if st.button("🎯 Start Mock Interview", type="primary", use_container_width=True):
                with st.spinner("Generating personalized interview questions…"):
                    try:
                        questions = generate_interview_questions(
                            st.session_state.resume_text,
                            st.session_state.jd_text,
                            gemini_api_key,
                            model_name,
                        )
                        st.session_state.interview_questions = questions
                        st.session_state.current_question_idx = 0
                        st.session_state.qa_history = []
                        st.session_state.interview_feedback = None
                        st.session_state.interview_active = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not generate questions: {e}")
        else:
            col_chat, col_status = st.columns([3, 1])

            with col_status:
                st.markdown("### 📊 Progress")
                total_q = len(st.session_state.interview_questions) or 5
                current = st.session_state.current_question_idx
                st.write(f"**Question {min(current + 1, total_q)} of {total_q}**")
                st.progress(current / total_q)

                st.markdown("---")
                if st.button("🛑 End & Evaluate", use_container_width=True):
                    if st.session_state.qa_history:
                        with st.spinner("Evaluating your responses…"):
                            try:
                                feedback = evaluate_mock_interview(
                                    st.session_state.qa_history,
                                    st.session_state.resume_text,
                                    st.session_state.jd_text,
                                    gemini_api_key,
                                    model_name,
                                )
                                st.session_state.interview_feedback = feedback
                                st.session_state.interview_active = False
                                st.success("Check the Performance Report tab!")
                            except Exception as e:
                                st.error(f"Evaluation failed: {e}")
                    else:
                        st.session_state.interview_active = False
                        st.rerun()

                if st.button("🔄 Restart", use_container_width=True):
                    st.session_state.interview_active = False
                    st.session_state.interview_questions = []
                    st.session_state.current_question_idx = 0
                    st.session_state.qa_history = []
                    st.session_state.interview_feedback = None
                    st.rerun()

            with col_chat:
                st.markdown("### 🗣️ Interview Session")
                for i, qa in enumerate(st.session_state.qa_history):
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(f"**Q{i+1}:** {qa['question']}")
                    with st.chat_message("user", avatar="👤"):
                        st.write(qa["answer"])

                curr_idx = st.session_state.current_question_idx
                if curr_idx < len(st.session_state.interview_questions):
                    current_q = st.session_state.interview_questions[curr_idx]
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(f"**Question {curr_idx + 1}:** {current_q}")
                    user_answer = st.chat_input("Type your response…")
                    if user_answer:
                        st.session_state.qa_history.append({"question": current_q, "answer": user_answer})
                        st.session_state.current_question_idx += 1
                        st.rerun()
                else:
                    st.balloons()
                    st.success("🎉 All questions answered!")
                    if st.button("📊 Generate Performance Report", type="primary", use_container_width=True):
                        with st.spinner("Compiling feedback report…"):
                            try:
                                feedback = evaluate_mock_interview(
                                    st.session_state.qa_history,
                                    st.session_state.resume_text,
                                    st.session_state.jd_text,
                                    gemini_api_key,
                                    model_name,
                                )
                                st.session_state.interview_feedback = feedback
                                st.session_state.interview_active = False
                                st.rerun()
                            except Exception as e:
                                st.error(f"Evaluation failed: {e}")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 4 — INTERVIEW PERFORMANCE REPORT
# ═══════════════════════════════════════════════════════════════════════════════
with tab4:
    st.header("📈 Interview Performance Report")

    if st.session_state.interview_feedback:
        report = st.session_state.interview_feedback
        score = report.overall_score

        if score >= 80:
            color, label = "#22D3EE", "Excellent Performance"
        elif score >= 60:
            color, label = "#FBBF24", "Good — Room to Improve"
        else:
            color, label = "#F87171", "Needs Significant Work"

        st.markdown(f"""
        <div class="glass-card-glow" style="text-align:center;">
            <div class="score-label">OVERALL INTERVIEW SCORE</div>
            <div class="score-value" style="background:linear-gradient(135deg,{color},#8B5CF6);
                -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                background-clip:text;">{score}/100</div>
            <div class="score-sublabel" style="color:{color};">{label}</div>
        </div>
        """, unsafe_allow_html=True)

        c_str, c_imp = st.columns(2)
        with c_str:
            st.markdown('<div class="section-hdr">🌟 Strengths</div>', unsafe_allow_html=True)
            for s in report.strengths:
                st.markdown(f'<div class="insight-card insight-green">💪 {s}</div>', unsafe_allow_html=True)
        with c_imp:
            st.markdown('<div class="section-hdr">🚀 Areas to Improve</div>', unsafe_allow_html=True)
            for imp in report.areas_for_improvement:
                st.markdown(f'<div class="insight-card insight-amber">📈 {imp}</div>', unsafe_allow_html=True)

        st.markdown("---")
        st.subheader("🔍 Question-by-Question Review")

        for idx, qa_eval in enumerate(report.qa_evaluations):
            with st.expander(
                f"Q{idx+1}: {qa_eval.question[:70]}… — Score: {qa_eval.score}/10",
                expanded=(idx == 0),
            ):
                st.markdown(f"**Your Answer:** _{qa_eval.answer}_")
                st.markdown(f"**Score:** `{qa_eval.score}/10`")
                st.info(f"**Feedback:** {qa_eval.feedback}")
                with st.container(border=True):
                    st.markdown("**💡 Model Answer (STAR Framework):**")
                    st.write(qa_eval.suggested_answer)

        report_md = f"# Interview Performance Report\n\n**Score:** {score}/100\n\n"
        report_md += "## Strengths\n" + "\n".join(f"- {s}" for s in report.strengths)
        report_md += "\n\n## Areas for Improvement\n" + "\n".join(f"- {a}" for a in report.areas_for_improvement)
        report_md += "\n\n## Detailed Breakdown\n\n"
        for i, q in enumerate(report.qa_evaluations):
            report_md += f"### Q{i+1}: {q.question}\n**Answer:** {q.answer}\n\n"
            report_md += f"**Score:** {q.score}/10\n\n**Feedback:** {q.feedback}\n\n"
            report_md += f"**Model Answer:** {q.suggested_answer}\n\n---\n\n"
        st.download_button(
            "📥 Download Full Report (.md)",
            data=report_md,
            file_name="Interview_Report.md",
            mime="text/markdown",
            use_container_width=True,
        )
    else:
        st.info("Complete a Mock Interview in the previous tab to see your report here.")


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 5 — COVER LETTER GENERATOR
# ═══════════════════════════════════════════════════════════════════════════════
with tab5:
    st.header("📝 AI Cover Letter Generator")
    st.write("Generate a compelling, role-specific cover letter in seconds.")

    if not st.session_state.resume_text or not st.session_state.jd_text:
        st.info("Load a resume and job description in the sidebar first.")
    else:
        tone = st.selectbox(
            "Tone & Style",
            options=["Formal & Professional", "Enthusiastic & Energetic", "Concise & Direct"],
            index=0,
        )

        if st.button("✨ Generate Cover Letter", type="primary", use_container_width=True):
            with st.spinner("Crafting your cover letter…"):
                try:
                    cl = generate_cover_letter(
                        st.session_state.resume_text,
                        st.session_state.jd_text,
                        tone,
                        gemini_api_key,
                        model_name,
                    )
                    st.session_state.cover_letter = cl
                    st.success("✅ Cover letter generated!")
                except Exception as e:
                    st.error(f"Failed: {e}")

        if st.session_state.cover_letter:
            cl = st.session_state.cover_letter

            st.markdown(f"""
            <div class="glass-card" style="margin-bottom:1.5rem;">
                <div style="color:#6B7294;font-size:0.72rem;text-transform:uppercase;letter-spacing:1.5px;margin-bottom:0.4rem;">Subject Line</div>
                <div style="font-size:1.05rem;font-weight:600;color:#FFFFFF;line-height:1.4;">{cl.subject_line}</div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown(f'<div class="letter-block">{cl.opening_paragraph}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="letter-block">{cl.body_paragraph_1}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="letter-block">{cl.body_paragraph_2}</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="letter-block">{cl.closing_paragraph}</div>', unsafe_allow_html=True)

            full_letter = (
                f"Subject: {cl.subject_line}\n\n"
                f"{cl.opening_paragraph}\n\n"
                f"{cl.body_paragraph_1}\n\n"
                f"{cl.body_paragraph_2}\n\n"
                f"{cl.closing_paragraph}"
            )
            st.download_button(
                "📥 Download Cover Letter (.txt)",
                data=full_letter,
                file_name="Cover_Letter.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 6 — LINKEDIN OPTIMIZER
# ═══════════════════════════════════════════════════════════════════════════════
with tab6:
    st.header("🔗 LinkedIn Profile Optimizer")
    st.write("Generate a recruiter-magnet LinkedIn headline, about section, and skill tags.")

    if not st.session_state.resume_text:
        st.info("Load your resume in the sidebar first.")
    else:
        target_role = st.text_input(
            "Target Role / Career Goal",
            placeholder="e.g. Senior Software Engineer, ML Engineer, Product Manager",
        )

        if st.button("🚀 Optimize LinkedIn", type="primary", use_container_width=True):
            if not target_role:
                st.warning("Enter a target role first.")
            else:
                with st.spinner("Optimizing your LinkedIn profile…"):
                    try:
                        lp = generate_linkedin_profile(
                            st.session_state.resume_text,
                            target_role,
                            gemini_api_key,
                            model_name,
                        )
                        st.session_state.linkedin_profile = lp
                        st.success("✅ LinkedIn profile optimized!")
                    except Exception as e:
                        st.error(f"Failed: {e}")

        if st.session_state.linkedin_profile:
            lp = st.session_state.linkedin_profile

            st.markdown('<div class="section-hdr">📌 Optimized Headline</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="linkedin-headline">{lp.headline}</div>', unsafe_allow_html=True)

            st.markdown('<div class="section-hdr">📝 About Section</div>', unsafe_allow_html=True)
            st.markdown(f'<div class="letter-block">{lp.about_summary}</div>', unsafe_allow_html=True)

            col_sk, col_feat = st.columns(2)
            with col_sk:
                st.markdown('<div class="section-hdr">🏷️ Skills to Add</div>', unsafe_allow_html=True)
                pills = "".join(f'<span class="pill pill-tech">{s}</span>' for s in lp.skills_to_add)
                st.markdown(pills, unsafe_allow_html=True)
            with col_feat:
                st.markdown('<div class="section-hdr">⭐ Featured Section Ideas</div>', unsafe_allow_html=True)
                for idea in lp.featured_section_ideas:
                    st.markdown(f'<div class="insight-card insight-cyan">💡 {idea}</div>', unsafe_allow_html=True)

            linkedin_text = (
                f"LINKEDIN HEADLINE\n{'='*40}\n{lp.headline}\n\n"
                f"ABOUT SECTION\n{'='*40}\n{lp.about_summary}\n\n"
                f"SKILLS\n{'='*40}\n" + "\n".join(f"• {s}" for s in lp.skills_to_add) + "\n\n"
                f"FEATURED IDEAS\n{'='*40}\n" + "\n".join(f"• {f}" for f in lp.featured_section_ideas)
            )
            st.download_button(
                "📥 Download LinkedIn Content (.txt)",
                data=linkedin_text,
                file_name="LinkedIn_Profile.txt",
                mime="text/plain",
                use_container_width=True,
            )


# ═══════════════════════════════════════════════════════════════════════════════
# TAB 7 — SALARY & CAREER INTELLIGENCE
# ═══════════════════════════════════════════════════════════════════════════════
with tab7:
    st.header("💰 Salary & Career Intelligence")

    if not st.session_state.resume_text:
        st.info("Load your resume in the sidebar first.")
    else:
        sub_tab1, sub_tab2, sub_tab3 = st.tabs([
            "💵 Salary Insights",
            "🧭 Career Roadmap",
            "🧑‍💼 Professional Persona",
        ])

        with sub_tab1:
            st.subheader("💵 Salary Range & Negotiation Guide")

            if not st.session_state.jd_text:
                st.info("Load a job description for salary estimation.")
            else:
                location = st.text_input(
                    "Your Location / Target Region",
                    placeholder="e.g. San Francisco, CA / Remote USA / Bangalore, India",
                )

                if st.button("💰 Get Salary Insights", type="primary", use_container_width=True):
                    if not location:
                        st.warning("Enter a location for accurate estimates.")
                    else:
                        with st.spinner("Analyzing market compensation data…"):
                            try:
                                si = generate_salary_insights(
                                    st.session_state.resume_text,
                                    st.session_state.jd_text,
                                    location,
                                    gemini_api_key,
                                    model_name,
                                )
                                st.session_state.salary_insight = si
                                st.success("✅ Salary insights ready!")
                            except Exception as e:
                                st.error(f"Failed: {e}")

                if st.session_state.salary_insight:
                    si = st.session_state.salary_insight

                    st.markdown(f"""
                    <div class="glass-card-glow" style="text-align:center;">
                        <div class="score-label">ESTIMATED SALARY RANGE</div>
                        <div class="salary-display">
                            ${si.estimated_range_low:,} — ${si.estimated_range_high:,}
                        </div>
                    </div>
                    """, unsafe_allow_html=True)

                    demand_map = {
                        "very high demand": "demand-very-high",
                        "high demand": "demand-high",
                        "moderate demand": "demand-moderate",
                        "lower demand": "demand-lower",
                    }
                    dclass = demand_map.get(si.market_demand.lower(), "demand-moderate")
                    st.markdown(
                        f'<div style="text-align:center;margin:1rem 0 1.5rem 0;">'
                        f'<span class="demand-badge {dclass}">{si.market_demand}</span></div>',
                        unsafe_allow_html=True,
                    )

                    col_have, col_add = st.columns(2)
                    with col_have:
                        st.markdown('<div class="section-hdr">🔥 Your High-Value Skills</div>', unsafe_allow_html=True)
                        pills = "".join(f'<span class="pill pill-demand">{s}</span>' for s in si.in_demand_skills_you_have)
                        st.markdown(pills, unsafe_allow_html=True)
                    with col_add:
                        st.markdown('<div class="section-hdr">📈 Learn for Higher Pay</div>', unsafe_allow_html=True)
                        for sk in si.skills_to_add_for_higher_pay:
                            st.markdown(f'<div class="insight-card insight-amber">🎯 {sk}</div>', unsafe_allow_html=True)

                    st.markdown("---")
                    st.markdown('<div class="section-hdr">🤝 Negotiation Tips</div>', unsafe_allow_html=True)
                    for tip in si.negotiation_tips:
                        st.markdown(f'<div class="insight-card insight-purple">💬 {tip}</div>', unsafe_allow_html=True)

        with sub_tab2:
            st.subheader("🧭 AI Career Guidance & Upskilling")

            career_goals = st.text_area(
                "Your Career Goals",
                placeholder="e.g. 'Transition from backend to DevOps', 'Reach Staff Engineer at FAANG'",
                height=120,
            )

            if st.button("🗺️ Generate Roadmap", type="primary", use_container_width=True):
                if not career_goals:
                    st.warning("Enter your career goals first.")
                else:
                    with st.spinner("Generating personalized career roadmap…"):
                        try:
                            guidance = generate_career_guidance(
                                st.session_state.resume_text,
                                career_goals,
                                gemini_api_key,
                                model_name,
                            )
                            st.session_state.career_guidance = guidance
                            st.success("✅ Roadmap generated!")
                        except Exception as e:
                            st.error(f"Failed: {e}")

            if st.session_state.career_guidance:
                g = st.session_state.career_guidance

                st.markdown('<div class="section-hdr">📝 Strategy Summary</div>', unsafe_allow_html=True)
                st.markdown(f'<div class="letter-block">{g.summary}</div>', unsafe_allow_html=True)

                col_r, col_c = st.columns(2)
                with col_r:
                    st.markdown('<div class="section-hdr">🎯 Target Roles</div>', unsafe_allow_html=True)
                    for role in g.recommended_roles:
                        st.markdown(f'<span class="pill pill-tech" style="margin-bottom:0.3rem;">🏷️ {role}</span>', unsafe_allow_html=True)
                with col_c:
                    st.markdown('<div class="section-hdr">📚 Certifications & Courses</div>', unsafe_allow_html=True)
                    for cert in g.suggested_certifications:
                        st.markdown(f'<div class="insight-card insight-cyan">🎓 {cert}</div>', unsafe_allow_html=True)

                st.markdown("---")
                st.markdown('<div class="section-hdr">🗺️ Upskilling Roadmap</div>', unsafe_allow_html=True)
                for idx, step in enumerate(g.upskilling_roadmap):
                    st.markdown(f'<div class="insight-card insight-purple"><strong>Step {idx+1}:</strong> {step}</div>', unsafe_allow_html=True)

        with sub_tab3:
            st.subheader("🧑‍💼 Professional Persona Analysis")
            st.write("Discover your professional archetype and learn how to leverage it.")

            if st.button("🔮 Analyze My Persona", type="primary", use_container_width=True):
                with st.spinner("Analyzing your professional DNA…"):
                    try:
                        persona = analyze_persona(
                            st.session_state.resume_text,
                            gemini_api_key,
                            model_name,
                        )
                        st.session_state.persona = persona
                        st.success("✅ Persona identified!")
                    except Exception as e:
                        st.error(f"Failed: {e}")

            if st.session_state.persona:
                p = st.session_state.persona

                st.markdown(f"""
                <div class="persona-card">
                    <div class="persona-title">{p.persona_title}</div>
                    <div class="persona-desc">{p.persona_description}</div>
                    <div class="persona-style-badge">🎨 {p.communication_style}</div>
                </div>
                """, unsafe_allow_html=True)

                col_s, col_t = st.columns(2)
                with col_s:
                    st.markdown('<div class="section-hdr">💪 Strengths to Amplify</div>', unsafe_allow_html=True)
                    for s in p.strengths_to_amplify:
                        st.markdown(f'<div class="insight-card insight-green">⚡ {s}</div>', unsafe_allow_html=True)
                with col_t:
                    st.markdown('<div class="section-hdr">🎯 Interview Positioning</div>', unsafe_allow_html=True)
                    for tip in p.interview_positioning_tips:
                        st.markdown(f'<div class="insight-card insight-purple">🗣️ {tip}</div>', unsafe_allow_html=True)
