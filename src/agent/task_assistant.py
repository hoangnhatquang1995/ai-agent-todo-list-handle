from tools import tools
from llm import llm_module
from state import AgentState
from prompts import tasks_system_prompt

llm_task_manager = llm_module.bind_tools(tools=tools)

def task_manager_node(state : AgentState):
    prompts = [tasks_system_prompt] + state["messages"]
    task_manager_response = llm_task_manager.invoke(prompts)
    return {
        "messages" : [task_manager_response]
    }

