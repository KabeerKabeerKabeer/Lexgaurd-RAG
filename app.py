import streamlit as st
import os
import time
from brain import create_db
from graph import oApp

# 1. Page Configuration
st.set_page_config(page_title="LexGuard | Enterprise Auditor", layout="wide", initial_sidebar_state="expanded")

# 2. Injecting "Surgical Luxury" CSS
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600&family=Playfair+Display:wght@400;600;700&display=swap');

    /* The Brighter, Noticeable Silver Gradient */
    .stApp {
        background: radial-gradient(circle at 50% 0%, #FFFFFF 0%, #F1F3F6 45%, #E2E5EA 100%) !important;
        font-family: 'Inter', sans-serif;
    }
    
    [data-testid="stAppViewContainer"] {
        background: transparent !important;
    }

    /* Hide standard Streamlit chrome EXCEPT the header */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {background-color: transparent !important;}
    .stDeployButton {display: none;}

    /* Sidebar Styling */
    [data-testid="stSidebar"] {
        background-color: rgba(250, 252, 255, 0.85) !important;
        backdrop-filter: blur(12px);
        border-right: 1px solid rgba(0,0,0,0.06);
    }

    /* Animations */
    @keyframes fadeUp {
        0% { opacity: 0; transform: translateY(15px); }
        100% { opacity: 1; transform: translateY(0); }
    }
    .animate-1 { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) forwards; }
    .animate-2 { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.15s forwards; opacity: 0; }
    .animate-3 { animation: fadeUp 0.8s cubic-bezier(0.16, 1, 0.3, 1) 0.3s forwards; opacity: 0; }

    /* Luxury Typography */
    .lex-title {
        font-family: 'Playfair Display', serif;
        font-weight: 700;
        font-size: 3.5rem;
        color: #0A0A0A;
        letter-spacing: -0.03em;
        margin-bottom: 0px;
        line-height: 1.1;
        transition: opacity 0.3s ease;
    }
    
    .lex-subtitle {
        font-family: 'Inter', sans-serif;
        font-weight: 300;
        font-size: 1.1rem;
        color: #52525B;
        letter-spacing: 0.02em;
        margin-top: 10px;
        margin-bottom: 3.5rem;
    }

    /* Interactive Logo */
    .logo-container {
        display: flex; align-items: center; gap: 12px;
        margin-bottom: 3.5rem; margin-top: 0.5rem;
        transition: transform 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: default;
    }
    .logo-container:hover {
        transform: translateX(4px);
    }

    /* Surgical Inputs Hover & Focus */
    .stTextInput > div > div > input {
        border-radius: 6px !important;
        border: 1px solid #D4D4D8 !important;
        background-color: #FFFFFF !important; 
        color: #18181B !important;
        font-size: 1.05rem !important;
        padding: 15px 20px !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.02) !important;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
    }
    
    .stTextInput > div > div > input:hover {
        border-color: #A1A1AA !important;
        box-shadow: 0 6px 16px rgba(0,0,0,0.06) !important;
    }
    
    .stTextInput > div > div > input:focus {
        border-color: #000000 !important;
        box-shadow: 0 0 0 1px #000000, 0 8px 20px rgba(0,0,0,0.08) !important;
    }

    /* Apple-esque Button Hover */
    .stButton > button {
        background: #09090B !important;
        color: #FFFFFF !important;
        border-radius: 6px !important;
        border: none !important;
        font-weight: 500 !important;
        font-size: 1rem !important;
        padding: 14px 24px !important;
        width: 100% !important;
        margin-top: 28px !important; 
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1) !important;
        box-shadow: 0 4px 12px rgba(0,0,0,0.1) !important;
    }
    
    .stButton > button:hover {
        background: #27272A !important;
        transform: translateY(-2px) !important;
        box-shadow: 0 8px 20px rgba(0,0,0,0.15) !important;
    }

    /* Capability Modules (The 3 Key Points) Interactive Cards */
    .module-card {
        flex: 1;
        padding: 1.5rem;
        border-radius: 8px;
        border: 1px solid transparent;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
        cursor: default;
    }
    
    .module-card:hover {
        background: rgba(255, 255, 255, 0.6);
        border: 1px solid rgba(0, 0, 0, 0.05);
        transform: translateY(-6px);
        box-shadow: 0 12px 30px -5px rgba(0, 0, 0, 0.08);
    }

    .module-header {
        font-family: 'Inter', sans-serif;
        font-size: 0.75rem;
        font-weight: 600;
        letter-spacing: 0.05em;
        color: #09090B;
        text-transform: uppercase;
        border-top: 1.5px solid #09090B;
        padding-top: 12px;
        margin-bottom: 8px;
        transition: border-color 0.3s ease;
    }
    
    .module-card:hover .module-header {
        border-top: 1.5px solid #3B82F6; /* Subtle accent color on hover */
    }

    .module-text {
        font-size: 0.85rem;
        color: #52525B;
        line-height: 1.5;
    }

    /* Audit Result Card Hover */
    .audit-card {
        background: #FFFFFF; 
        border: 1px solid #E4E4E7;
        border-radius: 8px;
        padding: 2.5rem;
        box-shadow: 0 10px 30px -5px rgba(0, 0, 0, 0.08);
        font-family: 'Inter', sans-serif;
        color: #18181B;
        line-height: 1.7;
        font-size: 1rem;
        transition: all 0.4s cubic-bezier(0.16, 1, 0.3, 1);
    }
    
    .audit-card:hover {
        transform: translateY(-2px);
        box-shadow: 0 15px 40px -5px rgba(0, 0, 0, 0.12);
        border-color: #D4D4D8;
    }
    
    /* Signature Hover */
    .signature-box {
        margin-top: 6rem;
        border-top: 1px solid #E4E4E7;
        padding-top: 1.5rem;
        transition: opacity 0.3s ease;
        opacity: 0.8;
    }
    .signature-box:hover {
        opacity: 1;
    }
    
    /* --- UPLOADER COMPONENT FIX --- */
    /* Fix the drag-and-drop box */
    [data-testid="stFileUploadDropzone"] {
        background-color: #FFFFFF !important;
        border: 1px dashed #D4D4D8 !important;
        border-radius: 6px !important;
    }
    [data-testid="stFileUploadDropzone"] div {
        color: #52525B !important;
    }
    
    /* Fix the uploaded file name and icon */
    [data-testid="stUploadedFile"] {
        background-color: #FFFFFF !important;
        border: 1px solid #E4E4E7 !important;
        border-radius: 6px !important;
        box-shadow: 0 2px 4px rgba(0,0,0,0.02) !important;
    }
    [data-testid="stUploadedFile"] div, 
    [data-testid="stUploadedFile"] span, 
    [data-testid="stUploadedFile"] svg {
        color: #18181B !important;
    }
    
    /* Fix the "Cross" Remove Button */
    [data-testid="stUploadedFile"] button {
        background: transparent !important;
        padding: 0 !important;
        margin: 0 !important;
        box-shadow: none !important;
        width: auto !important;
        height: auto !important;
    }
    [data-testid="stUploadedFile"] button:hover {
        background: #F4F4F5 !important;
        transform: none !important;
    }
    [data-testid="stUploadedFile"] button svg {
        fill: #A1A1AA !important; /* Light grey cross */
        transition: fill 0.2s ease;
    }
    [data-testid="stUploadedFile"] button:hover svg {
        fill: #E63946 !important; /* Turns subtle red when hovered */
    }
