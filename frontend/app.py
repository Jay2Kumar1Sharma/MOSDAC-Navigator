import streamlit as st
import requests

st.set_page_config(page_title="MOSDAC AI Help Bot", page_icon="🛰️", layout="wide")

API_URL = "http://127.0.0.1:8000/query"

st.title("🛰️ MOSDAC AI Help Bot")
st.caption("Your intelligent assistant for navigating MOSDAC data and services")

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello! I am an AI assistant powered by the content of the MOSDAC website. How can I help you?"}
    ]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Ask about satellites, data products, or documentation..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        message_placeholder = st.empty()
        message_placeholder.markdown("Thinking... 🧠")
        
        try:
            response = requests.post(API_URL, json={"query": prompt}, timeout=120)
            response.raise_for_status()
            full_response = response.json()["answer"]
            message_placeholder.markdown(full_response)
        except requests.exceptions.RequestException as e:
            full_response = f"Error: Could not connect to the backend. Please ensure it's running. Details: {e}"
            message_placeholder.error(full_response)

    st.session_state.messages.append({"role": "assistant", "content": full_response})