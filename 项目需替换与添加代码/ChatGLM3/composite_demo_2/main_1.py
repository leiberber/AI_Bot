import streamlit as st
st.set_page_config(
    page_title="ChatGLM3 Demo",
    page_icon=":robot:",
    layout='wide',
    initial_sidebar_state='expanded',
)


import demo_chat, demo_ci, demo_tool
from enum import Enum

DEFAULT_SYSTEM_PROMPT = '''
You are ChatGLM3, a large language model trained by Zhipu.AI. Follow the user's instructions carefully. Respond using markdown.
'''.strip()

# Set the title of the demo
st.title("ChatGLM3 （DialoChat）")

# Add your custom text here, with smaller font size
st.markdown(
    "<sub>智谱AI 公开在线技术文档: https://lslfd0slxc.feishu.cn/wiki/WvQbwIJ9tiPAxGk8ywDck6yfnof </sub> \n\n <sub> 更多 ChatGLM3-6B 的使用方法请参考文档。</sub>",
    unsafe_allow_html=True)

button_like_link = st.markdown(
    """
    <div style="display: inline-block;
               padding: 10px 20px;
               background-color: #007bff;
               color: white;
               text-align: center;
               font-size: 16px;
               border-radius: 5px;
               box-shadow: 0 4px 6px rgba(50,50,93,.11), 0 1px 3px rgba(0,0,0,.08);">
        <a href="http://10.242.224.109:8540/" target="_blank" style="color: white; text-decoration: none; display: inline-block; margin-right: 10px;">
            切换原始模型
        </a>
        <a href="http://10.242.224.109:8550/" target="_blank" style="color: white; text-decoration: none; display: inline-block;">
            切换微调模型1
        </a>
    </div>
    """,
    unsafe_allow_html=True
)


class Mode(str, Enum):
    CHAT, TOOL, CI = '💬 Chat', '🛠️ Tool', '🧑‍💻 Code Interpreter'


with st.sidebar:
    top_p = st.slider(
        'top_p', 0.0, 1.0, 0.8, step=0.01
    )
    temperature = st.slider(
        'temperature', 0.0, 1.5, 0.95, step=0.01
    )
    repetition_penalty = st.slider(
        'repetition_penalty', 0.0, 2.0, 1.1, step=0.01
    )
    max_new_token = st.slider(
        'Output length', 5, 32000, 256, step=1
    )

    cols = st.columns(2)
    export_btn = cols[0]
    clear_history = cols[1].button("Clear History", use_container_width=True)
    retry = export_btn.button("Retry", use_container_width=True)

    system_prompt = st.text_area(
        label="System Prompt (Only for chat mode)",
        height=300,
        value=DEFAULT_SYSTEM_PROMPT,
    )

prompt_text = st.chat_input(
    'Chat with ChatGLM3!',
    key='chat_input',
)

tab = st.radio(
    'Mode',
    [mode.value for mode in Mode],
    horizontal=True,
    label_visibility='hidden',
)

if clear_history or retry:
    prompt_text = ""

match tab:
    case Mode.CHAT:
        demo_chat.main(
            retry=retry,
            top_p=top_p,
            temperature=temperature,
            prompt_text=prompt_text,
            system_prompt=system_prompt,
            repetition_penalty=repetition_penalty,
            max_new_tokens=max_new_token
        )
    case Mode.TOOL:
        demo_tool.main(
            retry=retry,
            top_p=top_p,
            temperature=temperature,
            prompt_text=prompt_text,
            repetition_penalty=repetition_penalty,
            max_new_tokens=max_new_token,
            truncate_length=1024)
    case Mode.CI:
        demo_ci.main(
            retry=retry,
            top_p=top_p,
            temperature=temperature,
            prompt_text=prompt_text,
            repetition_penalty=repetition_penalty,
            max_new_tokens=max_new_token,
            truncate_length=1024)
    case _:
        st.error(f'Unexpected tab: {tab}')
