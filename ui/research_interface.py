"""
Research interface UI components for topic selection and validation.
"""
import streamlit as st
import asyncio
from typing import Dict, Optional, Any
from core.topic_processor import TopicProcessor
from utils.model_selector import ModelSelector


class ResearchInterface:
    """UI components for research workflow."""
    
    @staticmethod
    def render_topic_selection(project: Dict) -> Optional[Dict]:
        """
        Render topic selection interface.
        
        Args:
            project: Current project data
            
        Returns:
            Dict with selected topic info or None
        """
        st.subheader("📚 Topic Selection")
        
        # Get predefined topics
        all_topics = TopicProcessor.get_all_topics()
        
        # Topic input method
        input_method = st.radio(
            "How would you like to select a topic?",
            ["Choose from categories", "Enter custom topic"],
            horizontal=True
        )
        
        selected_topic = None
        
        if input_method == "Choose from categories":
            # Category selection
            col1, col2 = st.columns(2)
            
            with col1:
                category = st.selectbox(
                    "Category",
                    list(all_topics.keys())
                )
            
            with col2:
                topic = st.selectbox(
                    "Topic",
                    all_topics[category]
                )
            
            selected_topic = topic
            
        else:
            # Custom topic input
            custom_topic = st.text_input(
                "Enter your topic",
                value=project.get("topic", ""),
                placeholder="e.g., Projectile Motion, Quadratic Equations"
            )
            
            if custom_topic:
                # Show suggestions
                suggestions = TopicProcessor.get_topic_suggestions(custom_topic)
                if suggestions:
                    st.info(f"💡 Related topics: {', '.join(suggestions[:5])}")
                
                selected_topic = custom_topic
        
        # Educational level
        st.markdown("---")
        level = st.selectbox(
            "Educational Level",
            ["high_school", "university", "mixed"],
            index=["high_school", "university", "mixed"].index(project.get("level", "mixed"))
        )
        
        # Custom instructions
        with st.expander("⚙️ Advanced Options"):
            custom_instructions = st.text_area(
                "Custom Instructions (optional)",
                placeholder="Add any specific requirements or focus areas...",
                height=100
            )
        
        if selected_topic:
            return {
                "topic": selected_topic,
                "level": level,
                "custom_instructions": custom_instructions if custom_instructions else None
            }
        
        return None
    
    @staticmethod
    def render_research_generation(
        topic_info: Dict,
        project: Dict
    ) -> Optional[Dict]:
        """
        Render research generation interface.
        
        Args:
            topic_info: Topic selection info
            project: Current project data
            
        Returns:
            Generated research data or None
        """
        st.subheader("🔬 AI Research Generation")
        
        # Show what will be researched
        st.info(f"""
        **Topic:** {topic_info['topic']}  
        **Level:** {topic_info['level']}  
        **Model:** {ModelSelector.recommend_model('research') or 'Default'}
        """)
        
        # Model selection
        with st.expander("🤖 Model Selection"):
            available_models = ModelSelector.get_available_models()
            if available_models:
                model_ids = [m['id'] for m in available_models]
                recommended = ModelSelector.recommend_model('research')
                default_index = model_ids.index(recommended) if recommended in model_ids else 0
                
                selected_model = st.selectbox(
                    "Choose AI Model",
                    model_ids,
                    index=default_index,
                    help="Flash models are faster, Pro models provide more detailed analysis"
                )
            else:
                selected_model = None
                st.warning("Unable to fetch available models")
        
        # Generate button
        col1, col2 = st.columns([1, 3])
        with col1:
            generate_btn = st.button("🚀 Generate Research", type="primary", use_container_width=True)
        
        if generate_btn:
            with st.spinner("🔍 Researching topic... This may take 10-30 seconds..."):
                try:
                    # Create processor with selected model
                    engine = ModelSelector.get_engine_for_task(
                        "research",
                        custom_model=selected_model if selected_model else None
                    )
                    processor = TopicProcessor(engine=engine)
                    
                    # Generate research
                    research = asyncio.run(
                        processor.generate_research(
                            topic_info['topic'],
                            topic_info['level'],
                            topic_info.get('custom_instructions')
                        )
                    )
                    
                    if research.get("success"):
                        st.success("✅ Research generated successfully!")
                        return research
                    else:
                        st.error(f"❌ Research generation failed: {research.get('error', 'Unknown error')}")
                        return None
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    return None
        
        return None
    
    @staticmethod
    def render_research_validation(research: Dict, project: Dict) -> Dict:
        """
        Render research validation and editing interface.
        
        Args:
            research: Generated research data
            project: Current project data
            
        Returns:
            Validated/edited research data
        """
        st.subheader("✅ Research Validation")
        
        # Validate research structure
        processor = TopicProcessor()
        validation = processor.validate_research(research)
        
        if not validation["valid"]:
            st.warning("⚠️ Research data has some issues:")
            for warning in validation["warnings"]:
                st.write(f"- {warning}")
            if validation["missing_keys"]:
                st.write(f"- Missing keys: {', '.join(validation['missing_keys'])}")
        else:
            st.success("✅ Research data is valid")
        
        # Display research sections
        tabs = st.tabs(["📋 Overview", "💡 Concepts", "📐 Formulas", "🔬 Principles", "🌍 Applications"])
        
        with tabs[0]:  # Overview
            st.markdown(f"### {research.get('title', 'Research Results')}")
            
            col1, col2, col3 = st.columns(3)
            with col1:
                st.metric("Concepts", len(research.get("concepts", [])))
            with col2:
                st.metric("Formulas", len(research.get("formulas", [])))
            with col3:
                st.metric("Principles", len(research.get("principles", [])))
            
            # User notes
            st.markdown("---")
            user_notes = st.text_area(
                "📝 Your Notes",
                value=research.get("user_notes", ""),
                placeholder="Add your notes, modifications, or additional context...",
                height=150
            )
            research["user_notes"] = user_notes
        
        with tabs[1]:  # Concepts
            st.markdown("### Key Concepts")
            concepts = processor.extract_key_concepts(research)
            
            if concepts:
                for i, concept in enumerate(concepts):
                    with st.expander(f"**{concept['name']}**", expanded=i == 0):
                        st.write(f"**Definition:** {concept['definition']}")
                        if concept.get('importance'):
                            st.write(f"**Importance:** {concept['importance']}")
                        
                        # Allow editing
                        if st.checkbox(f"Edit concept {i+1}", key=f"edit_concept_{i}"):
                            concept['name'] = st.text_input("Name", value=concept['name'], key=f"name_{i}")
                            concept['definition'] = st.text_area("Definition", value=concept['definition'], key=f"def_{i}")
                            concept['importance'] = st.text_area("Importance", value=concept.get('importance', ''), key=f"imp_{i}")
            else:
                st.info("No concepts found in research data")
        
        with tabs[2]:  # Formulas
            st.markdown("### Mathematical Formulas")
            formulas = processor.extract_formulas(research)
            
            if formulas:
                for i, formula in enumerate(formulas):
                    with st.expander(f"Formula {i+1}", expanded=i == 0):
                        # Display LaTeX
                        if formula.get('latex'):
                            st.latex(formula['latex'])
                        
                        st.write(f"**Explanation:** {formula.get('explanation', 'N/A')}")
                        
                        # Variables
                        if formula.get('variables'):
                            st.write("**Variables:**")
                            for var, desc in formula['variables'].items():
                                st.write(f"- `{var}`: {desc}")
            else:
                st.info("No formulas found in research data")
        
        with tabs[3]:  # Principles
            st.markdown("### Physical Principles & Laws")
            principles = research.get("principles", [])
            
            if principles:
                for i, principle in enumerate(principles, 1):
                    st.write(f"{i}. {principle}")
            else:
                st.info("No principles found in research data")
        
        with tabs[4]:  # Applications
            st.markdown("### Real-World Applications")
            applications = research.get("applications", [])
            
            if applications:
                for i, app in enumerate(applications, 1):
                    st.write(f"{i}. {app}")
            else:
                st.info("No applications found in research data")
            
            # Misconceptions
            st.markdown("---")
            st.markdown("### ⚠️ Common Misconceptions")
            misconceptions = research.get("misconceptions", [])
            
            if misconceptions:
                for i, misc in enumerate(misconceptions, 1):
                    st.warning(f"{i}. {misc}")
            else:
                st.info("No misconceptions listed")
        
        return research
    
    @staticmethod
    def render_research_actions(research: Dict, project: Dict) -> str:
        """
        Render action buttons for research.
        
        Args:
            research: Research data
            project: Current project data
            
        Returns:
            Action taken ('save', 'regenerate', 'cancel', or '')
        """
        st.markdown("---")
        st.subheader("🎯 Next Steps")
        
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            if st.button("💾 Save & Continue", type="primary", use_container_width=True):
                return "save"
        
        with col2:
            if st.button("🔄 Regenerate", use_container_width=True):
                return "regenerate"
        
        with col3:
            if st.button("📤 Export Research", use_container_width=True):
                return "export"
        
        with col4:
            if st.button("❌ Cancel", use_container_width=True):
                return "cancel"
        
        return ""


# Made with Bob