import os

import streamlit as st

from groq import Groq

# Initialize Groq client (DO NOT hardcode keys)
api_key = os.getenv("GROQ_API_KEY")
if not api_key:
    st.error("Missing `GROQ_API_KEY`. Set it in your environment (or a local `.env`).")
    st.stop()

client = Groq(api_key=api_key)

# Streamlit page configuration

st.set_page_config(page_title="Chat with Groq", page_icon="💬")

st.title("💬 Chat Application")

st.caption("Powered by Groq LLaMA 3.3 70B")

# Initialize chat history in session state

if "messages" not in st.session_state:

    st.session_state.messages = []

# Display chat history

for message in st.session_state.messages:

    with st.chat_message(message["role"]):

        st.markdown(message["content"])

# Chat input

if prompt := st.chat_input("What would you like to know?"):

    # Add user message to chat history

    st.session_state.messages.append({"role": "user", "content": prompt})

    

    # Display user message

    with st.chat_message("user"):

        st.markdown(prompt)

    

    # Get assistant response

    with st.chat_message("assistant"):

        with st.spinner("Thinking..."):

            chat_completion = client.chat.completions.create(

                messages=st.session_state.messages,

                model="llama-3.3-70b-versatile",

                temperature=0.7,

                max_tokens=1024,

            )

            

            response = chat_completion.choices[0].message.content

            st.markdown(response)

    

    # Add assistant response to chat history

    st.session_state.messages.append({"role": "assistant", "content": response})

# Add a sidebar with options

with st.sidebar:

    st.header("Settings")

    

    if st.button("Clear Chat History"):

        st.session_state.messages = []

        st.rerun()

    

    st.divider()

    st.caption(
        "This chat application uses Groq's LLaMA 3.3 70B model for fast, high-quality responses."
    )