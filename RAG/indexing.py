import os
from openai import OpenAI
from dotenv import load_dotenv
from pathlib import Path
from langchain_community.document_loaders import PyPDFLoader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings
from langchain_qdrant import QdrantVectorStore


load_dotenv()
##reading the pdf
pdf_path = Path(__file__).parent / "database-data-warehousing-guide.pdf"
loader = PyPDFLoader(file_path=pdf_path)
docs= loader.load()

#chunking process
text_splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000, #char
    chunk_overlap=200 
)

split_docs = text_splitter.split_documents(documents=docs)

#vector embedding process
emb_mdl = OpenAIEmbeddings(
    # model="text_embedding-3-large"
    model="text-embedding-3-small"   # safer option

)

#using  emb_mdl create  embeddings of split_docs and store in db
vactor_store = QdrantVectorStore.from_documents(
    documents=split_docs,
    url = "http://localhost:6333",
    collection_name = "Datawarehouse_db",
    embedding=emb_mdl
)


# client = OpenAI()

# def ask_ai(question):

#     response = client.responses.create(
#         model="gpt-4.1",
#         input=question
#     )

#     return response.output[0].content[0].text.strip()


if __name__ == "__main__":
    # question = input("Ask something: ")
    
    # answer = ask_ai(question)
    
    # print("\nAI Response:\n", answer)
    # print("Doscs[0]",docs[5])
    print("indexing of document done")