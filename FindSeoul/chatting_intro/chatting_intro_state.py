import reflex as rx
from FindSeoul.homepage.home_state import HomeState
from FindSeoul.chatting_intro.chatting_intro_lang import chatting_intro_translation

from typing import Dict
import asyncio
import random
import string

def generate_thread_id(length=10):
    characters = string.ascii_letters + string.digits
    random_id = ''.join(random.choice(characters) for _ in range(length))
    return random_id

class ChatIntro(rx.State) :
    intro_cookie : str = rx.SessionStorage(name = "intro_cookie")
    chat_cookie : str = rx.SessionStorage(name = "chat_cookie")
    recommend_cookie : str = rx.SessionStorage(name = "recommend_cookie")
    
    #1. 이전(홈페이지) 상태 정보
    form_correct : bool = False
    travelinfo: Dict | None = None
    lang : str = "ko"
    
    #2. 동의여부
    agree_yn : bool = False
    
    #3. 관심사
    Interest_Hallyu : bool = False
    Interest_Traditional_Culture : bool = False
    Interest_Modern_Culture : bool = False
    Interest_Shopping : bool = False
    Outdoor_Activity_Preference : bool = False
    Indoor_Activity_Preference : bool = False
    Cultural_Experience_Preference : bool = False
    
    travel_purpose : list = []
    
    #4. 봇 멘트
    ment_list : dict[str, dict[str, str|list[str]]] = chatting_intro_translation
    now_ment : str
    ment_process : str
    
    #5. 다음 페이지에 넘길 변수
    thread_id : str | None = None
    
    #6. 상태변수
    is_loading : bool = False
    select_done : bool = False #관심사 선택 여부
    
    #0. 쿠키 상태 변경 및 변수 초기화
    @rx.event
    def check_cookie(self) : 
        # 채팅페이지에서 뒤로가기로 온 경우
        if self.chat_cookie == "done" :
            pass
        else :
            self.intro_cookie = "done"
            self.form_correct = False
            self.travelinfo = None
            self.agree_yn = False
            self.travel_purpose = []
            self.now_ment = ""
            self.ment_process = ""
            self.thread_id = ""
            self.is_loading = False
            self.select_done = False
            self.Interest_Hallyu= False
            self.Interest_Traditional_Culture= False
            self.Interest_Modern_Culture= False
            self.Interest_Shopping= False
            self.Outdoor_Activity_Preference= False
            self.Indoor_Activity_Preference= False
            self.Cultural_Experience_Preference= False
            return ChatIntro.call_home_info
            
    #1. 이전 상태정보를 불러오는 이벤트 핸들러
    @rx.event
    async def call_home_info(self) :
        home_info = await self.get_state(HomeState)
        self.form_correct = home_info.form_correct
        self.travelinfo = home_info.travelinfo
        self.lang = home_info.lang
        yield ChatIntro.check_auth_1
    
    #2. 사용자의 잘못된 접근을 방지하는 이벤트 핸들러
    @rx.event
    def check_auth_1(self) :
        if not self.form_correct :
            return [rx.window_alert("홈페이지에서 여행정보를 입력한 후, 채팅페이지에 진입해주세요."), ChatIntro.check_auth_2]
        else :
            return ChatIntro.start_mentioning
        
    @rx.event
    def check_auth_2(self) :
        if not self.form_correct :
            return rx.redirect(path="/")
    
    #3. 봇 멘트 이벤트 핸들러
    @rx.event
    async def start_mentioning(self) :
        self.now_ment = "" #초기화
        self.ment_process = "start"
        
        now_ment = self.ment_list[self.lang]['ment1']
        
        for chunk in now_ment :
            await asyncio.sleep(0.02)
            self.now_ment += chunk
            yield
        
        await asyncio.sleep(1)
        yield ChatIntro.second_mentioning
        
    @rx.event
    async def second_mentioning(self) :
        self.now_ment = "" 
        self.ment_process = "second"
        
        now_ment = self.ment_list[self.lang]['ment2']
        
        for chunk in now_ment :
            await asyncio.sleep(0.02)
            self.now_ment  += chunk
            yield
        
        await asyncio.sleep(1)
        yield ChatIntro.third_mentioning
        
    @rx.event
    async def third_mentioning(self) :
        self.now_ment = "" 
        self.ment_process = "third"
        
        now_ment = self.ment_list[self.lang]['ment3']
        
        for chunk in now_ment :
            await asyncio.sleep(0.02)
            self.now_ment  += chunk
            yield
        
        await asyncio.sleep(1)
        yield ChatIntro.fourth_mentioning

    @rx.event
    async def fourth_mentioning(self) :
        self.now_ment = "" 
        self.ment_process = "fourth"
        
        now_ment = self.ment_list[self.lang]['ment4']
        
        for chunk in now_ment :
            await asyncio.sleep(0.02)
            self.now_ment  += chunk
            yield
        
        await asyncio.sleep(1)
        yield ChatIntro.final_mentioning

    @rx.event
    async def final_mentioning(self) :
        self.now_ment = "" 
        self.ment_process = "final"
        
        now_ment = self.ment_list[self.lang]['ment5']
        
        for chunk in now_ment :
            await asyncio.sleep(0.02)
            self.now_ment  += chunk
            yield
    
    #3. 관심사 토글 메서드
    @rx.event
    def toggle_hallyu(self):
        self.Interest_Hallyu = not self.Interest_Hallyu

    @rx.event
    def toggle_traditional(self):
        self.Interest_Traditional_Culture = not self.Interest_Traditional_Culture
    @rx.event
    def toggle_modern(self):
        self.Interest_Modern_Culture = not self.Interest_Modern_Culture
    @rx.event
    def toggle_shopping(self):
        self.Interest_Shopping = not self.Interest_Shopping
    @rx.event
    def toggle_outdoor(self):
        self.Outdoor_Activity_Preference = not self.Outdoor_Activity_Preference
    @rx.event
    def toggle_indoor(self):
        self.Indoor_Activity_Preference = not self.Indoor_Activity_Preference
    @rx.event
    def toggle_cultural(self):
        self.Cultural_Experience_Preference = not self.Cultural_Experience_Preference
    
    #4. 채팅 시작 버튼
    @rx.event
    async def go_to_chatting(self) :
        self.is_loading = True
        yield ChatIntro.make_form
    
    @rx.event
    def make_form(self) :        
        if not any([
            self.Interest_Hallyu,
            self.Interest_Traditional_Culture,
            self.Interest_Modern_Culture,
            self.Interest_Shopping,
            self.Outdoor_Activity_Preference,
            self.Indoor_Activity_Preference,
            self.Cultural_Experience_Preference,
        ]):
            self.is_loading = False
            return rx.window_alert("한개 이상의 관심 여행 테마를 선택해주세요.")
        else :
            if self.lang == "ko" :
                if self.Interest_Hallyu :
                    self.travel_purpose.append("한류 여행")
                if self.Interest_Traditional_Culture :
                    self.travel_purpose.append("전통문화 여행")
                if self.Interest_Modern_Culture :
                    self.travel_purpose.append("현대문화 여행")
                if self.Interest_Shopping :
                    self.travel_purpose.append("쇼핑 여행")
                if self.Outdoor_Activity_Preference :
                    self.travel_purpose.append("아웃도어 활동 선호")
                if self.Indoor_Activity_Preference :
                    self.travel_purpose.append("인도어 활동 선호")
                if self.Cultural_Experience_Preference :
                    self.travel_purpose.append("문화체험 활동 선호")
            elif self.lang == "en":
                if self.Interest_Hallyu:
                    self.travel_purpose.append("Hallyu Tour")
                if self.Interest_Traditional_Culture:
                    self.travel_purpose.append("Traditional culture Tour")
                if self.Interest_Modern_Culture:
                    self.travel_purpose.append("Modern culture Tour")
                if self.Interest_Shopping:
                    self.travel_purpose.append("Shopping Tour")
                if self.Outdoor_Activity_Preference:
                    self.travel_purpose.append("Outdoor activities preference")
                if self.Indoor_Activity_Preference:
                    self.travel_purpose.append("Indoor activities preference")
                if self.Cultural_Experience_Preference:
                    self.travel_purpose.append("Cultural experience preference")
            
            self.travelinfo['travel_purpose'] = self.travel_purpose
            self.agree_yn = True
            self.thread_id = generate_thread_id()
            self.select_done = True
            return [rx.redirect("/chatting"),ChatIntro.set_is_loading(False)]
