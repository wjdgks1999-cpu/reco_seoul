import reflex as rx

PAGE_FLEX_STYLE = {
    "direction": "column",
    "width": "100vw",
    "height": "100vh",
    "background_color": "#f0f0f0",
    "@media (max-width: 768px)": {
        "background_color": "white"
    },
    "align" : "center",
    "justify" : "start",
}

CONTAINER_STYLE = {
    "width": "100%",
    "max_width": "1440px",
    "height" : "100vh",
    "margin": "0",
    "padding": "0 8px",
    "background_color": "white",  # 흰색 배경색 추가
}

NAVBAR_STYLE = {
    "width": "100%",
    "max_width": "1440px",
    "height": "auto",
    "background_color": "#4ecca3",
    "align": "center",
    "justify": "center",
    "box_shadow": "0 2px 4px rgba(0, 0, 0, 0.1)",
}

MESSAGE_STYLE = {
    "width" : "100%",
    "padding": "1em",
    "border-radius": "5px",
    "margin-top": "0.5em",
    "margin-bottom": "0.5em",
    "box-shadow": "0 2px 5px rgba(0, 0, 0, 0.2)",
    "display": "inline-block",
    "background-color": "#e0f2fe"
}