</style>
""", unsafe_allow_html=True)

# 3. Sidebar (Document Workspace)
with st.sidebar:
    st.markdown("""
    <div class='logo-container'>
        <div style='width: 32px; height: 32px; background: #09090B; border-radius: 4px; display: flex; align-items: center; justify-content: center; color: #fff; font-family: "Playfair Display", serif; font-weight: 700; font-size: 18px;'>L</div>
        <span style='font-family: "Inter", sans-serif; font-weight: 600; font-size: 1.15rem; letter-spacing: -0.02em; color: #09090B;'>LexGuard Core</span>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<div class='animate-1' style='margin-bottom: 1.5rem;'>", unsafe_allow_html=True)
    st.markdown("<h3 style='font-family: \"Playfair Display\", serif; font-weight: 600; font-size: 1.5rem; color: #111; margin-bottom: 4px;'>Workspace.</h3>", unsafe_allow_html=True)
    st.markdown("<p style='font-size: 0.85rem; color: #71717A; line-height: 1.5;'>Initialize the legal vector space by uploading the target contract.</p>", unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)
    
    oFile = st.file_uploader("", type="pdf", label_visibility="collapsed")
    
    if st.button("Initialize Knowledge Base"):
        if oFile:
            with st.spinner("Indexing document semantics..."):
                with open("test.pdf", "wb") as f:
                    f.write(oFile.getbuffer())
                create_db("test.pdf")
                time.sleep(0.5) 
            st.success("Vector space initialized.")
        else:
            st.error("Document required.")
            
    st.markdown("""
    <div class='signature-box'>
        <p style='font-size: 0.7rem; color: #A1A1AA; margin-bottom: 2px; letter-spacing: 0.04em; font-weight: 600;'>SYSTEM STATUS</p>
        <p style='font-size: 0.8rem; color: #10B981; font-weight: 500; margin-bottom: 20px;'>● Llama-3.3-70b Active</p>
        <p style='font-size: 0.85rem; color: #18181B; font-weight: 500;'>Architected by Kabeer Ali</p>
    </div>
    """, unsafe_allow_html=True)

