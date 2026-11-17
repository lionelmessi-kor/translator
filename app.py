import streamlit as st

from translator import LANGUAGES, MAX_CHARS, TranslationError, translate

# 버튼에 표시할 라벨 (UI 전용, 번역 로직과 무관)
BUTTON_LABELS = {
    "영어": "영어 · EN",
    "일본어": "일본어 · JA",
    "베트남어": "베트남어 · VI",
}

CSS = """
<style>
#MainMenu, footer, [data-testid="stToolbar"] {visibility: hidden;}
.block-container {max-width: 760px; padding-top: 3rem; padding-bottom: 4rem;}
.stMarkdown p.app-title {font-size: 2rem; font-weight: 700; margin: 0; letter-spacing: -0.02em; line-height: 1.3;}
.stMarkdown p.app-sub {opacity: .65; margin: .25rem 0 1.5rem 0;}
.stTextArea textarea {font-size: 1.05rem; line-height: 1.6; border-radius: 12px;}
.stButton > button {
    height: 3rem; border-radius: 12px; font-weight: 600;
    transition: transform .08s ease, box-shadow .15s ease;
}
.stButton > button:hover {transform: translateY(-1px); box-shadow: 0 4px 12px rgba(0,0,0,.12);}
.result-label {font-size: .85rem; font-weight: 600; opacity: .7; margin-bottom: .25rem;}
[data-testid="stCode"] pre, [data-testid="stCode"] code {
    font-family: "Source Sans", "Noto Sans KR", "Malgun Gothic", "Yu Gothic", sans-serif !important;
    font-size: 1.05rem; line-height: 1.7; white-space: pre-wrap;
}
@media (max-width: 640px) {
    .block-container {padding-top: 4rem;}
    .stMarkdown p.app-title {font-size: 1.6rem;}
}
</style>
"""


def inject_css() -> None:
    st.markdown(CSS, unsafe_allow_html=True)


def render_header() -> None:
    st.markdown(
        '<p class="app-title">🌐 AI 번역기</p>'
        '<p class="app-sub">글을 입력하고 번역할 언어를 선택하세요. 입력 언어는 자동으로 감지됩니다.</p>',
        unsafe_allow_html=True,
    )


def render_input() -> str:
    text = st.text_area(
        "번역할 글",
        height=200,
        max_chars=MAX_CHARS,
        placeholder="번역할 글을 입력하세요",
        label_visibility="collapsed",
    )
    st.caption(f"{len(text):,} / {MAX_CHARS:,}자")
    return text


def render_buttons() -> str | None:
    """눌린 버튼의 언어 이름(한글)을 반환한다. 아무것도 안 눌렸으면 None."""
    clicked = None
    for col, name in zip(st.columns(3), LANGUAGES):
        if col.button(BUTTON_LABELS[name], use_container_width=True, key=f"btn_{name}"):
            clicked = name
    return clicked


def render_result(language: str | None, text: str) -> None:
    st.divider()
    if language is None:
        st.info("버튼을 눌러 번역하세요.", icon="👆")
        return
    if not text.strip():
        st.warning("번역할 글을 입력해 주세요.", icon="✍️")
        return
    try:
        with st.spinner(f"{language}로 번역 중..."):
            result = translate(text, LANGUAGES[language])
    except TranslationError as e:
        st.error(str(e), icon="⚠️")
        return
    except Exception:
        st.error("알 수 없는 오류가 발생했습니다. 잠시 후 다시 시도해 주세요.", icon="⚠️")
        return
    with st.container(border=True):
        st.markdown(f'<div class="result-label">{language} 번역 결과</div>', unsafe_allow_html=True)
        st.code(result, language=None, wrap_lines=True)


def main() -> None:
    st.set_page_config(page_title="AI 번역기", page_icon="🌐", layout="centered")
    inject_css()
    render_header()
    text = render_input()
    language = render_buttons()
    render_result(language, text)


main()
