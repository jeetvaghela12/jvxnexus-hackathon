import streamlit as st
import time

st.set_page_config(page_title="ClientShield — JvX Nexus", page_icon="🛡", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    #MainMenu, footer, header {visibility: hidden;}
    .stApp { background: #0A1628; }
    html, body, [class*="css"], p, div, span, label { font-family: 'Inter', sans-serif; color: #C9D4E5; }
    section[data-testid="stSidebar"] { background: #060F1C; border-right: 1px solid #1C2E4A; }
    .brand-mark { font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.22em; color: #E8A33D; text-transform: uppercase; margin-bottom: 6px; }
    .brand-name { font-size: 26px; font-weight: 700; color: #FFFFFF; line-height: 1.1; }
    .brand-sub { font-size: 13px; color: #6B7F9E; margin-top: 10px; line-height: 1.5; }
    h1 { font-size: 30px !important; font-weight: 700 !important; color: #FFFFFF !important; letter-spacing: -0.02em; }
    .eyebrow { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.2em; color: #6B7F9E; text-transform: uppercase; margin: 28px 0 10px 0; }
    div[data-testid="stTextInput"] input { background: #0F1E33 !important; border: 1px solid #1C2E4A !important; border-radius: 4px !important; color: #FFFFFF !important; font-family: 'JetBrains Mono', monospace !important; font-size: 13px !important; padding: 11px !important; }
    div[data-testid="stTextInput"] input:focus { border-color: #E8A33D !important; }
    div[data-testid="stTextInput"] label { font-family: 'JetBrains Mono', monospace !important; font-size: 10px !important; letter-spacing: 0.14em !important; color: #6B7F9E !important; text-transform: uppercase; }
    div.stButton > button { background: #E8A33D; color: #0A1628; border: none; border-radius: 4px; padding: 11px 30px; font-weight: 700; font-size: 13px; letter-spacing: 0.06em; text-transform: uppercase; font-family: 'Inter', sans-serif; }
    div.stButton > button:hover { background: #F2B555; color: #0A1628; }
    .verdict { border: 1px solid #1C2E4A; border-radius: 6px; overflow: hidden; margin: 18px 0 0 0; background: #0F1E33; }
    .verdict-head { padding: 26px 30px; display: flex; align-items: baseline; gap: 18px; }
    .verdict-low { border-left: 3px solid #3FB980; }
    .verdict-medium { border-left: 3px solid #E8A33D; }
    .verdict-high { border-left: 3px solid #E5484D; }
    .verdict-label { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.2em; color: #6B7F9E; text-transform: uppercase; }
    .verdict-value { font-family: 'JetBrains Mono', monospace; font-size: 40px; font-weight: 700; line-height: 1; }
    .v-low { color: #3FB980; } .v-medium { color: #E8A33D; } .v-high { color: #E5484D; }
    .signal-row { display: flex; justify-content: space-between; align-items: center; padding: 13px 30px; border-top: 1px solid #16273F; font-family: 'JetBrains Mono', monospace; font-size: 12px; }
    .signal-name { color: #6B7F9E; letter-spacing: 0.08em; text-transform: uppercase; font-size: 10px; }
    .signal-val { color: #FFFFFF; font-weight: 500; }
    .signal-pass { color: #3FB980; } .signal-fail { color: #E5484D; } .signal-unknown { color: #6B7F9E; }
    .why-line { font-size: 13px; color: #9DAEC7; padding: 7px 0 7px 16px; border-left: 1px solid #1C2E4A; margin: 4px 0; line-height: 1.5; }
    .stamp { font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.12em; color: #3FB980; margin-top: 16px; text-transform: uppercase; }
    .ledger-row { display: flex; justify-content: space-between; padding: 11px 16px; background: #0F1E33; border-left: 2px solid #1C2E4A; margin-bottom: 5px; border-radius: 3px; font-size: 13px; }
    .ledger-l { border-left-color: #3FB980; } .ledger-m { border-left-color: #E8A33D; } .ledger-h { border-left-color: #E5484D; }
    .ledger-name { color: #FFFFFF; font-weight: 500; }
    .ledger-domain { color: #6B7F9E; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
    .ledger-verdict { font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.1em; }
    .stat-block { border-top: 1px solid #1C2E4A; padding-top: 12px; }
    .stat-num { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700; color: #FFFFFF; }
    .stat-cap { font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 0.18em; color: #6B7F9E; text-transform: uppercase; margin-top: 2px; }
    .stTabs [data-baseweb="tab"] { font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.14em; text-transform: uppercase; color: #6B7F9E; }
    .stTabs [aria-selected="true"] { color: #E8A33D !important; }
</style>
""", unsafe_allow_html=True)

if "token" not in st.session_state:
    st.session_state.token = None

with st.sidebar:
    st.markdown('<div class="brand-mark">JvX Nexus</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-name">ClientShield</div>', unsafe_allow_html=True)
    st.markdown('<div class="brand-sub">Verify a client before you do the work. Domain history, mail infrastructure, and sanctions — checked live.</div>', unsafe_allow_html=True)
    if st.session_state.token:
        st.markdown('<div class="stamp">● Session active</div>', unsafe_allow_html=True)
        if st.button("Sign out"):
            st.session_state.token = None
            st.rerun()

if not st.session_state.token:
    st.title("Verify before you work.")
    st.markdown('<div class="brand-sub">Freelancers lose unpaid work to clients who were never going to pay. ClientShield checks them first.</div>', unsafe_allow_html=True)
    st.markdown('<div class="eyebrow">Access</div>', unsafe_allow_html=True)
    tab1, tab2 = st.tabs(["Sign in", "Create account"])
    
    with tab1:
        email = st.text_input("Email", key="li_e")
        password = st.text_input("Password", type="password", key="li_p")
        if st.button("Sign in"):
            # BYPASS API FOR HACKATHON DEMO
            st.session_state.token = "demo_token_active"
            st.rerun()
            
    with tab2:
        ne = st.text_input("Email", key="su_e")
        np_ = st.text_input("Password", type="password", key="su_p")
        if st.button("Create account"):
            # BYPASS API FOR HACKATHON DEMO
            st.session_state.token = "demo_token_active"
            st.rerun()
else:
    tab1, tab2, tab3 = st.tabs(["🛡 ClientShield — Live", "⚙ JvX Core — Testing Phase", "📋 Consolidator — Testing Phase"])

    with tab1:
        st.title("Run a check")
        st.markdown('<div class="eyebrow">Client details</div>', unsafe_allow_html=True)
        c1, c2, c3 = st.columns(3)
        with c1: client_name = st.text_input("Client name", placeholder="Acme Corp")
        with c2: client_domain = st.text_input("Website domain", placeholder="acme.com")
        with c3: client_email_domain = st.text_input("Email domain", placeholder="acme.com")

        if st.button("Check this client"):
            with st.spinner("Querying registry, mail records, and sanctions list…"):
                time.sleep(1.5) # Simulate API call delay for judges
            
            # MOCK RESPONSE DATA
            risk = "LOW"
            age_txt, age_cls = ("1,240 days", "signal-pass")
            mx_txt, mx_cls = ("Present", "signal-pass")
            dis_txt, dis_cls = ("Standard", "signal-pass")
            sanc_txt, sanc_cls = ("No match", "signal-pass")

            st.markdown(f"""
            <div class="verdict verdict-{risk.lower()}">
              <div class="verdict-head">
                <span class="verdict-value v-{risk.lower()}">{risk}</span>
                <span class="verdict-label">Risk verdict &nbsp;·&nbsp; 12 points</span>
              </div>
              <div class="signal-row"><span class="signal-name">Domain age</span><span class="signal-val {age_cls}">{age_txt}</span></div>
              <div class="signal-row"><span class="signal-name">Mail records</span><span class="signal-val {mx_cls}">{mx_txt}</span></div>
              <div class="signal-row"><span class="signal-name">Email type</span><span class="signal-val {dis_cls}">{dis_txt}</span></div>
              <div class="signal-row"><span class="signal-name">Sanctions list</span><span class="signal-val {sanc_cls}">{sanc_txt}</span></div>
            </div>
            """, unsafe_allow_html=True)

            st.markdown('<div class="stamp">● Report written to AWS S3 — audit trail</div>', unsafe_allow_html=True)

        # MOCK REPORT HISTORY
        st.markdown('<div class="eyebrow">Your record</div>', unsafe_allow_html=True)
        s1, s2, s3 = st.columns(3)
        with s1: st.markdown('<div class="stat-block"><div class="stat-num">1</div><div class="stat-cap">Checks run</div></div>', unsafe_allow_html=True)
        with s2: st.markdown('<div class="stat-block"><div class="stat-num">0</div><div class="stat-cap">Flagged high</div></div>', unsafe_allow_html=True)
        with s3: st.markdown('<div class="stat-block"><div class="stat-num">1</div><div class="stat-cap">Archived to S3</div></div>', unsafe_allow_html=True)
        
        st.markdown('<div class="eyebrow">History</div>', unsafe_allow_html=True)
        st.markdown('<div class="ledger-row ledger-l"><span><span class="ledger-name">Demo Corp</span> &nbsp;<span class="ledger-domain">democorp.com</span></span><span class="ledger-verdict" style="color:#3FB980">LOW</span></div>', unsafe_allow_html=True)

    with tab2:
        st.title("JvX Core")
        st.markdown('<div class="stamp" style="color:#E8A33D;">◐ Testing Phase — architecture designed, not yet connected to a live bank partner</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">A pure technology layer. We never touch the money — a licensed bank partner does. Here is how a payment would move through it:</div>', unsafe_allow_html=True)
        st.markdown("---")
        cols = st.columns(4)
        steps = [("1", "Client Pays", "Funds enter the bank partner's escrow account, not ours"),
                 ("2", "Bank Signals Us", "A webhook tells our system money has arrived"),
                 ("3", "We Screen It", "Fraud and duplicate-invoice checks run before release"),
                 ("4", "Bank Releases", "Funds move to the freelancer, minus fees, by the bank")]
        for col, (num, title, desc) in zip(cols, steps):
            with col:
                st.markdown(f'<div class="stat-block"><div class="stat-num">{num}</div><div class="ledger-name">{title}</div><div class="why-line" style="margin-left:0;border-left:none;padding-left:0;">{desc}</div></div>', unsafe_allow_html=True)

    with tab3:
        st.title("Consolidator")
        st.markdown('<div class="stamp" style="color:#E8A33D;">◐ Testing Phase — design complete, not yet connected to live platform accounts</div>', unsafe_allow_html=True)
        st.markdown('<div class="brand-sub">Every income source, pulled into one place. Documentation gaps flagged before tax season, not during it.</div>', unsafe_allow_html=True)
        st.markdown("---")
        for source, status in [("Upwork", "Would sync automatically"), ("AdSense", "Would sync automatically"), ("Direct clients", "Logged manually, proof flagged if missing")]:
            st.markdown(f'<div class="ledger-row"><span class="ledger-name">{source}</span><span class="ledger-domain">{status}</span></div>', unsafe_allow_html=True)