import streamlit as st
import requests
import os
from typing import Dict, List
import pandas as pd
import json

# API configuration
API_URL = "https://generativelanguage.googleapis.com/v1beta/models/gemini-pro:generateContent"

# Get API key from environment variable
API_KEY = os.environ.get("GEMINI_API_KEY")

if not API_KEY:
    st.error("API key not found. Please set the GEMINI_API_KEY environment variable.")
    st.stop()

HEADERS = {
    'Content-Type': 'application/json',
    'Authorization': f'Bearer {API_KEY}'
}

def generate_content(prompt: str) -> str:
    try:
        st.write("Generating content...")
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={
                'contents': [{
                    'parts': [{
                        'text': prompt
                    }]
                }]
            }
        )
        response.raise_for_status()
        result = response.json()
        if 'candidates' in result and len(result['candidates']) > 0:
            return result['candidates'][0]['content']['parts'][0]['text']
        return "Error: No content generated"
    except requests.exceptions.RequestException as e:
        st.error(f"API Error: {str(e)}")
        return "Error generating content. Please check the API key and try again."
    except Exception as e:
        st.error(f"Unexpected Error: {str(e)}")
        return "Error generating content. Please try again later."

class Candidate:
    def __init__(self):
        self.name = ""
        self.email = ""
        self.phone = ""
        self.years_experience = 0
        self.desired_positions = []
        self.location = ""
        self.tech_stack = []
        self.technical_responses = {}

class TalentScoutAssistant:
    def __init__(self):
        self.conversation_history = []
        self.candidate = Candidate()
        self.conversation_ended = False

    def generate_greeting(self) -> str:
        prompt = """
        You are a TalentScout Hiring Assistant. Your task is to:
        1. Greet the candidate
        2. Explain your purpose
        3. Guide them through information gathering
        4. Keep the tone professional and friendly
        
        Start the conversation with a warm greeting.
        """
        return generate_content(prompt)

    def gather_candidate_info(self, field: str, value: str) -> str:
        if field == "name":
            self.candidate.name = value
            return "What's your email address?"
        elif field == "email":
            self.candidate.email = value
            return "What's your phone number?"
        elif field == "phone":
            self.candidate.phone = value
            return "How many years of experience do you have?"
        elif field == "years":
            self.candidate.years_experience = int(value)
            return "What positions are you interested in? (e.g., Software Engineer, Data Scientist)"
        elif field == "positions":
            self.candidate.desired_positions = value.split(',')
            return "Where are you currently located?"
        elif field == "location":
            self.candidate.location = value
            return "Please list your tech stack (programming languages, frameworks, tools):"
        elif field == "tech_stack":
            self.candidate.tech_stack = value.split(',')
            return self.generate_technical_questions()

    def generate_technical_questions(self) -> str:
        prompt = f"""
        Generate 3-5 technical questions for a candidate with the following tech stack:
        {', '.join(self.candidate.tech_stack)}
        
        The questions should:
        1. Cover different aspects of their tech stack
        2. Be relevant to their experience level ({self.candidate.years_experience} years)
        3. Include both theoretical and practical aspects
        4. Be clear and concise
        
        Format the questions in a numbered list.
        """
        questions = generate_content(prompt)
        self.candidate.technical_responses['questions'] = questions
        return f"Here are your technical questions:\n{questions}\n\nPlease answer these questions when you're ready."

    def handle_technical_response(self, question_num: int, response: str) -> str:
        self.candidate.technical_responses[f"q{question_num}"] = response
        return "Thank you! Please continue with the next question or type 'done' if finished."

    def end_conversation(self) -> str:
        prompt = f"""
        Generate a professional closing message for the candidate:
        Name: {self.candidate.name}
        Position: {', '.join(self.candidate.desired_positions)}
        Experience: {self.candidate.years_experience} years
        Tech Stack: {', '.join(self.candidate.tech_stack)}
        
        The message should:
        1. Thank them for their time
        2. Summarize their key information
        3. Explain next steps
        """
        return generate_content(prompt)

# Streamlit UI
def main():
    st.title("TalentScout Hiring Assistant")
    
    # Initialize session state
    if 'assistant' not in st.session_state:
        st.session_state.assistant = TalentScoutAssistant()
    
    # Display conversation history
    for msg in st.session_state.assistant.conversation_history:
        st.write(msg)
    
    # Get user input
    user_input = st.text_input("Your message:", "")
    
    if user_input:
        if user_input.lower() == 'exit':
            st.session_state.assistant.conversation_ended = True
            st.write(st.session_state.assistant.end_conversation())
        elif not st.session_state.assistant.candidate.name:
            st.session_state.assistant.candidate.name = user_input
            st.session_state.assistant.conversation_history.append(f"Candidate: {user_input}")
            st.session_state.assistant.conversation_history.append(
                st.session_state.assistant.gather_candidate_info("name", user_input)
            )
        elif not st.session_state.assistant.candidate.email:
            st.session_state.assistant.candidate.email = user_input
            st.session_state.assistant.conversation_history.append(f"Candidate: {user_input}")
            st.session_state.assistant.conversation_history.append(
                st.session_state.assistant.gather_candidate_info("email", user_input)
            )
        elif not st.session_state.assistant.candidate.phone:
            st.session_state.assistant.candidate.phone = user_input
            st.session_state.assistant.conversation_history.append(f"Candidate: {user_input}")
            st.session_state.assistant.conversation_history.append(
                st.session_state.assistant.gather_candidate_info("phone", user_input)
            )
        elif not st.session_state.assistant.candidate.years_experience:
            try:
                years = int(user_input)
                st.session_state.assistant.candidate.years_experience = years
                st.session_state.assistant.conversation_history.append(f"Candidate: {user_input} years")
                st.session_state.assistant.conversation_history.append(
                    st.session_state.assistant.gather_candidate_info("years", str(years))
                )
            except ValueError:
                st.write("Please enter a valid number for years of experience.")
        elif not st.session_state.assistant.candidate.desired_positions:
            st.session_state.assistant.candidate.desired_positions = user_input.split(',')
            st.session_state.assistant.conversation_history.append(f"Candidate: {user_input}")
            st.session_state.assistant.conversation_history.append(
                st.session_state.assistant.gather_candidate_info("positions", user_input)
            )
        elif not st.session_state.assistant.candidate.location:
            st.session_state.assistant.candidate.location = user_input
            st.session_state.assistant.conversation_history.append(f"Candidate: {user_input}")
            st.session_state.assistant.conversation_history.append(
                st.session_state.assistant.gather_candidate_info("location", user_input)
            )
        elif not st.session_state.assistant.candidate.tech_stack:
            st.session_state.assistant.candidate.tech_stack = user_input.split(',')
            st.session_state.assistant.conversation_history.append(f"Candidate: {user_input}")
            st.session_state.assistant.conversation_history.append(
                st.session_state.assistant.gather_candidate_info("tech_stack", user_input)
            )
        else:
            # Handle technical questions
            if user_input.lower() == 'done':
                st.session_state.assistant.conversation_ended = True
                st.write(st.session_state.assistant.end_conversation())
            else:
                # Store technical response
                st.session_state.assistant.conversation_history.append(f"Candidate: {user_input}")
                st.write(st.session_state.assistant.handle_technical_response(len(st.session_state.assistant.candidate.technical_responses), user_input))

if __name__ == "__main__":
    main()
