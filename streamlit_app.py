import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000"
st.set_page_config(page_title="JvX ClientShield", page_icon="🛡️", layout="wide")

st.markdown("""
<style>
    h1, h2, h3 { color: #0F2A5C; }
    .risk-low { background-color: #E7F3ED; border-left: 6px solid #1B7A4D; padding: 20px; border-radius: 8px; }
    .risk-medium { background-color: #FBEFE3; border-left: 6px solid #B5590C; padding: 20px; border-radius: 8px; }
    .risk-high { background-color: #FCE8E8; border-left: 6px solid #C0392B; padding: 20px; border-radius: 8px; }
    .risk-score-text { font-size: 32px; font-weight: bold; }
</style>
""", unsafe_allow_html=True)

if "token" not in st.session_state:
    st.session_state.token = None

with st.sidebar:
    st.markdown("## 🛡️ JvX Nexus")
    st.markdown("**ClientShield**")
    st.markdown("---")
    if st.session_state.token:
        st.success("Logged in")
        if st.button("Logout"):
            st.session_state.token = None
            st.rerun()

if not st.session_state.token:
    st.title("JvX Nexus — ClientShield")
    st.caption("Check a new client's legitimacy before you do unpaid work for them.")
    tab1, tab2 = st.tabs(["Login", "Sign Up"])
    with tab1:
        email = st.text_input("Email", key="login_email")
        password = st.text_input("Password", type="password", key="login_password")
        if st.button("Login", type="primary"):
            resp = requests.post(f"{API_URL}/auth/login", json={"email": email, "password": password})
            if resp.status_code == 200:
                st.session_state.token = resp.json()["access_token"]
                st.rerun()
            else:
                st.error("Login failed.")
    with tab2:
        new_email = st.text_input("Email", key="signup_email")
        new_password = st.text_input("Password", type="password", key="signup_password")
        if st.button("Sign Up", type="primary"):
            resp = requests.post(f"{API_URL}/auth/signup", json={"email": new_email, "password": new_password})
            if resp.status_code == 200:
                st.session_state.token = resp.json()["access_token"]
                st.rerun()
            else:
                st.error("Signup failed.")
else:
    st.title("ClientShield — Check a New Client")
    col1, col2 = st.columns(2)
    with col1:
        client_name = st.text_input("Client Name", placeholder="e.g. Acme Corp")
        client_domain = st.text_input("Client Website Domain", placeholder="e.g. example.com")
    with col2:
        client_email_domain = st.text_input("Client Email Domain", placeholder="e.g. example.com")

    if st.button("Run Check", type="primary"):
        headers = {"Authorization": f"Bearer {st.session_state.token}"}
        payload = {"client_name": client_name, "client_domain": client_domain, "client_email_domain": client_email_domain}
        with st.spinner("Checking domain age, MX records, sanctions..."):
            resp = requests.post(f"{API_URL}/clientshield/check", json=payload, headers=headers)
        if resp.status_code == 200:
            data = resp.json()
            risk = data["risk_score"]
            css_class = f"risk-{risk.lower()}"
            emoji = "✅" if risk == "LOW" else "⚠️" if risk == "MEDIUM" else "🚨"
            st.markdown(f'<div class="{css_class}"><div class="risk-score-text">{emoji} {risk} RISK</div></div>', unsafe_allow_html=True)
            st.markdown("### Signal Breakdown")
            c1, c2, c3, c4 = st.columns(4)
            c1.metric("Domain Age", f"{data['domain_age_days']} days" if data['domain_age_days'] else "Unknown")
            c2.metric("MX Valid", "Yes" if data['mx_valid'] else "No" if data['mx_valid'] is False else "Unknown")
            c3.metric("Disposable Email", "Yes ⚠️" if data['disposable_email'] else "No ✅")
            c4.metric("Sanctions Hit", "YES 🚨" if data['sanctions_hit'] else "No ✅")
        else:
            st.error(f"Error: {resp.text}")

    st.markdown("---")
    st.markdown("### Past Checks")
    headers = {"Authorization": f"Bearer {st.session_state.token}"}
    resp = requests.get(f"{API_URL}/clientshield/reports", headers=headers)
    if resp.status_code == 200:
        reports = resp.json()
        if reports:
            for r in reversed(reports):
                icon = {"LOW": "🟢", "MEDIUM": "🟡", "HIGH": "🔴"}.get(r["risk_score"], "⚪")
                st.write(f"{icon} **{r['client_name']}** ({r['client_domain']}) — {r['risk_score']}")
        else:
            st.info("No checks yet.")