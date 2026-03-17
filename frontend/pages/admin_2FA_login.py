import streamlit as st
from api import admin_request_otp, admin_verify_otp

st.set_page_config(page_title="Admin 2FA Login", page_icon="🛡️", layout="centered")

st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg,#0f172a,#1e293b,#334155);
}

.card {
    background: rgba(255,255,255,0.08);
    padding: 2rem;
    border-radius: 20px;
    box-shadow: 0 8px 24px rgba(0,0,0,0.25);
    backdrop-filter: blur(8px);
    color: white;
    max-width: 600px;
    margin: auto;
    margin-top: 40px;
}
</style>
""", unsafe_allow_html=True)

if "otp_requested" not in st.session_state:
    st.session_state["otp_requested"] = False

st.markdown('<div class="card">', unsafe_allow_html=True)
st.title("🛡️ Admin 2FA Login")

email = st.text_input("Admin Email")
password = st.text_input("Password", type="password")

if not st.session_state["otp_requested"]:
    if st.button("Request OTP"):
        response = admin_request_otp(email, password)

        if response.status_code == 200:
            st.success("OTP generated. Check the backend terminal.")
            st.session_state["otp_requested"] = True
            st.session_state["admin_email"] = email
        else:
            try:
                st.error(response.json().get("detail", "Request failed"))
            except Exception:
                st.error("Request failed")
else:
    otp_code = st.text_input("Enter OTP Code")

    if st.button("Verify OTP"):
        response = admin_verify_otp(st.session_state["admin_email"], otp_code)

        if response.status_code == 200:
            data = response.json()
            st.session_state["token"] = data["access_token"]
            st.session_state["email"] = st.session_state["admin_email"]
            st.session_state["role"] = data.get("role", "")
            st.success("Admin logged in successfully")
        else:
            try:
                st.error(response.json().get("detail", "OTP verification failed"))
            except Exception:
                st.error("OTP verification failed")

st.markdown("</div>", unsafe_allow_html=True)