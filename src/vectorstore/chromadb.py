import settings
import agent.embedding
from .type import Task
from langchain_chroma import Chroma
from typing import List
vectorstore = Chroma(
    collection_name="agent-todo-list",
    embedding_function=agent.embedding.embeddings,
    persist_directory="./cache/chromadb"
)

def vectorstore_get_retriever(search_kwargs ={"k": 5}):
    return vectorstore.as_retriever(search_kwargs=search_kwargs)

def vectorstore_add_task(task : Task):
    page_content = f"Time: {task.time}\nTask Name: {task.task_name}\nDescription: {task.description}"
    metadata = {"time": task.time, "task_name": task.task_name, "description": task.description}
    vectorstore.add_texts(texts=[page_content],metadatas=[metadata] )
    return f"Task added successfully."

def vectorstore_remove_task(task: Task):
    search_query = f"Time: {task.time}\nTask Name: {task.task_name}\nDescription: {task.description}"
    docs = vectorstore.similarity_search(search_query, k=1)
    if not docs :
        return f"[1][Error] task {str(task)} not found"
    doc = docs[0]
    print(f"==> doc = {doc.to_json()}")
    item = vectorstore.get(
        where= {
            "$and" : [
                {"task_name" : doc.metadata.get("task_name")},
                {"time" : doc.metadata.get("time")}
            ]
        } # type: ignore
    )

    if item and len(item["ids"]) > 0:
        ids = item["ids"]
        print(f"Found [ids] = {ids}")
        vectorstore.delete(ids)
        return f"[0] Task {doc.metadata.get('task_name')} removed"
    else:
        return f"Task not found"
    
def vectorstore_find_task(task: Task):
    search_query = f"Time: {task.time}\nTask Name: {task.task_name}\nDescription: {task.description}"
    docs = vectorstore.similarity_search(search_query, k=1)
    if not docs :
        return None
    doc = docs[0]
    print(f"==> doc = {doc.to_json()}")
    return Task(
        time=doc.metadata.get("time"),
        task_name=doc.metadata.get("task_name"),
        description=doc.metadata.get("description")
    )
    
def vectorstore_get_list() -> List[Task]:
    docs = vectorstore.get()
    tasks = []
    if not docs or docs.get("metadatas") is None:
        return tasks
    for metadata in docs.get("metadatas", []):
        task = Task(
            time=metadata.get("time"),
            task_name=metadata.get("task_name"),
            description=metadata.get("description")
        )
        tasks.append(task)
    return tasks