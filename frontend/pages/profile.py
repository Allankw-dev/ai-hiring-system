import streamlit as st
from api import my_resumes, my_applications


def render():
    if not st.session_state.get("token"):
        st.warning("Please log in first.")
        st.stop()

    if st.session_state.get("role") != "candidate":
        st.error("Access denied. Candidates only.")
        st.stop()

    st.markdown(
        """
        <style>
        .stApp {
            background: linear-gradient(135deg,#0f172a,#1e293b,#334155);
        }
        .profile-card {
            background: rgba(255,255,255,0.08);
            padding: 20px;
            border-radius: 18px;
            color: white;
            margin-bottom: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.title("👤 My Profile")

    email = st.session_state.get("email", "Unknown")

    col1, col2 = st.columns([1, 3])

    with col1:
        st.image("https://cdn-icons-png.flaticon.com/512/149/149071.png", width=150)

    with col2:
        st.markdown('<div class="profile-card">', unsafe_allow_html=True)
        st.subheader(email)
        st.write("Role: Candidate")
        st.markdown("</div>", unsafe_allow_html=True)

    st.divider()
    st.subheader("📄 My Resumes")

    resume_response = my_resumes()
    if resume_response.status_code == 200:
        resumes = resume_response.json()
        if resumes:
            for r in resumes:
                with st.container():
                    st.write(f"**File:** {r.get('file_name', 'N/A')}")
                    st.write(f"Experience: {r.get('experience_years', 'N/A')} years")
                    st.write(f"Verification: {r.get('verification_status', 'N/A')}")
                    st.divider()
        else:
            st.info("No resumes uploaded yet.")
    else:
        st.error("Could not load resumes.")

    st.subheader("📌 My Applications")
    app_response = my_applications()

    if app_response.status_code == 200:
        apps = app_response.json()
        if apps:
            st.dataframe(apps, use_container_width=True)
        else:
            st.info("No applications yet.")
    else:
        st.error("Could not load applications.")