import streamlit as st
import re
from prompts import (
    get_input_prompt,
    get_task_plan_prompt,
    get_output_prompt,
    get_quiz_answers_prompt,
)
from utils import get_openai_response

st.set_page_config(page_title="LearnUp!", page_icon="📘")
st.title("📘 LearnUp! – Your Exam Revision AI Agent")

if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

if "last_topic" not in st.session_state:
    st.session_state.last_topic = ""

if "last_quiz" not in st.session_state:
    st.session_state.last_quiz = ""

user_input = st.text_input("Ask a revision question (e.g., 'Quiz me on photosynthesis'):")

if st.button("Submit"):
    if user_input:
        # 1. Understand user input intent and topic
        input_prompt = get_input_prompt(user_input)
        parsed = get_openai_response(input_prompt, expect_json=True)
        topic = parsed.get("topic", user_input)
        intent = parsed.get("intent", "summary").lower()
        st.session_state.last_topic = topic

        # 2. Based on intent, handle quiz or general prompt
        if "quiz" in intent:
            final_prompt = get_output_prompt(topic, intent, "")
            output = get_openai_response(final_prompt)
            st.session_state.last_quiz = output
        else:
            plan_prompt = get_task_plan_prompt(topic, intent)
            task_plan = get_openai_response(plan_prompt)
            final_prompt = get_output_prompt(topic, intent, task_plan)
            output = get_openai_response(final_prompt)

        st.session_state.chat_history.append((user_input, output))

# Show conversation history
for q, a in reversed(st.session_state.chat_history):
    st.markdown(f"**🧑 You:** {q}")
    st.markdown(f"**🤖 LearnUp:** {a}")


# If there's a quiz in memory, allow showing answers
if st.session_state.last_quiz:
    if st.button("Show Answers"):
        answer_prompt = get_quiz_answers_prompt(
            st.session_state.last_quiz, st.session_state.last_topic
    )
    raw_answers = get_openai_response(answer_prompt)

    # Add spacing between questions and answers using Markdown formatting
    formatted_answers = re.sub(r'(?<=\d\.)', '\n', raw_answers)  # newline after question number
    formatted_answers = re.sub(r'(?<=\))(?=\s)', '\n', formatted_answers)  # newline after option label
    formatted_answers = re.sub(r'Answer:', '\n**✅ Answer:**', formatted_answers)  # bold answer label
    formatted_answers = formatted_answers.strip()

    st.markdown("### ✅ Quiz Answers:")
    st.markdown(formatted_answers, unsafe_allow_html=True)

