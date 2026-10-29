import reflex as rx
from datetime import datetime
from typing import Dict
import json
from FindSeoul.homepage.home_lang import home_translation

class HomeState(rx.State):
    intro_cookie : str = rx.SessionStorage(name = "intro_cookie")
    chat_cookie : str = rx.SessionStorage(name = "chat_cookie")
    recommend_cookie : str = rx.SessionStorage(name = "recommend_cookie")
    
    #1. 언어상태 변수
    lang: str = "ko"
    
    #2. 현재 연도 변수
    current_year: int = datetime.now().year
    
    #3. 언어 변경
    translation : dict[str, dict[str, str|list[str]]] = home_translation
    
    #4. 서비스 스타트에 필요한 수집 변수
    sites_per_day : int
    today = datetime.now().strftime("%Y-%m-%d")
    check_in_date: str = today
    check_out_date: str = today
    User_info : str = ""
    Companions : list[dict[str,str]] = [{"relation": "", "age": ""}]
    
    #5. 상태 변수
    form_correct : bool = False #정해진 양식에 맞춰서 travelinfo가 입력되어 다음 페이지에 넘어가나?
    is_loading : bool = False #로딩창을 뛰울깝쇼?
    
    #6. 다음 페이지에 넘겨야하는 변수
    travelinfo : Dict | None = None
    
    @rx.var(cache=True)
    def duration(self) -> int :
    # 날짜 문자열을 datetime 객체로 변환
        check_in_dt = datetime.strptime(self.check_in_date, "%Y-%m-%d")
        check_out_dt = datetime.strptime(self.check_out_date, "%Y-%m-%d")
        # 두 날짜 사이의 차이 계산 (일 수)
        delta = check_out_dt - check_in_dt
        # 총 일수 반환 (1박 2일이면 2 반환)
        return delta.days + 1

    #0. 변수 초기화
    @rx.event
    def initialize(self) :
        self.sites_per_day = 0
        self.check_in_date = self.today
        self.check_out_date = self.today
        self.Companions = [{"relation": "", "age": ""}]
        self.form_correct = False
        self.travelinfo = None
        self.User_info = ""
        
        #세션 쿠키값 초기화
        self.intro_cookie = ""
        self.chat_cookie = ""
        self.recommend_cookie = ""
        
    #1. 변수 변경 이벤트 핸들러
    @rx.event
    def change_language(self, lang: str):
        """언어 변경 이벤트 핸들러."""
        self.lang = lang
    @rx.event
    def set_sites_per_day(self, sites_per_day) :
        sites_per_day = int(sites_per_day)
        self.sites_per_day = sites_per_day
    @rx.event
    def set_check_in_date(self, check_in_date: str):
        self.check_in_date = check_in_date
        # check_in_date가 변경되었고, check_out_date가 새 check_in_date보다 이전이거나 같은 경우
        if check_in_date and self.check_out_date and self.check_out_date <= check_in_date:
            # check_in_date 다음 날짜로 check_out_date 설정
            # datetime을 사용하여 날짜 계산
            check_in_dt = datetime.strptime(check_in_date, "%Y-%m-%d")
            new_check_out_date = check_in_dt
            self.check_out_date = new_check_out_date.strftime("%Y-%m-%d")
    @rx.event
    def add_companion(self):
        """동반자 추가 함수."""
        self.Companions.append({"relation": "", "age": ""})
    @rx.event
    def remove_companion(self, index: int):
        """동반자 삭제 함수."""
        if len(self.Companions) > 1:  # 최소 1명은 유지
            self.Companions.pop(index)
    @rx.event
    def update_companion(self, index: int, field: str, value: str):
        """동반자 정보 업데이트 함수."""
        if 0 <= index < len(self.Companions):
            Companions_copy = self.Companions.copy()
            Companions_copy[index][field] = value
            self.Companions = Companions_copy
            
    #2. 데이터 검수 이벤트 핸들러
    @rx.event
    async def find_travel_course(self) :
        self.is_loading = True
        yield HomeState.check_form
        
    @rx.event
    def check_form(self) :
        '''제출 폼의 유효성을 검사한다.
        만약 폼이 비정상이면 오류 메시지를 띄운다.
        폼이 정상이라면 채팅페이지로 이동한다.
        '''
        self.form_correct = False #초기화
        
        #1. 일일 방문 횟수 검사
        if self.sites_per_day <= 0 or self.sites_per_day > 3 :
            self.is_loading = False
            return rx.window_alert("가능한 일일 방문 관광지 희망 개수를 작성해주세요.")
        #2. 추천개수 체크
        if (self.duration * self.sites_per_day) > 9 :
            self.is_loading = False
            return rx.window_alert("[베타버전] 추천 관광지 개수(여행 기간 X 일일 방문 관광지 희망 개수)는 9개를 넘을 수 없습니다.")
        #3. user_info 검사
        if not self.User_info.strip() :
            self.is_loading = False
            return rx.window_alert("유저의 정보를 입력해주세요.")
        #4. 동행자 정보 검사
        #(1). Companions가 1개인 경우(단독여행을 생각해야함)
        if len(self.Companions) == 1 :
            companion = self.Companions[0]
            relation_filled = bool(companion["relation"])
            age_filled = bool(companion["age"])
            if (relation_filled and not age_filled) or (not relation_filled and age_filled) :
                self.is_loading = False
                return rx.window_alert("동행자의 정보를 완성해주세요.")
        else :
            for companion in self.Companions :
                if not companion["relation"] or not companion["age"]:
                    self.is_loading = False
                    return rx.window_alert("동행자의 정보를 완성해주세요.")
        self.form_correct = True #통과시 True로 변환
        return HomeState.make_travel_info

    @rx.event
    def make_travel_info(self) :
        '''
        검사가 통과되었을 경우, travelinfo를 정리하여 다음 페이지 State에 넘김
        '''
        #Mutable Proxy를 python 객체로 바꾼다.
        user = str(self.User_info) #유저의 나이대
        check_in_date = str(self.check_in_date) #여행시작일
        check_out_date = str(self.check_out_date) #여행종료일
        stay_duration = int(self.duration) #여행기간
        desired_daily_destinations = int(self.sites_per_day) #일일 방문희망

        # JSON 직렬화/역직렬화로 companions 완전 변환
        companions_json = json.dumps(self.Companions)
        companions = json.loads(companions_json)

        self.travelinfo = {
            "user": user,
            "companions": companions,
            "check_in_date" : check_in_date,
            "check_out_date" : check_out_date,
            "stay_duration": stay_duration,
            "desired_daily_destinations": desired_daily_destinations,
        }
        return [rx.redirect(path= "/chatting_intro", is_external=False), HomeState.set_is_loading(False)]