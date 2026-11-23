
import streamlit as st
import json
from pathlib import Path
from difflib import SequenceMatcher

# Database file
file_path = Path(__file__).parent / "knowledge.json"


# Load saved information
def load_data():
    if not file_path.exists():
        save_data({"name": "Tasmin Hassan", "facts": []})

    with open(file_path, "r", encoding="utf-8") as file:
        return json.load(file)


# Save information
def save_data(data):
    with open(file_path, "w", encoding="utf-8") as file:
        json.dump(data, file, indent=4, ensure_ascii=False)


# Clean text before comparing
def clean_text(text):
    text = text.lower().strip()

    for mark in ["?", "!", ".", ",", "।"]:
        text = text.replace(mark, "")

    return " ".join(text.split())


# Compare two questions
def check_similarity(text1, text2):
    text1 = clean_text(text1)
    text2 = clean_text(text2)

    return SequenceMatcher(None, text1, text2).ratio()


# Find answer
def get_answer(question, data):
    question = clean_text(question)

    greetings = ["hi", "hello", "hey", "হাই", "হ্যালো"]

    if question in greetings:
        return "Hello! I am Tasmin AI. How can I help you?"

    if question in ["thanks", "thank you", "ধন্যবাদ"]:
        return "You're welcome!"

    best_score = 0
    best_answer = ""

    for item in data["facts"]:
        for saved_question in item["questions"]:
            score = check_similarity(question, saved_question)

            if score > best_score:
                best_score = score
                best_answer = item["answer"]

    if best_score >= 0.55:
        return best_answer

    return "Sorry, I don't know the answer yet. Please teach me from the sidebar."


# Page settings
st.set_page_config(
    page_title="Tasmin AI",
    page_icon="🤖",
    layout="centered"
)

data = load_data()


# Sidebar
with st.sidebar:

    st.title("🤖 Tasmin AI")
    st.write("Personal Information Chatbot")

    st.divider()

    # Add new information
    st.subheader("Add New Information")

    with st.form("add_form", clear_on_submit=True):

        topic = st.text_input("Topic")

        questions_text = st.text_area(
            "Questions",
            placeholder="Write one question per line"
        )

        answer = st.text_area("Answer")

        add_button = st.form_submit_button("Save Information")

        if add_button:
            questions = [
                q.strip()
                for q in questions_text.splitlines()
                if q.strip()
            ]

            if topic.strip() and questions and answer.strip():

                new_info = {
                    "topic": topic.strip(),
                    "questions": questions,
                    "answer": answer.strip()
                }

                data["facts"].append(new_info)
                save_data(data)

                st.success("Information saved successfully!")
                st.rerun()

            else:
                st.warning("Please fill in all fields.")

    st.divider()

    # View information
    st.subheader("Saved Information")

    if len(data["facts"]) == 0:
        st.info("No information saved yet.")

    else:
        for i, item in enumerate(data["facts"]):
            with st.expander(item["topic"]):
                st.write("Questions:")
                for question in item["questions"]:
                    st.write("- " + question)

                st.write("Answer:")
                st.write(item["answer"])

    st.divider()

    # Edit saved information
    st.subheader("Edit Information")

    if len(data["facts"]) > 0:

        edit_index = st.selectbox(
            "Select topic to edit",
            range(len(data["facts"])),
            format_func=lambda i: data["facts"][i]["topic"],
            key="edit_select"
        )

        selected_item = data["facts"][edit_index]

        with st.form("edit_form"):

            new_topic = st.text_input(
                "Edit Topic",
                value=selected_item["topic"]
            )

            new_questions = st.text_area(
                "Edit Questions",
                value="\n".join(selected_item["questions"])
            )

            new_answer = st.text_area(
                "Edit Answer",
                value=selected_item["answer"]
            )

            update_button = st.form_submit_button("Update Information")

            if update_button:
                questions = [
                    q.strip()
                    for q in new_questions.splitlines()
                    if q.strip()
                ]

                if new_topic.strip() and questions and new_answer.strip():

                    data["facts"][edit_index] = {
                        "topic": new_topic.strip(),
                        "questions": questions,
                        "answer": new_answer.strip()
                    }

                    save_data(data)
                    st.success("Information updated!")
                    st.rerun()

                else:
                    st.warning("Please fill in all fields.")

    else:
        st.info("Nothing to edit.")

    st.divider()

    # Delete one saved topic
    st.subheader("Delete Information")

    if len(data["facts"]) > 0:

        delete_index = st.selectbox(
            "Select topic to delete",
            range(len(data["facts"])),
            format_func=lambda i: data["facts"][i]["topic"],
            key="delete_select"
        )

        if st.button("Delete Selected Topic"):
            data["facts"].pop(delete_index)
            save_data(data)

            st.success("Selected topic deleted!")
            st.rerun()

    else:
        st.info("Nothing to delete.")

    st.divider()

    # Delete all saved questions
    st.subheader("Delete All Questions")

    confirm_delete = st.checkbox(
        "I want to delete all saved questions and answers"
    )

    if st.button(
        "Delete All Information",
        disabled=not confirm_delete
    ):
        data["facts"] = []
        save_data(data)

        st.success("All saved information deleted!")
        st.rerun()

    st.divider()

    # Clear chat history
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()


# Main chatbot page
st.title("🤖 Tasmin AI")

st.write("Hello! I am Tasmin AI. Ask me anything about Tasmin Hassan.")

st.divider()


# Chat memory for current session
if "messages" not in st.session_state:
    st.session_state.messages = []


# Show previous messages
for message in st.session_state.messages:

    with st.chat_message(message["role"]):
        st.write(message["content"])


# Chat input
user_question = st.chat_input("Ask me anything...")

if user_question:

    st.session_state.messages.append({
        "role": "user",
        "content": user_question
    })

    with st.chat_message("user"):
        st.write(user_question)

    bot_answer = get_answer(user_question, data)

    st.session_state.messages.append({
        "role": "assistant",
        "content": bot_answer
    })

    with st.chat_message("assistant"):
        st.write(bot_answer)
