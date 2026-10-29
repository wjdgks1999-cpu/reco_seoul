import reflex as rx

from FindSeoul.recopage.reco_state import RecomState
import FindSeoul.recopage.reco_style as st
from FindSeoul.recopage.reco_component import (navbar, avatar_ment, preferences_grid, 
                                         search_results_grid, evaluation_box,
                                         tourist_spot_list)

def final_progress_result() -> rx.Component :
    return rx.match(
        RecomState.select_results,
        ("user_prefer", preferences_grid()),
        ("searched", search_results_grid()),
        ("evaluations", evaluation_box()),
        ("final_results", tourist_spot_list())
    )

def final_progress() -> rx.Component :
    return  rx.vstack(
        rx.flex(
                rx.button(RecomState.reco_language_dict[RecomState.lang]["final_progress_button_text"][0],
                          on_click= RecomState.select_prefer, 
                          margin = "10px", 
                          color_scheme="mint",
                          color = "white",
                          max_height="50px",
                          font_size = "1em"),
                rx.button(RecomState.reco_language_dict[RecomState.lang]["final_progress_button_text"][1],
                          on_click=RecomState.select_search, 
                          margin = "10px", 
                          color_scheme="mint",
                          color = "white",
                          max_height="50px",
                          font_size = "1em"),
                rx.button(RecomState.reco_language_dict[RecomState.lang]["final_progress_button_text"][2],
                          on_click=RecomState.select_evaluation,
                          margin = "10px", 
                          color_scheme="mint",
                          color = "white",
                          max_height="50px",
                          font_size = "1em"),
                rx.button(RecomState.reco_language_dict[RecomState.lang]["final_progress_button_text"][3],
                        on_click=RecomState.select_final_results, 
                        margin = "10px", 
                        color_scheme="mint",
                        color = "white",
                        max_height="50px",
                        font_size = "1em"),
                justify="center",
                align = "center",
                wrap="wrap"
        ),
        rx.divider(),
        final_progress_result(),
        align="center",
    )

def stage_progress() -> rx.Component :
    return rx.match(
        RecomState.complete_stage,
        ("user_preferences_step", preferences_grid()),
        ("search_results_step", search_results_grid()),
        ("evaluation_step", evaluation_box()),
        ("end_step", final_progress()),
        rx.box()
    )

@rx.page(route="/recommend", title = "Reco", on_load=[RecomState.check_cookie])
def recommendation_page() -> rx.Component:
    # Welcome Page (Index)
    return rx.flex(
        navbar(),
        rx.container(
            avatar_ment(),
            rx.divider(),
            stage_progress(),
            **st.CONTAINER_STYLE,
        ),
        **st.PAGE_FLEX_STYLE,
    )