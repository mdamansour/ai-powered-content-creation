# Technical Specification - AI Educational Content Creator

## System Requirements

### Hardware Requirements
- **CPU**: Multi-core processor (4+ cores recommended)
- **RAM**: 8GB minimum, 16GB recommended
- **Storage**: 10GB free space for projects and cache
- **Audio**: Microphone for voice recording
- **GPU**: Optional, for faster Manim rendering

### Software Requirements
- **Python**: 3.9 or higher
- **FFmpeg**: Latest version
- **LaTeX**: For Manim mathematical rendering
- **Operating System**: Windows 10/11, macOS 10.15+, or Linux

## API Integration

### Google Gemini Flash Configuration

```python
# config/api_keys.py
import os
from dotenv import load_dotenv

load_dotenv()

class APIConfig:
    GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
    
    # Fallback for other providers
    OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
    ANTHROPIC_API_KEY = os.getenv("ANTHROPIC_API_KEY")
    
    @classmethod
    def get_active_provider(cls):
        if cls.GEMINI_API_KEY:
            return "gemini"
        elif cls.OPENAI_API_KEY:
            return "openai"
        elif cls.ANTHROPIC_API_KEY:
            return "anthropic"
        return None
```

```python
# core/ai_engine.py
import google.generativeai as genai
from typing import Dict, List, Optional
import json

class AIEngine:
    def __init__(self, api_key: str, model: str = "gemini-1.5-flash-latest"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model)
        self.chat = None
        
    def start_session(self, system_prompt: str):
        """Initialize a chat session with system context"""
        self.chat = self.model.start_chat(history=[])
        return self.chat
    
    async def generate_research(self, topic: str, level: str = "mixed") -> Dict:
        """Generate comprehensive research for a topic"""
        prompt = f"""
        Topic: {topic}
        Educational Level: {level}
        
        Provide a comprehensive analysis including:
        1. Core concepts (with definitions)
        2. Mathematical formulas (in LaTeX)
        3. Physical principles
        4. Prerequisites
        5. Real-world applications
        6. Common misconceptions
        7. Suggested practice problems
        
        Return as structured JSON with these keys:
        - title
        - concepts (array of objects with name, definition, importance)
        - formulas (array with latex, explanation, variables)
        - principles (array of key principles)
        - prerequisites (array of required knowledge)
        - applications (array of real-world uses)
        - misconceptions (array of common errors)
        - practice_problems (array of problem suggestions)
        """
        
        response = await self.model.generate_content_async(prompt)
        return self._parse_json_response(response.text)
    
    async def generate_scenario(self, concept: Dict, duration: int = 300) -> Dict:
        """Generate visualization scenario for a concept"""
        prompt = f"""
        Concept: {concept['name']}
        Definition: {concept['definition']}
        Target Duration: {duration} seconds
        
        Create a detailed visualization scenario with scenes.
        For each scene specify:
        1. Scene title
        2. Duration (seconds)
        3. Visualization type (manim/matplotlib/plotly)
        4. Visual elements to show
        5. Animation description
        6. Key teaching points
        7. Transition to next scene
        
        Return as JSON with array of scenes.
        """
        
        response = await self.model.generate_content_async(prompt)
        return self._parse_json_response(response.text)
    
    async def generate_script(self, scene: Dict) -> str:
        """Generate narration script for a scene"""
        prompt = f"""
        Scene: {scene['title']}
        Duration: {scene['duration']} seconds
        Visuals: {scene['visual_elements']}
        
        Write engaging narration that:
        - Explains the concept clearly
        - Matches the visual timing
        - Uses conversational tone
        - Includes emphasis points
        - Asks engaging questions
        - Provides smooth transitions
        
        Target word count: {int(scene['duration'] * 2.5)} words
        (assuming ~150 words per minute speaking rate)
        
        Return only the script text, no additional formatting.
        """
        
        response = await self.model.generate_content_async(prompt)
        return response.text.strip()
    
    def _parse_json_response(self, text: str) -> Dict:
        """Parse JSON from AI response, handling markdown code blocks"""
        # Remove markdown code blocks if present
        if "```json" in text:
            text = text.split("```json")[1].split("```")[0]
        elif "```" in text:
            text = text.split("```")[1].split("```")[0]
        
        try:
            return json.loads(text.strip())
        except json.JSONDecodeError:
            # Fallback: try to extract JSON-like structure
            return {"raw_text": text, "parsed": False}
