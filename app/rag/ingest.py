from pathlib import Path

from langchain_community.document_loaders import DirectoryLoader, TextLoader
from langchain_community.vectorstores import FAISS
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_huggingface import HuggingFaceEmbeddings

POLICY_DIR = Path("data/policies")
VECTOR_DB_DIR = Path("data/vector_store")

def build_policy_vector_store():
  loader = DirectoryLoader(
    str(POLICY_DIR),
    glob = "*.txt",
    loader_cls= TextLoader
  )
  
  documents= loader.load()
  
  splitter = RecursiveCharacterTextSplitter(
    chunk_size = 500,
    chunk_overlap = 100
  )
  
  chunks = splitter.split_documents(documents)
  
  embeddings = HuggingFaceEmbeddings(
    model_name = "sentence-transformers/all-MiniLM-L6-v2"
  )
  
  vector_store = FAISS.from_documents(chunks, embeddings)
  
  VECTOR_DB_DIR.mkdir(parents= True, exist_ok= True)
  vector_store.save_local(str(VECTOR_DB_DIR))
  
  print(f"loaded {len(documents)} documents")
  print(f"Created {len(chunks)} chunks")
  print(f"Saved Faiss vector store to {VECTOR_DB_DIR}")
  
  
if __name__ == "__main__" :
 build_policy_vector_store()