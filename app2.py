import pymongo
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter

# MongoDB Connection
client = pymongo.MongoClient("mongodb://localhost:27017/")  # or your MongoDB Atlas URI
db = client["faq_database"]
collection = db["faq_chunks"]

# Embedding model
embedding_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Text Splitter
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)


