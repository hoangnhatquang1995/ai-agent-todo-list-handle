from tools import tools
from datetime import datetime

from agent.llm import llm_module
from agent.state import AgentState
from agent.prompts import tasks_system_prompt
from tools.tasks import tool_tasks
from langchain.messages import ToolMessage,SystemMessage

llm_task_manager = llm_module.bind_tools(tools=tools)

def task_manager_node(state : AgentState):
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    time_context = f"""\nTHÔNG TIN HỆ THỐNG: Thời gian hiện tại là {now}. 
    Hãy dùng mốc này để tính toán và tự động quy đổi mọi biểu thức thời gian (như 'sáng mai', 'tuần sau') sang định dạng 'YYYY-MM-DD HH:MM:SS' khi lưu vào biến time."""
    
    dynamic_system_prompt = [tasks_system_prompt] + [SystemMessage(content= time_context)]
    
    prompts = dynamic_system_prompt + state["messages"]
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