```

## Visualization System

### Manim Integration

```python
# visualization/manim_renderer.py
from manim import *
import tempfile
import os

class ManimRenderer:
    def __init__(self, quality="medium_quality", fps=30):
        self.quality = quality
        self.fps = fps
        self.temp_dir = tempfile.mkdtemp()
    
    def render_equation_transformation(self, 
                                      start_eq: str, 
                                      end_eq: str,
                                      duration: float = 3.0) -> str:
        """Render equation transformation animation"""
        
        class EquationTransform(Scene):
            def construct(self):
                eq1 = MathTex(start_eq)
                eq2 = MathTex(end_eq)
                
                self.play(Write(eq1))
                self.wait(1)
                self.play(Transform(eq1, eq2), run_time=duration)
                self.wait(1)
        
        return self._render_scene(EquationTransform)
    
    def render_graph_animation(self, 
                               function: str,
                               x_range: tuple = (-5, 5),
                               y_range: tuple = (-5, 5)) -> str:
        """Render function graph animation"""
        
        class GraphAnimation(Scene):
            def construct(self):
                axes = Axes(
                    x_range=x_range,
                    y_range=y_range,
                    axis_config={"include_tip": True}
                )
                
                # Parse function string and create graph
                graph = axes.plot(lambda x: eval(function), color=BLUE)
                
                self.play(Create(axes))
                self.play(Create(graph), run_time=2)
                self.wait(1)
        
        return self._render_scene(GraphAnimation)
    
    def render_vector_field(self, 
                           field_func: str,
                           x_range: tuple = (-3, 3),
                           y_range: tuple = (-3, 3)) -> str:
        """Render vector field for physics concepts"""
        
        class VectorFieldScene(Scene):
            def construct(self):
                plane = NumberPlane(
                    x_range=x_range,
                    y_range=y_range
                )
                
                # Create vector field
                field = ArrowVectorField(
                    lambda pos: eval(field_func),
                    x_range=x_range,
                    y_range=y_range
                )
                
                self.play(Create(plane))
                self.play(Create(field), run_time=3)
                self.wait(1)
        
        return self._render_scene(VectorFieldScene)
    
    def _render_scene(self, scene_class) -> str:
        """Render a Manim scene and return video path"""
        output_file = os.path.join(self.temp_dir, f"scene_{id(scene_class)}.mp4")
        
        config.quality = self.quality
        config.frame_rate = self.fps
        config.output_file = output_file
        
        scene = scene_class()
        scene.render()
        
        return output_file
```

### Matplotlib Integration

```python
# visualization/matplotlib_renderer.py
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import numpy as np
from typing import Callable, Tuple

class MatplotlibRenderer:
    def __init__(self, figsize=(10, 6), dpi=100):
        self.figsize = figsize
        self.dpi = dpi
    
    def render_function_plot(self, 
                            func: Callable,
                            x_range: Tuple[float, float],
                            title: str = "",
                            xlabel: str = "x",
                            ylabel: str = "y") -> str:
        """Render static function plot"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        x = np.linspace(x_range[0], x_range[1], 1000)
        y = func(x)
        
        ax.plot(x, y, linewidth=2)
        ax.set_title(title, fontsize=16)
        ax.set_xlabel(xlabel, fontsize=12)
        ax.set_ylabel(ylabel, fontsize=12)
        ax.grid(True, alpha=0.3)
        
        output_path = f"temp_plot_{id(fig)}.png"
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        
        return output_path
    
    def render_animated_plot(self,
                            func: Callable,
                            x_range: Tuple[float, float],
                            frames: int = 100,
                            duration: float = 5.0) -> str:
        """Render animated function plot"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        x = np.linspace(x_range[0], x_range[1], 1000)
        line, = ax.plot([], [], linewidth=2)
        
        ax.set_xlim(x_range)
        ax.set_ylim(-10, 10)  # Adjust based on function
        ax.grid(True, alpha=0.3)
        
        def init():
            line.set_data([], [])
            return line,
        
        def animate(frame):
            # Gradually reveal the function
            idx = int((frame / frames) * len(x))
            line.set_data(x[:idx], func(x[:idx]))
            return line,
        
        anim = animation.FuncAnimation(
            fig, animate, init_func=init,
            frames=frames, interval=duration*1000/frames,
            blit=True
        )
        
        output_path = f"temp_anim_{id(fig)}.mp4"
        anim.save(output_path, writer='ffmpeg', fps=30)
        plt.close()
        
        return output_path
    
    def render_parametric_plot(self,
                              x_func: Callable,
                              y_func: Callable,
                              t_range: Tuple[float, float],
                              title: str = "Parametric Plot") -> str:
        """Render parametric curve"""
        fig, ax = plt.subplots(figsize=self.figsize, dpi=self.dpi)
        
        t = np.linspace(t_range[0], t_range[1], 1000)
        x = x_func(t)
        y = y_func(t)
        
        ax.plot(x, y, linewidth=2)
        ax.set_title(title, fontsize=16)
        ax.set_aspect('equal')
        ax.grid(True, alpha=0.3)
        
        output_path = f"temp_parametric_{id(fig)}.png"
        plt.savefig(output_path, bbox_inches='tight')
        plt.close()
        
        return output_path
