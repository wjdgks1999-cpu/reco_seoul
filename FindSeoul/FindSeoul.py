import reflex as rx
from FindSeoul.homepage.homepage import homepage

from FindSeoul.chatting_intro.chatting_intro import chatting_intro_page

from FindSeoul.chatpage.chatpage import chatting_page
from FindSeoul.chaterrorpage.chaterrorpage import error_analysis

from FindSeoul.recopage.recopage import recommendation_page
from FindSeoul.recoerrorpage.recoerrorpage import reco_error_analysis

from FindSeoul.coockie_manage.coockie_manage import cookie_page

app = rx.App(
    theme=rx.theme(
        appearance="light",  # 항상 라이트 모드 사용
        has_background=True,
        radius="large",
        accent_color="teal",
        # 다른 테마 속성들...
    ),
)