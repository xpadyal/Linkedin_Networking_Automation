import os
import time
import pandas as pd
from pypdf import PdfReader
from langchain_community.embeddings.edenai import EdenAiEmbeddings
from langchain_openai import OpenAIEmbeddings
from langchain_pinecone import PineconeVectorStore
from pinecone import Pinecone, ServerlessSpec
from langchain_openai import OpenAI
from langchain.chains import RetrievalQA
from langchain_core.prompts import PromptTemplate

# Initialize Pinecone and LLM globally
pine=os.environ['PINECONE_API_KEY'] = "9957e36c-76fc-428c-a38d-e9dc9778ad56"
os.environ['OPENAI_API_KEY'] = "sk-R8iAuCMCEXUot-vOJ1nLDxDNScJ2hjUyEz7Cnemc5RT3BlbkFJPXYWC09KL4v3za8k6HnM6CtiLPinkOJUx7PDb8jq8A"
llm = OpenAI(temperature=0, max_tokens=250)
pc = Pinecone(api_key=pine)

# Function to process CSV file
def process_csv(csv_file_path, filtered_csv_file_path, chunk_size=10000):
    def process_chunk(chunk):
        return chunk.filter(items=['Company','Job Title','Job Description' ])
    
    filtered_chunks = []
    csv_chunks = pd.read_csv(csv_file_path, chunksize=chunk_size)
    
    for chunk in csv_chunks:
        processed_chunk = process_chunk(chunk)
        filtered_chunks.append(processed_chunk)
    
    filtered_data = pd.concat(filtered_chunks)
    filtered_data.to_csv(filtered_csv_file_path, index=False)
    
    return filtered_csv_file_path

# Function to convert filtered CSV to structured text file
def convert_csv_to_text(filtered_csv_file_path, output_text_file_path):
    df = pd.read_csv(filtered_csv_file_path)
    
    with open(output_text_file_path, 'w') as file:
        for i, row in df.iterrows():
            heading = f"##job posting: {i + 1}\n"
            sentence = f"{row['Company']} has a job opening for {row['Job Title']} and the job details are {row['Job Description']}.\n"
            file.write(heading)
            file.write(sentence)
            file.write("\n")
    
    return output_text_file_path

# Function to create Pinecone index and vector store
def create_pinecone_index_and_store(structured_text_file_path, index_name="job-listing", chunk_size=1000, chunk_overlap=50):
    existing_indexes = [index_info["name"] for index_info in pc.list_indexes()]
    
    if index_name not in existing_indexes:
        
    
        pc.create_index(
            name=index_name,
            dimension=1536,
            metric="cosine",
            spec=ServerlessSpec(cloud="aws", region="us-east-1")
        )
    
        while not pc.describe_index(index_name).status["ready"]:
            time.sleep(1)
    
    index = pc.Index(index_name)
    
    with open(structured_text_file_path, 'r') as file:
        text = file.read()
    
    textsplitter = [chunk for chunk in text.split("##") if chunk.strip()]
    # filterjobtxt = textsplitter.split_text(text)
    
    embeddings = OpenAIEmbeddings(model="text-embedding-3-large",)
    docsearch = PineconeVectorStore.from_texts(textsplitter, embeddings, index_name=index_name)
    time.sleep(10)
    return docsearch

# Function to extract skills from resume
def extract_skills_from_resume(resume_file_path):
    resumepdf = PdfReader(resume_file_path)
    resumetxt = resumepdf.pages[0].extract_text()
    print(resumetxt)
    prompt_template = PromptTemplate.from_template(
        "Give a name of technical skills separated by commas from the given resume {resume} and the total professional work experience of the user in years only "
    )
    query = prompt_template.format(resume=resumetxt)
    answer = llm.invoke(query)
    
    return answer

# Function to find relevant jobs based on skills
def find_relevant_jobs(skills, docsearch):
    knowledge = PineconeVectorStore.from_existing_index(
        index_name="job-listing",
        embedding= OpenAIEmbeddings(model="text-embedding-3-large",)
    )
    qa = RetrievalQA.from_chain_type(
        llm=llm,
        chain_type="stuff",
        retriever=knowledge.as_retriever(search_type="mmr", top_k=3)
    )
    
    prompt_template = PromptTemplate.from_template(
        "Give the list of most relevant job titles and companies based on their job description from the database which aligns with the following keywords and work experience {keywords} "
    )
    query = prompt_template.format(keywords=skills)
    resultq = qa.invoke(query)
    
    return resultq['result']
