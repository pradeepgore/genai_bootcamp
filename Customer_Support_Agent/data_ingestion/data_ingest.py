import sys
from langchain_astradb import AstraDBVectorStore
from dotenv import load_dotenv
import os
import pandas as pd
from data_ingestion.data_transform import data_conveter
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Explicitly load the .env file from the root directory
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '../utils/.env'))

GOOGLE_API_KEY=os.getenv("GOOGLE_API_KEY")
ASTRA_DB_API_ENDPOINT=os.getenv("ASTRA_DB_API_ENDPOINT")
ASTRA_DB_APPLICATION_TOKEN=os.getenv("ASTRA_DB_APPLICATION_TOKEN")
ASTRA_DB_KEYSPACE=os.getenv("ASTRA_DB_KEYSPACE")

# Check for missing environment variables
if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY is not set. Please check your .env file.")
if not ASTRA_DB_API_ENDPOINT:
    raise ValueError("ASTRA_DB_API_ENDPOINT is not set. Please check your .env file.")
if not ASTRA_DB_APPLICATION_TOKEN:
    raise ValueError("ASTRA_DB_APPLICATION_TOKEN is not set. Please check your .env file.")
if not ASTRA_DB_KEYSPACE:
    raise ValueError("ASTRA_DB_KEYSPACE is not set. Please check your .env file.")

os.environ["GOOGLE_API_KEY"]=GOOGLE_API_KEY
os.environ["ASTRA_DB_API_ENDPOINT"]=ASTRA_DB_API_ENDPOINT
os.environ["ASTRA_DB_APPLICATION_TOKEN"]=ASTRA_DB_APPLICATION_TOKEN
os.environ["ASTRA_DB_KEYSPACE"]=ASTRA_DB_KEYSPACE


class ingest_data:
    def __init__(self):
        print("data ingestion class has init...")
        self.embeddings = GoogleGenerativeAIEmbeddings(model="models/text-embedding-004")
        self.data_conveter=data_conveter()
        
    
    def data_ingestion(self,status):
        vstore=AstraDBVectorStore(
            embedding=self.embeddings,
            collection_name="chatbotecomm",
            api_endpoint=ASTRA_DB_API_ENDPOINT,
            token=ASTRA_DB_APPLICATION_TOKEN,
            namespace=ASTRA_DB_KEYSPACE,
        )
        storage=status
        
        # Ensure the method always returns a tuple
        if storage is None:
            docs = self.data_conveter.data_transformation()
            inserted_ids = vstore.add_documents(docs)
            print(inserted_ids)
        else:
            inserted_ids = []  # Define an empty list to avoid unpacking issues

        return vstore, inserted_ids
            

if __name__ == '__main__':
    ingest_data=ingest_data()
    #vstore=ingest_data.data_ingestion("Not none")
    vstore, inserted_ids = ingest_data.data_ingestion("Not none")
    print(f"\nInserted {len(inserted_ids)} documents.")
    results=vstore.similarity_search("can you tell me the low budget headphone")
    for res in results:
        print(f"{res.page_content} {res.metadata}")