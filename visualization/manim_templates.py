"""
Professional Manim animation templates for educational content.
3Blue1Brown-style high-quality visualizations.
"""
from typing import Dict, Any, List


class ManimTemplates:
    """Collection of professional Manim animation templates."""
    
    @staticmethod
    def equation_transformation(equations: List[str], colors: List[str] = None) -> str:
        """
        Generate code for smooth equation transformations.
        
        Args:
            equations: List of LaTeX equations to transform between
            colors: Optional list of colors for each equation
            
        Returns:
            Manim code string
        """
        if not colors:
            colors = ["PRIMARY_COLOR"] * len(equations)
        
        code = f"""
# Equation Transformation (3Blue1Brown style)
equations = []
"""
        for i, (eq, color) in enumerate(zip(equations, colors)):
            code += f'equations.append(MathTex("{eq}", color={color}))\n'
        
        code += """
# Position first equation
equations[0].move_to(ORIGIN)
self.play(Write(equations[0]), run_time=NORMAL)
self.wait(QUICK)

# Transform through all equations
for i in range(1, len(equations)):
    equations[i].move_to(ORIGIN)
    self.play(
        Transform(equations[i-1], equations[i]),
        run_time=SLOW
    )
    self.wait(QUICK)
"""
        return code
    
    @staticmethod
    def geometric_construction(shape_type: str = "circle") -> str:
        """
        Generate code for geometric constructions.
        
        Args:
            shape_type: Type of shape ('circle', 'triangle', 'square', 'polygon')
            
        Returns:
            Manim code string
        """
        templates = {
            "circle": """
# Circle Construction with Annotations
circle = Circle(radius=2, color=PRIMARY_COLOR, stroke_width=THICK_STROKE)
center = Dot(ORIGIN, color=ACCENT_COLOR)
center_label = MathTex("O", color=TEXT_COLOR).next_to(center, DOWN, buff=0.2)

# Radius
radius = Line(ORIGIN, circle.point_at_angle(0), color=SECONDARY_COLOR, stroke_width=NORMAL_STROKE)
radius_label = MathTex("r", color=SECONDARY_COLOR).move_to(radius.get_center() + UP * 0.3)

# Animate construction
self.play(GrowFromCenter(center), run_time=QUICK)
self.play(Write(center_label), run_time=QUICK)
self.play(Create(circle), run_time=SLOW)
self.play(Create(radius), run_time=NORMAL)
self.play(Write(radius_label), run_time=QUICK)
self.wait(NORMAL)

# Highlight circumference
self.play(
    circle.animate.set_color(HIGHLIGHT_COLOR).set_stroke(width=BOLD_STROKE),
    run_time=NORMAL
)
self.wait(QUICK)
""",
            "triangle": """
# Triangle Construction with Labels
vertices = [
    np.array([-2, -1, 0]),
    np.array([2, -1, 0]),
    np.array([0, 2, 0])
]

# Create triangle
triangle = Polygon(*vertices, color=PRIMARY_COLOR, stroke_width=THICK_STROKE)
self.play(Create(triangle), run_time=SLOW)

# Add vertex labels
labels = []
label_texts = ["A", "B", "C"]
directions = [DL, DR, UP]
for vertex, text, direction in zip(vertices, label_texts, directions):
    dot = Dot(vertex, color=ACCENT_COLOR)
    label = MathTex(text, color=TEXT_COLOR).next_to(dot, direction, buff=0.2)
    self.play(GrowFromCenter(dot), Write(label), run_time=QUICK)
    labels.append((dot, label))

self.wait(NORMAL)

# Highlight sides
sides = [
    Line(vertices[0], vertices[1], color=SECONDARY_COLOR, stroke_width=BOLD_STROKE),
    Line(vertices[1], vertices[2], color=SECONDARY_COLOR, stroke_width=BOLD_STROKE),
    Line(vertices[2], vertices[0], color=SECONDARY_COLOR, stroke_width=BOLD_STROKE)
]
for side in sides:
    self.play(Create(side), run_time=QUICK)
self.wait(QUICK)
"""
        }
        return templates.get(shape_type, templates["circle"])
    
    @staticmethod
    def function_graph(function_latex: str = "x^2", x_range: tuple = (-3, 3)) -> str:
        """
        Generate code for function graphing with annotations.
        
        Args:
            function_latex: LaTeX representation of function
            x_range: Tuple of (min, max) for x-axis
            
        Returns:
            Manim code string
        """
        return f"""
# Function Graph with Axes (3Blue1Brown style)
axes = Axes(
    x_range=[{x_range[0]}, {x_range[1]}, 1],
    y_range=[-2, 10, 2],
    x_length=10,
    y_length=6,
    axis_config={{"color": GRID_COLOR, "stroke_width": THIN_STROKE}},
    tips=True
)

# Add labels
x_label = axes.get_x_axis_label("x", direction=RIGHT, buff=0.3)
y_label = axes.get_y_axis_label("y", direction=UP, buff=0.3)

# Create axes
self.play(Create(axes), Write(x_label), Write(y_label), run_time=SLOW)
self.wait(QUICK)

# Show function equation
func_eq = MathTex("f(x) = {function_latex}", color=PRIMARY_COLOR)
func_eq.to_edge(UP, buff=TITLE_BUFF)
self.play(Write(func_eq), run_time=NORMAL)
self.wait(QUICK)

# Plot the function
graph = axes.plot(
    lambda x: x**2,  # Modify based on function
    color=PRIMARY_COLOR,
    stroke_width=THICK_STROKE
)
self.play(Create(graph), run_time=DRAMATIC)
self.wait(NORMAL)

# Add point of interest
point_x = 2
point = Dot(axes.c2p(point_x, point_x**2), color=ACCENT_COLOR, radius=0.1)
point_label = MathTex(f"({point_x}, {point_x**2})", color=ACCENT_COLOR)
point_label.next_to(point, UR, buff=0.2)

self.play(GrowFromCenter(point), Write(point_label), run_time=NORMAL)
self.wait(NORMAL)

# Trace tangent line
tangent = axes.plot(
    lambda x: 2*point_x*(x - point_x) + point_x**2,
    color=SECONDARY_COLOR,
    stroke_width=NORMAL_STROKE,
    x_range=[point_x-1, point_x+1]
)
self.play(Create(tangent), run_time=NORMAL)
self.wait(QUICK)
"""
    
    @staticmethod
    def vector_visualization(vectors: List[tuple] = None) -> str:
        """
        Generate code for vector demonstrations.
        
        Args:
            vectors: List of (x, y) tuples for vectors
            
        Returns:
            Manim code string
        """
        if not vectors:
            vectors = [(2, 1), (1, 2), (3, 3)]
        
        return f"""
# Vector Visualization (3Blue1Brown style)
# Create coordinate plane
plane = NumberPlane(
    x_range=[-5, 5, 1],
    y_range=[-5, 5, 1],
    background_line_style={{
        "stroke_color": GRID_COLOR,
        "stroke_width": 1,
        "stroke_opacity": 0.3
    }}
)
self.play(Create(plane), run_time=SLOW)
self.wait(QUICK)

# Define vectors
vectors_data = {vectors}
vector_objects = []
vector_labels = []

# Create and animate vectors
colors = [PRIMARY_COLOR, SECONDARY_COLOR, ACCENT_COLOR]
for i, (vx, vy) in enumerate(vectors_data):
    # Create vector
    vec = Vector(
        [vx, vy, 0],
        color=colors[i % len(colors)],
        stroke_width=THICK_STROKE
    )
    
    # Create label
    label = MathTex(
        f"\\vec{{v}}_{i+1}",
        color=colors[i % len(colors)]
    ).next_to(vec.get_end(), UP, buff=0.2)
    
    # Animate
    self.play(GrowArrow(vec), run_time=NORMAL)
    self.play(Write(label), run_time=QUICK)
    self.wait(QUICK)
    
    vector_objects.append(vec)
    vector_labels.append(label)

self.wait(NORMAL)

# Show vector addition (if multiple vectors)
if len(vectors_data) >= 2:
    result_vec = Vector(
        [vectors_data[0][0] + vectors_data[1][0],
         vectors_data[0][1] + vectors_data[1][1], 0],
        color=HIGHLIGHT_COLOR,
        stroke_width=BOLD_STROKE
    )
    result_label = MathTex(
        "\\vec{{v}}_1 + \\vec{{v}}_2",
        color=HIGHLIGHT_COLOR
    ).next_to(result_vec.get_end(), UP, buff=0.2)
    
    self.play(
        GrowArrow(result_vec),
        Write(result_label),
        run_time=DRAMATIC
    )
    self.wait(NORMAL)
"""
    
    @staticmethod
    def number_line_animation(values: List[float] = None, concept: str = "integers") -> str:
        """
        Generate code for number line demonstrations.
        
        Args:
            values: List of values to highlight
            concept: Concept being demonstrated
            
        Returns:
            Manim code string
        """
        if not values:
            values = [-2, -1, 0, 1, 2]
        
        return f"""
# Number Line Animation (3Blue1Brown style)
# Create number line
number_line = NumberLine(
    x_range=[-5, 5, 1],
    length=12,
    color=GRID_COLOR,
    include_numbers=True,
    label_direction=DOWN,
    font_size=CAPTION_SIZE
)
number_line.move_to(ORIGIN)

# Title
title = Text("{concept.title()}", font_size=TITLE_SIZE, color=PRIMARY_COLOR)
title.to_edge(UP, buff=TITLE_BUFF)

self.play(Write(title), run_time=NORMAL)
self.play(Create(number_line), run_time=SLOW)
self.wait(QUICK)

# Highlight specific values
values = {values}
dots = []
labels = []

for val in values:
    # Create dot
    dot = Dot(
        number_line.n2p(val),
        color=ACCENT_COLOR,
        radius=0.12
    )
    
    # Create label
    label = MathTex(str(val), color=ACCENT_COLOR, font_size=BODY_SIZE)
    label.next_to(dot, UP, buff=0.3)
    
    # Animate
    self.play(
        GrowFromCenter(dot),
        Write(label),
        run_time=QUICK
    )
    
    dots.append(dot)
    labels.append(label)

self.wait(NORMAL)

# Pulse effect for emphasis
self.play(
    *[dot.animate.scale(1.5).set_color(HIGHLIGHT_COLOR) for dot in dots],
    run_time=QUICK
)
self.play(
    *[dot.animate.scale(1/1.5).set_color(ACCENT_COLOR) for dot in dots],
    run_time=QUICK
)
self.wait(NORMAL)
"""
    
    @staticmethod
    def concept_introduction(title: str, definition: str, key_points: List[str]) -> str:
        """
        Generate code for concept introduction with visual hierarchy.
        
        Args:
            title: Concept title
            definition: Definition text
            key_points: List of key points
            
        Returns:
            Manim code string
        """
        return f"""
# Concept Introduction (3Blue1Brown style)
# Title with dramatic entrance
title = Text("{title}", font_size=TITLE_SIZE, color=PRIMARY_COLOR, weight=BOLD)
title.to_edge(UP, buff=TITLE_BUFF)

# Zoom effect
title.scale(0.1)
self.play(
    title.animate.scale(10).set_opacity(0),
    rate_func=rush_from,
    run_time=INSTANT
)
title.scale(0.1).set_opacity(1)
self.play(
    title.animate.scale(1),
    rate_func=smooth,
    run_time=DRAMATIC
)

# Underline
underline = Line(
    title.get_left() + DOWN * 0.2,
    title.get_right() + DOWN * 0.2,
    color=ACCENT_COLOR,
    stroke_width=THICK_STROKE
)
self.play(Create(underline), run_time=NORMAL)
self.wait(NORMAL)

# Definition box
definition_text = Text(
    "{definition[:80]}...",
    font_size=BODY_SIZE,
    color=TEXT_COLOR,
    line_spacing=1.3
)
definition_text.move_to(ORIGIN + UP * 0.5)

definition_box = SurroundingRectangle(
    definition_text,
    color=SECONDARY_COLOR,
    buff=0.3,
    corner_radius=0.1
)

self.play(
    FadeIn(definition_box),
    Write(definition_text),
    run_time=SLOW
)
self.wait(NORMAL)

# Clear for key points
self.play(
    FadeOut(definition_text),
    FadeOut(definition_box),
    run_time=NORMAL
)

# Key points with bullets
key_points = {key_points[:3]}  # Limit to 3 points
bullets = VGroup()

for i, point in enumerate(key_points):
    # Bullet point
    bullet = Dot(color=ACCENT_COLOR, radius=0.12)
    bullet.to_edge(LEFT, buff=MARGIN).shift(UP * (1 - i * SPACING))
    
    # Text
    text = Text(
        point[:60],
        font_size=BODY_SIZE,
        color=TEXT_COLOR
    )
    text.next_to(bullet, RIGHT, buff=0.3)
    text.align_to(bullet, UP)
    
    # Animate
    self.play(GrowFromCenter(bullet), run_time=INSTANT)
    self.play(Write(text), run_time=NORMAL)
    self.wait(QUICK)
    
    bullets.add(bullet, text)

self.wait(NORMAL)

# Fade out everything
self.play(
    FadeOut(title),
    FadeOut(underline),
    FadeOut(bullets),
    run_time=NORMAL
)
"""


# Made with Bob