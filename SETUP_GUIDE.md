# Setup Guide - AI Educational Content Creator

## Prerequisites

### System Requirements

- **Operating System**: Windows 10/11, macOS 10.15+, or Linux
- **Python**: 3.9 or higher
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space
- **Microphone**: For voice recording
- **GPU**: Optional, for faster rendering

### Required Software

1. **Python 3.9+**
   - Download from [python.org](https://www.python.org/downloads/)
   - Ensure pip is installed

2. **FFmpeg**
   - **Windows**: Download from [ffmpeg.org](https://ffmpeg.org/download.html)
   - **macOS**: `brew install ffmpeg`
   - **Linux**: `sudo apt-get install ffmpeg`

3. **LaTeX** (for Manim mathematical rendering)
   - **Windows**: Install MiKTeX from [miktex.org](https://miktex.org/)
   - **macOS**: `brew install --cask mactex`
   - **Linux**: `sudo apt-get install texlive-full`

## Installation Steps

### 1. Clone or Download the Project

```bash
git clone https://github.com/yourusername/ai-powered-content-creation.git
cd ai-powered-content-creation
```

### 2. Create Virtual Environment

```bash
# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate
```

### 3. Install Python Dependencies

Create a `requirements.txt` file with the following content:

```txt
# Core Framework
streamlit>=1.30.0
python-dotenv>=1.0.0

# AI Integration
google-generativeai>=0.3.0

# Visualization Libraries
manim>=0.18.0
matplotlib>=3.8.0
plotly>=5.18.0
numpy>=1.24.0
scipy>=1.11.0
sympy>=1.12

# Audio Processing
sounddevice>=0.4.6
pydub>=0.25.1
librosa>=0.10.1
soundfile>=0.12.1

# Video Processing
moviepy>=1.0.3
ffmpeg-python>=0.2.0

# Data Validation
pydantic>=2.5.0

# Image Processing
pillow>=10.1.0

# Utilities
aiofiles>=23.2.1
```

Install dependencies:

```bash
pip install -r requirements.txt
```

### 4. Configure API Keys

Create a `.env` file in the project root:

```bash
# .env
GEMINI_API_KEY=your_gemini_api_key_here

# Optional: Other AI providers
OPENAI_API_KEY=your_openai_key_here
ANTHROPIC_API_KEY=your_anthropic_key_here

# Application Settings
APP_ENV=development
LOG_LEVEL=INFO
CACHE_ENABLED=true

# Paths
PROJECTS_DIR=data/projects
ASSETS_DIR=assets
CACHE_DIR=.cache
```

**Getting API Keys:**

1. **Google Gemini API Key**:
   - Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
   - Sign in with your Google account
   - Click "Create API Key"
   - Copy the key to your `.env` file

2. **OpenAI API Key** (optional):
   - Visit [OpenAI Platform](https://platform.openai.com/api-keys)
   - Create an account or sign in
   - Generate a new API key

3. **Anthropic API Key** (optional):
   - Visit [Anthropic Console](https://console.anthropic.com/)
   - Sign up and generate an API key

### 5. Create Project Structure

Create the following directory structure:

```
ai-powered-content-creation/
├── app.py
├── requirements.txt
├── .env
├── .gitignore
├── config/
│   ├── __init__.py
│   ├── settings.py
│   └── api_keys.py
├── core/
│   ├── __init__.py
│   ├── ai_engine.py
│   ├── topic_processor.py
│   ├── scenario_generator.py
│   └── script_generator.py
├── visualization/
│   ├── __init__.py
│   ├── manim_renderer.py
│   ├── matplotlib_renderer.py
│   ├── plotly_renderer.py
│   └── visualization_manager.py
├── audio/
│   ├── __init__.py
│   ├── recorder.py
│   ├── processor.py
│   └── mixer.py
├── video/
│   ├── __init__.py
│   ├── renderer.py
│   └── exporter.py
├── ui/
│   ├── __init__.py
│   ├── components.py
│   ├── topic_selection.py
│   ├── research_validation.py
│   ├── scenario_editor.py
│   ├── script_editor.py
│   ├── recording_studio.py
│   └── preview_player.py
├── utils/
│   ├── __init__.py
│   ├── file_manager.py
│   ├── project_manager.py
│   ├── cache_manager.py
│   └── helpers.py
├── assets/
│   ├── music/
│   ├── sounds/
│   └── templates/
├── data/
│   └── projects/
├── tests/
│   ├── __init__.py
│   ├── test_ai_engine.py
│   ├── test_visualization.py
│   ├── test_audio.py
│   └── test_video.py
└── docs/
    ├── USER_GUIDE.md
    ├── API_REFERENCE.md
    └── EXAMPLES.md
```

You can create this structure manually or use this Python script:

```python
import os

directories = [
    "config", "core", "visualization", "audio", "video", "ui", "utils",
    "assets/music", "assets/sounds", "assets/templates",
    "data/projects", "tests", "docs"
]

for directory in directories:
    os.makedirs(directory, exist_ok=True)
    init_file = os.path.join(directory.split('/')[0], "__init__.py")
    if not os.path.exists(init_file) and directory.split('/')[0] not in ['assets', 'data', 'docs']:
        open(init_file, 'a').close()

print("Project structure created successfully!")
```

### 6. Create .gitignore

Create a `.gitignore` file:

```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
venv/
env/
ENV/

# Environment variables
.env
.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# Project specific
data/projects/
.cache/
temp_*
*.mp4
*.wav
*.mp3

# OS
.DS_Store
Thumbs.db

# Logs
*.log
```

## Running the Application

### Development Mode

```bash
# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Run Streamlit app
streamlit run app.py
```

The application will open in your default browser at `http://localhost:8501`

### Production Mode

For production deployment, use:

```bash
streamlit run app.py --server.port=8501 --server.address=0.0.0.0
```

## Troubleshooting

### Common Issues

#### 1. FFmpeg Not Found

**Error**: `FileNotFoundError: [Errno 2] No such file or directory: 'ffmpeg'`

**Solution**:
- Ensure FFmpeg is installed and in your system PATH
- Test with: `ffmpeg -version`
- On Windows, add FFmpeg to PATH manually

#### 2. LaTeX Not Found (Manim)

**Error**: `LaTeX Error: File not found`

**Solution**:
- Install LaTeX distribution (MiKTeX, MacTeX, or TeX Live)
- Restart your terminal after installation
- Test with: `latex --version`

#### 3. Audio Device Not Found

**Error**: `sounddevice.PortAudioError: No input device found`

**Solution**:
- Check microphone is connected
- Grant microphone permissions to terminal/Python
- List devices: `python -c "import sounddevice as sd; print(sd.query_devices())"`

#### 4. Manim Rendering Slow

**Solution**:
- Use lower quality settings: `quality="low_quality"`
- Enable GPU acceleration if available
- Reduce animation complexity

#### 5. API Rate Limits

**Error**: `429 Too Many Requests`

**Solution**:
- Implement exponential backoff
- Use caching for repeated requests
- Consider upgrading API plan

#### 6. Memory Issues

**Error**: `MemoryError` or system slowdown

**Solution**:
- Close other applications
- Reduce video resolution
- Process scenes individually
- Increase system RAM

### Testing Installation

Run this test script to verify installation:

```python
# test_installation.py
import sys

def test_imports():
    """Test all required imports"""
    try:
        import streamlit
        print("✓ Streamlit installed")
        
        import google.generativeai
        print("✓ Google Generative AI installed")
        
        import manim
        print("✓ Manim installed")
        
        import matplotlib
        print("✓ Matplotlib installed")
        
        import plotly
        print("✓ Plotly installed")
        
        import sounddevice
        print("✓ Sounddevice installed")
        
        import pydub
        print("✓ Pydub installed")
        
        import moviepy
        print("✓ MoviePy installed")
        
        print("\n✓ All dependencies installed successfully!")
        return True
        
    except ImportError as e:
        print(f"\n✗ Import error: {e}")
        return False

def test_ffmpeg():
    """Test FFmpeg installation"""
    import subprocess
    try:
        result = subprocess.run(['ffmpeg', '-version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print("✓ FFmpeg is installed")
            return True
    except FileNotFoundError:
        print("✗ FFmpeg not found in PATH")
        return False

def test_latex():
    """Test LaTeX installation"""
    import subprocess
    try:
        result = subprocess.run(['latex', '--version'], 
                              capture_output=True, 
                              text=True)
        if result.returncode == 0:
            print("✓ LaTeX is installed")
            return True
    except FileNotFoundError:
        print("✗ LaTeX not found in PATH")
        return False

if __name__ == "__main__":
    print("Testing installation...\n")
    
    imports_ok = test_imports()
    ffmpeg_ok = test_ffmpeg()
    latex_ok = test_latex()
    
    if imports_ok and ffmpeg_ok and latex_ok:
        print("\n✓ Installation complete and verified!")
        sys.exit(0)
    else:
        print("\n✗ Installation incomplete. Please fix the issues above.")
        sys.exit(1)
```

Run the test:

```bash
python test_installation.py
```

## Configuration Options

### Visualization Settings

Edit `config/settings.py` to customize:

```python
VISUALIZATION_SETTINGS = {
    "manim_quality": "medium_quality",  # low_quality, medium_quality, high_quality
    "matplotlib_dpi": 100,
    "plotly_width": 800,
    "plotly_height": 600
}
```

### Audio Settings

```python
AUDIO_SETTINGS = {
    "sample_rate": 44100,
    "channels": 1,  # Mono
    "noise_reduction": True,
    "normalize": True
}
```

### Video Settings

```python
VIDEO_SETTINGS = {
    "resolution": (1920, 1080),  # Full HD
    "fps": 30,
    "bitrate": "5000k",
    "codec": "libx264"
}
```

### AI Settings

```python
AI_SETTINGS = {
    "provider": "gemini",
    "model": "gemini-1.5-flash-latest",
    "temperature": 0.7,
    "max_tokens": 8000
}
```

## Performance Optimization

### 1. Enable Caching

Set in `.env`:
```
CACHE_ENABLED=true
```

### 2. Use GPU Acceleration

For Manim rendering, ensure you have:
- CUDA-capable GPU (NVIDIA)
- CUDA toolkit installed
- PyTorch with CUDA support

### 3. Parallel Processing

The application automatically uses parallel processing for:
- Multiple scene rendering
- Audio processing
- Video encoding

### 4. Resource Management

Monitor resource usage:
```bash
# Check memory usage
python -c "import psutil; print(f'RAM: {psutil.virtual_memory().percent}%')"

# Check disk space
python -c "import shutil; print(f'Disk: {shutil.disk_usage('/').percent}%')"
```

## Docker Deployment (Optional)

### Build Docker Image

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

EXPOSE 8501

CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

Build and run:

```bash
# Build image
docker build -t ai-content-creator .

# Run container
docker run -p 8501:8501 -v $(pwd)/data:/app/data ai-content-creator
```

### Docker Compose

Create `docker-compose.yml`:

```yaml
version: '3.8'

services:
  app:
    build: .
    ports:
      - "8501:8501"
    volumes:
      - ./data:/app/data
      - ./assets:/app/assets
    environment:
      - GEMINI_API_KEY=${GEMINI_API_KEY}
    restart: unless-stopped
```

Run with:

```bash
docker-compose up -d
```

## Security Best Practices

### 1. API Key Management

- Never commit `.env` file to version control
- Use environment variables in production
- Rotate API keys regularly
- Set up API key restrictions in provider console

### 2. User Data Protection

- Encrypt sensitive project data
- Implement user authentication for multi-user setups
- Regular backups of project data
- Secure file upload validation

### 3. Network Security

- Use HTTPS in production
- Implement rate limiting
- Set up firewall rules
- Monitor for suspicious activity

## Backup and Recovery

### Backup Projects

```bash
# Create backup
tar -czf backup_$(date +%Y%m%d).tar.gz data/projects/

# Restore backup
tar -xzf backup_20260618.tar.gz
```

### Automated Backup Script

```python
# backup.py
import os
import shutil
from datetime import datetime

def backup_projects():
    backup_dir = "backups"
    os.makedirs(backup_dir, exist_ok=True)
    
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    backup_name = f"projects_backup_{timestamp}"
    
    shutil.make_archive(
        os.path.join(backup_dir, backup_name),
        'zip',
        'data/projects'
    )
    
    print(f"Backup created: {backup_name}.zip")

if __name__ == "__main__":
    backup_projects()
```

## Updating the Application

### Update Dependencies

```bash
# Update all packages
pip install --upgrade -r requirements.txt

# Update specific package
pip install --upgrade streamlit
```

### Update Application Code

```bash
# Pull latest changes
git pull origin main

# Reinstall dependencies if needed
pip install -r requirements.txt

# Restart application
streamlit run app.py
```

## Getting Help

### Resources

- **Documentation**: Check `docs/` folder
- **Examples**: See `docs/EXAMPLES.md`
- **API Reference**: See `docs/API_REFERENCE.md`

### Support Channels

- GitHub Issues: Report bugs and feature requests
- Discussions: Ask questions and share ideas
- Email: support@example.com

### Logging

Enable detailed logging:

```python
# In .env
LOG_LEVEL=DEBUG
```

View logs:

```bash
# Application logs
tail -f app.log

# Streamlit logs
streamlit run app.py --logger.level=debug
```

## Next Steps

After successful installation:

1. **Read the User Guide**: `docs/USER_GUIDE.md`
2. **Try Examples**: `docs/EXAMPLES.md`
3. **Create Your First Project**: Follow the tutorial
4. **Customize Settings**: Adjust configurations to your needs
5. **Explore Features**: Test all modules

## Conclusion

You now have a fully functional AI-powered educational content creation tool! The setup process ensures all dependencies are properly installed and configured for optimal performance.

For detailed usage instructions, proceed to the User Guide.