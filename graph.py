import os
from typing import TypedDict
from dotenv import load_dotenv
from langchain_groq import ChatGroq
from langchain_core.messages import HumanMessage
from langgraph.graph import StateGraph, END
from brain import create_db  # Import your function from brain.py
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

# 1. Define the memory (State)
class AgentState(TypedDict):
    sQuery: str
    sContext: str
    sResult: str

# 2. Search Node: Links to your Vector DB
def search_node(state: AgentState):
    print("--- AGENT: SEARCHING PDF ---")
    oEmbed = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2")
    # Connect to the folder brain.py created
    oDB = Chroma(persist_directory="./db_legal", embedding_function=oEmbed)
    lRes = oDB.similarity_search(state["sQuery"], k=3)
    sCtx = "\n".join([d.page_content for d in lRes])
    return {"sContext": sCtx}

# 3. Audit Node: The "Thinking" step
def audit_node(state: AgentState):
    print("--- AGENT: ANALYZING CLAUSES ---")
    oLLM = ChatGroq(model="llama-3.3-70b-versatile")
    
    sPrompt = f"""
    You are a Legal Compliance Expert. 
    Analyze the following context from a contract: {state['sContext']}
    Answer the user's question: {state['sQuery']}
    If there is a conflict or risk, highlight it clearly.
    """
    oMsg = oLLM.invoke([HumanMessage(content=sPrompt)])
    return {"sResult": oMsg.content}

# 4. Connect the Graph
builder = StateGraph(AgentState)
builder.add_node("search", search_node)
builder.add_node("audit", audit_node)

builder.set_entry_point("search")
builder.add_edge("search", "audit")
builder.add_edge("audit", END)

oApp = builder.compile()

if __name__ == "__main__":
    # 1. Mock a question
    test_input = {"sQuery": "What are the termination clauses?"}
    
    # 2. Run the graph
    print("Testing Graph...")
    result = oApp.invoke(test_input)
    
    # 3. Check results
    print("\n--- CONTEXT FOUND ---")
    print(result["sContext"][:200] + "...") # print first 200 chars
    
    print("\n--- AI ANALYSIS ---")
    print(result["sResult"])