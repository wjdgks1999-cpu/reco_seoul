import reflex as rx

from FindSeoul.homepage import home_style as st
from FindSeoul.homepage.home_state import HomeState

#1. navbar 섹션
#(1). 언어 변경 버튼
def language_button(text: str, lang: str) -> rx.Component:
    """언어 선택 버튼 컴포넌트."""
    return rx.button(
        text,
        on_click=HomeState.change_language(lang),
        bg=rx.cond(
            HomeState.lang == lang,
            "#f1f1f1",
            "transparent"
        ),
        **st.LANG_BUTTON_STYLE,
    )

def navbar() -> rx.Component:
    """네비게이션 바 컴포넌트."""
    return rx.flex(
        rx.hstack(
                rx.image(src= "/logo.png", width = "10em"),
                width="50%",  # 왼쪽 절반 차지,
                justify= "start",
                align="start",
        ),
        rx.flex(
            language_button("한국어", "ko"),
            language_button("English", "en"),
            gap="10",
            direction="row",
            align="center",
            justify="end",
            width = "50%",
        ),
        **st.NAVBAR_STYLE,
        as_="header",
    )

#2. hero 섹션
def hero() -> rx.Component:
    """히어로 섹션 컴포넌트."""
    return rx.flex(
            # 히어로 컨테이너 (외부 컨테이너)
            rx.flex(
                # 배경 이미지
                rx.image(
                    src="/seoul_spring_cherry_blossom.jpg",
                    alt="서울의 봄",
                    width="100%",
                    height="100%",
                    object_fit="cover",
                    position="absolute",
                    top="0",
                    left="0",
                    id="season-image",
                ),
                # 어두운 오버레이
                rx.flex(
                    position="absolute",
                    top="0",
                    left="0",
                    width="100%",
                    height="100%",
                    bg="rgba(0, 0, 0, 0.5)",
                ),
                # 콘텐츠
                rx.vstack(
                    # 제목
                    rx.heading(
                        HomeState.translation[HomeState.lang]["hero1"],
                        color="white",
                        font_size="2em",
                        text_shadow="2px 2px 4px rgba(0, 0, 0, 0.5)",
                        mb="4",
                        text_align="center",
                    ),
                    # 부제목
                    rx.text(
                        HomeState.translation[HomeState.lang]["hero2"],
                        color="white",
                        font_size="1.5em",
                        text_shadow="1px 1px 2px rgba(0, 0, 0, 0.7)",
                        mb="6",
                        text_align="center",
                    ),
                    position="absolute",
                    top="50%",
                    left="50%",
                    transform="translate(-50%, -50%)",
                    width="100%",
                    max_width="1000px",
                    spacing="3",
                    align="center",
                    justify="center",
                    px="4",
                    z_index="2",
                ),
                position="relative",
                width="100%",
                height="60vh",
                overflow="hidden",
            ),
        width="100%",
        direction="column",
    )

