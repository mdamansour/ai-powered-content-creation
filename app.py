"""
AI-Powered Educational Content Creation Tool
Main Streamlit Application
"""
import streamlit as st
from pathlib import Path
import sys

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from config.settings import get_settings
from config.api_keys import APIConfig
from utils.project_manager import ProjectManager
from ui.research_interface import ResearchInterface
from ui.workflow_pages import render_scenario_page, render_scripts_page, render_visualization_page


# Page configuration
st.set_page_config(
    page_title="AI Educational Content Creator",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)


def initialize_session_state():
    """Initialize Streamlit session state variables."""
    if 'current_project' not in st.session_state:
        st.session_state.current_project = None
    if 'project_manager' not in st.session_state:
        st.session_state.project_manager = ProjectManager()
    if 'current_page' not in st.session_state:
        st.session_state.current_page = "home"
    if 'api_configured' not in st.session_state:
        st.session_state.api_configured = APIConfig.is_configured()


def render_sidebar():
    """Render the sidebar navigation."""
    with st.sidebar:
        st.title("🎓 AI Content Creator")
        st.markdown("---")
        
        # API Configuration Status
        if st.session_state.api_configured:
            st.success("✓ API Configured")
            provider = APIConfig.get_active_provider()
            st.caption(f"Using: {provider.upper()}")
        else:
            st.error("⚠ API Not Configured")
            if st.button("Configure API"):
                st.session_state.current_page = "settings"
        
        st.markdown("---")
        
        # Navigation
        st.subheader("Navigation")
        
        if st.button("🏠 Home", use_container_width=True):
            st.session_state.current_page = "home"
        
        if st.button("➕ New Project", use_container_width=True):
            st.session_state.current_page = "new_project"
        
        if st.button("📂 Open Project", use_container_width=True):
            st.session_state.current_page = "open_project"
        
        if st.session_state.current_project:
            st.markdown("---")
            st.subheader("Current Project")
            st.info(f"**{st.session_state.current_project['title']}**")
            
            if st.button("📊 Project Dashboard", use_container_width=True):
                st.session_state.current_page = "dashboard"
        
        st.markdown("---")
        
        if st.button("⚙️ Settings", use_container_width=True):
            st.session_state.current_page = "settings"
        
        if st.button("❓ Help", use_container_width=True):
            st.session_state.current_page = "help"
        
        # Footer
        st.markdown("---")
        st.caption("v0.1.0 - Beta")
        st.caption("Made with ❤️ for educators")


