import reflex as rx
from FindSeoul.chatpage import chat_style as st
from FindSeoul.chatpage.chat_state import ChatState

#1. 상단바
def navbar() -> rx.Component :
    return rx.flex(
        rx.image(src= "/logo.png", width = "10em"),
        width = "100%",
        max_width = "1000px",
        background_color = "#4ecca3",
        align="center",
        justify="center",
        height="auto",
        box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
    )

#2. question-answer 컴포넌트 
#(1). 첫번째 채팅
def introduction(answer: str) -> rx.Component:
    return rx.box(
        rx.hstack(
                rx.avatar(src="/reco_bot.jpg", width ="10%", height = "auto", variant="solid", radius="full", color_scheme="plum"),
                rx.text(answer, style=st.ANSWER_STYLE, text_align = "left"),
                justify="start",
                align="center",
            ),
        margin_y="1em",
    )

#(2). 이후 채팅
def qa(question: str, answer: str) -> rx.Component:
    return rx.box(
        rx.hstack(
            rx.text(question, style=st.QUESTION_STYLE, text_align = "right"),
            rx.avatar(src="/human_imag.png", width ="10%", height = "auto", variant="solid", radius="full", color_scheme="plum"),
            justify="end",
            align="center",
        ),
        rx.hstack(
                rx.avatar(src="/reco_bot.jpg", width ="10%", height = "auto", variant="solid", radius="full", color_scheme="plum"),
                rx.text(answer, style=st.ANSWER_STYLE, text_align = "left"),
                justify="start",
                align="center",
            ),
        margin_y="1em",
    )

def chatting_history() -> rx.Component:
    return rx.box(
        introduction(answer=ChatState.first_ai_ment),
        rx.foreach(
            ChatState.chat_history,
            lambda messages: qa(messages[0], messages[1]),
        ),
        **st.CHAT_HISTORY_STYLE,
    )
    
#3. 채팅창 컴포넌트
#(1). 채팅 종료전
def chatting_action_bar() -> rx.Component:
    return rx.center(
        rx.form(
            rx.hstack(
                rx.input(
                    value=ChatState.question,
                    placeholder=ChatState.chat_language_dict[ChatState.lang]['action_bar_ment'],
                    on_change=ChatState.set_question,
                    style={"max_width": "780px",
                        "height": "50px",
                        "fontSize": "1.1rem",
                        "padding": "0 1rem",
                        "text_align": "left",
                        "flex": "1",  # Take available space
                        "margin_left": "10px",
                    },
                    disabled=ChatState.is_disabled,
                    id="question-input",
                ),
                rx.button(
                    rx.icon("send"),
                    type="submit",  # This makes it act as a form submit button
                    disabled=ChatState.is_disabled,
                    style={
                        "height": "50px",
                        "margin_left": "10px",
                    }
                ),
                width="100%",  # Make the hstack full width
                spacing="2",
                background_color = "mint",
            ),
            on_submit=ChatState.answering,
            width="100%",  # 폼의 너비를 100%로 설정
        ),
        width="100%"
    )

#(2). 채팅 종료후
def go_analysis_button() -> rx.Component:
    return rx.button(
            ChatState.chat_language_dict[ChatState.lang]['analysis_button_ment'],
            on_click=ChatState.go_to_recommendation,
            disabled=ChatState.going_recommend,
            color_scheme="mint",
            size="4",
            max_width="1000px",  # 입력 필드와 동일한 너비로 설정
            height="50px",
            margin_y="4",
            box_shadow="md",
            style={"fontSize": "1.5em"},  # 입력 필드와 동일한 폰트 크기
            width = "100%"
        )

def action_bar() -> rx.Component:
    return rx.cond(
            ChatState.chat_completed,
            go_analysis_button(),
            chatting_action_bar()
        )

#4. 로딩창
def loading_view() -> rx.Component :
    return  rx.flex(
                rx.spinner(size="2", color="white"),
                position="fixed",
                top=0,
                left=0,
                width="100vw",
                height="100vh",
                bg="rgba(0, 0, 0, 0.5)",  # 반투명 검은색
                align="center",
                justify="center",
        )