```

### Plotly Integration

```python
# visualization/plotly_renderer.py
import plotly.graph_objects as go
import plotly.express as px
import numpy as np
from typing import Callable, Tuple

class PlotlyRenderer:
    def __init__(self, width=800, height=600):
        self.width = width
        self.height = height
    
    def render_3d_surface(self,
                         func: Callable,
                         x_range: Tuple[float, float],
                         y_range: Tuple[float, float],
                         title: str = "3D Surface") -> str:
        """Render 3D surface plot"""
        x = np.linspace(x_range[0], x_range[1], 50)
        y = np.linspace(y_range[0], y_range[1], 50)
        X, Y = np.meshgrid(x, y)
        Z = func(X, Y)
        
        fig = go.Figure(data=[go.Surface(x=X, y=Y, z=Z)])
        fig.update_layout(
            title=title,
            width=self.width,
            height=self.height,
            scene=dict(
                xaxis_title='X',
                yaxis_title='Y',
                zaxis_title='Z'
            )
        )
        
        output_path = f"temp_3d_{id(fig)}.html"
        fig.write_html(output_path)
        
        return output_path
    
    def render_vector_field_3d(self,
                               field_func: Callable,
                               bounds: Tuple[float, float],
                               title: str = "Vector Field") -> str:
        """Render 3D vector field"""
        x, y, z = np.meshgrid(
            np.linspace(bounds[0], bounds[1], 10),
            np.linspace(bounds[0], bounds[1], 10),
            np.linspace(bounds[0], bounds[1], 10)
        )
        
        u, v, w = field_func(x, y, z)
        
        fig = go.Figure(data=go.Cone(
            x=x.flatten(),
            y=y.flatten(),
            z=z.flatten(),
            u=u.flatten(),
            v=v.flatten(),
            w=w.flatten(),
            colorscale='Blues',
            sizemode="absolute",
            sizeref=0.5
        ))
        
        fig.update_layout(
            title=title,
            width=self.width,
            height=self.height
        )
        
        output_path = f"temp_vector_{id(fig)}.html"
        fig.write_html(output_path)
        
        return output_path
    
    def render_interactive_graph(self,
                                data_points: dict,
                                plot_type: str = "scatter",
                                title: str = "") -> str:
        """Render interactive graph"""
        if plot_type == "scatter":
            fig = px.scatter(
                x=data_points['x'],
                y=data_points['y'],
                title=title
            )
        elif plot_type == "line":
            fig = px.line(
                x=data_points['x'],
                y=data_points['y'],
                title=title
            )
        
        fig.update_layout(
            width=self.width,
            height=self.height,
            hovermode='closest'
        )
        
        output_path = f"temp_interactive_{id(fig)}.html"
        fig.write_html(output_path)
        
        return output_path
```

## Audio System

### Voice Recording

```python
# audio/recorder.py
import sounddevice as sd
import numpy as np
import wave
import threading
from typing import Optional

