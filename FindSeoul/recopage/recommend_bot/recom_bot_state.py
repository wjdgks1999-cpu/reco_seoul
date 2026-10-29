from typing import List, Annotated, TypedDict, Dict, Any
from typing_extensions import TypedDict
from langgraph.graph.message import add_messages

#1. 데이터 모델, 노드, 조건함수 불러오기
from FindSeoul.data_model import TravelInfo, UserPreferences, EvaluationSpot, RecommendationResponse, Search_List

class Recommend_Graph_State(TypedDict) :
    lang : str #사전
    messages : Annotated[list, add_messages] #사전
    travel_info : TravelInfo #사전
    user_preferences : UserPreferences
    search_queries: Search_List
    add_search_queries : Search_List
    search_results : List
    passed_spots : List
    dropped_spots : List
    rewrite_search_results : List
    info_evaluation_docs : List
    reco_results : RecommendationResponse
    final_results : List
    error : Dict[str, Any]
    error_handled : bool