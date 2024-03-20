from dotenv import load_dotenv
load_dotenv()

import streamlit as st
import os
import google.generativeai as genai

genai.configure(api_key=os.getenv("google_api_key"))

# Default generation configuration (modify values as desired)
default_generation_config = {
    'temperature': 0.7,
    'top_p': 0.9,
    'top_k': 40,
    'max_output_tokens': 2048
}

def get_user_generation_config():
    # Create sliders and a text input for user control
    with st.sidebar:
        temperature = st.slider('Temperature', min_value=0.0, max_value=1.0, step=0.1, value=default_generation_config['temperature'])
        top_p = st.slider('Top P', min_value=0.0, max_value=1.0, step=0.01, value=default_generation_config['top_p'])
        top_k = st.number_input('Top K', min_value=0, value=default_generation_config['top_k'])
        max_tokens = st.number_input('Max Output Tokens', min_value=1, value=default_generation_config['max_output_tokens'])
    return {
        'temperature': temperature,
        'top_p': top_p,
        'top_k': top_k,
        'max_output_tokens': max_tokens
    }

## Function to load Gemini pro model and get response
def get_gemini_response(question, generation_config):
    model = genai.GenerativeModel(model_name='gemini-1.0-pro', generation_config=generation_config)
    chat = model.start_chat(history=[])
    response = chat.send_message(question, stream=True)
    return response

# Initialize our Streamlit app
st.title("Q&A Chatbot with Gemini Pro")
st.header("Gemini LLM Application")

# Create a horizontal container for layout
container = st.container()
col1, col2 = container.columns(2)

# Initialize chat history if not already initialized
if 'chat_history' not in st.session_state:
    st.session_state['chat_history'] = []

# User-defined generation configuration (place in sidebar to hide)
user_generation_config = get_user_generation_config()

# User input and chat history (centered)
with col1:
    user_input = st.text_input("Input: ", key="input")
    submit = st.button("Ask the question")

with col2:
    if 'chat_history' in st.session_state:
        #st.subheader('The chat history is')
        for role, text in st.session_state['chat_history']:
            st.write(f'{role} : {text}')

if submit and user_input:
    response = get_gemini_response(user_input, user_generation_config)

    # Add user query and response to session chat history
    st.session_state['chat_history'].append(('you', user_input))
    st.subheader('The Response is')

    for chunk in response:
        st.write(chunk.text)
        st.session_state['chat_history'].append(('bot', chunk.text))

if 'chat_history' in st.session_state:
    st.subheader('The chat history is')
    for role, text in st.session_state['chat_history']:
        st.write(f'{role} : {text}')
