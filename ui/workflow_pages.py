"""
Workflow pages for scenario and script generation.
"""
import streamlit as st
import asyncio
from typing import Dict
from ui.scenario_interface import ScenarioInterface, ScriptInterface


def render_scenario_page(project_manager):
    """Render the scenario design page."""
    if not st.session_state.current_project:
        st.warning("No project selected. Please open or create a project.")
        if st.button("➕ Create New Project"):
            st.session_state.current_page = "new_project"
        return
    
    project = st.session_state.current_project
    
    # Check if research exists
    research = project.get("research", {}).get("validated_concepts")
    if not research:
        st.warning("⚠️ Please complete the Research phase first")
        if st.button("← Go to Research"):
            st.session_state.current_page = "research"
        return
    
    st.title(f"🎬 Scenario Design: {project['title']}")
    st.caption(f"Topic: {project['topic']}")
    
    # Check if scenario already exists
    has_scenario = len(project.get("scenario", {}).get("scenes", [])) > 0
    
    if has_scenario and 'regenerate_scenario' not in st.session_state:
        st.info("✅ Scenario already created for this project")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👁️ View/Edit Scenario", use_container_width=True):
                st.session_state.view_scenario = True
        with col2:
            if st.button("🔄 Regenerate Scenario", use_container_width=True):
                st.session_state.regenerate_scenario = True
                st.rerun()
        
        if st.session_state.get('view_scenario'):
            st.markdown("---")
            scenario_data = project.get("scenario", {})
            edited = ScenarioInterface.render_scenario_editor(scenario_data, project)
            action = ScenarioInterface.render_scenario_actions(edited, project)
            
            if action == "save":
                project["scenario"] = edited
                if project_manager.save_project(project):
                    st.success("✅ Scenario updated!")
                    if 'view_scenario' in st.session_state:
                        del st.session_state.view_scenario
        return
    
    # Scenario workflow
    if 'scenario_step' not in st.session_state:
        st.session_state.scenario_step = 1
    
    # Step indicator
    steps = ["Generate Scenario", "Edit & Refine"]
    current_step = st.session_state.scenario_step
    
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
    
    # Step 1: Generate Scenario
    if current_step == 1:
        scenario = ScenarioInterface.render_scenario_generation(project, research)
        
        if scenario:
            st.session_state.scenario_data = scenario
            st.session_state.scenario_step = 2
            st.rerun()
    
    # Step 2: Edit & Refine
    elif current_step == 2:
        scenario = st.session_state.get('scenario_data')
        
        if not scenario:
            st.error("Scenario data missing. Please regenerate.")
            if st.button("← Back to Generation"):
                st.session_state.scenario_step = 1
                st.rerun()
            return
        
        edited = ScenarioInterface.render_scenario_editor(scenario, project)
        action = ScenarioInterface.render_scenario_actions(edited, project)
        
        if action == "save":
            # Save scenario to project
            project["scenario"] = edited
            project["status"] = "in_progress"
            
            if project_manager.save_project(project):
                st.success("✅ Scenario saved successfully!")
                st.info("Proceeding to Script Generation...")
                
                # Clean up session state
                for key in ['scenario_step', 'scenario_data', 'regenerate_scenario']:
                    if key in st.session_state:
                        del st.session_state[key]
                
                # Navigate to scripts page
                st.session_state.current_page = "scripts"
                st.rerun()
        
        elif action == "regenerate":
            st.session_state.scenario_step = 1
            if 'scenario_data' in st.session_state:
                del st.session_state.scenario_data
            st.rerun()
        
        elif action == "preview":
            st.markdown("---")
            st.subheader("📺 Scenario Preview")
            for i, scene in enumerate(edited.get("scenes", []), 1):
                with st.expander(f"Scene {i}: {scene.get('title', 'Untitled')}"):
                    ScenarioInterface.render_scene_preview(scene)
        
        elif action == "cancel":
            st.session_state.scenario_step = 1
            if 'scenario_data' in st.session_state:
                del st.session_state.scenario_data
            st.rerun()


