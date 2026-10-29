import reflex as rx
from typing import List, Dict, Optional, Any
import json
import asyncio

from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableConfig
from FindSeoul.data_model import TravelInfo
from FindSeoul.recopage.recommend_bot.recom_bot_graph import graph
from FindSeoul.chatpage.chat_state import ChatState
from FindSeoul.recopage.reco_lang import reco_translation

def messages_to_dict(messages):
    if isinstance(messages[0], BaseMessage):
        return [message.dict() for message in messages]
    else :
        return messages

def preprocess_document(document) :
    reform_data = {
    'spot_name' : document.metadata['spot_name'],
    'spot_category' : document.metadata['category'],
    'spot_description' : document.metadata['descriptions']
    }
    return reform_data

class RecomState(rx.State) :
    intro_cookie : str = rx.SessionStorage(name = "intro_cookie")
    chat_cookie : str = rx.SessionStorage(name = "chat_cookie")
    recommend_cookie : str = rx.SessionStorage(name = "recommend_cookie")
    
    #1. 이전 페이지 상태의 변수들
    lang : str = "ko"
    thread_id : str | None = None
    travelinfo : Dict | None = None
    message_list : list | None = None
    chat_completed : bool = False

    #2. 그래프 실행 상태 변수
    complete_stage : str = "start_step" # match로 컴포넌트를 보일 것임.
    error_happened : bool = False
    
    #3. 그래프 실행 결과 변수
    user_preferences : List[Dict] | None = None
    search_results : List[Dict] | None = None
    passed_spots : List[Dict] | None = None
    dropped_spots : List[Dict] | None = None
    final_results : List[Dict] | None = None
    error_result : Optional[str]
    
    #4. 추천 관광지 선택 변수
    final_results_id : List[str] | None = None
    is_selected : List[bool] | None = None
    selected_items : List[Dict] | None = None

    #5. reco 봇의 멘트
    bot_mention : str

    #6. 영어기능 지원
    reco_language_dict : dict[str, dict[str, str]] = reco_translation

    #7. 최종결과 페이징
    select_results : str = "final_results"
    now_page_idx : int = 0
    page_range : list
    page_select : list[bool]

    #0. 쿠키 상태 체크 및 변수 초기화
    @rx.event
    def check_cookie(self) :
        #(1). 스스로 새로고침한 경우 : 초기화 후 홈페이지로 보내기
        if self.intro_cookie == "done" and self.chat_cookie == "done" and self.recommend_cookie == "done" :
            self.thread_id = None
            self.travelinfo = None
            self.message_list = None
            self.chat_completed = False
            self.complete_stage = "start_step"
            self.error_happened = False
            self.user_preferences = None
            self.search_results = None
            self.passed_spots = None
            self.dropped_spots = None
            self.final_results = None
            self.error_result = None
            self.final_results_id = None
            self.is_selected = None
            self.selected_items = None
            self.bot_mention = ""
            self.select_results = "final_results"
            self.now_page_idx = 0
            self.page_range = []
            self.page_select = []
            return [rx.window_alert("추천 엔진이 실행 중일때 새로고침을 하지 말아주세요."), rx.redirect(path = "/")]
        #(2). 제대로 넘어온 경우
        elif self.intro_cookie == "done" and self.chat_cookie == "done" and self.recommend_cookie == "" :
            self.recommend_cookie = "done"
            self.thread_id = None
            self.travelinfo = None
            self.message_list = None
            self.chat_completed = False
            self.complete_stage = "start_step"
            self.error_happened = False
            self.user_preferences = None
            self.search_results = None
            self.passed_spots = None
            self.dropped_spots = None
            self.final_results = None
            self.error_result = None
            self.final_results_id = None
            self.is_selected = None
            self.selected_items = None
            self.bot_mention = ""
            self.select_results = "final_results"
            self.now_page_idx = 0
            self.page_range = []
            self.page_select = []
            return RecomState.check_auth_1
        #(3). 그 외의 경우(홈페이지 이관 후 넘어오는 경우, intro page에서 넘어오는 경우 등등)
        else :
            self.thread_id = None
            self.travelinfo = None
            self.message_list = None
            self.chat_completed = False
            self.complete_stage = "start_step"
            self.error_happened = False
            self.user_preferences = None
            self.search_results = None
            self.passed_spots = None
            self.dropped_spots = None
            self.final_results = None
            self.error_result = None
            self.final_results_id = None
            self.is_selected = None
            self.selected_items = None
            self.bot_mention = ""
            self.select_results = "final_results"
            self.now_page_idx = 0
            self.page_range = []
            self.page_select = []
            return [rx.window_alert("올바른 경로로 진입해주세요."), rx.redirect(path="/")]
        
    #1. check_auth & get previous state
    #(1). 페이지 진입 검수
    @rx.event
    async def check_auth_1(self) :
        getting_yn = await self.get_state(ChatState)
        self.chat_completed = getting_yn.chat_completed
        if self.chat_completed :
            return RecomState.call_messages_list
        else :
            return [rx.window_alert("채팅을 완료한 후 진입해주세요."), RecomState.check_auth_2]
    @rx.event
    async def check_auth_2(self) :
        if not self.chat_completed :
            return rx.redirect(path="/")

    #(2). 페이지 상태 불러오기
    @rx.event
    async def call_messages_list(self) :
        getting_item = await self.get_state(ChatState)
        self.lang = getting_item.lang
        self.message_list = getting_item.message_list
        self.travelinfo = getting_item.travelinfo
        self.thread_id = getting_item.thread_id
        return  RecomState.make_recommend

    #2. 그래프 실행(나중에 변경할 것)
    @rx.event
    async def make_recommend(self) : 
        #[중요] Reflex의 State 변수는 Mutable Proxy 객체임. 이를 입력값으로 넣기 전 꼭!!! Python 일반 객체로 변환할것(JSON 직렬화/역직렬화)
        lang = str(self.lang)
        
        message_list = messages_to_dict(self.message_list)
        messages_json = json.dumps(message_list)
        messages_list_clean = json.loads(messages_json)
        
        travel_info_json = json.dumps(self.travelinfo)
        travel_info_clean = json.loads(travel_info_json)
        
        #thread_id 설정
        config = RunnableConfig(recursion_limit=15, configurable={"thread_id": self.thread_id})

        #1. complete_stage = "start_step"
        self.complete_stage = "start_step" 
        self.bot_mention = ""
        yield
        now_bot_mention = self.reco_language_dict[self.lang]['start_ment']
        for chunk_msg in now_bot_mention :
            await asyncio.sleep(0.05)
            self.bot_mention += chunk_msg
            yield
        try :
            async for event in graph.astream({"lang": lang, "messages" : messages_list_clean,
                                              "travel_info" : TravelInfo(**travel_info_clean)},
                                             config=config,
                                             stream_mode="updates") :
                if list(event.keys())[0] == "scoring_agent" :
                    retry_count = 0
                    max_retries = 10
                    while not self.user_preferences and retry_count <= max_retries :
                        await asyncio.sleep(0.2)
                        state_key_list = list(graph.get_state(config= config).values.keys())
                        retry_count += 1
                        if "user_preferences" in state_key_list :
                            scoring_result = [item.model_dump() for item in graph.get_state(config).values['user_preferences'].preferences]
                            self.user_preferences = scoring_result
                            yield
                        
                            self.complete_stage = "user_preferences_step"
                            self.bot_mention = ""
                            yield
                            now_bot_mention = self.reco_language_dict[self.lang]['user_preferences_ment']
                            for chunk_msg in now_bot_mention :
                                await asyncio.sleep(0.05)
                                self.bot_mention += chunk_msg
                                yield
                if list(event.keys())[0] == "retrieval_node" :
                    retry_count = 0
                    max_retries = 10 
                    while not self.search_results and retry_count <= max_retries :
                        await asyncio.sleep(0.2)
                        state_key_list = list(graph.get_state(config= config).values.keys())
                        retry_count += 1
                        if 'search_results' in state_key_list :
                            self.search_results = [preprocess_document(documents) for documents in graph.get_state(config).values['search_results']]
                            yield
                    
                            self.complete_stage = "search_results_step"
                            self.bot_mention = ""
                            yield
                            now_bot_mention = self.reco_language_dict[self.lang]["search_results_ment"]
                            for chunk_msg in now_bot_mention :
                                await asyncio.sleep(0.05)
                                self.bot_mention += chunk_msg
                                yield
                if list(event.keys())[0] == "add_analysis_agent" :
                    self.bot_mention = ""
                    yield
                    now_bot_mention = self.reco_language_dict[self.lang]['add_analysis_ment']
                    for chunk_msg in now_bot_mention :
                        await asyncio.sleep(0.05)
                        self.bot_mention += chunk_msg
                        yield
                if list(event.keys())[0] == "evaluation_agent" :
                    retry_count = 0
                    max_retries = 10 
                    while not (self.passed_spots is not None or self.dropped_spots is not None) and retry_count <= max_retries :
                        await asyncio.sleep(0.2)
                        passed_spots = graph.get_state(config).values.get('passed_spots', None)
                        dropped_spots = graph.get_state(config).values.get('dropped_spots', None)
                        retry_count += 1
                        if passed_spots is not None or dropped_spots is not None:
                            passed_spots_list = [item.model_dump() for item in passed_spots]
                            self.passed_spots = passed_spots_list
                            dropped_spots_list = [item.model_dump() for item in dropped_spots]
                            self.dropped_spots = dropped_spots_list
                            yield
                    
                            self.complete_stage = "evaluation_step"
                            self.bot_mention = ""
                            yield
                            now_bot_mention = self.reco_language_dict[self.lang]["evaluation_ment"]
                            for chunk_msg in now_bot_mention :
                                await asyncio.sleep(0.05)
                                self.bot_mention += chunk_msg
                                yield
                if list(event.keys())[0] == "rewrite_agent" :
                    self.bot_mention = ""
                    yield
                    now_bot_mention = self.reco_language_dict[self.lang]['add_analysis_ment']
                    for chunk_msg in now_bot_mention :
                        await asyncio.sleep(0.05)
                        self.bot_mention += chunk_msg
                        yield
                if list(event.keys())[0] == "recommendation_node" :
                    self.bot_mention = ""
                    yield
                    now_bot_mention = self.reco_language_dict[self.lang]['recommendation_ment']
                    for chunk_msg in now_bot_mention :
                        await asyncio.sleep(0.05)
                        self.bot_mention += chunk_msg
                        yield    
                if list(event.keys())[0] == "error_handling_node" :
                    self.error_happened = True
                    self.bot_mention = ""
                    yield
                    now_bot_mention = self.reco_language_dict[self.lang]['error_ment']
                    for chunk_msg in now_bot_mention :
                        await asyncio.sleep(0.05)
                        self.bot_mention += chunk_msg
                        yield
        except Exception as event_error:
            print(f"Error processing event {list(event.keys())[0]}: {event_error}")
            yield
        finally :
            yield RecomState.setting_end

    @rx.event       
    async def setting_end(self) :
        config = RunnableConfig(recursion_limit=15, configurable={"thread_id": self.thread_id})
        
        if self.error_happened :
            retry_count = 0
            max_retries = 10 
            while not self.error_result and retry_count <= max_retries :
                await asyncio.sleep(0.2)
                get_error_message = graph.get_state(config=config).values.get('messages', None)
                error_messages = get_error_message[-1]
                if error_messages :
                    self.error_result = error_messages.content
                    return rx.redirect("/reco_errors")
        else :
            retry_count = 0
            max_retries = 10 
            while not self.final_results and retry_count <= max_retries :
                await asyncio.sleep(0.2)
                final_results = graph.get_state(config).values.get('final_results',None)
                retry_count += 1
                if final_results :
                    self.final_results = final_results
                    self.final_results_id = [item["id"] for item in self.final_results]
                    self.is_selected = [False] * len(self.final_results)
                    self.page_range = list(range(1,len(self.final_results)+1)) 
                    self.page_select = [True] + ([False] * (len(self.final_results) - 1))
                    return RecomState.last_bot_mention
    @rx.event
    async def last_bot_mention(self) :
        self.complete_stage = "end_step"
        self.bot_mention = ""
        yield
        now_bot_mention = self.reco_language_dict[self.lang]['end_ment']
        for chunk_msg in now_bot_mention :
            await asyncio.sleep(0.05)
            self.bot_mention += chunk_msg
            yield

    #3. 결과 선택 이벤트 핸들러
    @rx.event
    def select_prefer(self) :
        self.select_results = "user_prefer"
    
    @rx.event
    def select_search(self) :
        self.select_results = "searched"
    
    @rx.event
    def select_evaluation(self) :
        self.select_results = "evaluations"
    
    @rx.event
    def select_final_results(self) :
        self.select_results = "final_results"

    #4. 페이지 변경 이벤트 핸들러
    @rx.event
    def next_page_rendering(self, idx : int) :
        self.page_select[idx] = True
        self.page_select[self.now_page_idx] = False
        self.now_page_idx = idx

    #3. 관광지 선택 이벤트 핸들러
    @rx.event
    def selecting(self, idx:int) :
        if self.is_selected[idx] :
            self.is_selected[idx] = False
        else :
            self.is_selected[idx] = True

    #4. 스케쥴 시작 이벤트 핸들러
    @rx.event
    def start_schedule(self) :
        bool_list = self.is_selected
        id_list = self.final_results_id
        
        if sum(bool_list) < 2 :
            return rx.window_alert("최소한 2개 이상의 관광지를 선택해주세요.")
        
        selected_id = [id_list[i] for i in range(len(bool_list)) if bool_list[i]]
        self.selected_items = [item for item in self.final_results_id if item["id"] in selected_id]