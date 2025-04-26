import streamlit as st
import requests
import uuid
import pyperclip

FASTAPI_URL = "http://127.0.0.1:8000/query/"

# Custom CSS for Better UI
st.markdown("""
    <style>
        .feedback-container {
            display: flex;
            gap: 10px;
            margin-top: 5px;
        }
        .feedback-button {
            border: none;
            padding: 6px 12px;
            cursor: pointer;
            border-radius: 5px;
            font-size: 14px;
        }
        .like { background-color: #4CAF50; color: white; }
        .dislike { background-color: #FF5733; color: white; }
        .regenerate { background-color: #3498DB; color: white; }
        .copy { background-color: #555; color: white; }
        .feedback-area { margin-top: 10px; }
    </style>
""", unsafe_allow_html=True)

st.title("InfoGPT: Ask with Context. Get Real-Time Answers")

# Initialize session state
if 'threads' not in st.session_state:
    st.session_state.threads = {}
if 'current_thread_id' not in st.session_state:
    st.session_state.current_thread_id = None
if 'show_feedback' not in st.session_state:
    st.session_state.show_feedback = {}
if 'copied' not in st.session_state:
    st.session_state.copied = {}

def copy_answer(index):
    latest_answer = st.session_state.threads[st.session_state.current_thread_id][index]["answer"]
    pyperclip.copy(latest_answer)
    st.session_state[f"copied_{index}"] = True

def create_new_chat():
    new_thread_id = str(uuid.uuid4())
    st.session_state.threads[new_thread_id] = []
    st.session_state.current_thread_id = new_thread_id
    st.success(f"New chat created with Thread ID: {new_thread_id}")
    st.info("You are starting a new conversation. No previous memory is available.")

if st.button("Start a New Chat"):
    create_new_chat()

# Sidebar Chat History
with st.sidebar:
    st.header("Chat History")
    if st.session_state.threads:
        thread_list = [f"Thread {tid[:8]}" for tid in st.session_state.threads.keys()]
        selected_thread = st.selectbox("Select an Existing Chat", ["Select a Thread"] + thread_list)
        if selected_thread != "Select a Thread":
            selected_thread_id = list(st.session_state.threads.keys())[thread_list.index(selected_thread)]
            st.session_state.current_thread_id = selected_thread_id
    else:
        st.info("No threads available. Start a new chat.")

if st.session_state.current_thread_id:
    st.subheader(f"Active Chat Thread ID: {st.session_state.current_thread_id}")

# Input Area
user_query = st.text_input("Ask a Question:", placeholder="Type your question here...")

if st.button("Submit Question"):
    if not st.session_state.current_thread_id:
        st.error("Please create or select a chat before asking a question.")
    elif user_query:
        response = requests.post(FASTAPI_URL, json={"query": user_query, "config": {"thread_id": st.session_state.current_thread_id}})
        response_data = response.json()
        st.write("🔍 Debug - Raw Backend Response:", response_data)

        if response.status_code == 200:
            # Safely fetch response content
            agent_response = response_data.get("response") or response_data.get("message") or "[No response received from backend]"
            st.session_state.threads[st.session_state.current_thread_id].append({
                "question": user_query,
                "answer": agent_response,
                "feedback": None
            })
            st.session_state.show_feedback[len(st.session_state.threads[st.session_state.current_thread_id]) - 1] = False
            st.success("Your question has been answered.")
        else:
            st.error(f"Error: {response.status_code}")
    else:
        st.error("Please enter a question before submitting.")

# Display Conversation History
if st.session_state.current_thread_id:
    st.subheader("Conversation History")
    for index, qna in enumerate(st.session_state.threads[st.session_state.current_thread_id]):
        with st.expander(f"Question: {qna['question']}"):
            st.write(f"✅ **Answer:** {qna['answer']}")

            col1, col2, col3, col4 = st.columns(4)
            with col1:
                if st.button("👍 Like", key=f"like_{index}"):
                    st.session_state.threads[st.session_state.current_thread_id][index]["feedback"] = "like"
                    st.success("You liked the response!")

            with col2:
                if st.button("👎 Dislike", key=f"dislike_{index}"):
                    st.session_state.threads[st.session_state.current_thread_id][index]["feedback"] = "dislike"
                    st.session_state.show_feedback[index] = True
                    st.rerun()

            with col3:
                if st.button("📋 Copy", key=f"copy_{index}"):
                    copy_answer(index)
                    st.success("Copied to clipboard!")

            if st.session_state.show_feedback.get(index, False):
                feedback_text = st.text_area("Provide Feedback:", key=f"feedback_{index}")
                with col4:
                    if st.button("♻️ Regenerate", key=f"regenerate_{index}"):
                        new_query = f"{qna['question']} | Feedback: {feedback_text if feedback_text else 'Needs improvement'}"
                        response = requests.post(FASTAPI_URL, json={"query": new_query, "config": {"thread_id": st.session_state.current_thread_id}})
                        if response.status_code == 200:
                            regen_data = response.json()
                            new_answer = regen_data.get("response") or regen_data.get("message") or "[Regenerated response missing]"
                            st.session_state.threads[st.session_state.current_thread_id][index]["answer"] = new_answer
                            st.success("New response generated!")
                            st.rerun()
                        else:
                            st.error("Error in regenerating response.")

# Chat Controls
if st.session_state.current_thread_id:
    if st.button("Erase Chat"):
        st.session_state.threads[st.session_state.current_thread_id] = []
        st.success("Chat history cleared.")
        st.rerun()
    if st.button("Delete Chat"):
        del st.session_state.threads[st.session_state.current_thread_id]
        st.session_state.current_thread_id = None
        st.success("Thread has been deleted.")
        st.rerun()
