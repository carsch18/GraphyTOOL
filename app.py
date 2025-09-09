# app.py - GraphyBOOK Demo Application

import streamlit as st
import os
import requests
import json
from prompt_engine import run_generation_workflow
from agents import execute_code

# Page configuration
st.set_page_config(
    layout="centered",
    page_title="GraphyBOOK Demo",
    page_icon="🎬"
)

@st.cache_data(ttl=600)
def get_ollama_models():
    """Fetch available Ollama models"""
    try:
        response = requests.get("http://localhost:11434/api/tags")
        response.raise_for_status()
        model_list = response.json().get('models', [])
        return [model.get('name') for model in model_list if model.get('name')]
    except Exception as e:
        st.error(f"Ollama connection failed: {e}")
        return ["qwen:4b"]  # Fallback

# Initialize session state
if 'current_code' not in st.session_state:
    st.session_state.current_code = "# Generated code will appear here..."

# Header
st.title("🎬 GraphyBOOK Demo")
st.markdown("*AI-Powered Physics Animation Studio*")
st.divider()

# Model selection
ollama_models = get_ollama_models()
selected_model = st.selectbox("Choose AI Model:", ollama_models)

# Input section
st.subheader("📝 Create Animation")
prompt = st.text_area(
    "Describe your physics animation:",
    placeholder="Example: A red ball bouncing with gravity",
    height=100
)

generate_button = st.button("🚀 Generate Animation", type="primary", use_container_width=True)

# Main generation workflow
if generate_button and prompt:
    st.divider()
    st.subheader("🧠 AI Generation Process")
    
    # Create placeholders for real-time updates
    status_placeholder = st.empty()
    col_code, col_log = st.columns(2)
    
    with col_code:
        st.info("📝 Live Code Generation")
        code_placeholder = st.empty()
    
    with col_log:
        st.info("📊 Execution Log")
        log_placeholder = st.empty()

    full_code = ""
    
    # Listen to the AI workflow events
    for event_type, data in run_generation_workflow(prompt, selected_model):
        
        if event_type == "status":
            status_placeholder.info(f"🔄 {data}")
        
        elif event_type == "code_chunk":
            full_code += data
            code_placeholder.code(full_code, language="python")
        
        elif event_type == "code_final":
            st.session_state.current_code = data
            
        elif event_type == "success":
            status_placeholder.success("✅ Animation Generated Successfully!")
            st.subheader("🎬 Your Animation")
            st.video(data["path"])
            log_placeholder.text_area("Execution Log", data["log"], height=200)
            break
            
        elif event_type == "failure":
            st.warning(f"⚠️ Attempt {data['attempt']} failed: {data['reason']}")
            log_placeholder.text_area("Error Log", data['log'], height=200)
            
        elif event_type == "final_failure":
            status_placeholder.error(f"❌ {data}")
            break
            
        elif event_type == "error":
            status_placeholder.error(f"💥 Critical Error: {data}")
            break

# Code editor section
st.divider()
st.subheader("✏️ Code Editor")

edited_code = st.text_area(
    "Edit or paste your own Manim code:",
    value=st.session_state.current_code,
    height=300
)

if st.button("▶️ Run Code", use_container_width=True):
    if edited_code.strip() and "Generated code will appear here" not in edited_code:
        with st.spinner("Executing your code..."):
            success, result, log = execute_code(edited_code)
        
        if success:
            st.success("✅ Code executed successfully!")
            st.video(result)
            with st.expander("Show Execution Log"):
                st.text(log)
        else:
            st.error(f"❌ Execution failed: {result}")
            with st.expander("Show Error Log", expanded=True):
                st.text(log)
    else:
        st.warning("Please enter valid Manim code.")

# Footer
st.divider()
st.markdown("""
<div style='text-align: center; color: #666; font-size: 0.8em;'>
    <p>GraphyBOOK Demo - AI Physics Animation Studio</p>
    <p>Built with Streamlit • Manim • Ollama</p>
</div>
""", unsafe_allow_html=True)