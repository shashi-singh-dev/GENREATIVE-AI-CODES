from langchain_qdrant import QdrantVectorStore
from langchain_openai import OpenAIEmbeddings
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()
client = OpenAI()

# Embedding model
emb_mdl = OpenAIEmbeddings(
    model="text-embedding-3-small"
)

# Vector DB
vector_db = QdrantVectorStore.from_existing_collection(
    url="http://localhost:6333",
    collection_name="Datawarehouse_db",
    embedding=emb_mdl
)

print("💬 RAG Chat Started (type 'exit' to stop)\n")

while True:
    Query = input("> ")

    # Exit condition
    if Query.lower() in ["exit", "quit"]:
        print("👋 Exiting chat...")
        break

    # Search similar docs
    search_result = vector_db.similarity_search(query=Query)

    # Build context
    context = "\n\n\n".join([
        f"Page Content: {result.page_content}\n"
        f"Page Number: {result.metadata.get('page_label')}\n"
        f"File Location: {result.metadata.get('source')}"
        for result in search_result
    ])

    SYSTEM_PROMPT = f"""
    You are a helpful AI Assistant who answers user query based on the available context
    retrieved from a PDF file along with page contents and page number.
    You should only answer based on the given context and guide the user to correct page.

    Context:
    {context}
    """

    response = client.responses.create(
        model="gpt-4o-mini",
        input=[
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": Query}
        ]
    )

    print(f"\n🤖 {response.output_text}\n")