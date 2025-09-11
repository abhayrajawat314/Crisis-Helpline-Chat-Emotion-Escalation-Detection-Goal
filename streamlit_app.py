import streamlit as st
import requests

# Backend API URL (FastAPI running on localhost)
API_URL = "http://localhost:8000/predict"
RESET_URL = "http://localhost:8000/reset"

# Initialize Streamlit session state for conversation history and input
if "conversation_history" not in st.session_state:
    st.session_state.conversation_history = []
if "current_message" not in st.session_state:
    st.session_state.current_message = ""

st.title("Crisis Helpline Escalation Detection")

# Button to Reset Conversation
if st.button("Reset Conversation"):
    requests.post(RESET_URL)
    st.session_state.conversation_history = []
    st.session_state.current_message = ""
    st.success("Conversation history reset.")

# Select Speaker
speaker = st.selectbox("Who is sending the message?", ["user", "consultant"])

# Message Input
message = st.text_area(
    "Enter message text:",
    value=st.session_state.current_message,
    key="message_input",
    height=100
)

# Send Message Button
if st.button("Send Message"):
    if not message.strip():
        st.warning("Please enter a message.")
    else:
        # POST to the FastAPI backend
        response = requests.post(API_URL, json={"speaker": speaker, "text": message})
        
        if response.status_code == 200:
            result = response.json()
            
            # Append message to conversation history
            st.session_state.conversation_history.append({"speaker": speaker, "text": message})
            
            # Clear the text area
            st.session_state.current_message = ""
            
            # Display full conversation (read-only)
            st.subheader("Conversation History")
            for turn in st.session_state.conversation_history:
                st.markdown(f"**{turn['speaker'].capitalize()}**: {turn['text']}")
            
            # Display prediction result
            st.subheader("Model Output")
            st.json(result)
        else:
            st.error("Error contacting the backend API.")
