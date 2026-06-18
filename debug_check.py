"""
Diagnostic script to check for common issues in the AI content creation system.
Run this to identify potential problems.
"""
import json
import os
from pathlib import Path

def check_project_structure():
    """Check if project structure is correct."""
    print("=" * 60)
    print("DIAGNOSTIC CHECK - AI Content Creation System")
    print("=" * 60)
    
    issues = []
    warnings = []
    
    # Check core files exist
    core_files = [
        "core/ai_engine.py",
        "core/topic_processor.py",
        "core/scenario_generator.py",
        "core/script_generator.py",
        "ui/scenario_interface.py",
        "utils/model_selector.py"
    ]
    
    print("\n1. Checking core files...")
    for file in core_files:
        if os.path.exists(file):
            print(f"   ✅ {file}")
        else:
            print(f"   ❌ {file} - MISSING")
            issues.append(f"Missing file: {file}")
    
    # Check project data
    print("\n2. Checking project data...")
    data_dir = Path("data/projects")
    if data_dir.exists():
        projects = list(data_dir.glob("*/project.json"))
        print(f"   ✅ Found {len(projects)} project(s)")
        
        for proj_file in projects:
            try:
                with open(proj_file, 'r', encoding='utf-8') as f:
                    data = json.load(f)
                
                proj_id = data.get('project_id', 'unknown')
                topic = data.get('topic', 'N/A')
                print(f"\n   Project: {proj_id}")
                print(f"   Topic: {topic}")
                
                # Check research
                if 'research' in data:
                    research = data['research'].get('validated_concepts', {})
                    title = research.get('title', 'N/A')
                    concepts = len(research.get('concepts', []))
                    print(f"   Research Title: {title}")
                    print(f"   Concepts: {concepts}")
                    
                    if title != topic:
                        warnings.append(f"Title mismatch: '{title}' vs '{topic}'")
                
                # Check scenario
                if 'scenario' in data:
                    scenario = data['scenario']
                    scenes = len(scenario.get('scenes', []))
                    duration = scenario.get('total_duration', 0)
                    print(f"   Scenes: {scenes}")
                    print(f"   Duration: {duration}s")
                    
                    # Check scene durations
                    total_scene_duration = sum(s.get('duration', 0) for s in scenario.get('scenes', []))
                    if abs(total_scene_duration - duration) > 10:
                        warnings.append(f"Duration mismatch: scenes={total_scene_duration}s, target={duration}s")
                
                # Check scripts
                if 'scripts' in data:
                    scripts = data['scripts']
                    script_count = len(scripts)
                    print(f"   Scripts: {script_count}")
                    
                    if 'scenario' in data:
                        scene_count = len(data['scenario'].get('scenes', []))
                        if script_count < scene_count:
                            warnings.append(f"Missing scripts: {script_count}/{scene_count}")
                
            except Exception as e:
                issues.append(f"Error reading {proj_file}: {str(e)}")
    else:
        issues.append("data/projects directory not found")
    
    # Check .env file
    print("\n3. Checking configuration...")
    if os.path.exists('.env'):
        print("   ✅ .env file exists")
        with open('.env', 'r') as f:
            content = f.read()
            if 'GOOGLE_API_KEY' in content:
                print("   ✅ GOOGLE_API_KEY configured")
            else:
                issues.append("GOOGLE_API_KEY not found in .env")
    else:
        issues.append(".env file not found")
    
    # Summary
    print("\n" + "=" * 60)
    print("SUMMARY")
    print("=" * 60)
    
    if not issues and not warnings:
        print("✅ All checks passed! System looks healthy.")
    else:
        if issues:
            print(f"\n❌ ISSUES FOUND ({len(issues)}):")
            for issue in issues:
                print(f"   - {issue}")
        
        if warnings:
            print(f"\n⚠️  WARNINGS ({len(warnings)}):")
            for warning in warnings:
                print(f"   - {warning}")
    
    print("\n" + "=" * 60)
    print("If you're experiencing errors, please share:")
    print("1. The error message from the terminal")
    print("2. What you were doing when the error occurred")
    print("3. The output of this diagnostic script")
    print("=" * 60)

if __name__ == "__main__":
    check_project_structure()

# Made with Bob