class VoiceRecorder:
    def __init__(self, sample_rate=44100, channels=1):
        self.sample_rate = sample_rate
        self.channels = channels
        self.recording = False
        self.frames = []
        self.stream = None
    
    def start_recording(self):
        """Start recording audio"""
        self.recording = True
        self.frames = []
        
        def callback(indata, frames, time, status):
            if status:
                print(f"Recording status: {status}")
            if self.recording:
                self.frames.append(indata.copy())
        
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=callback
        )
        self.stream.start()
    
    def stop_recording(self) -> np.ndarray:
        """Stop recording and return audio data"""
        self.recording = False
        if self.stream:
            self.stream.stop()
            self.stream.close()
        
        if self.frames:
            return np.concatenate(self.frames, axis=0)
        return np.array([])
    
    def save_recording(self, filename: str, audio_data: np.ndarray):
        """Save recorded audio to WAV file"""
        with wave.open(filename, 'wb') as wf:
            wf.setnchannels(self.channels)
            wf.setsampwidth(2)  # 16-bit
            wf.setframerate(self.sample_rate)
            wf.writeframes((audio_data * 32767).astype(np.int16).tobytes())
    
    def get_audio_level(self) -> float:
        """Get current audio input level (0-1)"""
        if self.frames:
            recent_data = self.frames[-1] if len(self.frames) > 0 else np.array([0])
            return float(np.abs(recent_data).mean())
        return 0.0
    
    @staticmethod
    def list_input_devices():
        """List available audio input devices"""
        devices = sd.query_devices()
        input_devices = [d for d in devices if d['max_input_channels'] > 0]
        return input_devices
```

### Audio Processing

```python
# audio/processor.py
from pydub import AudioSegment
from pydub.effects import normalize, compress_dynamic_range
import librosa
import numpy as np

class AudioProcessor:
    @staticmethod
    def normalize_audio(audio_path: str, output_path: str) -> str:
        """Normalize audio levels"""
        audio = AudioSegment.from_file(audio_path)
        normalized = normalize(audio)
        normalized.export(output_path, format="wav")
        return output_path
    
    @staticmethod
    def remove_silence(audio_path: str, 
                      output_path: str,
                      silence_thresh: int = -40,
                      min_silence_len: int = 500) -> str:
        """Remove silence from audio"""
        audio = AudioSegment.from_file(audio_path)
        
        # Split on silence
        chunks = []
        for chunk in audio[::min_silence_len]:
            if chunk.dBFS > silence_thresh:
                chunks.append(chunk)
        
        if chunks:
            result = chunks[0]
            for chunk in chunks[1:]:
                result += chunk
            result.export(output_path, format="wav")
        
        return output_path
    
    @staticmethod
    def apply_noise_reduction(audio_path: str, output_path: str) -> str:
        """Apply noise reduction using spectral gating"""
        y, sr = librosa.load(audio_path)
        
        # Simple noise reduction via spectral gating
        S = librosa.stft(y)
        S_mag, S_phase = librosa.magphase(S)
        
        # Estimate noise floor
        noise_floor = np.median(S_mag, axis=1, keepdims=True)
        
        # Apply gate
        mask = S_mag > (noise_floor * 2)
        S_clean = S_mag * mask * S_phase
        
        # Reconstruct
        y_clean = librosa.istft(S_clean)
        
        # Save
        import soundfile as sf
        sf.write(output_path, y_clean, sr)
        
        return output_path
    
    @staticmethod
    def adjust_speed(audio_path: str, 
                    output_path: str,
                    speed_factor: float = 1.0) -> str:
        """Adjust audio playback speed"""
        audio = AudioSegment.from_file(audio_path)
        
        # Change speed without changing pitch
        sound_with_altered_frame_rate = audio._spawn(
            audio.raw_data,
            overrides={"frame_rate": int(audio.frame_rate * speed_factor)}
        )
        
        # Convert back to original frame rate
        result = sound_with_altered_frame_rate.set_frame_rate(audio.frame_rate)
        result.export(output_path, format="wav")
        
        return output_path
```

### Audio Mixing

```python
# audio/mixer.py
from pydub import AudioSegment
from typing import List, Tuple

