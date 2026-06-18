"""
Professional color schemes for educational visualizations.
Inspired by 3Blue1Brown and modern educational content.
"""
from typing import Dict, List
from enum import Enum


class ColorScheme(Enum):
    """Available color schemes."""
    BLUE_BROWN = "3blue1brown"
    DARK_MODE = "dark"
    LIGHT_MODE = "light"
    HIGH_CONTRAST = "high_contrast"
    WARM = "warm"
    COOL = "cool"


class Colors:
    """Professional color palettes for educational content."""
    
    # 3Blue1Brown signature colors
    BLUE_BROWN = {
        "background": "#0C0C0C",
        "primary": "#58C4DD",      # Signature blue
        "secondary": "#83C167",    # Green
        "accent": "#FC6255",       # Red/Pink
        "text": "#ECECEC",         # Light gray
        "highlight": "#FFFF00",    # Yellow
        "grid": "#404040",         # Dark gray
        "equation": "#FFFFFF",     # White for math
    }
    
    # Dark mode (modern, professional)
    DARK_MODE = {
        "background": "#1a1a1a",
        "primary": "#3498db",      # Blue
        "secondary": "#2ecc71",    # Green
        "accent": "#e74c3c",       # Red
        "text": "#ecf0f1",         # Light
        "highlight": "#f39c12",    # Orange
        "grid": "#2c3e50",         # Dark blue-gray
        "equation": "#ffffff",
    }
    
    # Light mode (clean, minimal)
    LIGHT_MODE = {
        "background": "#FFFFFF",
        "primary": "#2980b9",      # Dark blue
        "secondary": "#27ae60",    # Dark green
        "accent": "#c0392b",       # Dark red
        "text": "#2c3e50",         # Dark gray
        "highlight": "#f39c12",    # Orange
        "grid": "#bdc3c7",         # Light gray
        "equation": "#000000",
    }
    
    # High contrast (accessibility)
    HIGH_CONTRAST = {
        "background": "#000000",
        "primary": "#00FF00",      # Bright green
        "secondary": "#00FFFF",    # Cyan
        "accent": "#FF00FF",       # Magenta
        "text": "#FFFFFF",         # White
        "highlight": "#FFFF00",    # Yellow
        "grid": "#808080",         # Gray
        "equation": "#FFFFFF",
    }
    
    # Warm palette (inviting, energetic)
    WARM = {
        "background": "#2c1810",
        "primary": "#ff6b6b",      # Coral red
        "secondary": "#feca57",    # Yellow
        "accent": "#ee5a6f",       # Pink
        "text": "#f8f9fa",         # Off-white
        "highlight": "#ff9ff3",    # Light pink
        "grid": "#4a3428",         # Brown
        "equation": "#ffffff",
    }
    
    # Cool palette (calm, focused)
    COOL = {
        "background": "#0a1929",
        "primary": "#5dade2",      # Sky blue
        "secondary": "#48c9b0",    # Turquoise
        "accent": "#af7ac5",       # Purple
        "text": "#ecf0f1",         # Light
        "highlight": "#f8b739",    # Gold
        "grid": "#1c3a52",         # Dark blue
        "equation": "#ffffff",
    }
    
    @classmethod
    def get_scheme(cls, scheme: ColorScheme) -> Dict[str, str]:
        """
        Get color scheme by name.
        
        Args:
            scheme: ColorScheme enum value
            
        Returns:
            Dict with color definitions
        """
        scheme_map = {
            ColorScheme.BLUE_BROWN: cls.BLUE_BROWN,
            ColorScheme.DARK_MODE: cls.DARK_MODE,
            ColorScheme.LIGHT_MODE: cls.LIGHT_MODE,
            ColorScheme.HIGH_CONTRAST: cls.HIGH_CONTRAST,
            ColorScheme.WARM: cls.WARM,
            ColorScheme.COOL: cls.COOL,
        }
        return scheme_map.get(scheme, cls.BLUE_BROWN)
    
    @classmethod
    def get_manim_colors(cls, scheme: ColorScheme) -> str:
        """
        Get Manim color definitions as Python code.
        
        Args:
            scheme: ColorScheme enum value
            
        Returns:
            Python code string defining colors
        """
        colors = cls.get_scheme(scheme)
        
        code = f"""
# Color Scheme: {scheme.value}
BG_COLOR = "{colors['background']}"
PRIMARY_COLOR = "{colors['primary']}"
SECONDARY_COLOR = "{colors['secondary']}"
ACCENT_COLOR = "{colors['accent']}"
TEXT_COLOR = "{colors['text']}"
HIGHLIGHT_COLOR = "{colors['highlight']}"
GRID_COLOR = "{colors['grid']}"
EQUATION_COLOR = "{colors['equation']}"
"""
        return code


class VisualStyle:
    """Visual styling guidelines for professional animations."""
    
    # Font sizes (3Blue1Brown style)
    FONT_SIZES = {
        "title": 48,
        "heading": 40,
        "body": 32,
        "caption": 24,
        "small": 20,
    }
    
    # Animation timings (smooth and professional)
    TIMINGS = {
        "instant": 0.2,
        "quick": 0.5,
        "normal": 1.0,
        "slow": 1.5,
        "dramatic": 2.0,
    }
    
    # Spacing and layout
    LAYOUT = {
        "title_buffer": 0.5,
        "element_spacing": 0.8,
        "margin": 1.0,
        "line_spacing": 1.2,
    }
    
    # Stroke widths
    STROKES = {
        "thin": 2,
        "normal": 3,
        "thick": 4,
        "bold": 6,
    }
    
    @classmethod
    def get_style_code(cls) -> str:
        """Get Manim style definitions as Python code."""
        return f"""
# Visual Style Constants
TITLE_SIZE = {cls.FONT_SIZES['title']}
HEADING_SIZE = {cls.FONT_SIZES['heading']}
BODY_SIZE = {cls.FONT_SIZES['body']}
CAPTION_SIZE = {cls.FONT_SIZES['caption']}

INSTANT = {cls.TIMINGS['instant']}
QUICK = {cls.TIMINGS['quick']}
NORMAL = {cls.TIMINGS['normal']}
SLOW = {cls.TIMINGS['slow']}
DRAMATIC = {cls.TIMINGS['dramatic']}

TITLE_BUFF = {cls.LAYOUT['title_buffer']}
SPACING = {cls.LAYOUT['element_spacing']}
MARGIN = {cls.LAYOUT['margin']}

THIN_STROKE = {cls.STROKES['thin']}
NORMAL_STROKE = {cls.STROKES['normal']}
THICK_STROKE = {cls.STROKES['thick']}
BOLD_STROKE = {cls.STROKES['bold']}
"""


def get_complete_style(scheme: ColorScheme = ColorScheme.BLUE_BROWN) -> str:
    """
    Get complete style code for Manim scenes.
    
    Args:
        scheme: Color scheme to use
        
    Returns:
        Complete Python code for colors and styles
    """
    return Colors.get_manim_colors(scheme) + "\n" + VisualStyle.get_style_code()


# Made with Bob