from langchain_community.document_loaders import TextLoader
from langchain_community.embeddings import HuggingFaceEmbeddings
from langchain_community.vectorstores import FAISS
from langchain_community.llms import Together
from langchain.chains import RetrievalQA
from langchain.text_splitter import CharacterTextSplitter

# Load your FAQs document
loader = TextLoader("faqs.txt", encoding="utf-8")
docs = loader.load()
# Split the document into smaller chunks for embedding
splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=50)
chunks = splitter.split_documents(docs)

# Check if splitting worked
print(f"Total chunks: {len(chunks)}")

from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS

# Initialize the embedding model
embed_model = HuggingFaceEmbeddings(model_name="all-MiniLM-L6-v2")

# Convert text chunks into embeddings and store them in FAISS
vectorstore = FAISS.from_documents(chunks, embed_model)

# Check if FAISS has been populated
print("FAISS vector store has been created.")


from langchain_community.llms import Together
import os

# Set your Together API key
os.environ["TOGETHER_API_KEY"] = "8b2035e3b8314dd8f68f02c652751e447eb94870e2f580ed1bb4955287318a14"

# Initialize the Together model (DeepSeek)
llm = Together(
    model="deepseek-ai/DeepSeek-R1-Distill-Llama-70B-free",  # You can change to any model available on Together
    temperature=0.7,  # Controls the randomness of responses
    max_tokens=512     # Controls the response length
)

# Connect RetrievalQA with FAISS (retriever) and the LLM (language model)
qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    retriever=vectorstore.as_retriever(),
    return_source_documents=True  # Optional, if you want to return the source text as well
)

# Test if LLM is working with a question
question = "how can i buy laptop in UK?"

response = qa_chain.invoke({"query": question})
print(response["result"])  # This is the answer from the model
 
for i, doc in enumerate(response["source_documents"]):
    print(f"\n--- Source {i+1} ---\n{doc.page_content}")
