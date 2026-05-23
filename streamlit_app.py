# WP BRIGADE AI PROPOSAL GENERATOR
# IMPORTS
import streamlit as st
import requests
from datetime import datetime
import time
# PAGE CONFIG
st.set_page_config(

    page_title="WP Brigade AI Proposal Generator",

    page_icon="🚀",

    layout="wide",

    initial_sidebar_state="expanded"
)

# API CONFIG
API_BASE_URL = "http://127.0.0.1:8000"


# CUSTOM CSS
st.markdown("""

<style>

/* =====================================================
GLOBAL
===================================================== */

html, body, [class*="css"] {

    font-family: 'Segoe UI', sans-serif;

    background-color: #0F172A;
}

.main {

    background-color: #0F172A;

    color: white;
}

.block-container {

    padding-top: 2rem;

    padding-bottom: 2rem;

    max-width: 1500px;
}

/* =====================================================
SCROLLBAR
===================================================== */

::-webkit-scrollbar {

    width: 10px;
}

::-webkit-scrollbar-track {

    background: #111827;
}

::-webkit-scrollbar-thumb {

    background: #334155;

    border-radius: 10px;
}

/* =====================================================
HERO SECTION
===================================================== */

.hero-container {

    background: linear-gradient(
        135deg,
        #111827,
        #1E293B
    );

    padding: 50px;

    border-radius: 26px;

    border: 1px solid #334155;

    margin-bottom: 30px;
}

.hero-title {

    font-size: 54px;

    font-weight: 800;

    color: white;

    line-height: 1.2;
}

.hero-subtitle {

    font-size: 18px;

    color: #CBD5E1;

    margin-top: 15px;

    line-height: 1.7;
}

/* =====================================================
METRIC CARDS
===================================================== */

.metric-card {

    background: linear-gradient(
        145deg,
        #111827,
        #1E293B
    );

    border: 1px solid #334155;

    padding: 28px;

    border-radius: 20px;

    text-align: center;

    transition: 0.3s;
}

.metric-card:hover {

    transform: translateY(-5px);

    border-color: #3B82F6;
}

.metric-title {

    color: #94A3B8;

    font-size: 15px;

    margin-bottom: 10px;
}

.metric-value {

    color: white;

    font-size: 24px;

    font-weight: 700;
}

/* =====================================================
TEXT AREA
===================================================== */

.stTextArea textarea {

    background-color: #111827 !important;

    color: white !important;

    border-radius: 18px !important;

    border: 1px solid #334155 !important;

    padding: 20px !important;

    font-size: 16px !important;

    min-height: 320px !important;
}

/* =====================================================
BUTTON
===================================================== */

.stButton button {

    width: 100%;

    height: 60px;

    border-radius: 16px;

    border: none;

    background: linear-gradient(
        90deg,
        #2563EB,
        #7C3AED
    );

    color: white;

    font-size: 18px;

    font-weight: 700;

    transition: 0.3s;
}

.stButton button:hover {

    transform: scale(1.02);

    box-shadow: 0 0 20px rgba(59,130,246,0.4);
}

/* =====================================================
PROPOSAL BOX
===================================================== */

.proposal-box {

    background: #111827;

    padding: 40px;

    border-radius: 22px;

    border: 1px solid #334155;

    margin-top: 30px;

    overflow-x: auto;
}

/* =====================================================
SIDEBAR
===================================================== */

section[data-testid="stSidebar"] {

    background: #111827;
}

.sidebar-title {

    font-size: 26px;

    font-weight: 800;

    color: white;
}

/* =====================================================
STATUS CARD
===================================================== */

.status-card {

    background: #111827;

    border: 1px solid #334155;

    border-radius: 18px;

    padding: 18px;

    margin-bottom: 20px;
}

/* =====================================================
UPLOAD BOX
===================================================== */

[data-testid="stFileUploader"] {

    background: #111827;

    border: 1px dashed #475569;

    border-radius: 18px;

    padding: 15px;
}

/* =====================================================
SUCCESS BOX
===================================================== */

.stSuccess {

    border-radius: 12px;
}

</style>

""", unsafe_allow_html=True)

# SIDEBAR
with st.sidebar:

    st.markdown("""
    <div class="sidebar-title">
        WP Brigade AI
    </div>
    """, unsafe_allow_html=True)

    st.markdown("---")

    st.success("System Online")

    st.markdown("""

    ### AI Capabilities

    Proposal Generation  
    Semantic Search  
    RAG Architecture  
    FAISS Vector Search  
    PDF Intelligence  
    NLP Analysis  
    Gap Analysis  
    AI Question Generation  
    Teams Integration  
    Enterprise Prompting  

    """)

    st.markdown("---")

    st.markdown("""

    ### Technology Stack

    - Python
    - FastAPI
    - Streamlit
    - LangChain
    - FAISS
    - HuggingFace
    - SentenceTransformers
    - Groq LLM
    - NLP
    - RAG

    """)


# HERO SECTION


