from fastapi import Request,Response,FastAPI,Body,Header
from fastapi.exceptions import HTTPException

import vectorstore.chromadb as chromadb
from vectorstore.type import Task
from agent import talk_to_agent

app = FastAPI()


@app.get("/tasks")
def get_tasks():
    list = chromadb.vectorstore_get_list()
    return {"tasks": list}

@app.post("/tasks")
def add_task(task: dict = Body(...)):
    new_task = Task(
        time = task.get("time", ""),
        task_name= task.get("task_name", ""),
        description= task.get("description", "")
    )
    result = chromadb.vectorstore_add_task(new_task)
    if not result:
        raise HTTPException(status_code=400, detail="Failed to add task")
    return {"message": "Task added successfully"}

@app.post("/ask")
def ask(request: Request, body: dict = Body(...)):
    question = body.get("question", "")
    if not question:
        raise HTTPException(status_code=400, detail="Question is required")
    answer = talk_to_agent(question)
    return {
        "answer": answer['messages'][-1].content
    }