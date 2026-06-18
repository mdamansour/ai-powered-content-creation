"""
Scenario design interface UI components.
"""
import streamlit as st
import asyncio
from typing import Dict, Optional, List, Any
from pathlib import Path
from core.scenario_generator import ScenarioGenerator
from core.script_generator import ScriptGenerator
from utils.model_selector import ModelSelector
from visualization import VisualizationManager, RenderQuality


class ScenarioInterface:
    """UI components for scenario design workflow."""
    
    @staticmethod
    def render_scenario_generation(
        project: Dict,
        research: Dict
    ) -> Optional[Dict]:
        """
        Render scenario generation interface.
        
        Args:
            project: Current project data
            research: Research data
            
        Returns:
            Generated scenario or None
        """
        st.subheader("🎬 Scenario Generation")
        
        # Configuration
        col1, col2 = st.columns(2)
        
        with col1:
            target_duration = st.number_input(
                "Target Video Duration (seconds)",
                min_value=60,
                max_value=1800,
                value=300,
                step=30,
                help="Total duration for all scenes combined"
            )
        
        with col2:
            scene_count = st.number_input(
                "Number of Scenes",
                min_value=3,
                max_value=10,
                value=5,
                help="Suggested number of scenes"
            )
        
        # Custom instructions
        with st.expander("⚙️ Advanced Options"):
            custom_instructions = st.text_area(
                "Custom Instructions (optional)",
                placeholder="E.g., Focus on visual demonstrations, include real-world examples...",
                height=100
            )
            
            # Model selection
            available_models = ModelSelector.get_available_models()
            if available_models:
                model_ids = [m['id'] for m in available_models]
                recommended = ModelSelector.recommend_model('scenario')
                default_index = model_ids.index(recommended) if recommended in model_ids else 0
                
                selected_model = st.selectbox(
                    "AI Model",
                    model_ids,
                    index=default_index,
                    help="Pro models provide more detailed scenarios"
                )
            else:
                selected_model = None
        
        # Generate button
        if st.button("🚀 Generate Scenario", type="primary", use_container_width=True):
            with st.spinner("🎬 Creating visualization scenario... This may take 20-40 seconds..."):
                try:
                    # Create generator with selected model
                    engine = ModelSelector.get_engine_for_task(
                        "scenario",
                        custom_model=selected_model if selected_model else None
                    )
                    generator = ScenarioGenerator(engine=engine)
                    
                    # Generate scenario with scene count
                    scenario = asyncio.run(
                        generator.generate_scenario(
                            research,
                            target_duration,
                            scene_count,  # Pass the scene count from UI
                            custom_instructions if custom_instructions else None
                        )
                    )
                    
                    if scenario.get("success"):
                        st.success("✅ Scenario generated successfully!")
                        return scenario
                    else:
                        st.error(f"❌ Scenario generation failed: {scenario.get('error', 'Unknown error')}")
                        return None
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    return None
        
        return None
    
    @staticmethod
    def render_scenario_editor(
        scenario: Dict,
        project: Dict
    ) -> Dict:
        """
        Render scenario editing interface.
        
        Args:
            scenario: Scenario data
            project: Current project data
            
        Returns:
            Edited scenario data
        """
        st.subheader("✏️ Scenario Editor")
        
        # Validate scenario
        generator = ScenarioGenerator()
        validation = generator.validate_scenario(scenario)
        
        # Also validate visualizations
        viz_manager = VisualizationManager()
        scenes = scenario.get("scenes", [])
        viz_validations = [viz_manager.validate_scene(scene) for scene in scenes]
        viz_errors = sum(1 for v in viz_validations if not v["valid"])
        viz_warnings = sum(len(v.get("warnings", [])) for v in viz_validations)
        
        # Display validation results
        col1, col2, col3 = st.columns(3)
        with col1:
            if validation["valid"]:
                st.success("✅ Scenario Valid")
            else:
                st.error("❌ Scenario Errors")
        with col2:
            if viz_errors == 0:
                st.success("✅ All Scenes Valid")
            else:
                st.error(f"❌ {viz_errors} Scene Errors")
        with col3:
            if viz_warnings > 0:
                st.warning(f"⚠️ {viz_warnings} Warnings")
            else:
                st.success("✅ No Warnings")
        
        # Show detailed errors/warnings
        if not validation["valid"]:
            with st.expander("⚠️ Scenario Errors"):
                for error in validation.get("errors", []):
                    st.write(f"- {error}")
        
        if validation.get("warnings") or viz_warnings > 0:
            with st.expander("⚠️ All Warnings"):
                for warning in validation.get("warnings", []):
                    st.write(f"- Scenario: {warning}")
                for i, v in enumerate(viz_validations, 1):
                    for warning in v.get("warnings", []):
                        st.write(f"- Scene {i}: {warning}")
        
        # Overview
        scenes = scenario.get("scenes", [])
        total_duration = sum(s.get("duration", 0) for s in scenes)
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Total Scenes", len(scenes))
        with col2:
            st.metric("Total Duration", f"{total_duration}s ({total_duration//60}m {total_duration%60}s)")
        with col3:
            target = scenario.get("total_duration", 0)
            diff = total_duration - target
            st.metric("vs Target", f"{diff:+d}s", delta=f"{diff:+d}s")
        
        st.markdown("---")
        
        # Scene editor
        st.markdown("### 🎞️ Scenes")
        
        edited_scenes = []
        
        for i, scene in enumerate(scenes, 1):
            with st.expander(f"**Scene {i}: {scene.get('title', 'Untitled')}**", expanded=i == 1):
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    title = st.text_input(
                        "Title",
                        value=scene.get("title", ""),
                        key=f"title_{i}"
                    )
                
                with col2:
                    duration = st.number_input(
                        "Duration (s)",
                        min_value=10,
                        max_value=180,
                        value=scene.get("duration", 30),
                        key=f"duration_{i}"
                    )
                
                # Visualization type with features
                viz_options = ["manim", "matplotlib", "plotly"]
                viz_type = st.selectbox(
                    "Visualization Type",
                    viz_options,
                    index=viz_options.index(
                        scene.get("visualization_type", "manim").lower()
                    ),
                    key=f"viz_{i}",
                    help="Manim: Math animations | Matplotlib: Graphs | Plotly: 3D/Interactive"
                )
                
                # Show supported features for selected type
                viz_manager = VisualizationManager()
                features = viz_manager.get_renderer_features(viz_type)
                if features:
                    with st.expander(f"ℹ️ {viz_type.capitalize()} Features"):
                        st.write(", ".join(features))
                
                # Optional: Custom visualization code
                with st.expander("💻 Custom Code (Optional)"):
                    viz_code = st.text_area(
                        f"Custom {viz_type.capitalize()} Code",
                        value=scene.get("visualization_code", ""),
                        height=150,
                        key=f"code_{i}",
                        help=f"Write custom {viz_type} code for this scene"
                    )
                
                # Visual elements
                visual_elements = st.text_area(
                    "Visual Elements",
                    value="\n".join(scene.get("visual_elements", [])),
                    height=80,
                    key=f"visual_{i}",
                    help="One element per line"
                )
                
                # Animation description
                animation_desc = st.text_area(
                    "Animation Description",
                    value=scene.get("animation_description", ""),
                    height=100,
                    key=f"anim_{i}"
                )
                
                # Teaching points
                teaching_points = st.text_area(
                    "Teaching Points",
                    value="\n".join(scene.get("teaching_points", [])),
                    height=80,
                    key=f"teach_{i}",
                    help="One point per line"
                )
                
                # Transition
                transition = st.text_input(
                    "Transition to Next Scene",
                    value=scene.get("transition", ""),
                    key=f"trans_{i}"
                )
                
                # Build edited scene
                edited_scene = {
                    "id": scene.get("id", i),
                    "title": title,
                    "duration": duration,
                    "visualization_type": viz_type,
                    "visual_elements": [v.strip() for v in visual_elements.split("\n") if v.strip()],
                    "animation_description": animation_desc,
                    "teaching_points": [t.strip() for t in teaching_points.split("\n") if t.strip()],
                    "transition": transition,
                    "script_hint": scene.get("script_hint", "")
                }
                
                # Add visualization code if provided
                if viz_code and viz_code.strip():
                    edited_scene["visualization_code"] = viz_code.strip()
                
                # Add related research data if available
                if "related_concept" in scene:
                    edited_scene["related_concept"] = scene["related_concept"]
                if "related_formula" in scene:
                    edited_scene["related_formula"] = scene["related_formula"]
                
                edited_scenes.append(edited_scene)
        
        # Update scenario with edited scenes
        scenario["scenes"] = edited_scenes
        scenario["total_duration"] = sum(s["duration"] for s in edited_scenes)
        
        return scenario
    
    @staticmethod
    def render_scenario_actions(scenario: Dict, project: Dict) -> str:
        """
        Render action buttons for scenario.
        
        Args:
            scenario: Scenario data
            project: Current project data
            
        Returns:
            Action taken ('save', 'regenerate', 'preview', 'cancel', or '')
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
            if st.button("👁️ Preview", use_container_width=True):
                return "preview"
        
        with col4:
            if st.button("❌ Cancel", use_container_width=True):
                return "cancel"
        
        return ""
    
    @staticmethod
    def render_visualization_preview(scene: Dict, project: Dict) -> bool:
        """
        Render visualization preview for a scene.
        
        Args:
            scene: Scene data
            project: Current project data
            
        Returns:
            bool: True if preview was generated successfully
        """
        st.markdown(f"### 🎬 Preview: {scene.get('title', 'Scene')}")
        
        # Validation first
        viz_manager = VisualizationManager()
        validation = viz_manager.validate_scene(scene)
        
        if not validation["valid"]:
            st.error("⚠️ Cannot preview - scene has errors:")
            for error in validation.get("errors", []):
                st.write(f"- {error}")
            return False
        
        if validation["warnings"]:
            with st.expander("⚠️ Warnings"):
                for warning in validation["warnings"]:
                    st.write(f"- {warning}")
        
        # Preview button
        col1, col2 = st.columns([1, 3])
        
        with col1:
            quality = st.selectbox(
                "Preview Quality",
                ["low", "medium"],
                index=0,
                help="Low quality renders faster"
            )
        
        with col2:
            if st.button("🎥 Generate Preview", use_container_width=True):
                with st.spinner(f"Rendering preview... This may take {scene.get('duration', 30)} seconds..."):
                    try:
                        # Render preview
                        quality_enum = RenderQuality.LOW if quality == "low" else RenderQuality.MEDIUM
                        result = viz_manager.render_scene(scene, quality=quality_enum)
                        
                        if result.success and result.output_path:
                            st.success(f"✅ Preview rendered in {result.duration:.1f}s")
                            
                            # Display video
                            if result.output_path.exists():
                                st.video(str(result.output_path))
                                return True
                            else:
                                st.error("Preview file not found")
                                return False
                        else:
                            st.error(f"❌ Preview failed: {result.error}")
                            return False
                            
                    except Exception as e:
                        st.error(f"❌ Error: {str(e)}")
                        return False
        
        return False
    
    @staticmethod
    def render_scene_preview(scene: Dict):
        """
        Render preview of a single scene.
        
        Args:
            scene: Scene data
        """
        st.markdown(f"### 🎬 {scene.get('title', 'Scene Preview')}")
        
        col1, col2 = st.columns([2, 1])
        
        with col1:
            st.markdown("**Animation Description:**")
            st.write(scene.get("animation_description", "No description"))
            
            st.markdown("**Visual Elements:**")
            for elem in scene.get("visual_elements", []):
                st.write(f"- {elem}")
        
        with col2:
            st.info(f"""
            **Duration:** {scene.get('duration', 0)}s  
            **Type:** {scene.get('visualization_type', 'N/A')}  
            **Teaching Points:** {len(scene.get('teaching_points', []))}
            """)
        
        st.markdown("**Teaching Points:**")
        for point in scene.get("teaching_points", []):
            st.write(f"✓ {point}")
        
        if scene.get("transition"):
            st.markdown("**Transition:**")
            st.write(scene["transition"])


class ScriptInterface:
    """UI components for script generation and editing."""
    
    @staticmethod
    def render_script_generation(
        scenes: List[Dict],
        research: Dict,
        project: Dict
    ) -> Optional[Dict[str, str]]:
        """
        Render script generation interface.
        
        Args:
            scenes: List of scenes
            research: Research data
            project: Current project data
            
        Returns:
            Dict of generated scripts or None
        """
        st.subheader("📝 Script Generation")
        
        st.info(f"Generating scripts for {len(scenes)} scenes...")
        
        # Model selection
        with st.expander("⚙️ Model Selection"):
            available_models = ModelSelector.get_available_models()
            if available_models:
                model_ids = [m['id'] for m in available_models]
                recommended = ModelSelector.recommend_model('scripts')
                default_index = model_ids.index(recommended) if recommended in model_ids else 0
                
                selected_model = st.selectbox(
                    "AI Model",
                    model_ids,
                    index=default_index,
                    help="Flash models are faster for script generation"
                )
            else:
                selected_model = None
        
        # Generate button
        if st.button("🚀 Generate All Scripts", type="primary", use_container_width=True):
            with st.spinner("📝 Generating scripts... This may take 30-60 seconds..."):
                try:
                    # Create generator with selected model
                    engine = ModelSelector.get_engine_for_task(
                        "scripts",
                        custom_model=selected_model if selected_model else None
                    )
                    generator = ScriptGenerator(engine=engine)
                    
                    # Generate scripts
                    scripts = asyncio.run(
                        generator.generate_all_scripts(scenes, research)
                    )
                    
                    st.success(f"✅ Generated {len(scripts)} scripts!")
                    return scripts
                        
                except Exception as e:
                    st.error(f"❌ Error: {str(e)}")
                    return None
        
        return None
    
    @staticmethod
    def render_script_editor(
        scripts: Dict[str, str],
        scenes: List[Dict],
        project: Dict
    ) -> Dict[str, str]:
        """
        Render script editing interface.
        
        Args:
            scripts: Dict of scripts (scene_id -> script)
            scenes: List of scenes
            project: Current project data
            
        Returns:
            Edited scripts
        """
        st.subheader("✏️ Script Editor")
        
        edited_scripts = {}
        generator = ScriptGenerator()
        
        for i, scene in enumerate(scenes, 1):
            scene_id = str(scene.get("id", i))
            script = scripts.get(scene_id, "")
            
            with st.expander(f"**Scene {i}: {scene.get('title', 'Untitled')}**", expanded=i == 1):
                # Show scene info
                col1, col2, col3 = st.columns(3)
                with col1:
                    st.caption(f"Duration: {scene.get('duration', 0)}s")
                with col2:
                    st.caption(f"Type: {scene.get('visualization_type', 'N/A')}")
                with col3:
                    word_count = len(script.split())
                    st.caption(f"Words: {word_count}")
                
                # Script editor
                edited_script = st.text_area(
                    "Narration Script",
                    value=script,
                    height=200,
                    key=f"script_{scene_id}",
                    help="Edit the narration for this scene"
                )
                
                # Validation
                validation = generator.validate_script(edited_script, scene)
                
                col1, col2 = st.columns(2)
                with col1:
                    st.metric("Word Count", validation["word_count"])
                with col2:
                    st.metric("Est. Duration", f"{validation['estimated_duration']}s")
                
                if validation["warnings"]:
                    with st.expander("⚠️ Warnings"):
                        for warning in validation["warnings"]:
                            st.write(f"- {warning}")
                
                edited_scripts[scene_id] = edited_script
        
        return edited_scripts
    @staticmethod
    def render_batch_rendering(
        scenes: List[Dict],
        project: Dict,
        output_dir: Optional[Path] = None
    ) -> Dict[str, Any]:
        """
        Render all scenes in batch with progress tracking.
        
        Args:
            scenes: List of scenes to render
            project: Current project data
            output_dir: Optional output directory
            
        Returns:
            Dict with rendering results
        """
        st.subheader("🎬 Batch Rendering")
        
        if not scenes:
            st.warning("No scenes to render")
            return {}
        
        # Setup
        if output_dir is None:
            project_id = project.get("project_id", "unknown")
            output_dir = Path(f"data/projects/{project_id}/visualizations")
        
        output_dir.mkdir(parents=True, exist_ok=True)
        
        # Quality selection
        col1, col2 = st.columns(2)
        
        with col1:
            quality = st.selectbox(
                "Render Quality",
                ["low", "medium", "high", "ultra"],
                index=1,
                help="Higher quality takes longer to render"
            )
        
        with col2:
            # Estimate time
            viz_manager = VisualizationManager()
            estimated_time = viz_manager.estimate_total_render_time(scenes)
            st.metric("Estimated Time", f"{estimated_time/60:.1f} min")
        
        # Render button
        if st.button("🚀 Render All Scenes", type="primary", use_container_width=True):
            quality_enum = RenderQuality[quality.upper()]
            
            # Progress tracking
            progress_bar = st.progress(0)
            status_text = st.empty()
            results_container = st.container()
            
            results = {}
            
            def progress_callback(current, total, result):
                progress = current / total
                progress_bar.progress(progress)
                status_text.text(f"Rendering scene {current}/{total}...")
                
                with results_container:
                    if result.success:
                        st.success(f"✅ Scene {current}: {result.duration:.1f}s")
                    else:
                        st.error(f"❌ Scene {current}: {result.error}")
            
            # Render all scenes
            with st.spinner("Rendering scenes..."):
                try:
                    results = viz_manager.render_all_scenes(
                        scenes,
                        output_dir,
                        quality_enum,
                        progress_callback
                    )
                    
                    # Summary
                    successful = sum(1 for r in results.values() if r.success)
                    failed = len(results) - successful
                    
                    st.markdown("---")
                    col1, col2, col3 = st.columns(3)
                    with col1:
                        st.metric("Total Scenes", len(results))
                    with col2:
                        st.metric("Successful", successful)
                    with col3:
                        st.metric("Failed", failed)
                    
                    if successful == len(results):
                        st.success("🎉 All scenes rendered successfully!")
                    elif successful > 0:
                        st.warning(f"⚠️ {successful}/{len(results)} scenes rendered successfully")
                    else:
                        st.error("❌ All renders failed")
                    
                    return results
                    
                except Exception as e:
                    st.error(f"❌ Batch rendering failed: {str(e)}")
                    return {}
        
        return {}



# Made with Bob