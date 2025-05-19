# TalentScout Hiring Assistant

An intelligent chatbot assistant for TalentScout recruitment agency that helps in initial candidate screening and technical assessment.

## Features

- Interactive chat interface using Streamlit
- Candidate information gathering (name, contact, experience, etc.)
- Tech stack declaration and validation
- Dynamic technical question generation using Gemini AI
- Context-aware conversation flow
- Secure data handling

## Setup Instructions

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Set up environment variables:
Create a `.env` file in the project root with your Gemini API key:
```
GEMINI_API_KEY=your_api_key_here
```

4. Run the application:
```bash
streamlit run app.py
```

## Usage Guide

1. Open the Streamlit app in your browser
2. The chatbot will greet you and start gathering information
3. Follow the prompts to provide your:
   - Full name
   - Email address
   - Phone number
   - Years of experience
   - Desired positions
   - Current location
   - Tech stack (programming languages, frameworks, tools)
4. The chatbot will generate technical questions based on your tech stack
5. Answer the questions when prompted
6. Type 'done' when you've finished answering questions
7. The chatbot will provide a summary and next steps

## Technical Details

- **Language Model**: Google Gemini Pro
- **Frontend**: Streamlit
- **State Management**: Streamlit session state
- **Data Handling**: In-memory storage (can be extended to database)
- **Prompt Engineering**: Custom prompts for different conversation stages

## Prompt Design

The application uses multiple prompts for different stages:
1. Initial greeting and introduction
2. Information gathering
3. Technical question generation
4. Conversation closing and summary

Each prompt is designed to maintain context and provide clear guidance to the model.

## Security Considerations

- All sensitive information is handled through environment variables
- No persistent storage of candidate data (can be added with proper security measures)
- Input validation for numeric fields (years of experience)

## Optional Enhancements

1. Add database integration for candidate data persistence
2. Implement sentiment analysis
3. Add multilingual support
4. Add resume parsing capabilities
5. Implement candidate scoring system

## License

This project is for educational purposes only. All rights reserved by TalentScout.
