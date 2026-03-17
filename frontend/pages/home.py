import streamlit as st


def render():
    st.markdown("""
    <style>
    .stApp {
        background: linear-gradient(135deg, #0f172a, #111827, #1e293b);
        color: white;
    }

    .block-container {
        padding-top: 2rem;
        padding-bottom: 2rem;
        padding-left: 3rem;
        padding-right: 3rem;
        max-width: 1400px;
    }

    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}

    .hero {
        padding: 60px 40px;
        border-radius: 24px;
        background: linear-gradient(135deg, rgba(37,99,235,0.18), rgba(124,58,237,0.18));
        border: 1px solid rgba(255,255,255,0.08);
        backdrop-filter: blur(10px);
        box-shadow: 0 10px 35px rgba(0,0,0,0.25);
        margin-bottom: 30px;
    }

    .hero-badge {
        display: inline-block;
        padding: 8px 16px;
        border-radius: 999px;
        background: rgba(59,130,246,0.15);
        color: #93c5fd;
        font-size: 14px;
        font-weight: 600;
        margin-bottom: 20px;
        border: 1px solid rgba(147,197,253,0.25);
    }

    .hero-title {
        font-size: 58px;
        line-height: 1.1;
        font-weight: 800;
        color: #ffffff;
        margin-bottom: 16px;
    }

    .hero-title span {
        background: linear-gradient(90deg, #60a5fa, #a78bfa);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
    }

    .hero-text {
        font-size: 18px;
        color: #cbd5e1;
        max-width: 700px;
        line-height: 1.8;
        margin-bottom: 26px;
    }

    div.stButton > button {
        border-radius: 14px;
        padding: 0.85rem 1.4rem;
        font-size: 16px;
        font-weight: 600;
        border: none;
        transition: 0.3s ease;
        width: 100%;
    }

    div.stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 8px 20px rgba(0,0,0,0.22);
    }

    .section-title {
        font-size: 32px;
        font-weight: 700;
        color: white;
        margin-top: 15px;
        margin-bottom: 8px;
        text-align: center;
    }

    .section-subtitle {
        text-align: center;
        color: #94a3b8;
        font-size: 16px;
        margin-bottom: 28px;
    }

    .card {
        background: rgba(255,255,255,0.04);
        border: 1px solid rgba(255,255,255,0.08);
        border-radius: 22px;
        padding: 28px 22px;
        box-shadow: 0 8px 30px rgba(0,0,0,0.18);
        min-height: 230px;
        transition: 0.3s ease;
    }

    .card:hover {
        transform: translateY(-6px);
        border-color: rgba(96,165,250,0.35);
    }

    .card-icon {
        font-size: 34px;
        margin-bottom: 14px;
    }

    .card-title {
        font-size: 22px;
        font-weight: 700;
        color: #f8fafc;
        margin-bottom: 10px;
    }

    .card-text {
        font-size: 15px;
        color: #cbd5e1;
        line-height: 1.7;
    }
    </style>
    """, unsafe_allow_html=True)

    left, right = st.columns([1.4, 1])

    with left:
        st.markdown("""
        <div class="hero">
            <div class="hero-badge">⚡ Smart Recruitment Powered by AI</div>
            <div class="hero-title">
                Hire Smarter with <span>AI Hiring System</span>
            </div>
            <div class="hero-text">
                AI Hiring System is a smart recruitment platform that helps organizations
                screen resumes, rank candidates, manage job applications, and improve
                hiring decisions using intelligent automation.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with right:
        st.markdown("""
        <div class="hero">
            <div class="card-title">What this platform does</div>
            <div class="card-text">
                ✔ Resume upload and storage<br><br>
                ✔ AI-powered applicant scoring<br><br>
                ✔ Faster shortlisting of top talent<br><br>
                ✔ Better hiring workflow management<br><br>
                ✔ Secure and structured recruitment process
            </div>
        </div>
        """, unsafe_allow_html=True)

    btn1, btn2 = st.columns([1, 1])

    with btn1:
        if st.button("🚀 Get Started"):
            st.session_state.page = "Sign Up"
            st.rerun()

    with btn2:
        if st.button("🔐 Login"):
            st.session_state.page = "Login"
            st.rerun()

    st.markdown("<br><br>", unsafe_allow_html=True)

    st.markdown('<div class="section-title">Platform Features</div>', unsafe_allow_html=True)
    st.markdown(
        '<div class="section-subtitle">Everything needed for a modern recruitment workflow in one intelligent system.</div>',
        unsafe_allow_html=True
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown("""
        <div class="card">
            <div class="card-icon">📄</div>
            <div class="card-title">Resume Upload</div>
            <div class="card-text">
                Applicants can upload resumes in supported formats for review,
                storage, and automated analysis.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c2:
        st.markdown("""
        <div class="card">
            <div class="card-icon">🧠</div>
            <div class="card-title">AI Candidate Scoring</div>
            <div class="card-text">
                The system analyzes candidate resumes against job requirements
                and helps rank top applicants fairly.
            </div>
        </div>
        """, unsafe_allow_html=True)

    with c3:
        st.markdown("""
        <div class="card">
            <div class="card-icon">📊</div>
            <div class="card-title">Structured Hiring</div>
            <div class="card-text">
                Recruiters can review applications in an organized workflow and
                make better hiring decisions faster.
            </div>
        </div>
        """, unsafe_allow_html=True)