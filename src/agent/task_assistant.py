from tools import tools

from agent.llm import llm_module
from agent.state import AgentState
from agent.prompts import tasks_system_prompt

llm_task_manager = llm_module.bind_tools(tools=tools)

def task_manager_node(state : AgentState):
    prompts = [tasks_system_prompt] + state["messages"]
    task_manager_response = llm_task_manager.invoke(prompts)
    tools_called = task_manager_response.tool_calls
    print(f"Task Manager Assistant: Response: {task_manager_response.content}")
    print(f"Task Manager Assistant: Tools called: {tools_called}")
    if tools_called is not None and len(tools_called) > 0:
        for tool_call in tools_called:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            print(f"Tool Assistant : {tool_name} with arguments: {tool_args}")
    return {
        "messages" : [task_manager_response]
    }