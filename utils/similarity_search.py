from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from langchain_community.vectorstores import FAISS
import os

os.environ['GOOGLE_API_KEY'] = os.getenv('GOOGLE_API_KEY')

def load_text_file(file_path):
    loader = TextLoader(file_path, encoding='utf-8')
    return loader.load()

def split_documents(documents, chunk_size=1000, chunk_overlap=200):
    text_splitter = RecursiveCharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=chunk_overlap)
    return text_splitter.split_documents(documents)

def embed_documents(splits):
    embeddings = GoogleGenerativeAIEmbeddings(model="models/embedding-001")
    vectorstore = FAISS.from_documents(splits, embeddings)
    return vectorstore

def similarity_search(vectorstore, query, k=3):
    similar_docs = vectorstore.similarity_search(query, k=k)
    return similar_docs

def create_text_file(similar_docs, file_path):
    similar_text = "\n".join([doc.page_content for doc in similar_docs])
    with open(file_path, 'w') as f:
        f.write(similar_text)

def read_result(similar_docs, file_path):
    similar_text = ""
    for idx, doc in enumerate(similar_docs):
        similar_text += "--------------------------------------------------------------------------------------------------\n"
        similar_text += f"Doc {idx+1}\n"
        similar_text += f"{doc.metadata.get('source')}\n"
        similar_text += doc.page_content + "\n\n"

    with open(file_path, 'w') as f:
        f.write(similar_text)