def render_scripts_page(project_manager):
    """Render the script generation and editing page."""
    if not st.session_state.current_project:
        st.warning("No project selected. Please open or create a project.")
        if st.button("➕ Create New Project"):
            st.session_state.current_page = "new_project"
        return
    
    project = st.session_state.current_project
    
    # Check if scenario exists
    scenario = project.get("scenario", {})
    scenes = scenario.get("scenes", [])
    
    if not scenes:
        st.warning("⚠️ Please complete the Scenario Design phase first")
        if st.button("← Go to Scenario Design"):
            st.session_state.current_page = "scenario"
        return
    
    st.title(f"📝 Script Generation: {project['title']}")
    st.caption(f"Topic: {project['topic']} | Scenes: {len(scenes)}")
    
    # Check if scripts already exist
    has_scripts = bool(project.get("scripts"))
    
    if has_scripts and 'regenerate_scripts' not in st.session_state:
        st.info("✅ Scripts already generated for this project")
        
        col1, col2 = st.columns(2)
        with col1:
            if st.button("👁️ View/Edit Scripts", use_container_width=True):
                st.session_state.view_scripts = True
        with col2:
            if st.button("🔄 Regenerate Scripts", use_container_width=True):
                st.session_state.regenerate_scripts = True
                st.rerun()
        
        if st.session_state.get('view_scripts'):
            st.markdown("---")
            scripts = project.get("scripts", {})
            research = project.get("research", {}).get("validated_concepts", {})
            edited = ScriptInterface.render_script_editor(scripts, scenes, project)
            
            col1, col2 = st.columns(2)
            with col1:
                if st.button("💾 Save Scripts", type="primary", use_container_width=True):
                    project["scripts"] = edited
                    if project_manager.save_project(project):
                        st.success("✅ Scripts updated!")
                        if 'view_scripts' in st.session_state:
                            del st.session_state.view_scripts
            with col2:
                if st.button("❌ Cancel", use_container_width=True):
                    if 'view_scripts' in st.session_state:
                        del st.session_state.view_scripts
        return
    
    # Scripts workflow
    if 'scripts_step' not in st.session_state:
        st.session_state.scripts_step = 1
    
    # Step indicator
    steps = ["Generate Scripts", "Edit & Refine"]
    current_step = st.session_state.scripts_step
    
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
    
    # Step 1: Generate Scripts
    if current_step == 1:
        research = project.get("research", {}).get("validated_concepts", {})
        scripts = ScriptInterface.render_script_generation(scenes, research, project)
        
        if scripts:
            st.session_state.scripts_data = scripts
            st.session_state.scripts_step = 2
            st.rerun()
    
    # Step 2: Edit & Refine
    elif current_step == 2:
        scripts = st.session_state.get('scripts_data')
        
        if not scripts:
            st.error("Scripts data missing. Please regenerate.")
            if st.button("← Back to Generation"):
                st.session_state.scripts_step = 1
                st.rerun()
            return
        
        edited = ScriptInterface.render_script_editor(scripts, scenes, project)
        
        st.markdown("---")
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("💾 Save & Continue", type="primary", use_container_width=True):
                # Save scripts to project
                project["scripts"] = edited
                project["status"] = "in_progress"
                
                if project_manager.save_project(project):
                    st.success("✅ Scripts saved successfully!")
                    st.info("Ready for Audio Recording phase!")
                    
                    # Clean up session state
                    for key in ['scripts_step', 'scripts_data', 'regenerate_scripts']:
                        if key in st.session_state:
                            del st.session_state[key]
                    
                    # Navigate to dashboard
                    st.session_state.current_page = "dashboard"
                    st.rerun()
        
        with col2:
            if st.button("🔄 Regenerate", use_container_width=True):
                st.session_state.scripts_step = 1
                if 'scripts_data' in st.session_state:
                    del st.session_state.scripts_data
                st.rerun()
        
        with col3:
            if st.button("❌ Cancel", use_container_width=True):
                st.session_state.scripts_step = 1
                if 'scripts_data' in st.session_state:
                    del st.session_state.scripts_data
                st.rerun()


# Made with Bob