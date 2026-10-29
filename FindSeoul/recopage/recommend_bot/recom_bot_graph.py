from langgraph.graph import END, START, StateGraph
from langgraph.checkpoint.memory import MemorySaver
import os

from FindSeoul.recopage.recommend_bot.recom_bot_state import Recommend_Graph_State
from FindSeoul.recopage.recommend_bot.recom_bot_node import (scoring_agent, first_analysis_agent,
                                            add_analysis_agent, retrieval_node,
                                            evaluation_agent, rewrite_agent,
                                            rewrite_retrieval_node, recommendation_node,
                                            final_node,error_handling_node)
from FindSeoul.recopage.recommend_bot.recom_bot_node import (scoring_route, first_analysis_route, add_analysis_route,
                            retrieval_route, evaluation_route,
                            rewrite_retrieval_route, rewrite_agent_route,
                            recommendation_route, final_route)

flow = StateGraph(Recommend_Graph_State)
flow.add_node("scoring_agent", scoring_agent)
flow.add_node('first_analysis_agent', first_analysis_agent)
flow.add_node('add_analysis_agent',add_analysis_agent)
flow.add_node('retrieval_node',retrieval_node)
flow.add_node('evaluation_agent', evaluation_agent)
flow.add_node('rewrite_agent', rewrite_agent)
flow.add_node('rewrite_retrieval_node', rewrite_retrieval_node)
flow.add_node('recommendation_node', recommendation_node)
flow.add_node('final_node', final_node)
flow.add_node('error_handling_node', error_handling_node)

flow.add_edge(START, "scoring_agent")
flow.add_conditional_edges(
    "scoring_agent",
    scoring_route,
    ["first_analysis_agent", "error_handling_node"]
)
flow.add_conditional_edges(
    "first_analysis_agent",
    first_analysis_route,
    ["retrieval_node", "error_handling_node"]  # 순서 수정
)
flow.add_conditional_edges(
    "retrieval_node",
    retrieval_route,
    ["evaluation_agent", "add_analysis_agent", "error_handling_node"]  # 순서 수정
)
flow.add_conditional_edges(
    "add_analysis_agent",
    add_analysis_route,
    ["retrieval_node", "error_handling_node"]  # 순서 수정
)
flow.add_conditional_edges(
    "evaluation_agent",
    evaluation_route,
    ["recommendation_node", "rewrite_agent", "error_handling_node"]  # 순서 수정
)
flow.add_conditional_edges(
    "rewrite_agent",
    rewrite_agent_route,
    ["rewrite_retrieval_node", "error_handling_node"]  # 순서 수정
)
flow.add_conditional_edges(
    "rewrite_retrieval_node",
    rewrite_retrieval_route,
    ["evaluation_agent", "rewrite_agent", "error_handling_node"]
)
flow.add_conditional_edges(
    "recommendation_node",
    recommendation_route,
    ['final_node', "error_handling_node"]  # 순서 수정
)
flow.add_conditional_edges(
    'final_node',
    final_route,
    [END, "error_handling_node"]
)
flow.add_edge("error_handling_node", END)

memory = MemorySaver()
graph = flow.compile(checkpointer=memory)