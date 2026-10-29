import reflex as rx
from typing import Dict

from FindSeoul.chatpage.chat_state import ChatState

class ChatErrorState(rx.State) :
    intro_cookie : str = rx.SessionStorage(name = "intro_cookie")
    chat_cookie : str = rx.SessionStorage(name = "chat_cookie")
    recommend_cookie : str = rx.SessionStorage(name = "recommend_cookie")
    
    error_result : Dict | None = None
    is_errored : bool = False
    
    gone_home : bool = False
    
    @rx.event
    async def check_auth_1(self) :
        getting_yn = await self.get_state(ChatState)
        self.is_errored = getting_yn.error_happened
        if self.is_errored :
            return ChatErrorState.call_error_info
        else :
            return rx.window_alert("정상적인 방법으로 접근해주세요.")

    @rx.event
    async def check_auth_2(self) :
        if not self.is_errored :
            return rx.redirect(path="/")
    
    @rx.event
    async def call_error_info(self) :
        getting_error = await self.get_state(ChatState)
        self.error_result = getting_error.error_result
        self.intro_cookie = ""
        self.chat_cookie = ""
        self.recommend_cookie = ""
    
    @rx.event
    def go_home(self) :
        self.gone_home = True
        return rx.redirect(path="/")

def go_to_home_button() -> rx.Component :
    return rx.button(
            "홈페이지로 가기(Go Homepage)",
            on_click=ChatErrorState.go_home,
            disabled=ChatErrorState.gone_home,
            color_scheme="mint",
            color = "white",
            font_size = "1.5em",
            height="50px",
            margin_y="4",
            box_shadow="md",
            style={"fontSize": "1.5em"},  # 입력 필드와 동일한 폰트 크기
            width = "30%"
        )

@rx.page("/chat_errors", on_load=[ChatErrorState.check_auth_1,ChatErrorState.check_auth_2])
def error_analysis() -> rx.Component :
    return rx.flex(
        rx.text(ChatErrorState.error_result.to_string(), text_align = "center"),
        go_to_home_button(),
        direction="column",
        align="center",
    )