import streamlit as st
from api import list_jobs, apply_to_job, my_resumes


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
        .title {
            color: white;
            font-size: 2.2rem;
            font-weight: 700;
            margin-bottom: 1rem;
        }
        .job-card {
            background: rgba(255,255,255,0.08);
            padding: 22px;
            border-radius: 18px;
            box-shadow: 0 8px 24px rgba(0,0,0,0.25);
            margin-bottom: 18px;
            color: white;
        }
        </style>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="title">💼 Available Jobs</div>', unsafe_allow_html=True)

    response = list_jobs()
    if response.status_code != 200:
        st.error("Could not load jobs.")
        st.stop()

    jobs = response.json()
    if not jobs:
        st.info("No jobs available right now.")
        st.stop()

    resume_response = my_resumes()
    resumes = resume_response.json() if resume_response.status_code == 200 else []
    resume_options = {r["file_name"]: r["id"] for r in resumes}

    for job in jobs:
        st.markdown('<div class="job-card">', unsafe_allow_html=True)
        st.subheader(job["title"])
        st.write(f"**Company:** {job.get('company', 'Unknown')}")
        st.write(job.get("description", ""))
        st.write(f"**Required skills:** {job.get('required_skills', 'Not specified')}")
        st.write(f"**Minimum experience:** {job.get('min_experience', 0)} years")

        if resumes:
            selected_resume = st.selectbox(
                "Choose resume to apply",
                list(resume_options.keys()),
                key=f"resume_{job['id']}",
            )

            if st.button("Apply", key=f"apply_{job['id']}"):
                resume_id = resume_options[selected_resume]
                apply_response = apply_to_job(job["id"], resume_id)

                if apply_response.status_code in [200, 201]:
                    st.success("Application submitted successfully.")
                else:
                    try:
                        st.error(apply_response.json().get("detail", "Application failed."))
                    except Exception:
                        st.error("Application failed.")
                        st.write(apply_response.text)
        else:
            st.info("Upload a resume first before applying.")

        st.markdown("</div>", unsafe_allow_html=True)