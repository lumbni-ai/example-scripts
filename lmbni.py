import streamlit as st
from lumbni_client.client import LumbniClient
from streamlit_chat import message

client = LumbniClient(api_key="", mode="dev")
st.title("Lumbni AI Chat Application")

if "messages" not in st.session_state:
    st.session_state["messages"] = []
    st.session_state["user_prompts"] = []
    st.session_state["assistant_responses"] = []

for msg in st.session_state["messages"]:
    message(msg["content"], is_user=(msg["role"] == "user"))

if prompt_input := st.chat_input("Type your query here..."):
    user_message = {"role": "user", "content": prompt_input}
    st.session_state["messages"].append(user_message)
    message(prompt_input, is_user=True)
    response = client.generate_text(prompt=prompt_input, ref="custom")
    assistant_message = {"role": "assistant", "content": response['data']['outputs'][0]['message']['content']}
    st.session_state["messages"].append(assistant_message)
    message(assistant_message["content"], is_user=False)
    st.session_state["user_prompts"].append(prompt_input)
    st.session_state["assistant_responses"].append(assistant_message["content"])

st.sidebar.title("Chat History")
st.sidebar.subheader("User Prompts")
for prompt in st.session_state["user_prompts"]:
    st.sidebar.write(prompt)

st.sidebar.subheader("Assistant Responses")
for response in st.session_state["assistant_responses"]:
    st.sidebar.write(response)
