# User Guide - AI Educational Content Creator

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [Workflow Overview](#workflow-overview)
4. [Step-by-Step Tutorial](#step-by-step-tutorial)
5. [Advanced Features](#advanced-features)
6. [Best Practices](#best-practices)
7. [Tips and Tricks](#tips-and-tricks)
8. [Troubleshooting](#troubleshooting)

## Introduction

The AI Educational Content Creator is a comprehensive tool designed to streamline the creation of educational videos for mathematics and physics topics. It leverages AI to assist with research, visualization design, script generation, and video production.

### Key Features

- **AI-Powered Research**: Automatically expand topics and gather relevant information
- **Interactive Visualizations**: Create animations using Manim, Matplotlib, and Plotly
- **Script Generation**: AI-generated narration synchronized with visuals
- **Voice Recording**: Built-in recording studio with audio processing
- **Audio Mixing**: Add background music and sound effects
- **Video Compilation**: Automated video rendering and export

### Target Audience

- Educational content creators
- Math and physics teachers
- Online course instructors
- YouTube educators
- Students creating presentations

## Getting Started

### First Launch

1. **Start the Application**
   ```bash
   streamlit run app.py
   ```

2. **Configure API Key**
   - On first launch, you'll be prompted to enter your Gemini API key
   - The key will be saved securely in your `.env` file
   - You can change it later in Settings

3. **Explore the Interface**
   - Main navigation sidebar
   - Project dashboard
   - Quick start tutorial

### Interface Overview

```
┌─────────────────────────────────────────────────────────┐
│  AI Educational Content Creator                         │
├─────────────────────────────────────────────────────────┤
│ Sidebar:                    │ Main Area:                │
│ - New Project               │ - Project Dashboard       │
│ - Open Project              │ - Active Workspace        │
│ - Settings                  │ - Preview Panel           │
│ - Help                      │ - Edit Controls           │
└─────────────────────────────────────────────────────────┘
```

## Workflow Overview

### Complete Content Creation Process

```
1. Topic Selection
   ↓
2. AI Research & Expansion
   ↓
3. Research Validation
   ↓
4. Visualization Scenario Design
   ↓
5. Script Generation
   ↓
6. Review & Edit
   ↓
7. Voice Recording
   ↓
8. Audio Mixing
   ↓
9. Video Compilation
   ↓
10. Export & Share
```

### Estimated Time

- **Quick Video (5 min)**: 1-2 hours total
- **Standard Video (10-15 min)**: 2-4 hours total
- **Complex Video (20+ min)**: 4-8 hours total

## Step-by-Step Tutorial

### Example: Creating a Video on "Projectile Motion"

#### Step 1: Create New Project

1. Click **"New Project"** in the sidebar
2. Enter project details:
   - **Title**: "Understanding Projectile Motion"
   - **Topic**: "Projectile Motion"
   - **Target Level**: "High School"
   - **Duration**: "10 minutes"

3. Click **"Create Project"**

#### Step 2: AI Research Phase

The AI will automatically:
- Expand the topic into subtopics
- Identify key concepts
- Find relevant formulas
- Suggest real-world applications

**Example AI Output:**

```json
{
  "title": "Projectile Motion",
  "concepts": [
    {
      "name": "Trajectory",
      "definition": "The path followed by a projectile",
      "importance": "Core concept for understanding motion"
    },
    {
      "name": "Range",
      "definition": "Horizontal distance traveled",
      "importance": "Practical application"
    }
  ],
  "formulas": [
    {
      "latex": "y = x\\tan(\\theta) - \\frac{gx^2}{2v_0^2\\cos^2(\\theta)}",
      "explanation": "Trajectory equation",
      "variables": {
        "y": "vertical position",
        "x": "horizontal position",
        "θ": "launch angle",
        "v₀": "initial velocity",
        "g": "gravitational acceleration"
      }
    }
  ],
  "applications": [
    "Sports (basketball, soccer)",
    "Military ballistics",
    "Space exploration"
  ]
}
```

#### Step 3: Validate Research

Review the AI's findings:

1. **Check Concepts**
   - ✓ Trajectory - Correct
   - ✓ Range - Correct
   - ✓ Maximum Height - Correct
   - ✗ Time of Flight - Add more detail

2. **Verify Formulas**
   - Check LaTeX syntax
   - Verify mathematical accuracy
   - Add missing formulas if needed

3. **Edit Content**
   - Click "Edit" next to any concept
   - Add custom notes
   - Reorder items by dragging

4. **Add Custom Content**
   - Click "Add Concept"
   - Enter your own definitions
   - Include specific examples

5. **Approve Research**
   - Click "Approve & Continue"

#### Step 4: Visualization Scenario

The AI generates a scene-by-scene breakdown:

**Example Scenario:**

```
Scene 1: Introduction (30 seconds)
- Type: Manim animation
- Visual: Title card with projectile trajectory
- Script hint: "Today we'll explore projectile motion..."

Scene 2: Basic Concepts (60 seconds)
- Type: Matplotlib graph
- Visual: Parabolic trajectory with labeled axes
- Script hint: "A projectile follows a curved path..."

Scene 3: Breaking Down Components (90 seconds)
- Type: Manim animation
- Visual: Vector decomposition (horizontal + vertical)
- Script hint: "We can analyze motion in two dimensions..."

Scene 4: The Trajectory Equation (60 seconds)
- Type: Manim equation transformation
- Visual: Derive trajectory equation step-by-step
- Script hint: "Let's derive the mathematical formula..."

Scene 5: Real-World Example (90 seconds)
- Type: Plotly 3D visualization
- Visual: Basketball shot trajectory
- Script hint: "Consider a basketball player..."

Scene 6: Interactive Exploration (60 seconds)
- Type: Plotly interactive plot
- Visual: Adjustable parameters (angle, velocity)
- Script hint: "Let's see how changing the angle affects..."

Scene 7: Summary (30 seconds)
- Type: Manim animation
- Visual: Key points recap
- Script hint: "To summarize, projectile motion..."
```

#### Step 5: Review & Modify Scenario

1. **Preview Each Scene**
   - Click on scene cards to preview
   - Check visualization type
   - Review timing

2. **Edit Scenes**
   - Modify duration
   - Change visualization type
   - Update visual elements
   - Edit script hints

3. **Reorder Scenes**
   - Drag and drop to reorder
   - Ensure logical flow

4. **Add/Remove Scenes**
   - Click "Add Scene" to insert new
   - Click "Delete" to remove

5. **Approve Scenario**
   - Click "Generate Full Script"

#### Step 6: Script Generation

The AI generates complete narration for each scene:

**Example Script for Scene 2:**

```
Have you ever wondered why a thrown ball follows a curved path? 
This beautiful arc is what we call a parabolic trajectory, and 
it's one of the most fundamental concepts in physics.

When we launch a projectile - whether it's a ball, an arrow, or 
even a rocket - it moves in two dimensions simultaneously. 
Horizontally, it travels at a constant velocity, while vertically, 
it's constantly accelerating downward due to gravity.

The combination of these two motions creates the characteristic 
parabolic shape we see here. Notice how the projectile rises to 
a maximum height, then falls back down, all while moving forward.

This isn't just theory - you see this every day in sports, from 
a basketball arcing toward the hoop to a soccer ball curving 
through the air.
```

#### Step 7: Edit Script

1. **Review Generated Script**
   - Read through each scene's narration
   - Check for accuracy and clarity
   - Verify timing (word count vs. duration)

2. **Make Edits**
   - Click in text editor to modify
   - Add emphasis markers: **bold** for emphasis
   - Add pauses: [pause 2s]
   - Add questions for engagement

3. **Timing Indicators**
   - Green: Perfect timing
   - Yellow: Slightly fast/slow
   - Red: Needs adjustment

4. **Preview Script**
   - Text-to-speech preview (optional)
   - Estimate reading time
   - Check flow between scenes

5. **Approve Script**
   - Click "Proceed to Recording"

#### Step 8: Voice Recording

1. **Setup Recording**
   - Select microphone from dropdown
   - Test audio levels
   - Adjust input gain

2. **Recording Interface**
   ```
   ┌─────────────────────────────────────┐
   │ Scene 1: Introduction               │
   │ Duration: 30s                       │
   ├─────────────────────────────────────┤
   │ Script:                             │
   │ "Today we'll explore projectile..." │
   │                                     │
   │ [●] Record  [■] Stop  [▶] Play     │
   │ ━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━  │
   │ Level: ████████░░░░░░░░░░░░         │
   └─────────────────────────────────────┘
   ```

3. **Record Each Scene**
   - Click "Record" button
   - Read the script naturally
   - Click "Stop" when finished
   - Click "Play" to review

4. **Re-record if Needed**
   - Click "Re-record" to try again
   - Previous recording is saved as backup

5. **Audio Processing**
   - Auto-normalize volume
   - Remove background noise
   - Trim silence

6. **Complete Recording**
   - Click "All Scenes Recorded"
   - Proceed to audio mixing

#### Step 9: Audio Mixing

1. **Add Background Music**
   - Browse music library
   - Categories: Upbeat, Calm, Dramatic, Ambient
   - Preview tracks
   - Select and add to timeline

2. **Adjust Music Volume**
   - Slider: -40dB to 0dB
   - Recommended: -20dB to -15dB
   - Preview mix

3. **Enable Audio Ducking**
   - Toggle "Auto-duck music during speech"
   - Music automatically lowers when you speak
   - Adjust ducking amount

4. **Add Sound Effects**
   - Transition sounds
   - Emphasis effects
   - Ambient sounds
   - Place at specific timestamps

5. **Preview Mixed Audio**
   - Play full audio mix
   - Check balance
   - Adjust as needed

6. **Export Audio**
   - Click "Finalize Audio Mix"
   - Audio saved for video compilation

#### Step 10: Video Compilation

1. **Review Settings**
   - Resolution: 1920x1080 (Full HD)
   - Frame rate: 30 fps
   - Quality: High
   - Format: MP4

2. **Generate Visualizations**
   - Click "Render Visualizations"
   - Progress bar shows rendering status
   - Each scene rendered separately
   - Estimated time: 5-15 minutes

3. **Preview Scenes**
   - Review each rendered scene
   - Check visual quality
   - Verify timing

4. **Compile Final Video**
   - Click "Compile Video"
   - Combines all scenes
   - Syncs with audio
   - Adds transitions
   - Estimated time: 5-10 minutes

5. **Final Preview**
   - Watch complete video
   - Check audio-video sync
   - Verify quality

6. **Export Video**
   - Click "Export Final Video"
   - Choose export location
   - Video saved as MP4

#### Step 11: Share Your Video

Your video is now ready! You can:
- Upload to YouTube
- Share on educational platforms
- Use in classroom presentations
- Embed in online courses

## Advanced Features

### Custom Visualizations

#### Writing Custom Manim Code

```python
# In scenario editor, click "Custom Code"
from manim import *

class CustomScene(Scene):
    def construct(self):
        # Your custom animation
        circle = Circle(radius=2, color=BLUE)
        self.play(Create(circle))
        self.wait(1)
```

#### Custom Matplotlib Plots

```python
import matplotlib.pyplot as plt
import numpy as np

def custom_plot():
    x = np.linspace(0, 10, 100)
    y = np.sin(x)
    
    plt.plot(x, y)
    plt.title("Custom Sine Wave")
    plt.xlabel("x")
    plt.ylabel("sin(x)")
    
    return plt
```

### Batch Processing

Create multiple videos from a template:

1. **Create Template**
   - Design scenario once
   - Save as template

2. **Apply to Multiple Topics**
   - Select template
   - Enter different topics
   - AI adapts content

3. **Batch Render**
   - Queue multiple projects
   - Render overnight
   - Export all videos

### Collaboration Features

#### Export Project

```
File → Export Project → .zip
```

Share with collaborators who can:
- Review and edit
- Add comments
- Suggest changes

#### Import Project

```
File → Import Project → Select .zip
```

### Advanced Audio

#### Multi-track Recording

- Record multiple takes
- Select best segments
- Combine into final track

#### Audio Effects

- Reverb
- Compression
- EQ adjustment
- De-esser

### Video Effects

#### Transitions

- Fade
- Dissolve
- Wipe
- Zoom

#### Text Overlays

- Titles
- Subtitles
- Annotations
- Callouts

## Best Practices

### Content Creation

1. **Start Simple**
   - Begin with basic topics
   - Master the workflow
   - Gradually increase complexity

2. **Plan Ahead**
   - Outline key points before starting
   - Know your target audience
   - Set clear learning objectives

3. **Validate AI Output**
   - Always review AI-generated content
   - Verify mathematical accuracy
   - Check for clarity and coherence

4. **Iterate**
   - First draft is rarely perfect
   - Review and refine
   - Get feedback from others

### Visualization Design

1. **Keep It Simple**
   - One concept per scene
   - Avoid clutter
   - Use clear labels

2. **Use Appropriate Tools**
   - Manim: Equations, transformations
   - Matplotlib: Graphs, plots
   - Plotly: 3D, interactive

3. **Consistent Style**
   - Use same color scheme
   - Maintain font consistency
   - Keep animation speed uniform

4. **Progressive Complexity**
   - Start with simple visuals
   - Build up gradually
   - Recap complex concepts

### Script Writing

1. **Conversational Tone**
   - Write as you speak
   - Use simple language
   - Avoid jargon when possible

2. **Engagement**
   - Ask questions
   - Use examples
   - Tell stories

3. **Pacing**
   - ~150 words per minute
   - Include pauses
   - Vary sentence length

4. **Clarity**
   - Define terms
   - Explain step-by-step
   - Summarize key points

### Recording Tips

1. **Environment**
   - Quiet room
   - Minimal echo
   - Consistent background

2. **Technique**
   - Speak clearly
   - Maintain energy
   - Smile while speaking (improves tone)

3. **Equipment**
   - Use quality microphone
   - Pop filter recommended
   - Proper mic positioning

4. **Post-Processing**
   - Enable noise reduction
   - Normalize volume
   - Remove long pauses

## Tips and Tricks

### Keyboard Shortcuts

- `Ctrl+N`: New project
- `Ctrl+S`: Save project
- `Ctrl+P`: Preview
- `Space`: Play/Pause
- `Ctrl+Z`: Undo
- `Ctrl+Y`: Redo

### Time-Saving Features

1. **Templates**
   - Save successful projects as templates
   - Reuse scenario structures
   - Adapt for similar topics

2. **Snippets**
   - Save common script phrases
   - Reuse introduction/conclusion
   - Build personal library

3. **Presets**
   - Save visualization settings
   - Audio mixing presets
   - Export configurations

### Quality Optimization

1. **Preview Before Full Render**
   - Use low-quality preview
   - Check timing and flow
   - Final render only when satisfied

2. **Incremental Saves**
   - Save after each major step
   - Create version backups
   - Easy to revert if needed

3. **Resource Management**
   - Close other applications
   - Clear cache regularly
   - Monitor disk space

## Troubleshooting

### Common Issues

#### Audio-Video Sync Issues

**Problem**: Audio doesn't match video timing

**Solutions**:
- Check scene durations match script timing
- Verify audio file isn't corrupted
- Re-render with "Force Sync" option
- Adjust individual scene timing

#### Rendering Failures

**Problem**: Visualization rendering fails

**Solutions**:
- Check error log for details
- Verify LaTeX installation (for Manim)
- Simplify complex animations
- Try different quality settings
- Update visualization libraries

#### Poor Audio Quality

**Problem**: Recording has noise or distortion

**Solutions**:
- Check microphone settings
- Enable noise reduction
- Adjust input gain
- Use better recording environment
- Consider external microphone

#### Slow Performance

**Problem**: Application is slow or unresponsive

**Solutions**:
- Close unused projects
- Clear cache
- Reduce preview quality
- Disable real-time preview
- Upgrade hardware if needed

### Getting Help

1. **Check Documentation**
   - Read relevant sections
   - Review examples
   - Check API reference

2. **Search Issues**
   - GitHub issues
   - Community forums
   - FAQ section

3. **Contact Support**
   - Email: support@example.com
   - Include error logs
   - Describe steps to reproduce

## Conclusion

You now have a comprehensive understanding of the AI Educational Content Creator! Start with simple projects, experiment with features, and gradually build your skills.

Remember:
- The AI is your assistant, not a replacement for your expertise
- Quality content takes time - don't rush
- Iterate and improve with each project
- Share your creations and get feedback

Happy creating! 🎓🎬