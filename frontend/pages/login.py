import requests
import streamlit as st
from api import login


def render():
    st.markdown("""
    <div style="
        background: rgba(255,255,255,0.05);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 30px;
        box-shadow: 0 8px 24px rgba(0,0,0,0.2);
        margin-top: 10px;
    ">
        <h2 style="margin-top:0; color:white;">Login</h2>
        <p style="color:#cbd5e1;">Access your account to manage applications and track your progress.</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    with st.form("login_form"):
        email = st.text_input("Email")
        password = st.text_input("Password", type="password")
        submitted = st.form_submit_button("Login")

    if submitted:
        if not email or not password:
            st.warning("Please enter both email and password.")
            return

        try:
            with st.spinner("Logging in..."):
                response = login(email, password)

            if response.status_code == 200:
                data = response.json()
                st.session_state["token"] = data.get("access_token")
                st.session_state["role"] = data.get("role", "candidate")
                st.session_state["user_email"] = email
                st.success("Login successful.")
                st.rerun()
            else:
                try:
                    st.error(response.json().get("detail", "Login failed."))
                except Exception:
                    st.error(response.text if response.text else "Login failed.")

        except requests.exceptions.Timeout:
            st.error("Login request timed out. The backend may be hanging.")

        except requests.exceptions.ConnectionError:
            st.error("Could not connect to backend. Make sure FastAPI is running.")

        except Exception as e:
            st.error(f"Unexpected error: {str(e)}")

    st.markdown("<br>", unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Forgot Password?"):
            st.session_state.page = "Forgot Password"
            st.rerun()

    with col2:
        if st.button("Create Account"):
            st.session_state.page = "Sign Up"
            st.rerun()