st.markdown("""

<div class="hero-container">

<div class="hero-title">
Wp Brigade AI Proposal Generator
</div>

<div class="hero-subtitle">
AI + NLP + RAG + FAISS + FastAPI + Groq + PDF Intelligence

Designed for enterprise consultants, software houses,
AI solution architects, and proposal management teams.

</div>

</div>

""", unsafe_allow_html=True)


# METRICS
col1, col2, col3, col4 = st.columns(4)

metrics = [

    ("AI Engine", "Groq LLM"),
    ("Vector Search", "FAISS"),
    ("Framework", "LangChain"),
    ("Backend", "FastAPI")
]

for col, metric in zip(
    [col1, col2, col3, col4],
    metrics
):

    with col:

        st.markdown(f"""

        <div class="metric-card">

        <div class="metric-title">
        {metric[0]}
        </div>

        <div class="metric-value">
        {metric[1]}
        </div>

        </div>

        """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# BACKEND STATUS
st.subheader("Backend Status")

try:

    response = requests.get(
        f"{API_BASE_URL}/",
        timeout=5
    )

    if response.status_code == 200:

        st.success(
            "FastAPI Backend Connected Successfully"
        )

    else:

        st.error(
            "Backend Connection Failed"
        )

except Exception:

    st.error(
        "FastAPI Backend Is Not Running"
    )

# PDF UPLOAD SECTION
st.subheader("Upload Proposal Knowledge Base")

uploaded_files = st.file_uploader(

    "Upload Proposal Repository PDFs",

    type=["pdf"],

    accept_multiple_files=True
)

if uploaded_files:

    progress_bar = st.progress(0)

    total_files = len(uploaded_files)

    for index, file in enumerate(uploaded_files):

        try:

            files = {

                "file": (
                    file.name,
                    file.getvalue(),
                    "application/pdf"
                )
            }

            response = requests.post(

                f"{API_BASE_URL}/upload-pdf",

                files=files,

                timeout=600
            )

            if response.status_code == 200:

                st.success(
                    f"{file.name} uploaded successfully"
                )

            else:

                try:

                    error_data = response.json()

                    st.error(
                        error_data.get(
                            "detail",
                            "Upload Failed"
                        )
                    )

                except:

                    st.error(
                        f"Upload failed for {file.name}"
                    )

        except Exception as e:

            st.error(
                f"Upload Error: {str(e)}"
            )

        progress = int(
            ((index + 1) / total_files) * 100
        )

        progress_bar.progress(progress)


# REQUIREMENT SECTION
st.subheader("Client Requirements")

requirement = st.text_area(

    "Enter detailed business requirements",

    placeholder="""

Example:

We require an AI-powered Proposal Management System
integrated with Microsoft Teams.

Required Features:

- NLP Requirement Analysis
- Proposal Semantic Search
- PDF Knowledge Repository
- Generative AI Proposal Writing
- Gap Analysis
- Proposal Annotation
- Microsoft Teams Integration
- Cloud Deployment
- Security Compliance
- Role-Based Authentication
- Dashboard Analytics
- Proposal Review Workflow

""",

    height=320
)

# GENERATE BUTTON
generate_btn = st.button(
    "Generate Enterprise Proposal"
)

# PROPOSAL GENERATION
if generate_btn:

    if requirement.strip() == "":

        st.warning(
            "Please enter detailed project requirements."
        )

    elif len(requirement.strip()) < 20:

        st.warning(
            "Requirement is too short."
        )

    else:

        with st.spinner(

            "AI is analyzing requirements, "
            "performing semantic search, "
            "executing gap analysis, "
            "and generating proposal..."
        ):

            try:

                response = requests.post(

                    f"{API_BASE_URL}/generate-proposal",

                    json={
                        "requirement":
                        requirement
                    },

                    timeout=1200
                )

                if response.status_code == 200:

                    result = response.json()

                    proposal = result.get(
                        "proposal",
                        "No proposal generated."
                    )

                    st.success(
                        "Proposal Generated Successfully"
                    )

                    st.markdown(
                        '<div class="proposal-box">',
                        unsafe_allow_html=True
                    )

                    st.markdown(proposal)

                    st.markdown(
                        '</div>',
                        unsafe_allow_html=True
                    )

                    # DOWNLOAD BUTTON

                    st.download_button(

                        label="⬇ Download Proposal",

                        data=proposal,

                        file_name=f"""

    proposal_{
    datetime.now().strftime('%Y%m%d_%H%M%S')
    }.md
    """.replace("\n", ""),

                        mime="text/markdown"
                    )

                else:

                    try:

                        error_data = response.json()

                        st.error(
                            error_data.get(
                                "detail",
                                "API Error"
                            )
                        )

                    except:

                        st.error(
                            f"API Error: {response.status_code}"
                        )

            except requests.exceptions.ConnectionError:

                st.error(
                    "FastAPI Backend Is Not Running"
                )

            except requests.exceptions.Timeout:

                st.error(
                    "Request Timeout. Proposal generation took too long."
                )

            except Exception as e:

                st.error(
                    f"Unexpected Error: {str(e)}"
                )

# FOOTER

st.markdown("---")

st.caption(
    "WP Brigade AI Proposal Generator • Enterprise AI Solution"
)