# 4. Main Layout
col_left, col_main, col_right = st.columns([1, 8, 1])

with col_main:
    st.markdown("<div class='animate-1' style='margin-top: 2rem;'>", unsafe_allow_html=True)
    st.markdown('<p class="lex-title">LexGuard.</p>', unsafe_allow_html=True)
    st.markdown('<p class="lex-subtitle">Automated, rigorous compliance auditing powered by agentic reasoning.</p>', unsafe_allow_html=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown("<div class='animate-2'>", unsafe_allow_html=True)
    col_input, col_btn = st.columns([4.5, 1.5]) 
    with col_input:
        sUserQuery = st.text_input("Query", placeholder="Define your legal inquiry (e.g., 'Identify termination liabilities').", label_visibility="hidden")
    with col_btn:
        btn_execute = st.button("Execute Audit", use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    if btn_execute:
        if os.path.exists("./db_legal"):
            with st.spinner("Agent auditing clauses..."):
                dInput = {"sQuery": sUserQuery, "nIter": 0}
                oFinal = oApp.invoke(dInput)
                
                st.markdown("<div class='animate-3' style='margin-top: 2rem;'>", unsafe_allow_html=True)
                st.markdown("<h4 style='font-family: \"Playfair Display\", serif; font-weight: 600; color: #09090B; margin-bottom: 1.5rem;'>Audit Findings</h4>", unsafe_allow_html=True)
                
                st.markdown(f"<div class='audit-card'>{oFinal['sResult']}</div>", unsafe_allow_html=True)
                
                st.markdown("<br>", unsafe_allow_html=True)
                with st.expander("View Source Citations & Context"):
                    st.markdown(f"<div style='font-size: 0.85rem; color: #71717A; line-height: 1.6;'>{oFinal['sContext']}</div>", unsafe_allow_html=True)
                st.markdown("</div>", unsafe_allow_html=True)
        else:
            st.error("System Error: Awaiting document ingestion in the Workspace.")
    else:
        # Hover-enabled Capability Modules
        st.markdown("""
        <div class='animate-3' style='margin-top: 3.5rem; display: flex; gap: 2rem;'>
            <div class='module-card'>
                <div class='module-header'>I. Liability Assessment</div>
                <div class='module-text'>Scans the document for asymmetric indemnification, uncapped liability clauses, and hidden financial exposures.</div>
            </div>
            <div class='module-card'>
                <div class='module-header'>II. Termination Risks</div>
                <div class='module-text'>Identifies notice period discrepancies, auto-renewal triggers, and unfavorable exit conditions.</div>
            </div>
            <div class='module-card'>
                <div class='module-header'>III. Compliance Gaps</div>
                <div class='module-text'>Audits provisions against standard regulatory frameworks to flag missing mandatory clauses.</div>
            </div>
        </div>
        """, unsafe_allow_html=True)