import reflex as rx
from FindSeoul.chatpage.chat_state import ChatState
from FindSeoul.chatpage.chat_component import chatting_history, action_bar, navbar, loading_view
import FindSeoul.chatpage.chat_style as st

def loading_cond() -> rx.Component :
    return rx.cond(
        ChatState.next_page_loading,
        loading_view(),
        None
    )

@rx.page(route="/chatting", title="Chat",on_load=[ChatState.check_cookie])
def chatting_page() -> rx.Component:
    return rx.flex(
        rx.container(
            rx.vstack(
                # 헤더
                navbar(),
                
                # 채팅 영역 (스크롤 가능)
                chatting_history(),

                # 자동 스크롤을 위한 스크립트 (IIFE로 래핑해 전역 변수 충돌 방지)
                rx.script("""
                    (function() {
                        function scrollToBottom() {
                            const chatContainer = document.getElementById('chat-messages-history');
                            if (chatContainer) {
                                chatContainer.scrollTop = chatContainer.scrollHeight;
                            }
                        }
                        window.addEventListener('state_change', scrollToBottom);
                        window.addEventListener('load', scrollToBottom);
                        const container = document.getElementById('chat-messages-history');
                        if (container) {
                            const observer = new MutationObserver(scrollToBottom);
                            observer.observe(container, { childList: true, subtree: true });
                        }
                    })();
                """),
                
                # 입력 영역 (하단 고정)
                    rx.box(
                        action_bar(),
                        position="sticky",
                        bottom="0",
                        width="100%",
                        padding_y="1rem",
                        background_color="white",  # 배경색 추가
                    ),
                **st.CHAT_VSTACK
            ),
            loading_cond(),
            **st.CONTAINER_STYLE,
        ),
    **st.PAGE_FLEX_STYLE,
)