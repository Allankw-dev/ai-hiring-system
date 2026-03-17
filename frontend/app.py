import streamlit as st

from pages import home
from pages import login
from pages import sign_up
from pages import dashboard
from pages import jobs
from pages import applications
from pages import upload_resume
from pages import profile
from pages import admin_panel
from pages import forgot_password
from pages import reset_password

st.set_page_config(page_title="AI Hiring System", page_icon="🤖", layout="wide")

# ---------------------------
# GLOBAL STYLES
# ---------------------------
st.markdown("""
<style>
.stApp {
    background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
    color: white;
}

#MainMenu {visibility: hidden;}
footer {visibility: hidden;}
header {visibility: hidden;}

.block-container {
    padding-top: 1.2rem;
    padding-bottom: 2rem;
    max-width: 1300px;
}

section[data-testid="stSidebar"] {
    background: rgba(15, 23, 42, 0.95);
    border-right: 1px solid rgba(255,255,255,0.08);
}

div.stButton > button {
    border-radius: 12px;
    font-weight: 600;
    border: none;
    padding: 0.75rem 1rem;
}

div[role="radiogroup"] {
    display: flex;
    gap: 10px;
    flex-wrap: wrap;
    margin-bottom: 10px;
}

div[role="radiogroup"] label {
    background: rgba(255,255,255,0.05);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 12px;
    padding: 8px 14px;
}

div[role="radiogroup"] label p {
    color: white !important;
    font-weight: 600;
}

div[data-testid="stRadio"] > label {
    display: none;
}

.nav-card {
    background: rgba(255,255,255,0.04);
    border: 1px solid rgba(255,255,255,0.08);
    border-radius: 18px;
    padding: 14px 18px 10px 18px;
    margin-bottom: 18px;
}

.nav-title {
    color: #cbd5e1;
    font-size: 14px;
    margin-bottom: 8px;
}

.status-box {
    padding: 0.8rem 1rem;
    border-radius: 14px;
    margin-bottom: 1rem;
    font-weight: 600;
    border: 1px solid rgba(255,255,255,0.08);
}

.status-admin {
    background: rgba(37, 99, 235, 0.18);
    color: #dbeafe;
    border: 1px solid rgba(96, 165, 250, 0.3);
}

.status-candidate {
    background: rgba(16, 185, 129, 0.14);
    color: #d1fae5;
    border: 1px solid rgba(52, 211, 153, 0.28);
}
</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION DEFAULTS
# ---------------------------
if "token" not in st.session_state:
    st.session_state.token = None

if "role" not in st.session_state:
    st.session_state.role = None

if "user_email" not in st.session_state:
    st.session_state.user_email = None

if "page" not in st.session_state:
    st.session_state.page = "Home"

# ---------------------------
# HELPERS
# ---------------------------
def is_logged_in():
    return st.session_state.get("token") is not None


def is_admin():
    return st.session_state.get("role") == "admin"


def is_candidate():
    return st.session_state.get("role") == "candidate"


def logout():
    st.session_state.token = None
    st.session_state.role = None
    st.session_state.user_email = None
    st.session_state.page = "Home"
    st.success("Logged out successfully.")
    st.rerun()


def route_guard(page_name: str):
    public_pages = ["Home", "Login", "Sign Up", "Forgot Password", "Reset Password"]
    candidate_pages = ["Dashboard", "Jobs", "Applications", "Upload Resume", "Profile"]
    admin_pages = ["Admin Panel"]

    if page_name in public_pages:
        return

    if page_name in candidate_pages:
        if not is_logged_in():
            st.warning("Please log in first.")
            st.session_state.page = "Login"
            st.rerun()

        if not is_candidate():
            st.error("Access denied. Candidates only.")
            st.session_state.page = "Home"
            st.rerun()

    if page_name in admin_pages:
        if not is_logged_in():
            st.warning("Please log in first.")
            st.session_state.page = "Login"
            st.rerun()

        if not is_admin():
            st.error("Access denied. Admins only.")
            st.session_state.page = "Home"
            st.rerun()

# ---------------------------
# TOP NAVIGATION - VISIBLE EVERYWHERE
# ---------------------------
nav_pages = [
    "Home",
    "Login",
    "Sign Up",
    "Dashboard",
    "Jobs",
    "Applications",
    "Upload Resume",
    "Profile",
    "Admin Panel"
]

current_nav_page = st.session_state.page if st.session_state.page in nav_pages else "Home"

top_left, top_right = st.columns([8, 2])

with top_left:
    st.markdown("""
    <div class="nav-card">
        <div class="nav-title">Navigation</div>
    </div>
    """, unsafe_allow_html=True)

selected_page = st.radio(
    "Navigation",
    nav_pages,
    index=nav_pages.index(current_nav_page),
    horizontal=True,
    label_visibility="collapsed"
)

if st.session_state.page in nav_pages and selected_page != st.session_state.page:
    st.session_state.page = selected_page
    st.rerun()

with top_right:
    if is_logged_in():
        st.write("")
        st.write(f"**{st.session_state.role.title()}**")
        if st.button("Logout"):
            logout()

st.markdown("---")

# ---------------------------
# LOGIN STATUS
# ---------------------------
if is_logged_in() and st.session_state.user_email:
    if is_admin():
        st.markdown(
            f'<div class="status-box status-admin">🛡️ Logged in as Admin • {st.session_state.user_email}</div>',
            unsafe_allow_html=True
        )
    elif is_candidate():
        st.markdown(
            f'<div class="status-box status-candidate">👤 Logged in as Candidate • {st.session_state.user_email}</div>',
            unsafe_allow_html=True
        )

# ---------------------------
# ROUTING
# ---------------------------
page = st.session_state.page

route_guard(page)

if page == "Home":
    home.render()

elif page == "Login":
    login.render()

elif page == "Sign Up":
    sign_up.render()

elif page == "Dashboard":
    dashboard.render()

elif page == "Jobs":
    jobs.render()

elif page == "Applications":
    applications.render()

elif page == "Upload Resume":
    upload_resume.render()

elif page == "Profile":
    profile.render()

elif page == "Admin Panel":
    admin_panel.render()

elif page == "Forgot Password":
    forgot_password.render()

elif page == "Reset Password":
    reset_password.render()

else:
    st.session_state.page = "Home"
    st.rerun()