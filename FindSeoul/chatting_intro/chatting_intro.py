import reflex as rx
from FindSeoul.chatting_intro import chatting_intro_style as st
from FindSeoul.chatting_intro.chatting_intro_state import ChatIntro

from FindSeoul.chatting_intro.chatting_intro_component import navbar, avatar_ment, interest_buttons, go_to_chatting_button, loading_view

def joining_buttons() -> rx.Component :
    return rx.vstack(
        interest_buttons(),
        go_to_chatting_button(),
        align="center",
        justify="center"
    )

def showing_interest_buttons() -> rx.Component :
    return rx.match(
        ChatIntro.ment_process,
        ("final", joining_buttons())
    )

def loading_cond() -> rx.Component :
    return rx.cond(
        ChatIntro.is_loading,
        loading_view(),
        None
    )
    
@rx.page(route = "/chatting_intro", title="Intro", on_load=[ChatIntro.check_cookie])
def chatting_intro_page() -> rx.Component :
    return rx.flex(
        navbar(),
        loading_cond(),
        rx.container(
            avatar_ment(),
            rx.divider(),
            showing_interest_buttons(),
            **st.CONTAINER_STYLE
        ),
        **st.PAGE_FLEX_STYLE
    )