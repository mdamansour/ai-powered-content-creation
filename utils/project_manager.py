"""
Project management for saving, loading, and organizing educational content projects.
"""
import json
import os
from datetime import datetime
from typing import Dict, List, Optional
import uuid
from pathlib import Path
from config.settings import get_settings


class ProjectManager:
    """Manage educational content projects."""
    
    def __init__(self, projects_dir: str = None):
        """
        Initialize project manager.
        
        Args:
            projects_dir: Directory for storing projects (uses config if not provided)
        """
        if projects_dir is None:
            settings = get_settings()
            projects_dir = str(settings.paths.projects_dir)
        
        self.projects_dir = Path(projects_dir)
        self.projects_dir.mkdir(parents=True, exist_ok=True)
    
    def create_project(self, title: str, topic: str, level: str = "mixed") -> Dict:
        """
        Create a new project.
        
        Args:
            title: Project title
            topic: Educational topic
            level: Target educational level
            
        Returns:
            Dict: New project data
        """
        project = {
            "project_id": str(uuid.uuid4()),
            "title": title,
            "topic": topic,
            "level": level,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "draft",
            "research": {
                "raw_ai_output": None,
                "validated_concepts": [],
                "user_notes": ""
            },
            "scenario": {
                "scenes": [],
                "total_duration": 0
            },
            "scripts": {},
            "audio": {
                "voice_recordings": {},
                "background_music": None,
                "sound_effects": [],
                "mix_settings": {
                    "music_volume": -20,
                    "ducking_enabled": True,
                    "ducking_amount": -10
                }
            },
            "video": {
                "output_path": None,
                "settings": {
                    "resolution": [1920, 1080],
                    "fps": 30,
                    "bitrate": "5000k",
                    "quality": "high"
                }
            },
            "metadata": {
                "version": "1.0",
                "app_version": "0.1.0"
            }
        }
        
        self.save_project(project)
        return project
    
    def save_project(self, project: Dict) -> bool:
        """
        Save project to disk.
        
        Args:
            project: Project data dictionary
            
        Returns:
            bool: True if successful
        """
        try:
            project["updated_at"] = datetime.now().isoformat()
            
            project_dir = self.projects_dir / project["project_id"]
            project_dir.mkdir(parents=True, exist_ok=True)
            
            # Save main project file
            project_file = project_dir / "project.json"
            with open(project_file, 'w', encoding='utf-8') as f:
                json.dump(project, f, indent=2, ensure_ascii=False)
            
            # Create subdirectories for assets
            (project_dir / "audio").mkdir(exist_ok=True)
            (project_dir / "video").mkdir(exist_ok=True)
            (project_dir / "visualizations").mkdir(exist_ok=True)
            
            return True
        except Exception as e:
            print(f"Error saving project: {e}")
            return False
    
    def load_project(self, project_id: str) -> Optional[Dict]:
        """
        Load project from disk.
        
        Args:
            project_id: Project ID to load
            
        Returns:
            Dict: Project data or None if not found
        """
        try:
            project_file = self.projects_dir / project_id / "project.json"
            
            if not project_file.exists():
                return None
            
            with open(project_file, 'r', encoding='utf-8') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading project: {e}")
            return None
    
    def list_projects(self, status: str = None) -> List[Dict]:
        """
        List all projects with optional status filter.
        
        Args:
            status: Filter by status ('draft', 'in_progress', 'completed')
            
        Returns:
            List of project summaries
        """
        projects = []
        
        try:
            for project_dir in self.projects_dir.iterdir():
                if not project_dir.is_dir():
                    continue
                
                project = self.load_project(project_dir.name)
                if project is None:
                    continue
                
                # Filter by status if specified
                if status and project.get("status") != status:
                    continue
                
                # Create summary
                summary = {
                    "project_id": project["project_id"],
                    "title": project["title"],
                    "topic": project["topic"],
                    "level": project.get("level", "mixed"),
                    "status": project["status"],
                    "created_at": project["created_at"],
                    "updated_at": project["updated_at"],
                    "scene_count": len(project.get("scenario", {}).get("scenes", [])),
                    "has_audio": bool(project.get("audio", {}).get("voice_recordings")),
                    "has_video": bool(project.get("video", {}).get("output_path"))
                }
                projects.append(summary)
            
            # Sort by updated_at (most recent first)
            projects.sort(key=lambda x: x["updated_at"], reverse=True)
            
        except Exception as e:
            print(f"Error listing projects: {e}")
        
        return projects
    
    def delete_project(self, project_id: str) -> bool:
        """
        Delete a project and all its files.
        
        Args:
            project_id: Project ID to delete
            
        Returns:
            bool: True if successful
        """
        try:
            import shutil
            project_dir = self.projects_dir / project_id
            
            if project_dir.exists():
                shutil.rmtree(project_dir)
                return True
            return False
        except Exception as e:
            print(f"Error deleting project: {e}")
            return False
    
    def update_project_status(self, project_id: str, status: str) -> bool:
        """
        Update project status.
        
        Args:
            project_id: Project ID
            status: New status ('draft', 'in_progress', 'completed')
            
        Returns:
            bool: True if successful
        """
        project = self.load_project(project_id)
        if project is None:
            return False
        
        project["status"] = status
        return self.save_project(project)
    
    def get_project_path(self, project_id: str, subdir: str = None) -> Path:
        """
        Get path to project directory or subdirectory.
        
        Args:
            project_id: Project ID
            subdir: Optional subdirectory ('audio', 'video', 'visualizations')
            
        Returns:
            Path: Directory path
        """
        project_dir = self.projects_dir / project_id
        
        if subdir:
            return project_dir / subdir
        return project_dir
    
    def export_project(self, project_id: str, export_path: str) -> bool:
        """
        Export project as a zip file.
        
        Args:
            project_id: Project ID to export
            export_path: Path for exported zip file
            
        Returns:
            bool: True if successful
        """
        try:
            import shutil
            project_dir = self.projects_dir / project_id
            
            if not project_dir.exists():
                return False
            
            # Create zip archive
            base_name = export_path.replace('.zip', '')
            shutil.make_archive(base_name, 'zip', project_dir)
            return True
        except Exception as e:
            print(f"Error exporting project: {e}")
            return False
    
    def import_project(self, zip_path: str) -> Optional[str]:
        """
        Import project from zip file.
        
        Args:
            zip_path: Path to zip file
            
        Returns:
            str: Project ID if successful, None otherwise
        """
        try:
            import shutil
            import tempfile
            
            # Extract to temporary directory
            with tempfile.TemporaryDirectory() as temp_dir:
                shutil.unpack_archive(zip_path, temp_dir, 'zip')
                
                # Find project.json
                project_file = None
                for root, dirs, files in os.walk(temp_dir):
                    if 'project.json' in files:
                        project_file = os.path.join(root, 'project.json')
                        break
                
                if not project_file:
                    return None
                
                # Load project to get ID
                with open(project_file, 'r', encoding='utf-8') as f:
                    project = json.load(f)
                
                project_id = project["project_id"]
                
                # Copy to projects directory
                project_dir = self.projects_dir / project_id
                if project_dir.exists():
                    # Generate new ID if conflict
                    project_id = str(uuid.uuid4())
                    project["project_id"] = project_id
                    project_dir = self.projects_dir / project_id
                
                shutil.copytree(os.path.dirname(project_file), project_dir)
                
                # Save updated project
                self.save_project(project)
                
                return project_id
        except Exception as e:
            print(f"Error importing project: {e}")
            return None
    
    def get_project_statistics(self, project_id: str) -> Dict:
        """
        Get statistics about a project.
        
        Args:
            project_id: Project ID
            
        Returns:
            Dict: Project statistics
        """
        project = self.load_project(project_id)
        if project is None:
            return {}
        
        scenes = project.get("scenario", {}).get("scenes", [])
        total_duration = sum(scene.get("duration", 0) for scene in scenes)
        
        return {
            "project_id": project_id,
            "title": project["title"],
            "status": project["status"],
            "scene_count": len(scenes),
            "total_duration": total_duration,
            "has_research": bool(project.get("research", {}).get("validated_concepts")),
            "has_scenario": len(scenes) > 0,
            "has_scripts": bool(project.get("scripts")),
            "has_audio": bool(project.get("audio", {}).get("voice_recordings")),
            "has_video": bool(project.get("video", {}).get("output_path")),
            "completion_percentage": self._calculate_completion(project)
        }
    
    def _calculate_completion(self, project: Dict) -> int:
        """Calculate project completion percentage."""
        steps = [
            bool(project.get("research", {}).get("validated_concepts")),  # Research
            len(project.get("scenario", {}).get("scenes", [])) > 0,  # Scenario
            bool(project.get("scripts")),  # Scripts
            bool(project.get("audio", {}).get("voice_recordings")),  # Audio
            bool(project.get("video", {}).get("output_path"))  # Video
        ]
        
        completed = sum(steps)
        return int((completed / len(steps)) * 100)

# Made with Bob
