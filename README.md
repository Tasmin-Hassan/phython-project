
# Tasmin AI

Tasmin AI is a simple personal chatbot created using Python.

The main purpose of this project is to answer questions
about Tasmin Hassan using saved information.

## Language
Python

## Libraries
- Streamlit
- JSON
- difflib

## Features
- Simple chatbot interface
- Ask questions in English or Bangla
- Save new information
- View saved information
- Clear chat history

## How It Works
1. The user asks a question.
2. The chatbot checks the saved questions.
3. It finds the most similar question.
4. It displays the saved answer.
5. If no suitable answer is found, it shows a default message.

## How to Run

Install the required library:

pip install -r requirements.txt

Start the chatbot:

streamlit run app.py

Open the local address shown in the terminal.

## Future Improvements
- Add voice input
- Add a better search system
- Add a login system
- Connect an AI model
- Support PDF files

## Note
This is a simple knowledge-based chatbot.
It is not a fully trained AI model.
