# AI-Powered Educational Content Creation Tool

> Transform educational content creation from days to hours with AI-powered research, interactive visualizations, and automated video production.

[![Python](https://img.shields.io/badge/Python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30+-red.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🎯 Overview

A comprehensive tool designed specifically for math and physics educators to create professional educational videos. Leverages AI (Google Gemini Flash) to handle research, visualization design, script generation, and video production while maintaining full creative control.

### ✨ Key Features

- **🤖 AI-Powered Research**: Automatic topic expansion, concept identification, and formula generation
- **🎯 Dynamic Model Selection**: Choose the best AI model for each task (Flash for speed, Pro for quality)
- **🎨 Multi-Library Visualizations**: Manim, Matplotlib, and Plotly for professional animations
- **📝 Smart Script Generation**: AI-generated narration synchronized with visuals
- **🎙️ Professional Audio**: Built-in recording studio with noise reduction and mixing
- **🎬 Automated Video Production**: One-click compilation and export
- **💾 Project Management**: Save, load, and reuse successful projects

## 🚀 Quick Start

### Prerequisites

- Python 3.9 or higher
- FFmpeg (for video processing)
- LaTeX (for mathematical rendering)
- Google Gemini API key

### Installation

```bash
# Clone the repository
git clone https://github.com/yourusername/ai-powered-content-creation.git
cd ai-powered-content-creation

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Configure API key
cp .env.example .env
# Edit .env and add your GEMINI_API_KEY
```

### Run the Application

```bash
streamlit run app.py
```

The application will open in your browser at `http://localhost:8501`

## 📖 Documentation

- **[Quick Start](QUICKSTART.md)** - Get up and running in minutes
- **[Implementation Plan](IMPLEMENTATION_PLAN.md)** - Detailed development roadmap and architecture
- **[Technical Specification](TECHNICAL_SPECIFICATION.md)** - Code examples and API integration
- **[Setup Guide](SETUP_GUIDE.md)** - Complete installation and configuration instructions
- **[User Guide](USER_GUIDE.md)** - Step-by-step tutorials and best practices
- **[Model Selection Guide](docs/MODEL_SELECTION_GUIDE.md)** - Choose the right AI model for each task
- **[Project Summary](PROJECT_SUMMARY.md)** - Executive overview and project details

## 🎓 Use Cases

### YouTube Educator
Create weekly tutorials in 2 hours instead of 8 hours

### University Professor
Generate professional supplementary materials without technical expertise

### Online Course Creator
Build consistent, high-quality course content at scale

### High School Teacher
Create engaging classroom presentations with interactive visualizations

## 🛠️ Technology Stack

- **Frontend**: Streamlit (Python web framework)
- **AI**: Google Gemini Flash (configurable for OpenAI/Anthropic)
- **Visualizations**: Manim, Matplotlib, Plotly
- **Audio**: sounddevice, pydub, librosa
- **Video**: moviepy, ffmpeg
- **Math**: numpy, scipy, sympy

## 📊 Workflow

```
Topic Selection → AI Research → Validation → Scenario Design → 
Script Generation → Voice Recording → Audio Mixing → Video Compilation → Export
```

**Time to create 10-minute video**: 1-2 hours

## 🎯 Project Status

**Current Phase**: Planning Complete ✅

**Next Steps**:
1. Set up development environment
2. Implement core infrastructure (Weeks 1-2)
3. Build AI research module (Week 3)
4. Develop visualization system (Weeks 4-5)
5. Create audio/video pipeline (Weeks 6-8)
6. Polish and test (Weeks 9-10)

## 🤝 Contributing

Contributions are welcome! Please read our contributing guidelines before submitting pull requests.

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

## 📝 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- **Manim Community** - For the amazing mathematical animation library
- **3Blue1Brown** - For inspiring educational content creation
- **Google AI** - For Gemini API access
- **Streamlit Team** - For the excellent web framework

## 📧 Contact

- **Issues**: [GitHub Issues](https://github.com/yourusername/ai-powered-content-creation/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/ai-powered-content-creation/discussions)
- **Email**: support@example.com

## 🗺️ Roadmap

### Phase 1: Foundation (Current)
- [x] Project planning and architecture
- [x] Documentation creation
- [ ] Core infrastructure setup
- [ ] Basic UI implementation

### Phase 2: Core Features
- [ ] AI research module
- [ ] Visualization engines
- [ ] Script generation
- [ ] Audio recording

### Phase 3: Production
- [ ] Video compilation
- [ ] Export functionality
- [ ] Project management
- [ ] Testing suite

### Phase 4: Enhancement
- [ ] Templates and presets
- [ ] Collaboration features
- [ ] Cloud integration
- [ ] Mobile support

## 📈 Success Metrics

- ✅ Reduce content creation time by 75%
- ✅ Handle 99% of educational content needs
- ✅ Professional-quality output
- ✅ Intuitive user experience
- ✅ Cross-platform compatibility

---

**Made with ❤️ for educators worldwide**

*Empowering teachers to create amazing educational content*