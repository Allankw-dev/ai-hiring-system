import streamlit as st
from api import upload_resume, my_resumes


def render():
    # DO NOT use st.set_page_config() here if this file is imported by application.py
    # Keep st.set_page_config() only in the main application file.

    st.markdown("""
        <style>
        .main {
            background-color: #0f172a;
        }

        .title-text {
            font-size: 38px;
            font-weight: 700;
            color: #ffffff;
            margin-bottom: 5px;
        }

        .subtitle-text {
            font-size: 16px;
            color: #cbd5e1;
            margin-bottom: 25px;
        }

        .card {
            background: linear-gradient(135deg, #1e293b, #0f172a);
            padding: 25px;
            border-radius: 18px;
            box-shadow: 0 6px 20px rgba(0,0,0,0.25);
            border: 1px solid #334155;
            margin-bottom: 20px;
        }

        .section-header {
            font-size: 22px;
            font-weight: 600;
            color: #f8fafc;
            margin-bottom: 15px;
        }

        .success-box {
            padding: 12px;
            border-radius: 12px;
            background-color: #14532d;
            color: white;
            font-weight: 500;
        }

        .warning-box {
            padding: 12px;
            border-radius: 12px;
            background-color: #7c2d12;
            color: white;
            font-weight: 500;
        }

        .info-box {
            padding: 12px;
            border-radius: 12px;
            background-color: #1d4ed8;
            color: white;
            font-weight: 500;
        }

        div.stButton > button {
            width: 100%;
            background: linear-gradient(90deg, #2563eb, #7c3aed);
            color: white;
            font-size: 16px;
            font-weight: 600;
            border-radius: 12px;
            border: none;
            padding: 12px 0;
            transition: 0.3s ease-in-out;
        }

        div.stButton > button:hover {
            transform: scale(1.02);
            background: linear-gradient(90deg, #1d4ed8, #6d28d9);
        }

        .uploadedFile {
            border-radius: 10px !important;
        }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="title-text">📄 Upload Resume</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="subtitle-text">Upload your resume in PDF or TXT format and manage your submissions easily.</div>',
        unsafe_allow_html=True
    )

    if "token" not in st.session_state:
        st.markdown('<div class="warning-box">Please log in first.</div>', unsafe_allow_html=True)
        return

    col1, col2 = st.columns([1.2, 1])

    with col1:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Resume Upload</div>', unsafe_allow_html=True)

        uploaded_file = st.file_uploader(
            "Choose a resume file",
            type=["pdf", "txt"],
            help="Only PDF and TXT files are allowed"
        )

        if uploaded_file is not None:
            st.info(f"Selected file: **{uploaded_file.name}**")

        if st.button("Upload Resume"):
            if uploaded_file is None:
                st.markdown('<div class="warning-box">Choose a file first.</div>', unsafe_allow_html=True)
            else:
                response = upload_resume(uploaded_file)
                if response.status_code == 200:
                    st.markdown('<div class="success-box">Resume uploaded successfully.</div>', unsafe_allow_html=True)
                    st.json(response.json())
                else:
                    try:
                        st.error(response.json().get("detail", "Upload failed"))
                    except Exception:
                        st.error("Upload failed")

        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="card">', unsafe_allow_html=True)
        st.markdown('<div class="section-header">Upload Tips</div>', unsafe_allow_html=True)

        st.markdown("""
        ✅ Use a clear and professional resume  
        ✅ Include your skills and experience  
        ✅ Keep formatting neat and readable  
        ✅ PDF is usually the best choice  
        """)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 📁 My Resumes")

    response = my_resumes()
    if response.status_code == 200:
        resumes = response.json()
        if resumes:
            st.dataframe(resumes, use_container_width=True)
        else:
            st.markdown('<div class="info-box">No resumes uploaded yet.</div>', unsafe_allow_html=True)
    else:
        st.error("Could not load resumes.")