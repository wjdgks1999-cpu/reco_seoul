import reflex as rx

PAGE_FLEX_STYLE = {
    "direction": "column",
    "width": "100%",
    "min_height": "100vh",
    "height": "auto",
    "background_color": "#f0f0f0",
    "@media (max-width: 768px)": {
        "background_color": "white"
    },
    "align" : "center",
    "justify" : "center",
}

CONTAINER_STYLE = {
    "width": "100%",
    "max_width": "1440px",
    "margin": "0 auto",
    "padding": "0 16px",
    "background_color": "white",  # 흰색 배경색 추가
    "height" : "auto",
}

CHAT_VSTACK = {
    "height": "100vh",
    "width": "100%",
    "max_width": "1000px",
    "margin": "0 auto",
    "spacing": "4",
    "position": "relative",
    "align_items": "center",
    "justify_content": "space-between",  # 상단, 중간, 하단 요소 간격 조정
    "border": "2px solid #4ade80",
}

MESSAGE_STYLE = {
    "padding": "1em",
    "border_radius": "5px",
    "margin_y": "0.5em",
    "box_shadow": "rgba(0, 0, 0, 0.15) 0px 2px 8px",
    "max_width": "60em",
    "display": "inline-block",
}

# Set specific styles for questions and answers.
QUESTION_STYLE = {
    **MESSAGE_STYLE,
    "margin_left": "20%",
    "background_color": rx.color("gray", 4),
}

ANSWER_STYLE = {
    **MESSAGE_STYLE,
    "margin_right": "20%",
    "background_color": rx.color("accent", 8),
}

CHAT_HISTORY_STYLE = {
    "height": "100vh",  # 화면 높이의 70% 차지
    "width": "100%",
    "overflow_y": "auto",  # 스크롤 가능하게 설정
    "display": "flex",
    "flex_direction": "column",
    "padding": "1rem",
    "id" : "chat-messages-history",
}