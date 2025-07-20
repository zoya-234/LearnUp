import streamlit as st
from prompts import (
    get_input_prompt,
    get_task_plan_prompt,
    get_output_prompt,
    get_quiz_answers_prompt,
)
from utils import get_openai_response

st.set_page_config(page_title="LearnUp!", page_icon="📘")

st.title("📘 LearnUp! – Your Exam Revision AI Chatbot")

# Session state for messages
if "messages" not in st.session_state:
    st.session_state.messages = []

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

if "last_quiz" not in st.session_state:
    st.session_state.last_quiz = ""

# Display chat history
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# Chat input
user_input = st.chat_input("Ask me something (e.g., 'Quiz me on photosynthesis')")

if user_input:
    # Show user message
    st.session_state.messages.append({"role": "user", "content": user_input})
    with st.chat_message("user"):
        st.markdown(user_input)

    # Handle intent + response
    input_prompt = get_input_prompt(user_input)
    parsed = get_openai_response(input_prompt, expect_json=True)

    topic = parsed.get("topic", user_input)
    intent = parsed.get("intent", "summary").lower()
    st.session_state.last_topic = topic

    # Handle quiz or summary
    if "quiz" in intent:
        final_prompt = get_output_prompt(topic, intent, "")
        output = get_openai_response(final_prompt)
        st.session_state.last_quiz = output
    else:
        plan_prompt = get_task_plan_prompt(topic, intent)
        task_plan = get_openai_response(plan_prompt)
        final_prompt = get_output_prompt(topic, intent, task_plan)
        output = get_openai_response(final_prompt)

    # Show bot response
    st.session_state.messages.append({"role": "assistant", "content": output})
    with st.chat_message("assistant"):
        st.markdown(output)

# Option to show quiz answers
if st.session_state.last_quiz:
    with st.expander("✅ Show Quiz Answers"):
        answer_prompt = get_quiz_answers_prompt(
            st.session_state.last_quiz, st.session_state.last_topic
        )
        raw_answers = get_openai_response(answer_prompt)
        formatted = raw_answers.replace("\n", "\n\n")
        st.markdown(formatted)
