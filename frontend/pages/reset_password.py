import streamlit as st
from api import reset_password


def render():
    st.title("Reset Password")

    token = st.query_params.get("reset_token", "")

    if not token:
        st.error("Missing reset token.")
        return

    new_password = st.text_input("New Password", type="password")
    confirm_password = st.text_input("Confirm New Password", type="password")

    if st.button("Reset Password"):
        if not new_password or not confirm_password:
            st.warning("Please fill in both fields.")
            return

        if new_password != confirm_password:
            st.error("Passwords do not match.")
            return

        response = reset_password(token, new_password)

        if response.status_code == 200:
            st.success("Password reset successfully. You can now log in.")
        else:
            try:
                st.error(response.json().get("detail", "Could not reset password"))
            except Exception:
                st.error("Could not reset password")