class AudioMixer:
    @staticmethod
    def mix_voice_and_music(voice_path: str,
                           music_path: str,
                           output_path: str,
                           music_volume: float = -20,
                           ducking: bool = True) -> str:
        """Mix voice narration with background music"""
        voice = AudioSegment.from_file(voice_path)
        music = AudioSegment.from_file(music_path)
        
        # Adjust music volume
        music = music + music_volume
        
        # Loop music to match voice length
        if len(music) < len(voice):
            repeats = (len(voice) // len(music)) + 1
            music = music * repeats
        
        # Trim music to voice length
        music = music[:len(voice)]
        
        # Apply ducking if enabled
        if ducking:
            music = AudioMixer._apply_ducking(music, voice)
        
        # Mix
        mixed = voice.overlay(music)
        mixed.export(output_path, format="wav")
        
        return output_path
    
    @staticmethod
    def _apply_ducking(music: AudioSegment, 
                      voice: AudioSegment,
                      duck_amount: int = -10) -> AudioSegment:
        """Lower music volume when voice is present"""
        # Detect voice activity
        voice_chunks = voice[::100]  # Check every 100ms
        
        result = AudioSegment.empty()
        for i, chunk in enumerate(music[::100]):
            if i < len(voice_chunks) and voice_chunks[i].dBFS > -40:
                # Voice is present, duck music
                result += chunk + duck_amount
            else:
                # No voice, keep music at normal volume
                result += chunk
        
        return result
    
    @staticmethod
    def add_sound_effects(base_audio: str,
                         effects: List[Tuple[str, int]],
                         output_path: str) -> str:
        """Add sound effects at specific timestamps
        
        Args:
            base_audio: Path to base audio
            effects: List of (effect_path, timestamp_ms) tuples
            output_path: Output file path
        """
        base = AudioSegment.from_file(base_audio)
        
        for effect_path, timestamp in effects:
            effect = AudioSegment.from_file(effect_path)
            base = base.overlay(effect, position=timestamp)
        
        base.export(output_path, format="wav")
        return output_path
```

## Video Compilation

```python
# video/renderer.py
from moviepy.editor import *
from typing import List, Dict
import os

class VideoRenderer:
    def __init__(self, resolution=(1920, 1080), fps=30):
        self.resolution = resolution
        self.fps = fps
    
    def compile_video(self,
                     scenes: List[Dict],
                     audio_path: str,
                     output_path: str,
                     transitions: bool = True) -> str:
        """Compile scenes into final video with audio"""
        clips = []
        
        for scene in scenes:
            # Load visualization video/image
            if scene['type'] == 'video':
                clip = VideoFileClip(scene['path'])
            else:  # image
                clip = ImageClip(scene['path']).set_duration(scene['duration'])
            
            # Resize to target resolution
            clip = clip.resize(self.resolution)
            
            # Add transitions
            if transitions and len(clips) > 0:
                clip = clip.crossfadein(0.5)
            
            clips.append(clip)
        
        # Concatenate all clips
        final_video = concatenate_videoclips(clips, method="compose")
        
        # Add audio
        audio = AudioFileClip(audio_path)
        final_video = final_video.set_audio(audio)
        
        # Export
        final_video.write_videofile(
            output_path,
            fps=self.fps,
            codec='libx264',
            audio_codec='aac',
            temp_audiofile='temp-audio.m4a',
            remove_temp=True
        )
        
        return output_path
    
    def add_subtitles(self,
                     video_path: str,
                     subtitles: List[Dict],
                     output_path: str) -> str:
        """Add subtitles to video
        
        Args:
            subtitles: List of {'text': str, 'start': float, 'end': float}
        """
        video = VideoFileClip(video_path)
        
        subtitle_clips = []
        for sub in subtitles:
            txt_clip = TextClip(
                sub['text'],
                fontsize=24,
                color='white',
                bg_color='black',
                size=video.size
            )
            txt_clip = txt_clip.set_position(('center', 'bottom'))
            txt_clip = txt_clip.set_start(sub['start'])
            txt_clip = txt_clip.set_duration(sub['end'] - sub['start'])
            subtitle_clips.append(txt_clip)
        
        # Composite video with subtitles
        final = CompositeVideoClip([video] + subtitle_clips)
        final.write_videofile(output_path, codec='libx264')
        
        return output_path
```

## Streamlit UI Components

```python
# ui/components.py
import streamlit as st
from typing import Callable, Any

class UIComponents:
    @staticmethod
    def render_progress_bar(progress: float, text: str = ""):
        """Render progress bar with text"""
        st.progress(progress, text=text)
    
    @staticmethod
    def render_editable_text(key: str, 
                            default_value: str,
                            label: str = "",
                            height: int = 200) -> str:
        """Render editable text area"""
        return st.text_area(
            label,
            value=default_value,
            key=key,
            height=height
        )
    
    @staticmethod
    def render_scene_card(scene: Dict, 
                         on_edit: Callable,
                         on_delete: Callable):
        """Render a scene card with edit/delete buttons"""
        with st.container():
            col1, col2, col3 = st.columns([3, 1, 1])
            
            with col1:
                st.subheader(scene['title'])
                st.write(f"Duration: {scene['duration']}s")
                st.write(f"Type: {scene['visualization_type']}")
            
            with col2:
                if st.button("Edit", key=f"edit_{scene['id']}"):
                    on_edit(scene)
            
            with col3:
                if st.button("Delete", key=f"delete_{scene['id']}"):
                    on_delete(scene)
    
    @staticmethod
    def render_audio_player(audio_path: str, label: str = "Audio"):
        """Render audio player"""
        st.audio(audio_path, format='audio/wav')
        st.caption(label)
    
    @staticmethod
    def render_video_player(video_path: str, label: str = "Video"):
        """Render video player"""
        st.video(video_path)
        st.caption(label)
```

## Data Persistence

```python
# utils/project_manager.py
import json
import os
from datetime import datetime
from typing import Dict, Optional
import uuid

class ProjectManager:
    def __init__(self, projects_dir: str = "data/projects"):
        self.projects_dir = projects_dir
        os.makedirs(projects_dir, exist_ok=True)
    
    def create_project(self, title: str, topic: str) -> Dict:
        """Create a new project"""
        project = {
            "project_id": str(uuid.uuid4()),
            "title": title,
            "topic": topic,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat(),
            "status": "draft",
            "research": {},
            "scenario": {"scenes": []},
            "audio": {},
            "video": {}
        }
        
        self.save_project(project)
        return project
    
    def save_project(self, project: Dict):
        """Save project to disk"""
        project["updated_at"] = datetime.now().isoformat()
        
        project_dir = os.path.join(self.projects_dir, project["project_id"])
        os.makedirs(project_dir, exist_ok=True)
        
        project_file = os.path.join(project_dir, "project.json")
        with open(project_file, 'w') as f:
            json.dump(project, f, indent=2)
    
    def load_project(self, project_id: str) -> Optional[Dict]:
        """Load project from disk"""
        project_file = os.path.join(
            self.projects_dir,
            project_id,
            "project.json"
        )
        
        if os.path.exists(project_file):
            with open(project_file, 'r') as f:
                return json.load(f)
        return None
    
    def list_projects(self) -> list:
        """List all projects"""
        projects = []
        for project_id in os.listdir(self.projects_dir):
            project = self.load_project(project_id)
            if project:
                projects.append({
                    "id": project["project_id"],
                    "title": project["title"],
                    "topic": project["topic"],
                    "status": project["status"],
                    "updated_at": project["updated_at"]
                })
        
        return sorted(projects, key=lambda x: x["updated_at"], reverse=True)
    
    def delete_project(self, project_id: str):
        """Delete a project"""
        import shutil
        project_dir = os.path.join(self.projects_dir, project_id)
        if os.path.exists(project_dir):
            shutil.rmtree(project_dir)
```

## Configuration Management

```python
# config/settings.py
from pydantic import BaseModel, Field
from typing import Optional

class VisualizationSettings(BaseModel):
    manim_quality: str = Field(default="medium_quality")
    matplotlib_dpi: int = Field(default=100)
    plotly_width: int = Field(default=800)
    plotly_height: int = Field(default=600)

class AudioSettings(BaseModel):
    sample_rate: int = Field(default=44100)
    channels: int = Field(default=1)
    noise_reduction: bool = Field(default=True)
    normalize: bool = Field(default=True)

class VideoSettings(BaseModel):
    resolution: tuple = Field(default=(1920, 1080))
    fps: int = Field(default=30)
    bitrate: str = Field(default="5000k")
    codec: str = Field(default="libx264")

class AISettings(BaseModel):
    provider: str = Field(default="gemini")
    model: str = Field(default="gemini-1.5-flash-latest")
    temperature: float = Field(default=0.7)
    max_tokens: int = Field(default=8000)

class AppSettings(BaseModel):
    visualization: VisualizationSettings = Field(default_factory=VisualizationSettings)
    audio: AudioSettings = Field(default_factory=AudioSettings)
    video: VideoSettings = Field(default_factory=VideoSettings)
    ai: AISettings = Field(default_factory=AISettings)
    
    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
```

## Error Handling

```python
# utils/error_handler.py
import logging
from functools import wraps
from typing import Callable

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def handle_errors(func: Callable) -> Callable:
    """Decorator for error handling"""
    @wraps(func)
    async def wrapper(*args, **kwargs):
        try:
            return await func(*args, **kwargs)
        except Exception as e:
            logger.error(f"Error in {func.__name__}: {str(e)}")
            raise
    return wrapper

class ContentCreationError(Exception):
    """Base exception for content creation errors"""
    pass

class AIGenerationError(ContentCreationError):
    """Error during AI content generation"""
    pass

class VisualizationError(ContentCreationError):
    """Error during visualization rendering"""
    pass

class AudioProcessingError(ContentCreationError):
    """Error during audio processing"""
    pass

class VideoRenderingError(ContentCreationError):
    """Error during video rendering"""
    pass
```

## Performance Optimization

```python
# utils/cache_manager.py
import hashlib
import pickle
import os
from functools import wraps

class CacheManager:
    def __init__(self, cache_dir: str = ".cache"):
        self.cache_dir = cache_dir
        os.makedirs(cache_dir, exist_ok=True)
    
    def cache_result(self, func):
        """Decorator to cache function results"""
        @wraps(func)
        def wrapper(*args, **kwargs):
            # Create cache key from function name and arguments
            key = self._create_key(func.__name__, args, kwargs)
            cache_file = os.path.join(self.cache_dir, f"{key}.pkl")
            
            # Check if cached result exists
            if os.path.exists(cache_file):
                with open(cache_file, 'rb') as f:
                    return pickle.load(f)
            
            # Execute function and cache result
            result = func(*args, **kwargs)
            with open(cache_file, 'wb') as f:
                pickle.dump(result, f)
            
            return result
        return wrapper
    
    def _create_key(self, func_name: str, args: tuple, kwargs: dict) -> str:
        """Create cache key from function name and arguments"""
        key_data = f"{func_name}_{str(args)}_{str(kwargs)}"
        return hashlib.md5(key_data.encode()).hexdigest()
    
    def clear_cache(self):
        """Clear all cached results"""
        for file in os.listdir(self.cache_dir):
            os.remove(os.path.join(self.cache_dir, file))
```

## Testing Strategy

```python
# tests/test_ai_engine.py
import pytest
from core.ai_engine import AIEngine

@pytest.fixture
def ai_engine():
    return AIEngine(api_key="test_key")

def test_research_generation(ai_engine):
    """Test AI research generation"""
    result = ai_engine.generate_research("Projectile Motion", "high_school")
    assert "concepts" in result
    assert "formulas" in result
    assert len(result["concepts"]) > 0

def test_scenario_generation(ai_engine):
    """Test scenario generation"""
    concept = {
        "name": "Newton's Second Law",
        "definition": "F = ma"
    }
    result = ai_engine.generate_scenario(concept, duration=300)
    assert "scenes" in result
    assert len(result["scenes"]) > 0

# tests/test_visualization.py
def test_manim_rendering():
    """Test Manim rendering"""
    from visualization.manim_renderer import ManimRenderer
    renderer = ManimRenderer()
    output = renderer.render_equation_transformation("x^2", "x^2 + 2x + 1")
    assert os.path.exists(output)

# tests/test_audio.py
def test_audio_recording():
    """Test audio recording"""
    from audio.recorder import VoiceRecorder
    recorder = VoiceRecorder()
    devices = recorder.list_input_devices()
    assert len(devices) > 0
```

## Deployment Considerations

### Docker Configuration

```dockerfile
# Dockerfile
FROM python:3.11-slim

# Install system dependencies
RUN apt-get update && apt-get install -y \
    ffmpeg \
    texlive-full \
    && rm -rf /var/lib/apt/lists/*

# Set working directory
WORKDIR /app

# Copy requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose Streamlit port
EXPOSE 8501

# Run application
CMD ["streamlit", "run", "app.py", "--server.port=8501", "--server.address=0.0.0.0"]
```

### Environment Variables

```bash
# .env.example
GEMINI_API_KEY=your_api_key_here
OPENAI_API_KEY=optional
ANTHROPIC_API_KEY=optional

# Application settings
APP_ENV=development
LOG_LEVEL=INFO
CACHE_ENABLED=true

# Paths
PROJECTS_DIR=data/projects
ASSETS_DIR=assets
CACHE_DIR=.cache
```

## Conclusion

This technical specification provides detailed implementation guidance for all major components of the AI-powered educational content creation tool. Each module is designed to be modular, testable, and maintainable, with clear interfaces and error handling.