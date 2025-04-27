import pymongo
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import CharacterTextSplitter
from dotenv import load_dotenv
import os
# Load environment variables from .env file
load_dotenv()

# Access the variables
together_api_key = os.getenv("TOGETHER_API_KEY")
mongo_uri = os.getenv("MONGO_URI")

# MongoDB Connection
client = pymongo.MongoClient(mongo_uri)  # or your MongoDB Atlas URI
db = client["financialdata"]
collection = db["faqs"]

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

# Function to read the contents of the text file (book1.txt)
def read_text_file(file_path):
    with open(file_path, "r", encoding="utf-8") as file:
        return file.read()

# Example function to chunk large input into smaller pieces
def chunk_input(text, max_tokens=8193):
    # Break the text into chunks of a reasonable size (e.g., 4000 tokens)
    chunk_size = max_tokens // 2  # Leave some room for the response
    chunks = [text[i:i + chunk_size] for i in range(0, len(text), chunk_size)]
    return chunks

# Load your book text (book1.txt)
file_path = "book1.txt"
large_text = read_text_file(file_path)

# Chunk the large text into smaller pieces
chunks = chunk_input(large_text)

# to convert pdf to txt in oreder to load it to the knowledge base    

# import fitz  # PyMuPDF

# def convert_pdf_to_txt(pdf_path: str, txt_path: str):
#     doc = fitz.open(pdf_path)
#     text = ""
#     for page in doc:
#         text += page.get_text()

#     with open(txt_path, "w", encoding="utf-8") as f:
#         f.write(text)

#     print(f"✅ PDF converted and saved to: {txt_path}")



# import os
# print(os.getcwd())  # shows your current working directory
# pdf_path = os.path.join("pdf_src", "mfl.pdf")
# txt_path = "book1.txt"

# convert_pdf_to_txt(pdf_path, txt_path)


update_knowledge_base("faqs2.txt")  # Call this function to update the knowledge base    

def search_from_db(query: str, top_k: int = 4):
    query_embedding = embedding_model.embed_query(query)

    results = collection.aggregate([
        {
            "$vectorSearch": {
                "queryVector": query_embedding,
                "path": "embedding",
                "numCandidates": 100,
                "limit": top_k,
                "index": "vector_index"  # Must be pre-created on MongoDB
            }
        }
    ])
    
    return list(results)


from langchain_community.llms import Together
from langchain.schema import Document

# LLM Setup (Together or OpenAI or whatever you like)
import os
os.environ["TOGETHER_API_KEY"] = together_api_key

llm = Together(
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",
    temperature=0.5,
    max_tokens=512
)

def answer_query(query: str):
    results = search_from_db(query)

    sources = [Document(page_content=doc["content"]) for doc in results]

    # Very simple QA chain simulation
    combined_text = "\n\n".join(doc.page_content for doc in sources)

    prompt = f"base on the contxt {sources} give answer to the question :{query}"
    
    response = llm.invoke(prompt)
    return response

# lets try it out :)
response = answer_query("how can i get rich fast? what are the tips and mindset do i need to have?")
print(response)

