⚖️ LexGuard Core
Automated, rigorous compliance auditing powered by agentic reasoning.

LexGuard is an enterprise-grade Legal Compliance AI designed to ingest complex contractual documents and actively audit them for liabilities, termination risks, and compliance gaps.

Unlike standard linear RAG (Retrieval-Augmented Generation) pipelines, LexGuard utilizes LangGraph to create an agentic reasoning loop. It doesn't just retrieve text; it acts as an autonomous auditor, critically analyzing clauses for asymmetries and inconsistencies before presenting findings in a highly refined, "surgical luxury" interface.

Deployed and Accessible at
https://lexgaurd.streamlit.app

🚀 Key Capabilities
Agentic Orchestration: Replaces naive single-shot retrieval with an iterative LangGraph state machine, allowing the LLM to process and reason over retrieved context before answering.

Sub-Second Inference: Powered by Llama-3.3-70b-versatile via the Groq API, enabling heavy reasoning tasks to execute with near-instant latency.

Local Vector Space: Utilizes ChromaDB and HuggingFace (all-MiniLM-L6-v2) embeddings to securely index documents on the fly without leaking proprietary text to external vector hosting services.

Bespoke UI/UX: A custom-engineered Streamlit interface overriding default components with raw CSS to provide a clean, distraction-free environment mirroring high-end legal software.

🛠️ Technical Architecture
The Stack
Orchestration: LangChain & LangGraph

Inference Engine: Groq (Llama 3.3 70B)

Embeddings: HuggingFace sentence-transformers

Vector Store: ChromaDB (Ephemeral/Local)

Frontend: Streamlit with Custom CSS injection

The Agentic Flow (graph.py)
Ingestion: User uploads a PDF. brain.py chunks and embeds the document into a local SQLite-backed Chroma database.

State Initialization: The user query initializes the AgentState.

Retrieval Node: Performs semantic search against the legal database.

Audit Node: The core reasoning engine analyzes the retrieved clauses against the user's compliance query, actively hunting for contradictions or risks.

💻 Local Quickstart
Want to run LexGuard on your local machine?

1. Clone the repository

git clone https://github.com/YourUsername/LexGuard-RAG.git
cd LexGuard-RAG

2. Install dependencies

pip install -r requirements.txt


3. Configure Environment Variables
Create a .env file in the root directory:

GROQ_API_KEY=your_groq_key_here
HF_TOKEN=your_huggingface_key_here

4. Launch the interface

streamlit run app.py

🗺️ Product Roadmap (V2 Architecture)
LexGuard is actively being upgraded from a single-agent auditor to a Multi-Agent Conversational System:

[ ] Structural Map-Reduce Auditing: Upgrading the ingestion pipeline to parse documents by structural headers (Articles/Clauses) and map over the entire document to eliminate blind spots.

[ ] The Editor Agent: Implementing a conversational router to allow users to command the AI to rewrite and amend specific clauses (e.g., "Change the grace period to 6 months").

[ ] Security Guardrails: Adding self-critique nodes to mathematically prevent hallucinations and block prompt injection attempts.

[ ] Threaded Memory: Integrating SQLite checkpointers to maintain conversational state across multi-turn legal drafting sessions.

Architected for rigorous compliance by Kabeer Ali.