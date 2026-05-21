import streamlit as st
import os
from utils.resume_parser import extract_text_from_pdf
from utils.chatbot import load_gemini_model, generate_response
from utils.voice_clone import clone_voice
from utils.prompts import INTERVIEW_QUESTIONS
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Page Config
st.set_page_config(page_title="AI Voice Clone Interview Bot", layout="wide")

# Custom Styling
st.markdown("""
    <style>
    .main {
        background-color: #f8f9fa;
    }
    .stButton>button {
        width: 100%;
        border-radius: 5px;
        height: 3em;
        background-color: #4CAF50;
        color: white;
    }
    </style>
    """, unsafe_allow_html=True)

# Application Title
st.title("🎙️ AI Voice Clone Interview Bot")
st.subheader("An AI version of you that answers interview questions in your own voice")

# Sidebar Instructions
with st.sidebar:
    st.header("How to Use")
    st.info("""
    1. **Upload Resume**: Help the AI learn about you.
    2. **Upload Voice**: Provide a 10-20 sec sample of your voice.
    3. **Set API Key**: Enter your Google Gemini API Key.
    4. **Select Question**: Pick a question and hit generate!
    """)
    st.divider()
    api_key_input = st.text_input("Gemini API Key", type="password", help="Get one at aistudio.google.com")

# Initialize Session State
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""

# Step 1 & 2: File Uploads
col1, col2 = st.columns(2)

with col1:
    st.header("1. Upload Resume")
    resume_file = st.file_uploader("Upload PDF Resume", type=["pdf"])
    if resume_file:
        with st.spinner("Extracting resume data..."):
            st.session_state.resume_text = extract_text_from_pdf(resume_file)
            st.success("Resume processed!")

with col2:
    st.header("2. Upload Voice Sample")
    voice_file = st.file_uploader("Upload Voice (WAV/MP3)", type=["wav", "mp3"])
    if voice_file:
        # Save voice file locally for reference
        if not os.path.exists("data"):
            os.makedirs("data")
        voice_path = os.path.join("data", "user_voice.wav")
        with open(voice_path, "wb") as f:
            f.write(voice_file.getbuffer())
        st.success("Voice sample saved!")

st.divider()

# Step 3: Question Selection
st.header("3. Select Your Question")
selected_question = st.selectbox("Choose a question:", INTERVIEW_QUESTIONS + ["Custom Question"])

custom_q = ""
if selected_question == "Custom Question":
    custom_q = st.text_input("Enter your custom question:")

final_question = custom_q if selected_question == "Custom Question" else selected_question

# Step 4: Generate Answer
if st.button("Generate AI Answer"):
    # Error Handling for missing inputs
    if not api_key_input and not os.getenv("GOOGLE_API_KEY"):
        st.error("Please provide a Gemini API Key in the sidebar or .env file.")
    elif not st.session_state.resume_text:
        st.error("Please upload your resume first.")
    elif not voice_file:
        st.error("Please upload a voice sample first.")
    elif selected_question == "Custom Question" and not custom_q:
        st.error("Please enter a custom question.")
    else:
        with st.spinner("Generating personalized response..."):
            # Load Gemini
            model = load_gemini_model(api_key_input)
            if model:
                # Generate text response
                response_text = generate_response(model, st.session_state.resume_text, final_question)
                
                # Update Chat History
                st.session_state.chat_history.append({"question": final_question, "answer": response_text})
                
                st.write("### AI Response:")
                st.write(response_text)
                
                # Clone Voice
                with st.spinner("Cloning your voice and generating audio..."):
                    if not os.path.exists("outputs"):
                        os.makedirs("outputs")
                    output_audio_path = os.path.join("outputs", "response_voice.wav")
                    
                    # Call TTS
                    success = clone_voice(response_text, os.path.join("data", "user_voice.wav"), output_audio_path)
                    
                    if success:
                        st.audio(output_audio_path, format="audio/wav")
                        st.success("Voice cloned successfully!")
                    else:
                        st.error("Voice generation failed. Check terminal for errors.")
            else:
                st.error("Failed to initialize Gemini. Check your API Key.")

# Chat History Section
if st.session_state.chat_history:
    with st.expander("View Chat History"):
        for chat in reversed(st.session_state.chat_history):
            st.write(f"**Q:** {chat['question']}")
            st.write(f"**A:** {chat['answer']}")
            st.divider()
