import reflex as rx

class Cookie_Manage_State(rx.State) :
    intro_cookie : str = rx.SessionStorage(name = "intro_cookie")
    chat_cookie : str = rx.SessionStorage(name = "chat_cookie")
    recommend_cookie : str = rx.SessionStorage(name = "recommend_cookie")

@rx.page(route = "/cookie_manage")
def cookie_page() -> rx.Component :
    return rx.flex(
        rx.text(f'intro_cookie : {Cookie_Manage_State.intro_cookie}', text_align = "center", size = "3"),
        rx.text(f'chat_cookie : {Cookie_Manage_State.chat_cookie}', text_align = "center", size = "3"),
        rx.text(f'recommend_cookie : {Cookie_Manage_State.recommend_cookie}', text_align = "center", size = "3"),
        direction = "column",
        align = "center",
        justify = "center",
        width = "100%"
    )

