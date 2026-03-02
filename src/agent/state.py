from pydantic import BaseModel,Field
from typing import Annotated, List,Dict,Any,TypedDict, Optional,Literal

from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages


class RouteDecision(BaseModel):
    select : Literal["general_assistant", "task_manager_assistant"] = Field(
        description= "Dựa vào input message, xác định xem nên chọn general assistant hay task manager assistant để xử lý."
    )
    reason : str = Field(
        description = "Lý do tại sao chọn. Cần giải thích đơn giản sumary về lựa chọn"
    )

class AgentState(TypedDict) :
    messages : Annotated[List[AnyMessage],add_messages]
    route_decision : Optional[RouteDecision]
    