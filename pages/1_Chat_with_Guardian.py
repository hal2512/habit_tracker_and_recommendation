import streamlit as st
import speech_recognition as sr
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from chatbot import GuardianChatbot

st.set_page_config(page_title="Chat with Consultant", page_icon="💬")

st.title("💬 Chat with The Consultant")
st.markdown("Ask about your habits, get advice, or check your wellness status.")

if "bot" not in st.session_state:
    st.session_state.bot = GuardianChatbot()

if "messages" not in st.session_state:
    st.session_state.messages = [
        {"role": "assistant", "content": "Hello. I am listening. How are you feeling today?"}
    ]

def listen_to_mic():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        st.toast("🎤 Listening... Speak now!")
        try:
            audio = r.listen(source, timeout=5)
            text = r.recognize_google(audio)
            return text
        except sr.WaitTimeoutError:
            st.error("Time out. I didn't hear anything.")
        except sr.UnknownValueError:
            st.warning("I couldn't understand what you said.")
        except sr.RequestError:
            st.error("Network error with Google Speech Recognition.")
    return None

with st.sidebar:
    st.header("🎙️ Voice Interface")
    st.markdown("Click the button and speak into your microphone.")

    if st.button("🎤 Click to Speak", type="primary"):
        user_voice_input = listen_to_mic()
        if user_voice_input:
            st.session_state.messages.append({"role": "user", "content": user_voice_input})

            response = st.session_state.bot.get_response(user_voice_input, current_stats={'sleep_hours': 5},
                                                         is_risk=True)

            st.session_state.messages.append({"role": "assistant", "content": response})
            st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.write(msg["content"])

if prompt := st.chat_input("Type here..."):
    with st.chat_message("user"):
        st.write(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    response = st.session_state.bot.get_response(prompt, current_stats={'sleep_hours': 5}, is_risk=True)

    with st.chat_message("assistant"):
        st.write(response)
    st.session_state.messages.append({"role": "assistant", "content": response})