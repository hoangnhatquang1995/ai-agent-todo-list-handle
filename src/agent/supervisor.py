from state import AgentState,RouteDecision
from agent.llm import llm_module 
from tools import tools 
from prompts import supervisor_system_prompt

llm_supervisor = llm_module.with_structured_output(RouteDecision)

def supervisor_node(state : AgentState):
    prompts = [supervisor_system_prompt] + state["messages"]
    try:
        route_decision = llm_supervisor.invoke(prompts)
        print(f"Supervisor : Choice - {route_decision.select}, Reason - {route_decision.reason}")
    except Exception as e:
        route_decision = RouteDecision(
            select = "general_assistant",
            reason = f"Không thể đưa ra quyết định điều phối do lỗi: {str(e)}. Chọn general_assistant để xử lý yêu cầu."
        )
    return {
        "route_decision" : route_decision
    }

def route_condition(state: AgentState) -> str :
    if state["route_decision"] is None :
        return "general_assistant"
    return state["route_decision"].select

