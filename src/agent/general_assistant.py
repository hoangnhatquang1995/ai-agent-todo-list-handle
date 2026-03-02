from tools import tools

from agent.llm import llm_module
from agent.state import AgentState
from agent.prompts import general_system_prompt

llm_general_assistant = llm_module.bind_tools(tools=tools)

def general_assistant_node(state : AgentState):
    prompts = [general_system_prompt] + state["messages"]
    general_assistant_response = llm_general_assistant.invoke(prompts)
    print(f"General Assistant: Response: {general_assistant_response.content}")
    return {
        "messages" : [general_assistant_response]
    }

