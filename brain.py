import os
from dotenv import load_dotenv
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_community.vectorstores import Chroma

load_dotenv()

def create_db (sFile):
    # load pdf
    oLoad = PyPDFLoader(sFile)
    lDocs = oLoad.load()
    
    # split text
    oSplit = RecursiveCharacterTextSplitter(chunk_size=600, chunk_overlap=50)
    lChunks = oSplit.split_documents(lDocs)
    
    # use free embeddings
    sMod = "sentence-transformers/all-MiniLM-L6-v2"
    oEmbed = HuggingFaceEmbeddings(model_name=sMod)
    
    # save local db
    sDir = "./db_legal"
    oDB = Chroma.from_documents(lChunks, oEmbed, persist_directory=sDir)
    
    return oDB

if __name__ == "__main__":
    # check if test.pdf exists before running
    if os.path.exists("test.pdf"):
        create_db("test.pdf")
        print("Success: db_legal folder created.")
    else:
        print("Error: test.pdf not found in folder.")