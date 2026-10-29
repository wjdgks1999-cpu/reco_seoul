import reflex as rx
from FindSeoul.recopage import reco_style as st
from FindSeoul.recopage.reco_state import RecomState
from typing import Any, Dict

#1. 상단바
def navbar() -> rx.Component :
    return rx.flex(
        rx.image(src= "/logo.png", width = "10em"),
        width = "100%",
        max_width = "1440px",
        background_color = "#4ecca3",
        align="center",
        justify="center",
        height="auto",
        box_shadow="0 2px 4px rgba(0, 0, 0, 0.1)",
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
                        RecomState.bot_mention,
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

#3. UserPreferences
def preferences_item(item: rx.Var[Dict[str, Any]], idx : int) -> rx.Component:
    return rx.card(
        rx.data_list.root(
            rx.data_list.item(
                rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['preferences_item_text'][0]),
                rx.data_list.value(rx.badge(item['interest_big_category']), variant = "soft", radius = "full")
            ),
            rx.data_list.item(
                rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['preferences_item_text'][1]),
                rx.data_list.value(item['interest_small_category'])
            ),
            rx.data_list.item(
                rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['preferences_item_text'][2]),
                rx.data_list.value(item['interest_level'])
            ),
            rx.data_list.item(
                rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['preferences_item_text'][3]),
                rx.data_list.value(item['confidence'])
            ),
            rx.data_list.item(
                rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['preferences_item_text'][4]),
                rx.data_list.value(item['reason'])
            ),
        ),
        class_name=f"item item-{idx}",
    )
    
def preferences_grid() -> rx.Component :
    return rx.grid(
        rx.foreach(
            RecomState.user_preferences,
            lambda item, idx : preferences_item(item=item, idx= idx),
        ),
        columns={
        "base": "1",   # 모든 화면(base) → 1열
        "md":   "2"    # md(48em) 이상 → 2열
        },
        **st.ANIMATION_PREFERENCE_GRID_BOX
    )


#4. Search_Result 카드
def search_results_card(item : rx.Var[Dict[str,Any]], idx : int) -> rx.Component :
    return rx.card(
            rx.data_list.root(
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['search_results_card_text'][0]),
                    rx.data_list.value(rx.badge(item['spot_name']), variant = "soft", radius = "full")
                ),
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['search_results_card_text'][1]),
                    rx.data_list.value(item['spot_category'])
                ),
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['search_results_card_text'][2]),
                    rx.data_list.value(item['spot_description'])
                )
            ),
            class_name=f"item item-{idx}",
        )

#(2). search_results 그리드
def search_results_grid() -> rx.Component :
    return rx.grid(
        rx.foreach(
            RecomState.search_results,
            lambda item, idx : search_results_card(item=item, idx=idx),
        ),
        **st.ANIMATION_SEARCH_RESULTS_GRID_BOX
    )

#5. 평가 카드
def evaluation_card(item : rx.Var[Dict[str,Any]], idx : int) -> rx.Component :
    return rx.card(
            rx.data_list.root(
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['evaluation_card_text'][0]),
                    rx.data_list.value(rx.badge(item['spot_name']), variant = "soft", radius = "full")
                ),
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['evaluation_card_text'][1]),
                    rx.data_list.value(item['matching_score'])
                ),
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['evaluation_card_text'][2]),
                    rx.data_list.value(item['evaluation_reason'])
                ),
            ),
            class_name=f"item item-{idx}",
        )

#(1). passed grid
def passed_grid() -> rx.Component :
    return rx.grid(
        rx.foreach(
            RecomState.passed_spots,
            lambda item, idx : evaluation_card(item=item, idx=idx),
        ),
        **st.ANIMATION_EVALUATION_GRID_BOX
    )

#(2). dropped grid
def dropped_grid() -> rx.Component :
    return rx.grid(
        rx.foreach(
            RecomState.dropped_spots,
            evaluation_card,
        ),
        **st.ANIMATION_EVALUATION_GRID_BOX
    )

#(3). flex box
def evaluation_box() -> rx.Component :
    return rx.grid(
        rx.vstack(
            rx.text(
                RecomState.reco_language_dict[RecomState.lang]['evaluation_card_text'][3],
                font_size = "1em",
                text_align="center",
                color="#1e40af",  # 더 진한 파란색
                background="linear-gradient(to right, #e6f7ff, #bae7ff)",  # 그라디언트 배경
                padding="12px 20px",
                border_radius="12px",
                font_weight="bold",
                letter_spacing="0.5px",
                box_shadow="0 4px 6px rgba(0, 0, 0, 0.1)",
                border="1px solid #91caff",  # 테두리 추가
                _hover={
                    "background": "linear-gradient(to right, #bae7ff, #91caff)",
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 6px 8px rgba(0, 0, 0, 0.15)",
                },
                transition="all 0.3s ease",
            ),
            passed_grid(),
            align="center",
            margin_top = "30px",
            margin_bottom = "2px"
        ),
        rx.vstack(
            rx.text(
                RecomState.reco_language_dict[RecomState.lang]['evaluation_card_text'][4],
                font_size = "1em",
                text_align="center",
                color="white",
                background="linear-gradient(to right, #f87171, #ef4444)",  # 붉은색 그라디언트 배경
                padding="12px 20px",
                border_radius="12px",
                font_weight="bold",
                letter_spacing="0.5px",
                box_shadow="0 4px 6px rgba(239, 68, 68, 0.2)",
                border="1px solid #ef4444",  # 테두리 추가
                _hover={
                    "background": "linear-gradient(to right, #ef4444, #dc2626)",
                    "transform": "translateY(-2px)",
                    "box_shadow": "0 6px 8px rgba(239, 68, 68, 0.25)",
                },
                transition="all 0.3s ease",
            ),
            dropped_grid(),
            align="center",
            margin_top = "30px",
            margin_bottom = "2px"
        ),
        width = "100%",
        columns={
        "base": "1",   # 모든 화면(base) → 1열
        "md":   "2"    # md(48em) 이상 → 2열
        },
    )