def render_home_page():
    """Render the home page."""
    st.title("🎓 AI-Powered Educational Content Creator")
    st.markdown("### Transform educational content creation from days to hours")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric("Projects", len(st.session_state.project_manager.list_projects()))
    
    with col2:
        completed = len(st.session_state.project_manager.list_projects(status="completed"))
        st.metric("Completed", completed)
    
    with col3:
        in_progress = len(st.session_state.project_manager.list_projects(status="in_progress"))
        st.metric("In Progress", in_progress)
    
    st.markdown("---")
    
    # Quick Start
    st.subheader("🚀 Quick Start")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        #### Create Your First Video
        
        1. **Select a Topic** - Choose from math or physics topics
        2. **AI Research** - Let AI gather and organize information
        3. **Design Visuals** - AI suggests animations and visualizations
        4. **Generate Script** - AI creates synchronized narration
        5. **Record Voice** - Use built-in recording studio
        6. **Mix Audio** - Add music and sound effects
        7. **Compile Video** - Automated video production
        8. **Export & Share** - Download your finished video
        """)
        
        if st.button("➕ Create New Project", type="primary", use_container_width=True):
            st.session_state.current_page = "new_project"
    
    with col2:
        st.markdown("""
        #### Key Features
        
        - 🤖 **AI-Powered Research** - Automatic topic expansion
        - 🎨 **Multi-Library Visuals** - Manim, Matplotlib, Plotly
        - 📝 **Smart Scripts** - Synchronized narration
        - 🎙️ **Audio Studio** - Recording & mixing
        - 🎬 **Auto Production** - One-click video compilation
        - 💾 **Project Management** - Save and reuse
        """)
        
        if st.button("📖 View Documentation", use_container_width=True):
            st.session_state.current_page = "help"
    
    st.markdown("---")
    
    # Recent Projects
    st.subheader("📁 Recent Projects")
    
    projects = st.session_state.project_manager.list_projects()
    
    if projects:
        for project in projects[:5]:  # Show last 5
            with st.expander(f"**{project['title']}** - {project['topic']}"):
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.write(f"**Status:** {project['status']}")
                    st.write(f"**Level:** {project['level']}")
                
                with col2:
                    st.write(f"**Scenes:** {project['scene_count']}")
                    st.write(f"**Updated:** {project['updated_at'][:10]}")
                
                with col3:
                    if st.button("Open", key=f"open_{project['project_id']}"):
                        st.session_state.current_project = st.session_state.project_manager.load_project(
                            project['project_id']
                        )
                        st.session_state.current_page = "dashboard"
                        st.rerun()
    else:
        st.info("No projects yet. Create your first project to get started!")


def render_new_project_page():
    """Render the new project creation page."""
    st.title("➕ Create New Project")
    
    with st.form("new_project_form"):
        st.subheader("Project Details")
        
        title = st.text_input(
            "Project Title",
            placeholder="e.g., Understanding Projectile Motion"
        )
        
        topic = st.text_input(
            "Topic",
            placeholder="e.g., Projectile Motion"
        )
        
        level = st.selectbox(
            "Educational Level",
            ["high_school", "university", "mixed"],
            index=2
        )
        
        col1, col2 = st.columns(2)
        
        with col1:
            duration = st.number_input(
                "Target Duration (minutes)",
                min_value=1,
                max_value=60,
                value=10
            )
        
        with col2:
            st.write("")  # Spacing
        
        submitted = st.form_submit_button("Create Project", type="primary", use_container_width=True)
        
        if submitted:
            if not title or not topic:
                st.error("Please fill in all required fields")
            else:
                # Create project
                project = st.session_state.project_manager.create_project(
                    title=title,
                    topic=topic,
                    level=level
                )
                
                st.session_state.current_project = project
                st.success(f"✓ Project '{title}' created successfully!")
                st.info("Proceeding to AI Research phase...")
                
                # Navigate to dashboard
                st.session_state.current_page = "dashboard"
                st.rerun()


def render_open_project_page():
    """Render the open project page."""
    st.title("📂 Open Project")
    
    projects = st.session_state.project_manager.list_projects()
    
    if not projects:
        st.info("No projects found. Create a new project to get started!")
        if st.button("➕ Create New Project"):
            st.session_state.current_page = "new_project"
        return
    
    # Filter options
    col1, col2 = st.columns([2, 1])
    
    with col1:
        search = st.text_input("🔍 Search projects", placeholder="Search by title or topic...")
    
    with col2:
        status_filter = st.selectbox(
            "Filter by status",
            ["all", "draft", "in_progress", "completed"]
        )
    
    # Filter projects
    filtered_projects = projects
    
    if search:
        filtered_projects = [
            p for p in filtered_projects
            if search.lower() in p['title'].lower() or search.lower() in p['topic'].lower()
        ]
    
    if status_filter != "all":
        filtered_projects = [p for p in filtered_projects if p['status'] == status_filter]
    
    st.markdown("---")
    
    # Display projects
    if filtered_projects:
        for project in filtered_projects:
            with st.container():
                col1, col2, col3, col4 = st.columns([3, 2, 2, 1])
                
                with col1:
                    st.markdown(f"### {project['title']}")
                    st.caption(f"Topic: {project['topic']}")
                
                with col2:
                    status_color = {
                        "draft": "🟡",
                        "in_progress": "🔵",
                        "completed": "🟢"
                    }
                    st.write(f"{status_color.get(project['status'], '⚪')} {project['status']}")
                    st.caption(f"Level: {project['level']}")
                
                with col3:
                    st.write(f"📊 {project['scene_count']} scenes")
                    st.caption(f"Updated: {project['updated_at'][:10]}")
                
                with col4:
                    if st.button("Open", key=f"open_{project['project_id']}", use_container_width=True):
                        st.session_state.current_project = st.session_state.project_manager.load_project(
                            project['project_id']
                        )
                        st.session_state.current_page = "dashboard"
                        st.rerun()
                
                st.markdown("---")
    else:
        st.info("No projects match your search criteria")


def render_dashboard_page():
    """Render the project dashboard."""
    if not st.session_state.current_project:
        st.warning("No project selected. Please open or create a project.")
        return
    
    project = st.session_state.current_project
    
    st.title(f"📊 {project['title']}")
    st.caption(f"Topic: {project['topic']} | Level: {project.get('level', 'mixed')}")
    
    # Progress indicators
    stats = st.session_state.project_manager.get_project_statistics(project['project_id'])
    
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Completion", f"{stats['completion_percentage']}%")
    
    with col2:
        st.metric("Scenes", stats['scene_count'])
    
    with col3:
        duration_min = stats['total_duration'] // 60
        st.metric("Duration", f"{duration_min}m")
    
    with col4:
        st.metric("Status", project['status'])
    
    st.markdown("---")
    
    # Workflow steps
    st.subheader("📋 Workflow")
    
    steps = [
        ("Research", stats['has_research'], "research"),
        ("Scenario", stats['has_scenario'], "scenario"),
        ("Scripts", stats['has_scripts'], "scripts"),
        ("Visualizations", stats['has_scenario'], "visualizations"),
        ("Audio", stats['has_audio'], "audio"),
        ("Video", stats['has_video'], "video")
    ]
    
    cols = st.columns(len(steps))
    
    for i, (step_name, completed, step_id) in enumerate(steps):
        with cols[i]:
            if completed:
                st.success(f"✓ {step_name}")
            else:
                st.info(f"○ {step_name}")
            
            if st.button(f"Go to {step_name}", key=f"goto_{step_id}", use_container_width=True):
                if step_id == "research":
                    st.session_state.current_page = "research"
                    st.rerun()
                elif step_id == "scenario":
                    st.session_state.current_page = "scenario"
                    st.rerun()
                elif step_id == "scripts":
                    st.session_state.current_page = "scripts"
                    st.rerun()
                elif step_id == "visualizations":
                    st.session_state.current_page = "visualizations"
                    st.rerun()
                else:
                    st.info(f"{step_name} module coming soon!")
    
    st.markdown("---")
    
    # Project actions
    st.subheader("🔧 Actions")
    
    col1, col2, col3 = st.columns(3)
    
    with col1:
        if st.button("💾 Save Project", use_container_width=True):
            if st.session_state.project_manager.save_project(project):
                st.success("Project saved!")
    
    with col2:
        if st.button("📤 Export Project", use_container_width=True):
            st.info("Export feature coming soon!")
    
    with col3:
        if st.button("🗑️ Delete Project", use_container_width=True):
            st.warning("Delete confirmation coming soon!")


def render_research_page():
    """Render the research page for AI-powered topic research."""
    if not st.session_state.current_project:
        st.warning("No project selected. Please open or create a project.")
        if st.button("➕ Create New Project"):
            st.session_state.current_page = "new_project"
        return
    
    project = st.session_state.current_project
    
    st.title(f"🔬 Research: {project['title']}")
    st.caption(f"Topic: {project['topic']}")
    
    # Check if research already exists
    has_research = bool(project.get("research", {}).get("validated_concepts"))
    
    if has_research and 'regenerate_research' not in st.session_state:
        st.info("✅ Research already completed for this project")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👁️ View Research", use_container_width=True):
                st.session_state.view_research = True
        with col2:
            if st.button("🔄 Regenerate Research", use_container_width=True):
                st.session_state.regenerate_research = True
                st.rerun()
        
        if st.session_state.get('view_research'):
            st.markdown("---")
            research_data = project.get("research", {}).get("validated_concepts", {})
            if research_data:
                validated = ResearchInterface.render_research_validation(research_data, project)
                
                if st.button("💾 Save Changes"):
                    project["research"]["validated_concepts"] = validated
                    if st.session_state.project_manager.save_project(project):
                        st.success("✅ Research updated!")
        return
    
    # Research workflow
    if 'research_step' not in st.session_state:
        st.session_state.research_step = 1
    
    # Step indicator
    steps = ["Topic Selection", "Generate Research", "Validate & Edit"]
    current_step = st.session_state.research_step
    
    cols = st.columns(len(steps))
    for i, step in enumerate(steps, 1):
        with cols[i-1]:
            if i < current_step:
                st.success(f"✓ {step}")
            elif i == current_step:
                st.info(f"▶ {step}")
            else:
                st.write(f"○ {step}")
    
    st.markdown("---")
    
    # Step 1: Topic Selection
    if current_step == 1:
        topic_info = ResearchInterface.render_topic_selection(project)
        
        if topic_info and st.button("Next: Generate Research →", type="primary"):
            st.session_state.topic_info = topic_info
            st.session_state.research_step = 2
            st.rerun()
    
    # Step 2: Generate Research
    elif current_step == 2:
        topic_info = st.session_state.get('topic_info')
        
        if not topic_info:
            st.error("Topic information missing. Please go back.")
            if st.button("← Back to Topic Selection"):
                st.session_state.research_step = 1
                st.rerun()
            return
        
        research = ResearchInterface.render_research_generation(topic_info, project)
        
        if research:
            st.session_state.research_data = research
            st.session_state.research_step = 3
            st.rerun()
        
        if st.button("← Back to Topic Selection"):
            st.session_state.research_step = 1
            st.rerun()
    
    # Step 3: Validate & Edit
    elif current_step == 3:
        research = st.session_state.get('research_data')
        
        if not research:
            st.error("Research data missing. Please regenerate.")
            if st.button("← Back to Generation"):
                st.session_state.research_step = 2
                st.rerun()
            return
        
        validated = ResearchInterface.render_research_validation(research, project)
        action = ResearchInterface.render_research_actions(validated, project)
        
        if action == "save":
            # Save research to project
            project["research"]["raw_ai_output"] = research
            project["research"]["validated_concepts"] = validated
            project["status"] = "in_progress"
            
            if st.session_state.project_manager.save_project(project):
                st.success("✅ Research saved successfully!")
                st.info("Proceeding to Scenario Design...")
                
                # Clean up session state
                if 'research_step' in st.session_state:
                    del st.session_state.research_step
                if 'topic_info' in st.session_state:
                    del st.session_state.topic_info
                if 'research_data' in st.session_state:
                    del st.session_state.research_data
                if 'regenerate_research' in st.session_state:
                    del st.session_state.regenerate_research
                
                # Navigate to dashboard
                st.session_state.current_page = "dashboard"
                st.rerun()
        
        elif action == "regenerate":
            st.session_state.research_step = 2
            if 'research_data' in st.session_state:
                del st.session_state.research_data
            st.rerun()
        
        elif action == "export":
            import json
            research_json = json.dumps(validated, indent=2)
            st.download_button(
                "📥 Download Research JSON",
                research_json,
                file_name=f"{project['title']}_research.json",
                mime="application/json"
            )
        
        elif action == "cancel":
            # Reset to step 1
            st.session_state.research_step = 1
            if 'research_data' in st.session_state:
                del st.session_state.research_data
            st.rerun()


def render_settings_page():
    """Render the settings page."""
    st.title("⚙️ Settings")
    
    tab1, tab2, tab3 = st.tabs(["API Configuration", "Model Selection", "About"])
    
    with tab1:
        st.subheader("API Configuration")
        
        provider = st.selectbox(
            "AI Provider",
            ["gemini", "openai", "anthropic"],
            index=0
        )
        
        api_key = st.text_input(
            f"{provider.upper()} API Key",
            type="password",
            value=APIConfig.get_api_key(provider) or ""
        )
        
        if st.button("Save API Key"):
            if api_key:
                APIConfig.set_api_key(provider, api_key)
                st.session_state.api_configured = True
                st.success("API key saved!")
            else:
                st.error("Please enter an API key")
        
        st.markdown("---")
        st.info("""
        **Getting API Keys:**
        - **Gemini**: Visit [Google AI Studio](https://makersuite.google.com/app/apikey)
        - **OpenAI**: Visit [OpenAI Platform](https://platform.openai.com/api-keys)
        - **Anthropic**: Visit [Anthropic Console](https://console.anthropic.com/)
        """)
    
    with tab2:
        st.subheader("Model Selection")
        
        if not st.session_state.api_configured:
            st.warning("⚠️ Please configure your API key first in the API Configuration tab.")
        else:
            try:
                from core.ai_engine import AIEngine, GeminiModelRegistry
                
                # Get current provider
                provider = APIConfig.get_active_provider()
                
                if provider == "gemini":
                    st.markdown("### Available Gemini Models")
                    
                    # Get available models
                    api_key = APIConfig.get_api_key("gemini")
                    if not api_key:
                        st.error("API key not found. Please configure it first.")
                        return
                    available_models = GeminiModelRegistry.get_available_models(api_key)
                    
                    if available_models:
                        # Display models in expandable sections
                        for model in available_models:
                            with st.expander(f"**{model['name']}** - {model['id']}"):
                                st.write(f"**Description:** {model['description']}")
                                st.write(f"**Max Tokens:** {model['max_tokens']:,}")
                                st.write(f"**Vision Support:** {'✓' if model['supports_vision'] else '✗'}")
                                st.write(f"**Best For:** {', '.join(model['best_for'])}")
                        
                        st.markdown("---")
                        st.markdown("### Model Recommendations by Task")
                        
                        col1, col2 = st.columns(2)
                        
                        with col1:
                            st.markdown("**📚 Research & Analysis**")
                            research_model = GeminiModelRegistry.recommend_model("research")
                            st.info(f"Recommended: `{research_model}`")
                            
                            st.markdown("**📝 Script Generation**")
                            script_model = GeminiModelRegistry.recommend_model("scripts")
                            st.info(f"Recommended: `{script_model}`")
                        
                        with col2:
                            st.markdown("**🎬 Scenario Design**")
                            scenario_model = GeminiModelRegistry.recommend_model("scenario")
                            st.info(f"Recommended: `{scenario_model}`")
                            
                            st.markdown("**⚡ Quick Tasks**")
                            quick_model = GeminiModelRegistry.recommend_model("quick_tasks")
                            st.info(f"Recommended: `{quick_model}`")
                        
                        st.markdown("---")
                        st.markdown("### Default Model Selection")
                        
                        settings = get_settings()
                        current_default = settings.ai.model
                        
                        model_options = [m['id'] for m in available_models]
                        current_index = model_options.index(current_default) if current_default in model_options else 0
                        
                        selected_model = st.selectbox(
                            "Default Model for All Tasks",
                            model_options,
                            index=current_index,
                            help="This model will be used by default unless you specify a different one for a specific task"
                        )
                        
                        if st.button("Set as Default Model"):
                            # Update settings (note: this is runtime only, doesn't persist to .env)
                            settings.ai.model = selected_model
                            st.success(f"✓ Default model set to: {selected_model}")
                            st.info("💡 Tip: You can still choose different models for specific tasks during content creation")
                    else:
                        st.error("Unable to fetch available models. Please check your API key.")
                
                elif provider == "openai":
                    st.info("OpenAI model selection coming soon!")
                
                elif provider == "anthropic":
                    st.info("Anthropic model selection coming soon!")
                
                else:
                    st.warning("No AI provider configured.")
                    
            except Exception as e:
                st.error(f"Error loading model information: {str(e)}")
                st.info("Make sure your API key is valid and you have internet connection.")
    
    with tab3:
        st.subheader("About")
        st.markdown("""
        ### AI-Powered Educational Content Creator
        **Version:** 0.1.0 (Beta)
        
        A comprehensive tool for creating professional educational videos
        focused on mathematics and physics.
        
        **Features:**
        - AI-powered research and content generation
        - Multi-library visualizations (Manim, Matplotlib, Plotly)
        - Integrated audio recording and mixing
        - Automated video compilation
        
        **Documentation:** See USER_GUIDE.md
        
        **Support:** GitHub Issues
        
        Made with ❤️ for educators worldwide
        """)


def render_help_page():
    """Render the help page."""
    st.title("❓ Help & Documentation")
    
    tab1, tab2, tab3 = st.tabs(["Quick Start", "Features", "Troubleshooting"])
    
    with tab1:
        st.markdown("""
        ### Quick Start Guide
        
        #### 1. Configure API
        - Go to Settings → API Configuration
        - Enter your Gemini API key
        - Save the configuration
        
        #### 2. Create Project
        - Click "New Project"
        - Enter project details
        - Click "Create Project"
        
        #### 3. Follow Workflow
        - **Research**: AI expands your topic
        - **Scenario**: Design visual scenes
        - **Scripts**: Generate narration
        - **Audio**: Record your voice
        - **Video**: Compile final video
        
        For detailed instructions, see the USER_GUIDE.md file.
        """)
    
    with tab2:
        st.markdown("""
        ### Features Overview
        
        #### AI Research
        - Automatic topic expansion
        - Concept identification
        - Formula generation
        - Application suggestions
        
        #### Visualizations
        - **Manim**: Mathematical animations
        - **Matplotlib**: Graphs and plots
        - **Plotly**: 3D interactive visualizations
        
        #### Audio Production
        - Built-in recording studio
        - Noise reduction
        - Background music
        - Sound effects
        
        #### Video Compilation
        - Automated rendering
        - Audio-video sync
        - Multiple export formats
        """)
    
    with tab3:
        st.markdown("""
        ### Troubleshooting
        
        #### API Issues
        - Verify API key is correct
        - Check internet connection
        - Ensure API quota is available
        
        #### Performance Issues
        - Close other applications
        - Reduce video quality settings
        - Clear cache
        
        #### For More Help
        - Check SETUP_GUIDE.md
        - Review TECHNICAL_SPECIFICATION.md
        - Open GitHub issue
        """)


def main():
    """Main application entry point."""
    # Initialize
    initialize_session_state()
    
    # Render sidebar
    render_sidebar()
    
    # Render current page
    page = st.session_state.current_page
    
    if page == "home":
        render_home_page()
    elif page == "new_project":
        render_new_project_page()
    elif page == "open_project":
        render_open_project_page()
    elif page == "dashboard":
        render_dashboard_page()
    elif page == "settings":
        render_settings_page()
    elif page == "research":
        render_research_page()
    elif page == "scenario":
        render_scenario_page(st.session_state.project_manager)
    elif page == "scripts":
        render_scripts_page(st.session_state.project_manager)
    elif page == "visualizations":
        render_visualization_page(st.session_state.project_manager)
    elif page == "help":
        render_help_page()
    else:
        render_home_page()


if __name__ == "__main__":
    main()

# Made with Bob
