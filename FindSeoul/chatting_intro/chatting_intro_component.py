import reflex as rx
from FindSeoul.chatting_intro.chatting_intro_state import ChatIntro
from FindSeoul.chatting_intro import chatting_intro_style as st

#1. 상단바
def navbar() -> rx.Component :
    return rx.flex(
        rx.image(src= "/logo.png", width = "10em"),
        **st.NAVBAR_STYLE
    )

#2. 아바타 및 소개
def avatar_ment() -> rx.Component :
    return  rx.hstack(
                rx.avatar(src="/reco_bot.jpg",
                        height="auto",
                        width="20%",
                        margin_left = "2rem",
                        variant = "solid",
                        color_scheme = "plum",
                        radius = "full"),
                rx.flex(
                    rx.text(
                        ChatIntro.now_ment,
                        **st.MESSAGE_STYLE,
                        text_align="left",
                        font_size="clamp(14px, 2vw, 18px)",
                    ),
                    align="start",
                    justify="start",
                    # 여백 조정
                    border_radius="8px",
                    padding="0.5em",
                    margin_left="0.5em",
                    width = "70%"
                ),
                justify="center",
                align = "start",
                height = "auto",
                width = "100%",
                margin_top = "16px",
                margin_bottom = "16px",
            )

#3. 관심사 선택 버튼
def make_button(label: str, state_var: rx.Var[bool], toggle_fn):
    # 골드 톤과 그림자를 활용한 럭셔리 스타일
    gold = '#D4AF37'
    shadow = '0 8px 15px rgba(212, 175, 55, 0.5)'
    return rx.cond(
        state_var,
        # 선택된 상태: 골드 그라데이션 배경 + 화이트 텍스트
        rx.button(
            label,
            on_click=toggle_fn,
            bg_gradient='linear(to-r, #FFD700, #D4AF37)',
            color='white',
            font_size='xl',
            font_weight='semibold',
            border_radius='2xl',
            min_w='6rem',
            min_h='2.5rem',
            box_shadow=shadow,
            _hover={
                'transform': 'scale(1.05)',
                'box_shadow': '0 10px 20px rgba(212, 175, 55, 0.7)',
            },
            transition='all 0.2s ease-in-out',
            left_icon='check',
            width = "20%",
            height = "clamp(40px, 20vh, 60px)"
        ),
        # 미선택 상태: 골드 테두리 + 투명 배경
        rx.button(
            label,
            on_click=toggle_fn,
            bg='transparent',
            color=gold,
            font_size='xl',
            font_weight='medium',
            border=f'2px solid {gold}',
            border_radius='2xl',
            min_w='6rem',
            min_h='2.5rem',
            _hover={
                'bg': 'rgba(212,175,55,0.1)',
                'transform': 'scale(1.05)',
            },
            transition='all 0.2s ease-in-out',
            width = "20%",
            height = "clamp(40px, 20vh, 60px)"
        ),
    )

def interest_buttons() -> rx.Component :
    return rx.flex(
        make_button(ChatIntro.ment_list[ChatIntro.lang]['button_text'][0],
                    ChatIntro.Interest_Hallyu, ChatIntro.toggle_hallyu),
        make_button(ChatIntro.ment_list[ChatIntro.lang]['button_text'][1],
                    ChatIntro.Interest_Traditional_Culture, ChatIntro.toggle_traditional),
        make_button(ChatIntro.ment_list[ChatIntro.lang]['button_text'][2],
                    ChatIntro.Interest_Modern_Culture, ChatIntro.toggle_modern),
        make_button(ChatIntro.ment_list[ChatIntro.lang]['button_text'][3],
                    ChatIntro.Interest_Shopping, ChatIntro.toggle_shopping),
        make_button(ChatIntro.ment_list[ChatIntro.lang]['button_text'][4],
                    ChatIntro.Outdoor_Activity_Preference, ChatIntro.toggle_outdoor),
        make_button(ChatIntro.ment_list[ChatIntro.lang]['button_text'][5],
                    ChatIntro.Indoor_Activity_Preference, ChatIntro.toggle_indoor),
        make_button(ChatIntro.ment_list[ChatIntro.lang]['button_text'][6], 
                    ChatIntro.Cultural_Experience_Preference, ChatIntro.toggle_cultural),
        wrap='wrap',
        gap='1rem',
        p='1.5rem',
        justify='center',
        margin_top="32px",
        margin_bottom="8px",
        align = "center",
    )

#4. 채팅 시작 버튼
def go_to_chatting_button() -> rx.Component :
    return rx.button(
            ChatIntro.ment_list[ChatIntro.lang]['go_to_chat'],
            on_click=ChatIntro.go_to_chatting,
            disabled=ChatIntro.select_done,
            color_scheme="mint",
            color = "white",
            font_size = "1.5em",
            height="50px",
            margin_y="4",
            box_shadow="md",
            style={"fontSize": "1.5em"},  # 입력 필드와 동일한 폰트 크기
            width = "30%"
        )

#5. 로딩창
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
