from langgraph.graph import StateGraph,START,END
from langgraph.prebuilt import ToolNode

from agent.supervisor import supervisor_node,route_condition
from agent.general_assistant import general_assistant_node
from agent.task_assistant import task_manager_node
from agent.state import AgentState

builder : StateGraph | None = None

def build_graph():
    global builder
    print("Building state graph...")
    if builder is None :
        builder = StateGraph(AgentState)
        builder.add_node("supervisor",supervisor_node)
        builder.add_node("general",general_assistant_node)
        builder.add_node("task",task_manager_node)

        builder.add_edge(START,"supervisor")
        builder.add_conditional_edges("supervisor",route_condition,{
            "general_assistant" : "general",
            "task_manager_assistant" : "task"
        })
        builder.add_edge("general",END)
        builder.add_edge("task",END)
    return builder.compile()