import settings
import agent.embedding

from langchain_chroma import Chroma

vectorstore = Chroma(
    collection_name="agent-todo-list",
    embedding_function=agent.embedding.embeddings,
    persist_directory="./cache/chromadb"
)

def get_retriever(search_kwargs ={"k": 5}):
    return vectorstore.as_retriever(search_kwargs=search_kwargs)

