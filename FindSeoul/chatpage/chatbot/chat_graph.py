from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver

#1. 데이터 모델, 노드, 조건함수, 상태 불러오기
from FindSeoul.chatpage.chatbot.chat_graph_state import Chat_Graph_State
from FindSeoul.chatpage.chatbot.chat_node import request_collect_agent, collection_completed, error_handling_node
from FindSeoul.chatpage.chatbot.chat_node import request_collect_route

#2. 그래프 생성함수
flow = StateGraph(Chat_Graph_State)
flow.add_node("request_collect_agent", request_collect_agent)
flow.add_node("collection_completed", collection_completed)
flow.add_node("error_handling_node", error_handling_node)

flow.add_edge(START, "request_collect_agent")

flow.add_conditional_edges("request_collect_agent",
                            request_collect_route,
                            ["request_collect_agent", END, "collection_completed", "error_handling_node"])

flow.add_edge("collection_completed", END)