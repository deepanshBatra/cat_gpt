import os
import json
import getpass
import streamlit as st
from langchain_core.prompts import ChatPromptTemplate
from langchain_groq import ChatGroq

# Get API Key and handle the input
groq_api = os.environ.get("GROQ_API_KEY")

if 'GROQ_API_KEY' not in os.environ:
    os.environ['GROQ_API_KEY'] = getpass.getpass("Enter your Groq API: ")

# Initialize the LLM and prompt template
template = """
Answer the question below:
Imagine you’re Dandon, a royal cat who reigns over your kingdom of soft pillows and cozy corners. You are the embodiment of calm and sophistication—your days are spent indulging in luxurious naps and savoring your favorite gourmet meals. Nothing ruffles your fur, as you are the picture of chill. You are a queen of serenity, never hurried, always elegant, and above all, content. Answer the following question with the grace and wisdom of a queen, also your owner's name is koko, here is the context: {context}
Question: {question}
"""

llm = ChatGroq(api_key=groq_api, temperature=0, model="mixtral-8x7b-32768")

prompt = ChatPromptTemplate.from_template(template)

chain = prompt | llm

# Function to load conversation history
def load_conversation_history(filename="conversation_history_dandon.json"):
    if os.path.exists(filename):
        with open(filename, "r") as file:
            try:
                return json.load(file)
            except json.JSONDecodeError:
                return {}  # Return an empty dictionary if file is empty/corrupted
    else:
        # Create the file with an empty JSON object if it doesn't exist
        with open(filename, "w") as file:
            json.dump({}, file)
        return {}

# Function to save conversation history
def save_conversation_history(history, filename="conversation_history_dandon.json"):
    with open(filename, "w") as file:
        json.dump(history, file, indent=4)

# Streamlit UI setup
st.set_page_config(page_title="Chat with AI", page_icon="🤖", initial_sidebar_state="collapsed")

# Initialize session state for conversation history and context
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = load_conversation_history()
    st.session_state.context = ""

# Display title
col1, col2 = st.columns([1, 7])  # Adjust the width ratio as needed
with col1:
    st.image("dandon.webp", width=80)  # Adjust width as needed
with col2:
    st.markdown("<h1 style='display: flex; align-items: center;'>Chat with Dandon 🐱</h1>", unsafe_allow_html=True)

# User input for question
user_input = st.text_input("You:", "")

# Handle user input
if user_input:
    if user_input.lower() == "exit":
        st.write("Session ended.")
    else:
        # Process the new question through the Groq AI model
        result = chain.invoke({"context": st.session_state.context, "question": user_input})
        st.write(f"Dandon: {result.content}")

        # Save the new conversation entry
        st.session_state.conversation_history[user_input] = result.content

        # Update the context with the new user input and bot response
        st.session_state.context += f"\nUser: {user_input}\nAI: {result.content}"

        # Save the updated conversation history
        save_conversation_history(st.session_state.conversation_history)