#3. category 섹션
#(1). 카테고리 카드
def category_card(icon: str, title: str, description: str, link : str) -> rx.Component:
    """카테고리 카드 컴포넌트."""
    return rx.flex(
        rx.vstack(
            rx.box(height = "4px"),
            # 아이콘
            rx.icon(
                icon,
                font_size="24px",
                color=st.COLORS["primary"],
                mb="4",
            ),
            # 제목
            rx.heading(
                title,
                size="5",
                mb="2",
                text_align="center",
            ),
            rx.text(
                description,
                color=st.COLORS["text_light"],
                mb="4",
                text_align="center",
                flex_grow="1",
                height="60px",  # 설명 텍스트 영역 높이 고정
                overflow_y="auto",  # 내용이 많으면 스크롤 허용
            ),
            # 버튼
            rx.button(
                HomeState.translation[HomeState.lang]["button_text"],
                on_click= rx.redirect(link, is_external=True),
                **st.OUTLINE_BUTTON_STYLE,
            ),
            rx.box(height = "4px"),
            align="center",
            justify="start",
            width = "100%",
            height = "100%",
            border=f"1px solid {st.COLORS['border']}",
            border_radius="8px",
            transition="all 0.3s",
            _hover={
                "transform": "translateY(-5px)",
                "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            },
            p="6",
        ),
        width=["100%", "calc(50% - 16px)", "calc(25% - 16px)"],
        margin="8px",
    )

#(2). 카테고리 섹션
def category_section() -> rx.Component:
    """카테고리 섹션 컴포넌트."""
    return rx.flex(
        rx.vstack(
            rx.center(
                rx.heading(
                    HomeState.translation[HomeState.lang]["category_head"],
                    size="8",  # 명확한 크기 지정
                    margin_top = "32px",
                    margin_bottom="1px",
                ),
            width="100%",
            ),
            rx.center(  # 카드 그리드 중앙 정렬
                rx.flex(  # flex를 사용하여 카드 배치
                    category_card(
                        "map-pin",
                        HomeState.translation[HomeState.lang]["category_name_1"][0],
                        HomeState.translation[HomeState.lang]["category_name_1"][1],
                        HomeState.translation[HomeState.lang]["home_url"][0]
                    ),
                    category_card(
                        "compass",
                        HomeState.translation[HomeState.lang]["category_name_2"][0],
                        HomeState.translation[HomeState.lang]["category_name_2"][1],
                        HomeState.translation[HomeState.lang]["home_url"][1]
                    ),
                    category_card(
                        "calendar",
                        HomeState.translation[HomeState.lang]["category_name_3"][0],
                        HomeState.translation[HomeState.lang]["category_name_3"][1],
                        HomeState.translation[HomeState.lang]["home_url"][2]
                    ),
                    category_card(
                        "star",
                        HomeState.translation[HomeState.lang]["category_name_4"][0],
                        HomeState.translation[HomeState.lang]["category_name_4"][1],
                        HomeState.translation[HomeState.lang]["home_url"][3]
                    ),
                    justify="center",  # 중앙 정렬
                    wrap="wrap",  # 줄바꿈 가능하도록
                    gap="6",  # 카드 간 간격
                    width="100%",
                    align_items="stretch",
                ),
                width="100%",
            ),
            spacing="9",
            width="100%",
            max_width="1400px",  # 최대 너비 설정
        ),
        width = "100%",
        align="center",
        justify="center",
    )

#4. Planner 섹션
def form_group(label: str, component: rx.Component) -> rx.Component:
    """폼 그룹 컴포넌트."""
    return rx.flex(
        rx.text(
            label,
            as_="label",
            display="block",
            margin_bottom="12px",  # 간격 조정
            font_weight="500",
            color=st.COLORS["text"],
            font_size="16px",  # 폰트 크기 명시
        ),
        component,
        direction = "column",
        wrap="wrap",
        min_width="250px",
        margin="10px",  # 각 폼 그룹 사이 간격 추가
        align = "center"
    )

def user_info() -> rx.Component :
    return rx.hstack(
        rx.select(
        items =HomeState.translation[HomeState.lang]["user"],
        value=HomeState.translation[HomeState.lang]["user"][0],
        disabled=True,
        bg="#f5f5f5",
        **st.INFO,
        ),
        rx.select(
            items=HomeState.translation[HomeState.lang]["age"],
            placeholder=HomeState.translation[HomeState.lang]["planner_instruction"][1],
            value = HomeState.User_info,
            on_change= HomeState.set_User_info,
            bg="white",
            **st.INFO,
        ),
        align="center"
    )

def Companions_info(index:int) -> rx.Component :
    return rx.hstack(
        rx.select(
            items=HomeState.translation[HomeState.lang]["companion"],
            placeholder=HomeState.translation[HomeState.lang]["planner_instruction"][0],
            value=HomeState.Companions[index]["relation"],
            on_change=lambda value: HomeState.update_companion(index, "relation", value),
            bg="white",
            **st.INFO,
        ),
        rx.select(
            items=HomeState.translation[HomeState.lang]["age"],
            placeholder=HomeState.translation[HomeState.lang]["planner_instruction"][1],
            value=HomeState.Companions[index]["age"],
            on_change=lambda value: HomeState.update_companion(index, "age", value),
            bg="white",
            **st.INFO,
        ),
        # 추가/삭제 버튼
        rx.cond(
            index == 0,
            # 첫 번째 행이면 추가 버튼
            rx.button(
                rx.icon("plus"),
                on_click=HomeState.add_companion,
                bg=st.COLORS["primary"],
                color="white",
                border="none",
                border_radius="4px",
                width="32px",
                height="32px",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                _hover={"bg": st.COLORS["primary_dark"]},
                class_name="btn-small",
            ),
            # 첫 번째 행이 아니면 삭제 버튼
            rx.button(
                rx.icon("minus"),
                on_click=lambda: HomeState.remove_companion(index),
                bg=st.COLORS["primary"],
                color="white",
                border="none",
                border_radius="4px",
                width="32px",
                height="32px",
                display="flex",
                align_items="center",
                justify_content="center",
                cursor="pointer",
                _hover={"bg": st.COLORS["primary_dark"]},
                class_name="btn-small",
            ),
        ),
        gap="10px",
        align_items="center",
        width="100%",  # 행 전체 너비 지정
        margin_bottom="10px",
    )

def planner_section() -> rx.Component :
    return rx.flex(
        rx.vstack(
                # 섹션 제목
            rx.heading(
                HomeState.translation[HomeState.lang]["planner_head"],
                size="8",
                margin_top="16px",
                margin_bottom="8px",
                text_align="center",
            ),
            # 섹션 설명
            rx.text(
                HomeState.translation[HomeState.lang]["planner_description"],
                text_align="center",
                margin_bottom="24px",
            ),
            rx.flex(
                    form_group(
                        HomeState.translation[HomeState.lang]["planner_category"][3],
                        rx.flex(
                            rx.input(
                                type="date",
                                value=HomeState.check_in_date,
                                on_change=HomeState.set_check_in_date,
                                min= HomeState.today,  # 오늘 이후의 날짜만 선택 가능
                                flex="1",
                                padding="8px 12px",
                                border=f"1px solid {st.COLORS['border']}",
                                border_radius="4px",
                                bg="white",
                                class_name="date-input",
                                height="40px",
                            ),
                            rx.text(
                                "~",
                                margin="0 8px",
                                align_self="center",
                            ),
                            rx.input(
                                type="date",
                                value=HomeState.check_out_date,
                                on_change=HomeState.set_check_out_date,
                                # 체크인 날짜 이후로만 선택 가능하도록 설정
                                min=rx.cond(
                                    HomeState.check_in_date != "",
                                    HomeState.check_in_date,
                                    HomeState.today
                                ),
                                flex="1",
                                padding="8px 12px",
                                border=f"1px solid {st.COLORS['border']}",
                                border_radius="4px",
                                bg="white",
                                class_name="date-input",
                                height="40px",
                            ),
                        ),
                    ),
                    form_group(
                        HomeState.translation[HomeState.lang]["planner_category"][2],
                        rx.input(
                            type="number",
                            value=HomeState.sites_per_day,
                            on_change=HomeState.set_sites_per_day,
                            min="1",
                            max="10",
                            width="100%",
                            padding="8px 12px",
                            border=f"1px solid {st.COLORS['border']}",
                            border_radius="4px",
                            bg="white",
                            height="40px",
                        ),
                    ),
                    form_group(
                        HomeState.translation[HomeState.lang]["planner_category"][4],
                        user_info(),
                    ),
                    rx.vstack(
                        rx.text(
                            HomeState.translation[HomeState.lang]["planner_category"][5],
                            as_="label",
                            display="block",
                            margin_bottom="12px",  # 간격 조정
                            font_weight="500",
                            color=st.COLORS["text"],
                            font_size="16px",  # 폰트 크기 명시,
                            text_align = "center",
                        ),
                        rx.foreach(
                            HomeState.Companions,
                            lambda Companions, index : Companions_info(index),
                        ),
                        align="center",
                    ),
                    wrap="wrap",
                    direction="row",
                    align="center",
                    justify="center",
                    width = "100%",
                    height = "auto"
                ),
                rx.button(
                    HomeState.translation[HomeState.lang]["planner_instruction"][4],
                    on_click=HomeState.find_travel_course,
                    **st.PRIMARY_BUTTON_STYLE,
                    margin_top="16px",
                    width="200px",
                ),
                align="center",
                width = "100%",
                height = "auto"
            ),
        bg=st.COLORS["background"],
        border_radius="8px",
        padding="32px",
        margin_top="40px",
        margin_bottom="40px",
        align="center",
        direction="column",
        width = "100%",
        max_width = "1400px",
    )

#5. destination 섹션
def destination_card(image_src: str, title: str, badge: str, description: str, link:str) -> rx.Component:
    """관광지 카드 컴포넌트."""
    return rx.box(
        rx.vstack(
            # 이미지
            rx.image(
                src=image_src,
                alt=title,
                width="100%",
                height="200px",
                object_fit="cover",
                border_top_left_radius="8px",
                border_top_right_radius="8px",
            ),
            
            # 컨텐츠 영역
            rx.vstack(
                # 제목
                rx.heading(
                    title,
                    size="5",
                    mb="2",
                ),
                
                # 배지 (카테고리 표시)
                rx.box(
                    badge,
                    bg=f"rgba(20, 184, 166, 0.1)",
                    color=st.COLORS["primary"],
                    border_radius="4px",
                    padding="4px 8px",
                    font_size="0.875rem",
                    display="inline-block",
                    mb="2",
                ),
                
                # 설명 텍스트
                rx.text(
                    description,
                    color=st.COLORS["text_light"],
                    margin_bottom="4",
                    min_height="48px",
                ),
                
                # 버튼
                rx.button(
                    HomeState.translation[HomeState.lang]["button_text"],
                    on_click= rx.redirect(link, is_external=True),
                    width="100%",
                    **st.OUTLINE_BUTTON_STYLE,
                ),
                
                align="start",
                padding="16px",
                width="100%",
                spacing="2",
            ),
            width="100%",
            align="stretch",
            border_radius="8px",
            border=f"1px solid {st.COLORS['border']}",
            overflow="hidden",
            transition="all 0.3s",
            _hover={
                "transform": "translateY(-5px)",
                "box_shadow": "0 4px 12px rgba(0, 0, 0, 0.1)",
            },
        ),
        width=["100%", "calc(50% - 16px)", "calc(25% - 16px)"],
        margin="8px",
    )


def destination_section() -> rx.Component:
    """인기 명소 섹션 컴포넌트."""
    return rx.center(
        rx.vstack(
            # 섹션 제목
            rx.center(
                rx.heading(
                    HomeState.translation[HomeState.lang]["destination_header"],
                    size="8",
                    margin_top="32px",
                    margin_bottom="1px",
                ),
                width="100%",
            ),
            # 카드 그리드
            rx.center(
                rx.flex(
                    # 경복궁
                    destination_card(
                        "/gyeongbokgung.jpg",
                        HomeState.translation[HomeState.lang]["item_name"][0],
                        HomeState.translation[HomeState.lang]["item_category"][0],
                        HomeState.translation[HomeState.lang]["item_description"][0],
                        HomeState.translation[HomeState.lang]["item_url"][0]
                    ),
                    
                    # 남산서울타워
                    destination_card(
                        "/namsan_tower.jpg",
                        HomeState.translation[HomeState.lang]["item_name"][1],
                        HomeState.translation[HomeState.lang]["item_category"][1],
                        HomeState.translation[HomeState.lang]["item_description"][1],
                        HomeState.translation[HomeState.lang]["item_url"][1]
                    ),
                    
                    # 홍대
                    destination_card(
                        "/hongdae.jpg",
                        HomeState.translation[HomeState.lang]["item_name"][2],
                        HomeState.translation[HomeState.lang]["item_category"][2],
                        HomeState.translation[HomeState.lang]["item_description"][2],
                        HomeState.translation[HomeState.lang]["item_url"][2]
                    ),
                    
                    # 동대문디자인플라자
                    destination_card(
                        "/ddp.jpg",
                        HomeState.translation[HomeState.lang]["item_name"][3],
                        HomeState.translation[HomeState.lang]["item_category"][3],
                        HomeState.translation[HomeState.lang]["item_description"][3],
                        HomeState.translation[HomeState.lang]["item_url"][3]
                    ),
                    justify="center",
                    wrap="wrap",
                    gap="6",
                    width="100%",
                    align="stretch",
                ),
                width="100%",
            ),
            spacing="9",
            width="100%",
            max_width="1400px",
        ),
        width="100%",
    )

#6. footer 섹션
def term_of_service() -> rx.Component :
    return rx.alert_dialog.root(
            rx.alert_dialog.trigger(
                rx.button(HomeState.translation[HomeState.lang]['foot'][0], color = "black", background_color= "#f9fafb"),
                ),
            rx.alert_dialog.content(
                rx.alert_dialog.title(HomeState.translation[HomeState.lang]['terms_of_service_title'][0], style={"whiteSpace": "pre-line"}),
                rx.alert_dialog.description(HomeState.translation[HomeState.lang]['terms_of_service_content'][0], style={"whiteSpace": "pre-line"}),
                rx.spacer(height = "10px"),
                rx.alert_dialog.title(HomeState.translation[HomeState.lang]['terms_of_service_title'][1], style={"whiteSpace": "pre-line"}),
                rx.alert_dialog.description(HomeState.translation[HomeState.lang]['terms_of_service_content'][1], style={"whiteSpace": "pre-line"}),
                rx.spacer(height = "10px"),
                rx.alert_dialog.title(HomeState.translation[HomeState.lang]['terms_of_service_title'][2], style={"whiteSpace": "pre-line"}),
                rx.alert_dialog.description(HomeState.translation[HomeState.lang]['terms_of_service_content'][2], style={"whiteSpace": "pre-line"}),
                rx.spacer(height = "10px"),
                rx.alert_dialog.title(HomeState.translation[HomeState.lang]['terms_of_service_title'][3], style={"whiteSpace": "pre-line"}),
                rx.alert_dialog.description(HomeState.translation[HomeState.lang]['terms_of_service_content'][3], style={"whiteSpace": "pre-line"}),
                rx.spacer(height = "10px"),
                rx.alert_dialog.title(HomeState.translation[HomeState.lang]['terms_of_service_title'][4], style={"whiteSpace": "pre-line"}),
                rx.alert_dialog.description(HomeState.translation[HomeState.lang]['terms_of_service_content'][4], style={"whiteSpace": "pre-line"}),
                rx.spacer(height = "10px"),
                rx.alert_dialog.title(HomeState.translation[HomeState.lang]['terms_of_service_title'][5], style={"whiteSpace": "pre-line"}),
                rx.alert_dialog.description(HomeState.translation[HomeState.lang]['terms_of_service_content'][5], style={"whiteSpace": "pre-line"}),
                rx.spacer(height = "10px"),
                rx.alert_dialog.title(HomeState.translation[HomeState.lang]['terms_of_service_title'][6], style={"whiteSpace": "pre-line"}),
                rx.alert_dialog.description(HomeState.translation[HomeState.lang]['terms_of_service_content'][6], style={"whiteSpace": "pre-line"}),
                rx.spacer(height = "10px"),
                rx.alert_dialog.title(HomeState.translation[HomeState.lang]['terms_of_service_title'][7], style={"whiteSpace": "pre-line"}),
                rx.alert_dialog.description(HomeState.translation[HomeState.lang]['terms_of_service_content'][7], style={"whiteSpace": "pre-line"}),
                rx.spacer(height = "10px"),
                rx.flex(
                    rx.alert_dialog.cancel(
                    rx.button("Close", color_scheme="mint")  
                    ),
                ),
            ),
    )

def privacy_policy() -> rx.Component :
    return rx.alert_dialog.root(
        rx.alert_dialog.trigger(
            rx.button(HomeState.translation[HomeState.lang]['foot'][1], color = "black", background_color= "#f9fafb"),
        ),
        rx.alert_dialog.content(
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][0], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][1], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][2], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][3], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][4], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][5], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][6], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][7], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][8], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][9], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.alert_dialog.description(HomeState.translation[HomeState.lang]['privacy_policy_content'][10], style={"whiteSpace": "pre-line"}),
            rx.spacer(height = "10px"),
            rx.flex(
                rx.alert_dialog.cancel(
                rx.button("Close", color_scheme="mint")  
                ),
            ),
        )
    )

def footer() -> rx.Component :
    return rx.flex(
        rx.hstack(
            term_of_service(),
            privacy_policy(),
            align="center",
            wrap="wrap",
            gap = "6",
            width = "100%",
            justify="center",
        ),
        rx.divider(),
        rx.text(
            HomeState.translation[HomeState.lang]["copywrite"],
            text_align="center",
            color=st.COLORS["text_lighter"],
            padding_top="4",
        ),
        direction="column",
        align="center",
        justify="center",
        width = "100%",
        bg=st.COLORS["background"],
        padding_y="10",
        margin_top="32px",
    )

#7. 로딩창
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