#6. 추천카드
def tourist_spot_card(item: rx.Var[Dict[str,Any]]) -> rx.Component:
    return rx.vstack(
        rx.hstack(
            rx.box(
                rx.heading(item["spot_name"], font_size="1.5em", color="white", align="center"),
                bg="rgba(0, 0, 0, 0.7)",
                p="3",
                border_radius="0 lg 0 0",
                width="90%",
            ),
            rx.box(
                rx.text(f"{item['evaluation_score']}%", font_size="1em", color="black"),
                bg="white",
                border="2px solid #4ecca3",  # 민트색 테두리
                border_radius="md",          # 테두리 모서리 둥글게
                width="10%",
                p="2",                       # 내부 여백
                text_align="center",         # 텍스트 가운데 정렬
            ),
            width = "100%",
        ),
        rx.box(
            rx.data_list.root(
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][0]),
                    rx.data_list.value(rx.badge(item['category']), variant = "soft", radius = "full")
                ),
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][1]),
                    rx.data_list.value(item['description']), variant = "soft", radius = "full")
                ),
            p="4",
            width="100%",
            height = "100%",
            overflow_y="auto",
        ),
        rx.flex(
            rx.image(
                src=item['image_url'],
                object_fit="cover",
                border_radius="sm",
                width="70%",
                height = "100%",
                alt="관광지 이미지",
            ),
            justify= "center",
            width = "100%",
        ),
        rx.divider(),
        rx.hstack(
            rx.icon("star", color="yellow"),
            rx.text(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][2], font_weight="bold", color="gray.700"),
            width="100%",
            align_items="center",
        ),
        rx.text(item["recommend_mention"], color="gray", mb="2"),
        rx.hstack(
            rx.icon("lightbulb", color="green"),
            rx.text(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][3], font_weight="bold", color="gray.700"),
            width="100%",
            align_items="center",
        ),
        rx.text(item["evaluation_reason"], color="gray", mb="2"),
        rx.divider(),
        rx.box(
            rx.data_list.root(
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][4]),
                    rx.data_list.value(item['formatted_address'], variant = "soft", radius = "full")
                ),
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][5]),
                    rx.data_list.value(rx.link(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][6], href=item['content_url'], is_external=True), variant = "soft", radius = "full")
                ),
                rx.data_list.item(
                    rx.data_list.label(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][7]),
                    rx.data_list.value(rx.link(RecomState.reco_language_dict[RecomState.lang]['tourist_spot_card_text'][8], href=item['google_maps_uri'], is_external=True), variant = "soft", radius = "full")
                ),
                width = "100%",
                size="3",
            ),
            width = "100%",
        ),
        width = "100%",
        height = "100%",
        margin_top = "16px",
        margin_botton = "2px",
        spacing="3",
        align="center",
    )

def page_num_button(num: int, idx: int) -> rx.Component:
    return rx.cond(
        # 선택된 페이지 번호(idx)가 True일 때
        RecomState.page_select[idx],
        rx.button(
            num,
            color_scheme="mint",          # 기본 배경
            color="white",           # 글자색
            _hover={"bg": "blue.600"},  # 마우스 오버 시
            _active={"bg": "blue.700", "transform": "scale(0.95)"},  # 클릭 시
            border_radius="md",
            px="4",
            py="2",
        ),
        # 선택되지 않은 경우
        rx.button(
            num,
            bg="gray",
            color="white",
            _hover={"bg": "gray.300"},
            _active={"bg": "gray.400", "transform": "scale(0.95)"},
            border_radius="md",
            px="4",
            py="2",
            on_click= RecomState.next_page_rendering(idx)
        )
    )

def tourist_spot_list() -> rx.Component :
    return rx.flex(
            tourist_spot_card(item= RecomState.final_results[RecomState.now_page_idx]),
            rx.divider(),
            rx.hstack(
                rx.foreach(RecomState.page_range,
                        lambda num, idx: page_num_button(num=num, idx=idx)),
                justify="between",
                margin_top = "16px",
                margin_bottom = "16px",
            ),
            **st.FINAL_RESULT_FLEX_BOX
        )