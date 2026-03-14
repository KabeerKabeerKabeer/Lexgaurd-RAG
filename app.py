import streamlit as st
import os
from brain import create_db
from graph import oApp

st.set_page_config(page_title="LexGuard RAG", page_icon="⚖️")

st.title("⚖️ LexGuard: Agentic Legal RAG")
st.markdown("Build for Legal Compliance Audit")

# Sidebar for PDF Upload
with st.sidebar:
    st.header("Setup")
    oFile = st.file_uploader("Upload Legal PDF", type="pdf")
    if st.button("Process Document"):
        if oFile:
            # Save file locally
            with open("test.pdf", "wb") as f:
                f.write(oFile.getbuffer())
            # Create the Vector DB using brain.py
            create_db("test.pdf")
            st.success("Database Created!")
        else:
            st.error("Please upload a file.")

# Main Chat Area
sUserQuery = st.text_input("Ask a question about the contract:")

if st.button("Analyze"):
    if os.path.exists("./db_legal"):
        with st.spinner("Agent is auditing..."):
            # Run the LangGraph flow
            dInput = {"sQuery": sUserQuery}
            oFinal = oApp.invoke(dInput)
            
            st.subheader("Audit Result")
            st.write(oFinal["sResult"])
            
            with st.expander("Show Source Context"):
                st.info(oFinal["sContext"])
    else:
        st.warning("Please process a document in the sidebar first.")