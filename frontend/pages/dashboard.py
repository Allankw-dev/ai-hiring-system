import streamlit as st
from api import my_resumes, my_applications, list_jobs


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
            background: linear-gradient(135deg, #0f172a, #1e293b, #334155);
        }
        .main-title {
            color: white;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 0.3rem;
        }
        .sub-text {
            color: #cbd5e1;
            margin-bottom: 1.5rem;
        }
        .card {
            background: rgba(255, 255, 255, 0.08);
            padding: 20px;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            backdrop-filter: blur(8px);
            text-align: center;
            color: white;
        }
        .card h3 {
            margin: 0;
            font-size: 1.1rem;
            color: #cbd5e1;
        }
        .card h1 {
            margin: 10px 0 0 0;
            font-size: 2rem;
            color: white;
        }
        .section-box {
            background: rgba(255, 255, 255, 0.08);
            padding: 20px;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            backdrop-filter: blur(8px);
            color: white;
            margin-top: 20px;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="main-title">📊 Dashboard</div>', unsafe_allow_html=True)
    st.markdown('<div class="sub-text">Welcome to your AI Hiring System dashboard.</div>', unsafe_allow_html=True)

    resumes_response = my_resumes()
    applications_response = my_applications()
    jobs_response = list_jobs()

    resume_count = len(resumes_response.json()) if resumes_response.status_code == 200 else 0
    application_count = len(applications_response.json()) if applications_response.status_code == 200 else 0
    job_count = len(jobs_response.json()) if jobs_response.status_code == 200 else 0

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown(
            f"""
            <div class="card">
                <h3>My Resumes</h3>
                <h1>{resume_count}</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col2:
        st.markdown(
            f"""
            <div class="card">
                <h3>My Applications</h3>
                <h1>{application_count}</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    with col3:
        st.markdown(
            f"""
            <div class="card">
                <h3>Available Jobs</h3>
                <h1>{job_count}</h1>
            </div>
            """,
            unsafe_allow_html=True,
        )

    st.markdown('<div class="section-box">', unsafe_allow_html=True)
    st.subheader("My Application Status")

    if applications_response.status_code == 200:
        apps = applications_response.json()
        if apps:
            st.dataframe(apps, use_container_width=True)
        else:
            st.info("No applications yet.")
    else:
        st.error("Could not load applications.")

    st.markdown("</div>", unsafe_allow_html=True)