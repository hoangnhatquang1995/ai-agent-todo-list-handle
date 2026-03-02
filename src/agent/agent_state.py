from pydantic import BaseModel,Field
from typing import Annotated, List,Dict,Any,TypedDict, Optional,Literal

from langchain.messages import AnyMessage
from langgraph.graph.message import add_messages


class RouteDecision(BaseModel):
    select : Literal["placeholder_agent_1", "placeholder_agent_2"] = Field(
        description= ""
    )

class AgentState(TypedDict) :
    messages : Annotated[List[AnyMessage],add_messages]

    