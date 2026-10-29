from typing import Annotated, TypedDict, Dict, Any
from typing_extensions import TypedDict

from langgraph.graph.message import add_messages

#1. 데이터 모델, 노드, 조건함수 불러오기
from FindSeoul.data_model import TravelInfo

class Chat_Graph_State(TypedDict) :
    language : str
    messages : Annotated[list, add_messages]
    travel_info : TravelInfo
    error : Dict[str, Any]
    error_handled : bool