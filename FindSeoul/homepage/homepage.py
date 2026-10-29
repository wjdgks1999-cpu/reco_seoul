import reflex as rx

from FindSeoul.homepage import home_style as st
from FindSeoul.homepage.home_component import navbar, hero, category_section, planner_section, destination_section, footer, loading_view
from FindSeoul.homepage.home_state import HomeState

def loading_cond() -> rx.Component :
  return rx.cond(
    HomeState.is_loading,
   loading_view(),
   None
  )


@rx.page(route = "/", title="Home",on_load = [HomeState.initialize])
def homepage() -> rx.Component:
    return rx.flex(
            rx.flex(
            navbar(),
            
            hero(),
            
            category_section(),
            
            planner_section(),
            
            destination_section(),
            
            footer(),
            
            loading_cond(),
            **st.CONTAINER_STYLE
        ),       
        **st.PAGE_FLEX_STYLE
    )