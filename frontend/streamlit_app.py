import streamlit as st
import requests

st.set_page_config(page_title="AI Hiring System", layout="centered")
st.title("🤖 AI Hiring Intelligence System")
st.markdown(
    "Automated resume screening system using AI and NLP similarity scoring.")

# --- Candidate Analysis ---
st.header("Candidate Analysis")

name = st.text_input("Candidate Name")
resume_text = st.text_area("Paste Resume Text")
job_desc = st.text_area("Paste Job Description")

if st.button("Analyze Candidate"):
    if not name or not resume_text or not job_desc:
        st.warning("Please fill all fields!")
    else:
        with st.spinner("Analyzing candidate..."):
            try:
                response = requests.post(
                    "http://127.0.0.1:8000/analyze",
                    json={
                        "name": name,
                        "resume_text": resume_text,
                        "job_description": job_desc
                    }
                )
                data = response.json()

                score = round(data['match_score'], 2)
                exp = data['experience']

                st.success(f"✅ Match Score: **{score}%**")
                st.progress(score/100)
                st.info(f"🧑‍💼 Estimated Experience: **{exp} years**")
            except:
                st.error(
                    "Could not connect to backend. Make sure backend is running.")

st.markdown("---")

# --- View All Candidates ---
st.header("All Candidates")
if st.button("Refresh Candidate List"):
    try:
        response = requests.get("http://127.0.0.1:8000/candidates")
        candidates = response.json()
        if candidates:
            st.table(candidates)
        else:
            st.info("No candidates yet.")
    except:
        st.error("Could not fetch candidates. Make sure backend is running.")
