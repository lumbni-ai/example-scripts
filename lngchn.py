import streamlit as st
import os
from langchain.chat_models import init_chat_model
from langchain_core.messages import HumanMessage, AIMessage
from streamlit_chat import message

if not os.environ.get("MISTRAL_API_KEY"):
    os.environ["MISTRAL_API_KEY"] = ""

model = init_chat_model("mistral-large-latest", model_provider="mistralai")

st.title("Mistral LLM Chat Application with Context")

if "messages" not in st.session_state:
    st.session_state.messages = []

if "user_prompts" not in st.session_state:
    st.session_state.user_prompts = []

if "assistant_responses" not in st.session_state:
    st.session_state.assistant_responses = []

for i, msg in enumerate(st.session_state.messages):
    message(msg["content"], is_user=(msg["role"] == "user"), key=f"msg_{i}")

max_tokens = st.sidebar.slider("Select max number of previous tokens to use:", 0, 1000, 5)

prompt_input = st.chat_input("Type your query here...")

if prompt_input:
    user_message = {"role": "user", "content": prompt_input}
    st.session_state.messages.append(user_message)
    message(prompt_input, is_user=True, key=f"user_{len(st.session_state.messages)-1}")

    if max_tokens > 0:
        context_messages = st.session_state.messages[-max_tokens:]
    else:
        context_messages = [user_message]

    response = model.invoke(context_messages)

    assistant_message = {"role": "assistant", "content": response.content}
    st.session_state.messages.append(assistant_message)
    message(response.content, key=f"assistant_{len(st.session_state.messages)-1}")

    st.session_state.user_prompts.append(prompt_input)
    st.session_state.assistant_responses.append(response.content)

if st.button("Clear Chat"):
    st.session_state.messages.clear()
    st.session_state.user_prompts.clear()
    st.session_state.assistant_responses.clear()

st.sidebar.title("Chat History")
st.sidebar.subheader("User Prompts")
for prompt in st.session_state.user_prompts:
    st.sidebar.write(prompt)

st.sidebar.subheader("Assistant Responses")
for response in st.session_state.assistant_responses:
    st.sidebar.write(response)
