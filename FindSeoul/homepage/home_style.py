PAGE_FLEX_STYLE = {
    "direction": "column",
    "width": "100%",
    "min_height": "100vh",
    "height": "auto",
    "background_color": "#f0f0f0",
    "@media (max-width: 768px)": {
        "background_color": "white"
    },
    "wrap": "wrap",
    "align":"center",
    "justify":"between",
}

CONTAINER_STYLE = {
    "direction": "column",
    "width": "100%",
    "max_width": "1440px",
    "min_height": "100vh",
    "height": "auto",
    "background_color": "white",
    "wrap": "wrap",
    "align":"center",
    "justify":"start",
}

COLORS = {
    "primary": "#14b8a6",
    "primary_dark": "#0d9488",
    "background": "#f9fafb",
    "border": "#eaeaea",
    "text": "#333",
    "text_light": "#666",
    "text_lighter": "#777",
}

BUTTON_STYLE = {
    "border_radius": "4px",
    "cursor": "pointer",
    "transition": "all 0.3s",
    "font_weight": "500",
    "padding": "12px 24px",
}

PRIMARY_BUTTON_STYLE = {
    **BUTTON_STYLE,
    "background_color": COLORS["primary"],
    "color": "white",
    "border": "none",
    "_hover": {"background_color": COLORS["primary_dark"]},
}

OUTLINE_BUTTON_STYLE = {
    **BUTTON_STYLE,
    "background_color": "transparent",
    "border": f"1px solid {COLORS['primary']}",
    "color": COLORS["primary"],
    "_hover": {"background_color": f"rgba(20, 184, 166, 0.1)"},
}

LANG_BUTTON_STYLE = {
    "border": "1px solid #e2e8f0",
    "padding": "8px 12px",
    "cursor": "pointer",
    "border_radius": "4px",
    "transition": "all 0.3s",
    "color": "#333",
    "font_weight": "normal",
    "_hover": {"bg": "#a5f3e4"},
}

NAVBAR_STYLE = {
    "justify": "between",
    "align": "stretch",
    "width": "100%",
    "bg": "#c5f6e8",
    "padding": "2em",
    "height" : "auto",
    "max_height": "10vh",
}

INFO = {
    "flex": "1",
    "padding": "8px 12px",
    "border": f"1px solid {COLORS['border']}",
    "border_radius": "4px",
    "height": "40px",
    "font_size": "14px",
    "width": "auto",  # 너비 명시적 지정
}