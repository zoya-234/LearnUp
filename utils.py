import streamlit as st
import google.generativeai as genai
import json
import traceback


api_key = st.secrets["GEMINI_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel("gemini-2.0-flash")  # Or whichever is available

def get_openai_response(prompt, expect_json=False):
    try:
        print(f"Prompt Sent to Gemini:\n{prompt}\n")

        response = model.generate_content(prompt)
        print("Raw Gemini Response Object:", response)

        if hasattr(response, "text") and response.text:
            text = response.text.strip()
        elif hasattr(response, "parts"):
            text = "\n".join([part.text for part in response.parts if hasattr(part, "text")])
        else:
            text = ""

        print("Parsed Gemini Output:", text)

        if not text:
            return "⚠️ Gemini gave an empty response. Try rewording the prompt."

        if expect_json:
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                print("⚠️ JSON parse error.")
                return {"error": "Could not parse JSON from Gemini output."}

        return text

    except Exception as e:
        print("⚠️ Exception occurred:", str(e))
        print(traceback.format_exc())
        return f"⚠️ Gemini Error: {str(e)}"
