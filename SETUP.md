# 🚀 GraphyBOOK Setup Guide

## Prerequisites

1. **Python 3.8+** installed on your system
2. **Ollama** for local LLM support
3. **FFmpeg** for video processing (required by Manim)

## Installation Steps

### 1. Clone and Setup
```bash
git clone <your-repo-url>
cd GRAPHYBOOK
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Install System Dependencies

**macOS:**
```bash
brew install ffmpeg
```

**Ubuntu/Debian:**
```bash
sudo apt update
sudo apt install ffmpeg
```

**Windows:**
Download FFmpeg from https://ffmpeg.org/download.html and add to PATH

### 3. Setup Ollama

**Install Ollama:**
```bash
# macOS/Linux
curl -fsSL https://ollama.ai/install.sh | sh

# Windows: Download from https://ollama.ai/download
```

**Start Ollama and pull a model:**
```bash
ollama serve
ollama pull qwen:4b  # Recommended lightweight model
# or
ollama pull llama2:7b  # Alternative option
```

### 4. Test Installation

**Test Manim:**
```bash
python demo_examples.py
```

**Test Ollama connection:**
```bash
curl http://localhost:11434/api/tags
```

### 5. Run the Application

```bash
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Select AI Model**: Choose from available Ollama models
2. **Enter Prompt**: Describe your physics animation
3. **Generate**: Watch AI create code in real-time
4. **Edit**: Modify the generated code if needed
5. **Export**: Download your animation video

## Example Prompts

- "A red ball bouncing on the ground"
- "Simple pendulum swinging back and forth"
- "Sine wave propagating from left to right"
- "Two circles colliding elastically"
- "Projectile motion with parabolic trajectory"

## Troubleshooting

**Ollama not responding:**
- Check if Ollama service is running: `ollama serve`
- Verify model is installed: `ollama list`

**Manim errors:**
- Ensure FFmpeg is installed and in PATH
- Check Python version compatibility (3.8+)
- Verify all dependencies are installed

**Streamlit issues:**
- Clear browser cache
- Restart the application
- Check console for error messages

## Configuration

**Model Selection:**
Edit the default model in `app.py`:
```python
selected_model = st.selectbox("Choose AI Model:", ollama_models)
```

**Quality Settings:**
Modify quality options in `agents.py`:
```python
quality_settings = {
    "480p": "-ql",
    "720p": "-qm", 
    "1080p": "-qh"
}
```

## Development

**Project Structure:**
```
GRAPHYBOOK/
├── app.py              # Main Streamlit app
├── prompt_engine.py    # AI workflow engine
├── agents.py          # Code execution
├── prompts/           # AI templates
├── demo_examples.py   # Sample animations
└── requirements.txt   # Dependencies
```

**Adding New Features:**
1. Modify prompt templates in `prompts/`
2. Extend agents in `agents.py`
3. Update UI in `app.py`

## Support

For issues or questions:
1. Check the troubleshooting section
2. Review Manim documentation: https://docs.manim.community/
3. Check Ollama documentation: https://ollama.ai/docs

---

**Happy animating! 🎬✨**