from dotenv import load_dotenv #추후 삭제
load_dotenv('.env') #추후 삭제

from typing import  Optional
from pydantic import BaseModel, Field

from langgraph.graph import END
from langchain_core.messages import ToolMessage, AIMessage, HumanMessage
from langchain.prompts import (SystemMessagePromptTemplate, ChatPromptTemplate, MessagesPlaceholder)
from langchain_openai import ChatOpenAI

from FindSeoul.chatpage.chatbot.chat_graph_state import Chat_Graph_State

import os
openai_key = os.getenv('OPENAI_API_KEY', '')

#%% 1. 프롬프트 및 함수 정의
#(1). 템플릿 불러오기 및 프롬프트 구성
with open("FindSeoul/chatpage/chatbot/prompt/request_collect_prompt_v4.md", "r", encoding="utf-8") as f:
    request_collect_template = f.read()
request_collect_system = SystemMessagePromptTemplate.from_template(request_collect_template)

chatting_prompt = ChatPromptTemplate.from_messages([
    request_collect_system,
    MessagesPlaceholder(variable_name="message_history")
])

# (2).정보수집 완료 호출 툴 정의
class interest_info(BaseModel) :
    """Information of interest collected"""
    interest_big_category : str = Field(description="대주제")
    interest_small_category : str = Field(description="세부 관심 항목")
    interest_level: Optional[int] = Field(None, description="관심도 (1-5 척도)")

class conversaton_completed(BaseModel) : 
    """Invoke this tool when you're done collecting the necessary information."""
    interest_list : list[interest_info]
    
request_collect_tools = [conversaton_completed]

#%% 2. 노드 정의
#(1). request_collect_agent
async def request_collect_agent(state : Chat_Graph_State) :    
    try : 
        if state.get('language') == 'ko' :
            language = "한국어"
        elif state.get('language') == 'en' :
            language = "English"
        travel_info_load = state.get("travel_info")
        messages_history = state.get("messages", None)

        input_data = {
            "language": language,
            "companions_info": travel_info_load.companions,
            "travel_purpose": travel_info_load.travel_purpose,
            "user_info": travel_info_load.user,
            "message_history": messages_history
        }
        
        llm = ChatOpenAI(model="gpt-4o-mini", api_key=openai_key)
        llm_with_tools = llm.bind_tools(tools=request_collect_tools)
        chain = chatting_prompt | llm_with_tools
        
        response = await chain.ainvoke(input_data)
        
        return {"messages" : [response]}
        
    except Exception as e :
        return {
            "error": {
                "node": "request_collect_agent",
                "message": str(e),
                "type": type(e).__name__
            }
        }

#(2). 툴 신호를 받을 노드
async def collection_completed(state : Chat_Graph_State) :
    return {
        "messages": [
            ToolMessage(
                content="we've finished gathering your users' needs, and we're ready to start recommending destinations.",
                tool_call_id=state["messages"][-1].tool_calls[0]["id"],
            )
        ]
    }

#%% 3. 에러 핸들링 노드
def error_handling_node(state : Chat_Graph_State):
    # 에러 정보 추출
    error = state.get("error", {})
    error_type = error.get("type", "UnknownError")
    error_message = error.get("message", "알 수 없는 오류가 발생했습니다.")
    error_node = error.get("node", "unknown_node")
    
    # 에러 유형별 사용자 친화적 메시지 생성
    user_friendly_message = ""
    
    # 에러 유형에 따른 분류 및 메시지 생성
    if "BadRequestError" in error_type:
        if "context_length_exceeded" in error_message or "maximum context length" in error_message:
            user_friendly_message = "입력 또는 대화 내용이 너무 깁니다. 더 짧은 내용으로 다시 시도해주세요."
        elif "rate_limit" in error_message:
            user_friendly_message = "API 요청 한도를 초과했습니다. 잠시 후 다시 시도해주세요."
        elif "invalid content" in error_message.lower():
            user_friendly_message = "부적절한 내용이 감지되었습니다. 다른 방식으로 요청해주세요."
        else:
            user_friendly_message = "AI 모델 요청 처리 중 오류가 발생했습니다. 다른 방식으로 시도해보세요."
    
    elif "ValidationError" in error_type:
        # Pydantic 유효성 검증 오류
        if "missing" in error_message.lower():
            user_friendly_message = "필수 정보가 누락되었습니다. 모든 필요한 정보를 제공해주세요."
        elif "not a valid" in error_message.lower():
            user_friendly_message = "입력된 정보의 형식이 올바르지 않습니다. 다시 확인해주세요."
        else:
            user_friendly_message = "입력 데이터 검증에 실패했습니다. 입력 형식을 확인해주세요."
    
    elif "JSONDecodeError" in error_type:
        # JSON 파싱 오류
        user_friendly_message = "데이터 형식을 처리하는 중 오류가 발생했습니다. 시스템이 응답을 올바르게 해석하지 못했습니다."
    
    elif "OutputParserException" in error_type:
        # 출력 파싱 오류
        user_friendly_message = "AI의 응답을 적절한 형식으로 변환하는 데 실패했습니다. 다시 시도해주세요."
    
    elif "ConnectionError" in error_type:
        # 네트워크 연결 오류
        if "timeout" in error_message.lower():
            user_friendly_message = "서버 응답 시간이 초과되었습니다. 네트워크 상태를 확인하고 다시 시도해주세요."
        else:
            user_friendly_message = "네트워크 연결 중 오류가 발생했습니다. 인터넷 연결을 확인해주세요."
    elif "GraphRecursionError" in error_type:
        # LangGraph 그래프 순환 참조 오류
        user_friendly_message = "사용 횟수를 초과하였습니다. 관리자에게 문의하세요."

    elif "OpenAIError" in error_type:
        # LangGraph 그래프 순환 참조 오류
        user_friendly_message = "API 키 관련 오류가 발생했습니다. 관리자에게 문의하세요."
    
    else:
        # 그 외 모든 에러
        user_friendly_message = "알 수 없는 오류가 발생했습니다. [새로운 채팅]으로 다시 시도해주세요."
    
    # 노드별 추가 정보 제공
    node_specific_info = ""
    if error_node == "request_collect_agent":
        node_specific_info = "사용자 선호도 수집 중 오류가 발생했습니다."
    
    # 최종 에러 메시지 조합
    final_error_message = f"{node_specific_info} {user_friendly_message}"
    
    # 메시지 목록에 에러 메시지 추가
    add_error_message = AIMessage(content = final_error_message)
    
    return {
        "messages": [add_error_message],
        "error_handled": True,  # 에러 처리 완료 표시
    }

#%% 4. 상태정의 함수정의
def request_collect_route(state) :
    error = state.get("error", None)
    if error :
        return "error_handling_node"
    
    messages = state["messages"]
    if isinstance(messages[-1], AIMessage) and messages[-1].tool_calls :
        return "collection_completed"
    elif not isinstance(messages[-1], HumanMessage):
        return END
    return "request_collect_agent"