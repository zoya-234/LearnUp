def get_input_prompt(user_input):
    return (
        f"Please extract the topic and intent from this text. "
        f"Return either as JSON like {{\"topic\": \"...\", \"intent\": \"...\"}} "
        f"or as: topic, intent.\n"
        f"Text: \"{user_input}\""
    )

def get_task_plan_prompt(topic, intent):
    return (
        f"Create a short, clear 3-step teaching plan for the topic '{topic}' "
        f"using the method '{intent}'. Use simple language with line breaks."
    )

def get_output_prompt(topic, intent, task_plan):
    intent = intent.lower()

    quiz_intents = ["quiz", "test knowledge", "generate quiz questions", "request quiz questions", "write quiz questions"]

    if any(q in intent for q in quiz_intents):
        return build_final_prompt(f"quiz me on {topic}")
    
    elif "summary" in intent:
        return (
            f"You are LearnUp, an expert tutor. Summarize the topic '{topic}' in simple academic language "
            f"that even a beginner can understand. Use clear line breaks and add helpful emojis."
        )
    
    else:
        return (
            f"You are LearnUp, a friendly tutor. Write a short helpful note about '{topic}' "
            f"in clear, accessible language."
        )

def build_final_prompt(user_input):
    topic = user_input.strip().replace("quiz me on", "").strip()
    return (
        f"You are LearnUp, a friendly expert tutor. "
        f"Your job is to help a student review the topic '{topic}'.\n\n"
        f"Please create exactly 3 multiple-choice questions about {topic}, each with 4 options (a, b, c, d). "
        f"Make the questions clear and academic. Use emojis to make it student-friendly. "
        f"Start with a warm greeting like 'Hi there! 📘 Let's test your knowledge!'\n\n"
        f"Format each question on a new line with options clearly listed."
    )

def get_quiz_answers_prompt(questions_text, topic):
    return (
        f"You previously generated the following quiz questions on the topic '{topic}':\n\n"
        f"{questions_text}\n\n"
        f"Now, please list the correct answer for each question with a brief explanation. "
        f"Use this format:\n"
        f"Q1: b) Answer – because ...\nQ2: c) Answer – because ...\n"
    )


