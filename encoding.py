from langchain_cohere.llms import Cohere
from langchain_cohere import CohereEmbeddings
from langchain.text_splitter import CharacterTextSplitter
from langchain.vectorstores import Pinecone
from langchain.chains.question_answering import load_qa_chain
from langchain.docstore.document import Document
from pinecone import Pinecone, ServerlessSpec
import time
import os
from langchain_pinecone import PineconeVectorStore
# Set Cohere API key
os.environ["COHERE_API_KEY"] = "KzzamuEHYNDNBc65wgnxklRcngZA1agQC8UxOVu6"
os.environ["PINECONE_API_KEY"] = "9957e36c-76fc-428c-a38d-e9dc9778ad56"
embeddings = CohereEmbeddings()

# Set Pinecone API key
# os.environ["PINECONE_API_KEY"] = "YOUR_PINECONE_API_KEY"  # Replace with your actual API key
pc = Pinecone(api_key=os.environ["PINECONE_API_KEY"])
llm = Cohere()

# Function to load text data from file
def load_text_data(file_path):
    with open(file_path, 'r') as file:
        data = file.readlines()
    return [line.strip() for line in data]

# Function to split text data into chunks
def split_text_data(text_data, chunk_size=512, overlap=50):
    splitter = CharacterTextSplitter(chunk_size=chunk_size, chunk_overlap=overlap)
    chunks = []
    for text in text_data:
        chunks.extend(splitter.split_text(text))
    return chunks

# Initialize Pinecone index
index_name = "linkedin-post"
existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]

if index_name in existing_indexes:
    print(f"Deleting existing index: {index_name}")
    pc.delete_index(index_name)

print(f"Creating index: {index_name}")
pc.create_index(
    name=index_name,
    dimension=4096,  # Ensure this matches the dimension of the embeddings used
    metric="cosine",
    spec=ServerlessSpec(cloud="aws", region="us-east-1"),
)
while not pc.describe_index(index_name).status["ready"]:
    print("Waiting for index to be ready...")
    time.sleep(1)

index = pc.Index(index_name)

# Load and split text data
text_data = load_text_data('collected_data.txt')
text_chunks = split_text_data(text_data)
print(f"Split text into {len(text_chunks)} chunks.")

# Convert text chunks to documents
documents = [Document(page_content=chunk) for chunk in text_chunks]

# Upsert documents into Pinecone
docsearch = PineconeVectorStore.from_documents(documents, embeddings, index_name=index_name)
print(f"Upserted {len(documents)} documents into Pinecone.")

# Save text data for reference
with open('text_data.txt', 'w') as file:
    for line in text_data:
        file.write(line + '\n')

chain = load_qa_chain(llm, chain_type="stuff")

def chatbot_response(query):
    docs = docsearch.similarity_search(query, k=3)
    answer = chain.run(input_documents=docs, question=query)
    return answer

# Example usage
query = "write all the post found"
insight = chatbot_response(query)
print(insight)
