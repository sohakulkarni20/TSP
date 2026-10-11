import streamlit as st


def apply_styles():
    st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=DM+Mono:wght@400;500&family=Manrope:wght@400;500;600;700;800&display=swap');
    :root { color-scheme: dark; }
    html, body, [class*="css"] { font-family: 'Manrope', sans-serif; }
    .stApp { background: #0b0f19; color: #e8edf6; }
    [data-testid="stSidebar"] { background: #101522; border-right: 1px solid #222b3c; }
    [data-testid="stSidebar"] * { color: #e8edf6; }
    .block-container { padding-top: 1.8rem; padding-bottom: 2rem; max-width: 1500px; }
    .hero { padding: 1.2rem 0 1.4rem 0; }
    .eyebrow { color: #42e8d4; font: 500 .72rem 'DM Mono', monospace; letter-spacing: .18em; }
    .hero h1 { font-size: clamp(2.6rem, 5vw, 4.2rem); letter-spacing: -.07em; font-weight: 800; line-height: 1.05; margin: .35rem 0; color: #f8fafc; }
    .hero h1 span { color: #42e8d4; }
    .hero p { color: #93a4bb; font-size: 1.05rem; margin: .5rem 0 0; }
    .section-title { color: #aab8cc; font: 500 .75rem 'DM Mono', monospace; letter-spacing: .12em; margin: .6rem 0 .35rem; }
    [data-testid="stMetric"] { background: #121a29; border: 1px solid #253147; border-radius: 14px; padding: 14px 16px; }
    [data-testid="stMetricLabel"] { color: #93a4bb; }
    [data-testid="stMetricValue"] { color: #f8fafc; }
    div.stButton > button[kind="primary"] { background: #42e8d4; color: #06111a; border: none; font-weight: 800; }
    div.stButton > button { border-radius: 10px; min-height: 2.7rem; }
    .stAlert { border-radius: 12px; }
    .footer { border-top: 1px solid #263043; padding-top: 1rem; margin-top: 2rem; color: #64748b; font: .7rem 'DM Mono', monospace; letter-spacing: .1em; }
    </style>
    """, unsafe_allow_html=True)
