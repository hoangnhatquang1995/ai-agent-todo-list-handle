from tools import tools

from agent.llm import llm_module
from agent.state import AgentState
from agent.prompts import tasks_system_prompt
from tools.tasks import tool_tasks
from langchain.messages import ToolMessage
llm_task_manager = llm_module.bind_tools(tools=tools)

def task_manager_node(state : AgentState):
    prompts = [tasks_system_prompt] + state["messages"]
    task_manager_response = llm_task_manager.invoke(prompts)
    tools_called = task_manager_response.tool_calls
    print(f"Task Manager Assistant: Response: {task_manager_response.content}")
    print(f"Task Manager Assistant: Tools called: {tools_called}")
    msg = [task_manager_response]
    if tools_called is not None and len(tools_called) > 0:
        for tool_call in tools_called:
            tool_name = tool_call["name"]
            tool_args = tool_call["args"]
            tool_id =  tool_call["id"]
            print(f"Tool Assistant : {tool_name} with arguments: {tool_args}")
            if tool_name in tool_tasks:
                tool = tool_tasks[tool_name]
                tool_result = tool.invoke(tool_args)
                print(f"Tool Assistant : Result of {tool_name} is: {tool_result}")
                msg = msg + [
                    ToolMessage(content=tool_result, 
                                name =tool_name,
                                tool_call_id = tool_id)
                ]
            else:
                print(f"Tool Assistant : Tool {tool_name} not found.")
    return {
        "messages" : msg
    }