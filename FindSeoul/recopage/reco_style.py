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

ANIMATION_PREFERENCE_GRID_BOX = {
    "width" : "100%",
    "flow" : "row-dense",
    # 애니메이션 키프레임 정의
    "@keyframes fadeIn": {
        "0%": {
            "opacity": 0,
            "transform": "translateY(20px)",
        },
        "100%": {
            "opacity": 1,
            "transform": "translateY(0)",
        },
    },
    # 기본 아이템 스타일 추가
    ".item": {
        "opacity": 0,
        "size" : "1",
    },
    # hover 효과 추가
    ".item:hover": {
        "transform": "translateY(-4px)",
        "box_shadow": "0 8px 16px rgba(0,0,0,0.15)",
        "border": "1px solid #38B2AC",
    },
    # 각 아이템별 애니메이션 지연 시간
    ".item-0": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "0.4s",
    },
    ".item-1": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "0.6s",
    },
    ".item-2": {
        "animation": "fadeIn 0.5s ease forwards", 
        "animation_delay": "0.8s",
    },
    ".item-3": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.0s", 
    },
    ".item-4": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.2s",
    },
    ".item-5": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.4s",
    },
    ".item-6": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.6s",
    },
    ".item-7": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.8s",
    },
    ".item-8": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.0s",
    },
    ".item-9": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.2s",
    },
    ".item-10": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.4s",
    },
    ".item-11": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.6s",
    },
    ".item-12": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.8s",
    },
    ".item-13": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.0s",
    },
    ".item-14": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.2s",
    },
    ".item-15": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.4s",
    },
    ".item-16": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.6s",
    },
    ".item-17": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.8s",
    },
    ".item-18": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.0s",
    },
    ".item-19": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.2s",
    },
    ".item-20": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.4s",
    },
}


ANIMATION_SEARCH_RESULTS_GRID_BOX = {
    "columns" : "1",
    "width" : "100%",
    "flow" : "row-dense",
    # 애니메이션 키프레임 정의
    "@keyframes fadeIn": {
        "0%": {
            "opacity": 0,
            "transform": "translateY(20px)",
        },
        "100%": {
            "opacity": 1,
            "transform": "translateY(0)",
        },
    },
    # 기본 아이템 스타일 추가
    ".item": {
        "opacity": 0,
        "size" : "1",
    },
    # hover 효과 추가
    ".item:hover": {
        "transform": "translateY(-4px)",
        "box_shadow": "0 8px 16px rgba(0,0,0,0.15)",
        "border": "1px solid #38B2AC",
    },
    # 각 아이템별 애니메이션 지연 시간
    ".item-0": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "0.4s",
    },
    ".item-1": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "0.6s",
    },
    ".item-2": {
        "animation": "fadeIn 0.5s ease forwards", 
        "animation_delay": "0.8s",
    },
    ".item-3": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.0s", 
    },
    ".item-4": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.2s",
    },
    ".item-5": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.4s",
    },
    ".item-6": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.6s",
    },
    ".item-7": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.8s",
    },
    ".item-8": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.0s",
    },
    ".item-9": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.2s",
    },
    ".item-10": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.4s",
    },
    ".item-11": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.6s",
    },
    ".item-12": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.8s",
    },
    ".item-13": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.0s",
    },
    ".item-14": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.2s",
    },
    ".item-15": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.4s",
    },
    ".item-16": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.6s",
    },
    ".item-17": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.8s",
    },
    ".item-18": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.0s",
    },
    ".item-19": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.2s",
    },
    ".item-20": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.4s",
    },
}

ANIMATION_EVALUATION_GRID_BOX = {
    "columns" : "1",
    "width" : "100%",
    "flow" : "row-dense",
    # 애니메이션 키프레임 정의
    "@keyframes fadeIn": {
        "0%": {
            "opacity": 0,
            "transform": "translateY(20px)",
        },
        "100%": {
            "opacity": 1,
            "transform": "translateY(0)",
        },
    },
    # 기본 아이템 스타일 추가
    ".item": {
        "opacity": 0,
        "size" : "1",
    },
    # hover 효과 추가
    ".item:hover": {
        "transform": "translateY(-4px)",
        "box_shadow": "0 8px 16px rgba(0,0,0,0.15)",
        "border": "1px solid #38B2AC",
    },
    # 각 아이템별 애니메이션 지연 시간
    ".item-0": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "0.4s",
    },
    ".item-1": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "0.6s",
    },
    ".item-2": {
        "animation": "fadeIn 0.5s ease forwards", 
        "animation_delay": "0.8s",
    },
    ".item-3": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.0s", 
    },
    ".item-4": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.2s",
    },
    ".item-5": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.4s",
    },
    ".item-6": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.6s",
    },
    ".item-7": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "1.8s",
    },
    ".item-8": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.0s",
    },
    ".item-9": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.2s",
    },
    ".item-10": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.4s",
    },
    ".item-11": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.6s",
    },
    ".item-12": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "2.8s",
    },
    ".item-13": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.0s",
    },
    ".item-14": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.2s",
    },
    ".item-15": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.4s",
    },
    ".item-16": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.6s",
    },
    ".item-17": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "3.8s",
    },
    ".item-18": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.0s",
    },
    ".item-19": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.2s",
    },
    ".item-20": {
        "animation": "fadeIn 0.5s ease forwards",
        "animation_delay": "4.4s",
    },
}

FINAL_RESULT_FLEX_BOX = {
    "justify": "center",
    "direction": "column",
    "align": "center",
    "spacing": "2",
}