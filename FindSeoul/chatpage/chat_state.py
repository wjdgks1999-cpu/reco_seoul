import reflex as rx
import json
from typing import Dict, Any

from FindSeoul.chatpage.chatbot.chat_graph import flow
from langchain_core.runnables import RunnableConfig
from langchain_core.messages import HumanMessage
from langchain.prompts import HumanMessagePromptTemplate, AIMessagePromptTemplate
from psycopg_pool import AsyncConnectionPool
from langgraph.checkpoint.postgres.aio import AsyncPostgresSaver
from FindSeoul.chatting_intro.chatting_intro_state import ChatIntro
from FindSeoul.data_model import TravelInfo
from FindSeoul.chatpage.chat_lang import chatting_translation

#1. ChatState 정의
class ChatState(rx.State) :
    intro_cookie : str = rx.SessionStorage(name = "intro_cookie")
    chat_cookie : str = rx.SessionStorage(name = "chat_cookie")
    recommend_cookie : str = rx.SessionStorage(name = "recommend_cookie")

    #1. 이전(홈페이지) 상태 정보
    form_correct : bool = False
    travelinfo : Dict | None = None
    thread_id : str | None = None
    lang : str = "ko"
    agree_yn : bool = False
    
    #2. 대화 및 대화내역 변수
    question : str
    answer : str
    chat_history : list[tuple[str,str]]
    
    #3. 프로세스 관리 변수
    is_loading : bool = False #AI 대답 상태
    chat_completed : bool = False #대화 종료 상태
    error_happened : bool = False #에러 발생 상태
    first_answer_yn : bool =  True #첫번째 답변 상태
    next_page_loading : bool = False #다음 페이지 넘어갈 때 로딩창
    going_recommend : bool = False #분석 시작하기 버튼을 눌렀는지 여부
    
    #4. 대화 결과 변수
    snapshot_state : dict[str, Any] #매턴 대화가 끝날때마다 최신 state.values 값을 저장
    message_list : list | None = None #대화 내역을 저장할 상태 변수
    error_result : Dict | None = None #에러 정보를 저장할 상태 변수

    #5. 영어기능 지원
    chat_language_dict : dict[str, dict[str, str]] = chatting_translation
    
    #6. 유저의 답변 제출을 막는 상태(True일 때 disabled가 됨)
    @rx.var
    def is_disabled(self) -> bool : #AI가 대답 중일때, 대화가 종료되었을때, 에러가 발생했을 때 사용자의 입력을 막음
        return self.is_loading or self.chat_completed or self.error_happened
    
    #7. 첫번째 AI 멘트
    @rx.var
    def first_ai_ment(self) -> str :
        if self.travelinfo : 
            travel_purpose = self.travelinfo.get('travel_purpose','')
            if self.lang == "ko" :
                return f"안녕하세요 유저님! 유저님께서 {travel_purpose}에 관심이 있다고 말씀해주셨는데, 더 정확한 추천을 위해 지금부터 관련 질문을 드려도 될까요?"
            elif self.lang == "en" :
                return f"Hello! You mentioned that you're interested in {travel_purpose}, can I ask you some related questions now to help me make more accurate recommendations?"
        else : 
            return "아직 채팅을 시작하지 않았어요."
    
    #0. 쿠키 상태 체크 및 변수 초기화화
    @rx.event
    def check_cookie(self) : 
        if self.intro_cookie == "done" and self.chat_cookie == "done" and self.recommend_cookie == "" :
            pass
        elif self.intro_cookie == "done" and self.chat_cookie == "done" and self.recommend_cookie == "done" :
            pass
        elif self.intro_cookie == "done" and self.chat_cookie == "" :
            self.chat_cookie = "done"
            self.form_correct = False
            self.travelinfo = None
            self.thread_id = None
            self.agree_yn = False
            self.question = ""
            self.answer = ""
            self.chat_history = []
            self.is_loading = False
            self.chat_completed = False
            self.error_happened = False
            self.first_answer_yn = True
            self.next_page_loading = False
            self.snapshot_state = {}
            self.message_list = None
            self.error_result = None
            self.going_recommend = False
            return ChatState.call_travel_info
        else :
            self.chat_cookie = "done"
            self.form_correct = False
            self.travelinfo = None
            self.thread_id = None
            self.agree_yn = False
            self.question = ""
            self.answer = ""
            self.chat_history = []
            self.is_loading = False
            self.chat_completed = False
            self.error_happened = False
            self.first_answer_yn = True
            self.next_page_loading = False
            self.snapshot_state = {}
            self.message_list = None
            self.error_result = None
            self.going_recommend = False
            return [rx.window_alert("올바른 경로로 채팅페이지에 진입해주세요."), rx.redirect(path="/")]
        
    #1. 이전(홈페이지) 상태 정보를 불러오는 이벤트 핸들러(페이지 로딩시 실행)
    @rx.event
    async def call_travel_info(self) :
        getting_basic_info = await self.get_state(ChatIntro)
        self.form_correct = getting_basic_info.form_correct
        self.travelinfo = getting_basic_info.travelinfo
        self.thread_id = getting_basic_info.thread_id
        self.lang = getting_basic_info.lang
        self.agree_yn = getting_basic_info.agree_yn
        return ChatState.check_auth_1

    #2. 사용자의 잘못된 접근을 방지하는 이벤트 핸들러(페이지 로딩시 실행)
    @rx.event
    def check_auth_1(self) :
        if not self.agree_yn :
            return [rx.window_alert("올바른 경로로 채팅페이지에 진입해주세요."), ChatState.check_auth_2]
    @rx.event
    def check_auth_2(self) :
        if not self.agree_yn :
            return rx.redirect(path="/")

    #3. 대화를 진행하는 함수 : 사용자가 대답 또는 질문을 입력시 실행됨
    @rx.event
    async def answering(self) :
        #로딩 설정
        self.is_loading = True
        
        # 챗봇의 대답을 담을 answer 변수 초기화
        self.answer = ""
        self.chat_history.append((self.question, self.answer))
        
        # 답변을 내보내기 전에 질문자의 답변을 액션바에서 삭제한다.
        question_copy = self.question #복사해놓기
        self.question = ""
        yield
        
        #입력정보를 Mutable Proxy 객체에서 Python 일반 객체로 변환
        travel_info_json = json.dumps(self.travelinfo)
        travel_info_clean = json.loads(travel_info_json)
        lang_clean = str(self.lang)
        
        #DB 연결 정보 불러오기
        DB_URI = 'postgresql://jhyoon:rhdrka1234!@svc.sel4.cloudtype.app:30772/postgres?sslmode=disable'
        connection_kwargs = {
            "autocommit": True,
            "prepare_threshold": 0,
        }
        
        try : 
            async with AsyncConnectionPool(conninfo=DB_URI, max_size=5, kwargs= connection_kwargs) as pool:
                #(1). 체크포인트 및 graph 설정
                checkpointer = AsyncPostgresSaver(pool)
                using_graph = flow.compile(checkpointer=checkpointer)
                config = RunnableConfig(configurable={"thread_id": self.thread_id})
                
                #(2). 유저 답변 설정
                query_list = [HumanMessage(content=question_copy)]
                if self.first_answer_yn :
                    if lang_clean == "ko" :
                        first_human = HumanMessagePromptTemplate.from_template("안녕. 서울여행 관광지 추천을 받으려고 왔어.")
                        first_ai = AIMessagePromptTemplate.from_template("유저님께서 {travel_purpose}에 관심이 있다고 말씀해주셨는데, 더 정확한 추천을 위해 지금부터 관련 질문을 드려도 될까요?")

                        input_query_list = [
                            first_human.format_messages()[0],
                            first_ai.format_messages(travel_purpose = travel_info_clean['travel_purpose'])[0],
                        ] + query_list
                        
                        self.first_answer_yn = False
                        yield
                    elif lang_clean == "en" :
                        first_human = HumanMessagePromptTemplate.from_template("Hello. I'm looking for recommendations for tourist attractions in Seoul.")
                        first_ai = AIMessagePromptTemplate.from_template("You mentioned that you're interested in {travel_purpose}, can I ask you some related questions now to help me make more accurate recommendations?")
                        input_query_list = [
                            first_human.format_messages()[0],
                            first_ai.format_messages(travel_purpose = travel_info_clean['travel_purpose'])[0],
                        ] + query_list
                        self.first_answer_yn = False
                        yield
                else :
                    input_query_list = query_list
                    yield
                
                #(3). 그래프 실행
                try : 
                    async for chunk_msg, metadata in using_graph.astream({"messages" : input_query_list,
                                                                        "language":lang_clean,
                                                                        "travel_info": TravelInfo(**travel_info_clean)},
                                                                        config=config,
                                                                        stream_mode="messages") :
                        if metadata["langgraph_node"] == "request_collect_agent" and chunk_msg.content :
                            self.answer += chunk_msg.content
                            self.chat_history[-1] = (question_copy, self.answer)
                            yield
                        elif metadata["langgraph_node"] == "request_collect_agent" and hasattr(chunk_msg, "tool_calls") and chunk_msg.tool_calls:
                            end_messages = self.chat_language_dict[self.lang]['end_message']
                            self.answer = end_messages
                            self.chat_history[-1] = (question_copy, self.answer)
                            self.chat_completed = True
                            yield
                        elif metadata["langgraph_node"] == "error_handling_node" :
                            error_message = self.chat_language_dict[self.lang]['error_message']
                            self.answer = error_message
                            self.chat_history[-1] = (question_copy, self.answer)
                            self.chat_completed = False
                            self.error_happened = True
                            yield
                except Exception as event_error :
                    print(f"Error processing event {metadata['langgraph_node']}: {event_error}")
                    error_message = self.chat_language_dict[self.lang]['error_message']
                    self.answer = error_message
                    self.chat_history[-1] = (question_copy, self.answer)
                    self.chat_completed = False
                    self.error_happened = True
                    yield
                finally :
                    #(4). snapshot 저장
                    snapshot_state = await checkpointer.aget(config)
                    self.snapshot_state = snapshot_state['channel_values']
                    yield                      
        except Exception as event_error :
            print(f"Error processing event: {event_error}")
            yield
        finally :
            self.is_loading = False
            yield ChatState.set_focus_or_error

    @rx.event
    def set_focus_or_error(self):
        if self.error_happened and not self.chat_completed :
            error = self.snapshot_state.get('error', None)
            self.error_result = error
            return rx.redirect("/chat_errors")
        elif not self.chat_completed :
            return rx.set_focus("question-input")

    @rx.event
    def go_to_recommendation(self) :
        self.next_page_loading = True
        self.message_list = self.snapshot_state['messages']
        self.going_recommend = True
        return [rx.redirect("/recommend"), ChatState.set_next_page_loading(False)]