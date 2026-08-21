import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="ClientShield — JvX Nexus", page_icon="🛡", layout="wide")

st.markdown("""
<link href="https://fonts.googleapis.com/css2?family=JetBrains+Mono:wght@400;500;700&family=Inter:wght@400;500;600;700&display=swap" rel="stylesheet">
<style>
    #MainMenu, footer, header {visibility: hidden;}

    .stApp { background: #0A1628; }
    html, body, [class*="css"], p, div, span, label { font-family: 'Inter', sans-serif; color: #C9D4E5; }

    section[data-testid="stSidebar"] { background: #060F1C; border-right: 1px solid #1C2E4A; }

    .brand-mark {
        font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.22em;
        color: #E8A33D; text-transform: uppercase; margin-bottom: 6px;
    }
    .brand-name { font-size: 26px; font-weight: 700; color: #FFFFFF; line-height: 1.1; }
    .brand-sub { font-size: 13px; color: #6B7F9E; margin-top: 10px; line-height: 1.5; }

    h1 { font-size: 30px !important; font-weight: 700 !important; color: #FFFFFF !important; letter-spacing: -0.02em; }

    .eyebrow {
        font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.2em;
        color: #6B7F9E; text-transform: uppercase; margin: 28px 0 10px 0;
    }

    div[data-testid="stTextInput"] input {
        background: #0F1E33 !important; border: 1px solid #1C2E4A !important;
        border-radius: 4px !important; color: #FFFFFF !important;
        font-family: 'JetBrains Mono', monospace !important; font-size: 13px !important; padding: 11px !important;
    }
    div[data-testid="stTextInput"] input:focus { border-color: #E8A33D !important; }
    div[data-testid="stTextInput"] label { font-family: 'JetBrains Mono', monospace !important;
        font-size: 10px !important; letter-spacing: 0.14em !important; color: #6B7F9E !important; text-transform: uppercase; }

    div.stButton > button {
        background: #E8A33D; color: #0A1628; border: none; border-radius: 4px;
        padding: 11px 30px; font-weight: 700; font-size: 13px;
        letter-spacing: 0.06em; text-transform: uppercase; font-family: 'Inter', sans-serif;
    }
    div.stButton > button:hover { background: #F2B busy55; color: #0A1628; }

    .verdict {
        border: 1px solid #1C2E4A; border-radius: 6px; overflow: hidden; margin: 18px 0 0 0;
        background: #0F1E33;
    }
    .verdict-head { padding: 26px 30px; display: flex; align-items: baseline; gap: 18px; }
    .verdict-low { border-left: 3px solid #3FB980; }
    .verdict-medium { border-left: 3px solid #E8A33D; }
    .verdict-high { border-left: 3px solid #E5484D; }
    .verdict-label {
        font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.2em;
        color: #6B7F9E; text-transform: uppercase;
    }
    .verdict-value { font-family: 'JetBrains Mono', monospace; font-size: 40px; font-weight: 700; line-height: 1; }
    .v-low { color: #3FB980; } .v-medium { color: #E8A33D; } .v-high { color: #E5484D; }

    .signal-row {
        display: flex; justify-content: space-between; align-items: center;
        padding: 13px 30px; border-top: 1px solid #16273F;
        font-family: 'JetBrains Mono', monospace; font-size: 12px;
    }
    .signal-name { color: #6B7F9E; letter-spacing: 0.08em; text-transform: uppercase; font-size: 10px; }
    .signal-val { color: #FFFFFF; font-weight: 500; }
    .signal-pass { color: #3FB980; } .signal-fail { color: #E5484D; } .signal-unknown { color: #6B7F9E; }

    .why-line {
        font-size: 13px; color: #9DAEC7; padding: 7px 0 7px 16px;
        border-left: 1px solid #1C2E4A; margin: 4px 0; line-height: 1.5;
    }

    .stamp {
        font-family: 'JetBrains Mono', monospace; font-size: 10px; letter-spacing: 0.12em;
        color: #3FB980; margin-top: 16px; text-transform: uppercase;
    }

    .ledger-row {
        display: flex; justify-content: space-between; padding: 11px 16px;
        background: #0F1E33; border-left: 2px solid #1C2E4A; margin-bottom: 5px;
        border-radius: 3px; font-size: 13px;
    }
    .ledger-l { border-left-color: #3FB980; } .ledger-m { border-left-color: #E8A33D; } .ledger-h { border-left-color: #E5484D; }
    .ledger-name { color: #FFFFFF; font-weight: 500; }
    .ledger-domain { color: #6B7F9E; font-family: 'JetBrains Mono', monospace; font-size: 11px; }
    .ledger-verdict { font-family: 'JetBrains Mono', monospace; font-size: 11px; letter-spacing: 0.1em; }

    .stat-block { border-top: 1px solid #1C2E4A; padding-top: 12px; }
    .stat-num { font-family: 'JetBrains Mono', monospace; font-size: 28px; font-weight: 700; color: #FFFFFF; }
    .stat-cap { font-family: 'JetBrains Mono', monospace; font-size: 9px; letter-spacing: 0.18em; color: #6B7F9E; text-transform: uppercase; margin-top: 2px; }

    .stTabs [data-baseweb="tab"] { font-family: 'JetBrains Mono', monospace; font-size: 11px;
        letter-spacing: 0.14em; text-transform: uppercase; color: #6B7F9E; }
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
            r = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
            if r.status_code == 200:
                st.session_state.token = r.json()["access_token"]
                st.rerun()
            else:
                st.error("Those credentials didn't match. Check the email and password and try again.")
    with tab2:
        ne = st.text_input("Email", key="su_e")
        np_ = st.text_input("Password", type="password", key="su_p")
        if st.button("Create account"):
            r = requests.post(f"{API_URL}/auth/signup", json={"email": ne, "password": np_})
            if r.status_code == 200:
                st.session_state.token = r.json()["access_token"]
                st.rerun()
            else:
                st.error("That email is already registered. Sign in instead.")
else:
    st.title("Run a check")
    st.markdown('<div class="eyebrow">Client details</div>', unsafe_allow_html=True)
    c1, c2, c3 = st.columns(3)
    with c1: client_name = st.text_input("Client name", placeholder="Acme Corp")
    with c2: client_domain = st.text_input("Website domain", placeholder="acme.com")
    with c3: client_email_domain = st.text_input("Email domain", placeholder="acme.com")

    if st.button("Check this client"):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        payload = {"client_name": client_name, "client_domain": client_domain, "client_email_domain": client_email_domain}
        with st.spinner("Querying registry, mail records, and sanctions list…"):
            r = requests.post(f"{API_URL}/clientshield/check", json=payload, headers=headers)

        if r.status_code == 200:
            d = r.json()
            risk = d["risk_score"]

            age = d.get("domain_age_days")
            age_txt, age_cls = ("Not found", "signal-unknown") if age is None else (
                (f"{age:,} days", "signal-pass") if age >= 180 else (f"{age:,} days", "signal-fail"))
            mx = d.get("mx_valid")
            mx_txt, mx_cls = ("Not found", "signal-unknown") if mx is None else (
                ("Present", "signal-pass") if mx else ("Missing", "signal-fail"))
            dis_txt, dis_cls = ("Disposable", "signal-fail") if d.get("disposable_email") else ("Standard", "signal-pass")
            sanc_txt, sanc_cls = ("Match found", "signal-fail") if d.get("sanctions_hit") else ("No match", "signal-pass")

            st.markdown(f"""
<div class="verdict verdict-{risk.lower()}">
  <div class="verdict-head">
    <span class="verdict-value v-{risk.lower()}">{risk}</span>
    <span class="verdict-label">Risk verdict &nbsp;·&nbsp; {d.get('risk_points')} points</span>
  </div>
  <div class="signal-row"><span class="signal-name">Domain age</span><span class="signal-val {age_cls}">{age_txt}</span></div>
  <div class="signal-row"><span class="signal-name">Mail records</span><span class="signal-val {mx_cls}">{mx_txt}</span></div>
  <div class="signal-row"><span class="signal-name">Email type</span><span class="signal-val {dis_cls}">{dis_txt}</span></div>
  <div class="signal-row"><span class="signal-name">Sanctions list</span><span class="signal-val {sanc_cls}">{sanc_txt}</span></div>
</div>
""", unsafe_allow_html=True)

            if d.get("reasoning"):
                st.markdown('<div class="eyebrow">How this was scored</div>', unsafe_allow_html=True)
                for line in d["reasoning"]:
                    st.markdown(f'<div class="why-line">{line}</div>', unsafe_allow_html=True)

            if d.get("s3_stored"):
                st.markdown('<div class="stamp">● Report written to AWS S3 — audit trail</div>', unsafe_allow_html=True)
        else:
            st.error("The check didn't complete. Confirm the domain is spelled correctly and run it again.")

    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    rp = requests.get(f"{API_URL}/clientshield/reports", headers=headers)
    if rp.status_code == 200:
        reports = rp.json()
        if reports:
            st.markdown('<div class="eyebrow">Your record</div>', unsafe_allow_html=True)
            s1, s2, s3 = st.columns(3)
            highs = sum(1 for x in reports if x["risk_score"] == "HIGH")
            with s1: st.markdown(f'<div class="stat-block"><div class="stat-num">{len(reports)}</div><div class="stat-cap">Checks run</div></div>', unsafe_allow_html=True)
            with s2: st.markdown(f'<div class="stat-block"><div class="stat-num">{highs}</div><div class="stat-cap">Flagged high</div></div>', unsafe_allow_html=True)
            with s3: st.markdown(f'<div class="stat-block"><div class="stat-num">{len(reports)}</div><div class="stat-cap">Archived to S3</div></div>', unsafe_allow_html=True)

            st.markdown('<div class="eyebrow">History</div>', unsafe_allow_html=True)
            for x in reversed(reports):
                cls = {"LOW": "ledger-l", "MEDIUM": "ledger-m", "HIGH": "ledger-h"}.get(x["risk_score"], "")
                col = {"LOW": "#3FB980", "MEDIUM": "#E8A33D", "HIGH": "#E5484D"}.get(x["risk_score"], "#6B7F9E")
                st.markdown(f'<div class="ledger-row {cls}"><span><span class="ledger-name">{x["client_name"]}</span> &nbsp;<span class="ledger-domain">{x["client_domain"]}</span></span><span class="ledger-verdict" style="color:{col}">{x["risk_score"]}</span></div>', unsafe_allow_html=True)
        else:
            st.markdown('<div class="eyebrow">Your record</div>', unsafe_allow_html=True)
            st.markdown('<div class="why-line">No checks yet. Run your first one above.</div>', unsafe_allow_html=True)