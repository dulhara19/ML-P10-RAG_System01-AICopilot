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


def update_knowledge_base(file_path: str):
    # Load the file
    loader = TextLoader(file_path, encoding="utf-8")
    documents = loader.load()
    
    # Split into chunks
    chunks = splitter.split_documents(documents)
    
    for chunk in chunks:
        content = chunk.page_content
        embedding = embedding_model.embed_query(content)
        
        # Insert into MongoDB
        collection.insert_one({
            "content": content,
            "embedding": embedding
        })

    print(f"✅ {file_path} processed and added to DB.")

def search_from_db(query: str, top_k: int = 4):
    query_embedding = embedding_model.embed_query(query)

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": top_k,
                "index": "faq_vector_index"  # Must be pre-created on MongoDB
            }
        }
    ])
    

    return list(results)






from langchain_community.llms import Together
from langchain.schema import Document

# LLM Setup (Together or OpenAI or whatever you like)
import os
os.environ["TOGETHER_API_KEY"] = "your-api-key"

llm = Together(
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    temperature=0.7,
    max_tokens=512
)

def answer_query(query: str):
    results = search_from_db(query)

    sources = [Document(page_content=doc["content"]) for doc in results]

    # Very simple QA chain simulation
    combined_text = "\n\n".join(doc.page_content for doc in sources)
    prompt = f"Answer the following question based on the context:\n\n{combined_text}\n\nQuestion: {query}\nAnswer:"
    
    response = llm.invoke(prompt)
    return response
