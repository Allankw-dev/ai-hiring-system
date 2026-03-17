import streamlit as st
from api import forgot_password


def render():
    st.title("Forgot Password")
    st.write("Enter your registered email to receive a password reset link.")

    email = st.text_input("Email")

    if st.button("Send Reset Link"):
        if not email.strip():
            st.warning("Please enter your email.")
            return

        response = forgot_password(email)

        if response.status_code == 200:
            st.success("If your email exists in the system, a reset link has been sent.")
        else:
            st.error("Could not send reset link.")