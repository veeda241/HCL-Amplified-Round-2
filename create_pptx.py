"""
Generate a professional PowerPoint presentation for SkillRoute Research Paper.
Run: python create_pptx.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Color Palette ──────────────────────────────────────────────
BG_DARK      = RGBColor(0x0F, 0x17, 0x2A)   # Deep navy
BG_LIGHT     = RGBColor(0x1E, 0x29, 0x3B)   # Slate
ACCENT_BLUE  = RGBColor(0x38, 0xBD, 0xF8)   # Bright blue
ACCENT_PURPLE= RGBColor(0xA7, 0x8B, 0xFA)   # Purple
ACCENT_GREEN = RGBColor(0x4A, 0xDE, 0x80)   # Green
ACCENT_ORANGE= RGBColor(0xFB, 0x92, 0x3C)   # Orange
ACCENT_PINK  = RGBColor(0xF4, 0x72, 0xB6)   # Pink
WHITE        = RGBColor(0xFF, 0xFF, 0xFF)
GRAY_LIGHT   = RGBColor(0xCB, 0xD5, 0xE1)
GRAY_MED     = RGBColor(0x94, 0xA3, 0xB8)
GRAY_DARK    = RGBColor(0x47, 0x55, 0x69)

prs = Presentation()
prs.slide_width  = Inches(13.333)
prs.slide_height = Inches(7.5)

SW = prs.slide_width
SH = prs.slide_height


# ── Helpers ────────────────────────────────────────────────────

def _set_bg(slide, color):
    bg = slide.background
    fill = bg.fill
    fill.solid()
    fill.fore_color.rgb = color

def _add_textbox(slide, left, top, width, height):
    return slide.shapes.add_textbox(left, top, width, height)

def _set_text(tf, text, size=18, bold=False, color=WHITE, align=PP_ALIGN.LEFT, font_name="Calibri"):
    tf.clear()
    tf.word_wrap = True
    p = tf.paragraphs[0]
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align
    return p

def _add_paragraph(tf, text, size=16, bold=False, color=WHITE, align=PP_ALIGN.LEFT, space_before=Pt(6), font_name="Calibri"):
    p = tf.add_paragraph()
    p.text = text
    p.font.size = Pt(size)
    p.font.bold = bold
    p.font.color.rgb = color
    p.font.name = font_name
    p.alignment = align
    if space_before:
        p.space_before = space_before
    return p

def _add_rounded_rect(slide, left, top, width, height, fill_color, border_color=None):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    if border_color:
        shape.line.color.rgb = border_color
        shape.line.width = Pt(1.5)
    else:
        shape.line.fill.background()
    shape.shadow.inherit = False
    return shape

def _add_circle(slide, left, top, size, fill_color):
    shape = slide.shapes.add_shape(
        MSO_SHAPE.OVAL, left, top, size, size
    )
    shape.fill.solid()
    shape.fill.fore_color.rgb = fill_color
    shape.line.fill.background()
    shape.shadow.inherit = False
    return shape

def _add_slide_number(slide, num, total=20):
    tb = _add_textbox(slide, Inches(12.0), Inches(7.05), Inches(1.2), Inches(0.4))
    _set_text(tb.text_frame, f"{num} / {total}", size=10, color=GRAY_MED, align=PP_ALIGN.RIGHT)


# ── Slide Builders ─────────────────────────────────────────────

def slide_title(slide):
    _set_bg(slide, BG_DARK)
    # Accent line
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.06))
    shape.fill.solid(); shape.fill.fore_color.rgb = ACCENT_BLUE; shape.line.fill.background()
    # Title
    tb = _add_textbox(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.5))
    _set_text(tb.text_frame, "AI-Powered Career Decision-Making", size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    _add_paragraph(tb.text_frame, "Integrating Psychological Theories into\nPersonalized Learning Platforms", size=28, color=ACCENT_BLUE, align=PP_ALIGN.CENTER, space_before=Pt(12))
    # Subtitle
    tb2 = _add_textbox(slide, Inches(3), Inches(4.5), Inches(7.3), Inches(1.2))
    _set_text(tb2.text_frame, "[Your Name]", size=20, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)
    _add_paragraph(tb2.text_frame, "Department of Psychology  •  [Your College Name]  •  August 2026", size=14, color=GRAY_MED, align=PP_ALIGN.CENTER, space_before=Pt(8))


def slide_problem(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 2)
    # Header
    tb = _add_textbox(slide, Inches(0.8), Inches(0.4), Inches(8), Inches(0.7))
    _set_text(tb.text_frame, "🎯  The Problem: Career Indecision", size=30, bold=True, color=WHITE)
    # Stat box
    box = _add_rounded_rect(slide, Inches(0.8), Inches(1.4), Inches(4), Inches(2.5), BG_LIGHT, ACCENT_BLUE)
    tb = _add_textbox(slide, Inches(1.2), Inches(1.6), Inches(3.2), Inches(2))
    _set_text(tb.text_frame, "80%", size=64, bold=True, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)
    _add_paragraph(tb.text_frame, "of students experience significant\ncareer confusion during education", size=16, color=GRAY_LIGHT, align=PP_ALIGN.CENTER, space_before=Pt(8))
    # Challenges
    challenges = [
        ("Too many career options", "→ Overwhelm", ACCENT_ORANGE),
        ("Lack of personalized guidance", "→ Generic advice", ACCENT_PINK),
        ("Rapidly changing industry demands", "→ Outdated information", ACCENT_PURPLE),
        ("No clear learning order", "→ Directionless exploration", ACCENT_GREEN),
    ]
    for i, (title, desc, color) in enumerate(challenges):
        y = Inches(1.4 + i * 1.1)
        box = _add_rounded_rect(slide, Inches(5.3), y, Inches(7.2), Inches(0.9), BG_LIGHT)
        tb = _add_textbox(slide, Inches(5.6), y + Inches(0.1), Inches(6.6), Inches(0.7))
        _set_text(tb.text_frame, title, size=16, bold=True, color=color)
        _add_paragraph(tb.text_frame, desc, size=14, color=GRAY_LIGHT, space_before=Pt(2))


def slide_research_question(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 3)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.7))
    _set_text(tb.text_frame, "🔬  Central Research Question", size=30, bold=True, color=WHITE)
    # Question box
    box = _add_rounded_rect(slide, Inches(1.2), Inches(1.5), Inches(10.9), Inches(1.8), BG_LIGHT, ACCENT_PURPLE)
    tb = _add_textbox(slide, Inches(1.6), Inches(1.7), Inches(10.1), Inches(1.4))
    _set_text(tb.text_frame, "\"How can psychological theories of career decision-making,\nself-efficacy, and adaptive learning be operationalized\nin an AI-powered learning platform?\"", size=20, bold=False, color=ACCENT_PURPLE, align=PP_ALIGN.CENTER)
    # Contributions
    contribs = [
        ("1", "Theoretical\nOperationalization", "Translating abstract psychology\nconstructs into computational mechanisms", ACCENT_BLUE),
        ("2", "System\nArchitecture", "Embedding psychological principles\nat every layer of the system", ACCENT_GREEN),
        ("3", "Practical\nImpact", "Demonstrating psychologically grounded\nAI produces better career guidance", ACCENT_ORANGE),
    ]
    for i, (num, title, desc, color) in enumerate(contribs):
        x = Inches(1.0 + i * 4.0)
        box = _add_rounded_rect(slide, x, Inches(3.8), Inches(3.6), Inches(3.0), BG_LIGHT)
        circle = _add_circle(slide, x + Inches(1.5), Inches(4.0), Inches(0.7), color)
        tb = _add_textbox(slide, x + Inches(1.5), Inches(4.05), Inches(0.7), Inches(0.6))
        _set_text(tb.text_frame, num, size=24, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
        tb2 = _add_textbox(slide, x + Inches(0.2), Inches(4.9), Inches(3.2), Inches(0.8))
        _set_text(tb2.text_frame, title, size=16, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
        tb3 = _add_textbox(slide, x + Inches(0.2), Inches(5.7), Inches(3.2), Inches(0.8))
        _set_text(tb3.text_frame, desc, size=12, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)


def slide_solution(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 4)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.7))
    _set_text(tb.text_frame, "💡  The Solution: SkillRoute", size=30, bold=True, color=WHITE)
    # Subtitle
    tb = _add_textbox(slide, Inches(0.8), Inches(1.2), Inches(10), Inches(0.5))
    _set_text(tb.text_frame, "An AI-powered career decision-making & personalized learning platform", size=16, color=GRAY_LIGHT)
    # Feature cards
    features = [
        ("🧠", "Decides", "Not just recommends —\ndecides the best career path", ACCENT_BLUE),
        ("📋", "Profiles", "5-step psychological\nassessment of learner", ACCENT_PURPLE),
        ("🗺️", "Plans", "Personalized, time-bound\nlearning roadmaps", ACCENT_GREEN),
        ("📊", "Tracks", "Monitors progress &\nadapts to performance", ACCENT_ORANGE),
        ("🎯", "Assesses", "Tests actual skills vs.\nself-reported abilities", ACCENT_PINK),
    ]
    for i, (icon, title, desc, color) in enumerate(features):
        x = Inches(0.5 + i * 2.5)
        box = _add_rounded_rect(slide, x, Inches(2.0), Inches(2.2), Inches(2.8), BG_LIGHT, color)
        tb = _add_textbox(slide, x, Inches(2.2), Inches(2.2), Inches(0.6))
        _set_text(tb.text_frame, icon, size=32, align=PP_ALIGN.CENTER)
        tb2 = _add_textbox(slide, x, Inches(2.9), Inches(2.2), Inches(0.5))
        _set_text(tb2.text_frame, title, size=18, bold=True, color=color, align=PP_ALIGN.CENTER)
        tb3 = _add_textbox(slide, x + Inches(0.15), Inches(3.5), Inches(1.9), Inches(1.0))
        _set_text(tb3.text_frame, desc, size=13, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)
    # Tech stack
    box = _add_rounded_rect(slide, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.5), BG_LIGHT)
    tb = _add_textbox(slide, Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.3))
    _set_text(tb.text_frame, "Tech Stack", size=16, bold=True, color=GRAY_MED)
    techs = [
        ("React + Tailwind", ACCENT_BLUE), ("FastAPI", ACCENT_GREEN),
        ("Groq LLM", ACCENT_PURPLE), ("Firebase", ACCENT_ORANGE),
    ]
    for i, (t, c) in enumerate(techs):
        _add_paragraph(tb.text_frame, f"  •  {t}", size=14, color=c, space_before=Pt(4))


def slide_theories_overview(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 5)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "🧠  Theoretical Framework: 7 Psychology Theories", size=28, bold=True, color=WHITE)
    theories = [
        ("Holland's RIASEC", "Career personality-environment fit", ACCENT_BLUE, "INPUT"),
        ("Bandura's Self-Efficacy", "Belief in one's capabilities", ACCENT_GREEN, "FEEDBACK"),
        ("Vygotsky's ZPD", "Zone of proximal development", ACCENT_PURPLE, "ADAPTIVE"),
        ("Deci & Ryan's SDT", "Autonomy, competence, relatedness", ACCENT_ORANGE, "INPUT"),
        ("Dunning-Kruger", "Metacognitive bias correction", ACCENT_PINK, "ASSESSMENT"),
        ("Locke & Latham", "Goal setting theory", RGBColor(0x22,0xD3,0xEE), "STRUCTURE"),
        ("Csikszentmihalyi", "Flow theory", RGBColor(0xFB,0xBF,0x24), "ADAPTIVE"),
    ]
    for i, (name, desc, color, layer) in enumerate(theories):
        y = Inches(1.2 + i * 0.82)
        box = _add_rounded_rect(slide, Inches(0.8), y, Inches(11.7), Inches(0.72), BG_LIGHT)
        # Colored left bar
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.08), Inches(0.72))
        bar.fill.solid(); bar.fill.fore_color.rgb = color; bar.line.fill.background()
        tb = _add_textbox(slide, Inches(1.2), y + Inches(0.08), Inches(4.5), Inches(0.55))
        _set_text(tb.text_frame, name, size=17, bold=True, color=color)
        tb2 = _add_textbox(slide, Inches(5.5), y + Inches(0.08), Inches(5), Inches(0.55))
        _set_text(tb2.text_frame, desc, size=14, color=GRAY_LIGHT)
        # Layer badge
        badge = _add_rounded_rect(slide, Inches(10.8), y + Inches(0.15), Inches(1.4), Inches(0.4), color)
        tb3 = _add_textbox(slide, Inches(10.8), y + Inches(0.15), Inches(1.4), Inches(0.4))
        _set_text(tb3.text_frame, layer, size=9, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)


def slide_theory_detail(slide, num, emoji, title, theory_text, implementation_lines, color, code_snippet=""):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, num)
    # Header
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, f"{emoji}  Theory: {title}", size=28, bold=True, color=color)
    # Theory box
    box = _add_rounded_rect(slide, Inches(0.8), Inches(1.1), Inches(11.7), Inches(1.3), BG_LIGHT, color)
    tb = _add_textbox(slide, Inches(1.2), Inches(1.2), Inches(10.9), Inches(1.1))
    _set_text(tb.text_frame, "Theory:", size=14, bold=True, color=color)
    _add_paragraph(tb.text_frame, theory_text, size=14, color=GRAY_LIGHT, space_before=Pt(4))
    # Implementation
    box2 = _add_rounded_rect(slide, Inches(0.8), Inches(2.7), Inches(11.7), Inches(2.0), BG_LIGHT)
    tb = _add_textbox(slide, Inches(1.2), Inches(2.8), Inches(10.9), Inches(1.8))
    _set_text(tb.text_frame, "In SkillRoute:", size=14, bold=True, color=WHITE)
    for line in implementation_lines:
        _add_paragraph(tb.text_frame, f"  •  {line}", size=14, color=GRAY_LIGHT, space_before=Pt(6))
    # Code snippet (if any)
    if code_snippet:
        box3 = _add_rounded_rect(slide, Inches(0.8), Inches(5.0), Inches(11.7), Inches(2.0), RGBColor(0x0C, 0x12, 0x22))
        tb = _add_textbox(slide, Inches(1.2), Inches(5.1), Inches(10.9), Inches(1.8))
        _set_text(tb.text_frame, "Implementation:", size=12, bold=True, color=ACCENT_GREEN)
        _add_paragraph(tb.text_frame, code_snippet, size=11, color=GRAY_LIGHT, space_before=Pt(6), font_name="Consolas")


def slide_architecture(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 13)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "🏗️  System Architecture", size=28, bold=True, color=WHITE)
    # Frontend box
    fe = _add_rounded_rect(slide, Inches(0.8), Inches(1.2), Inches(11.7), Inches(1.5), BG_LIGHT, ACCENT_BLUE)
    tb = _add_textbox(slide, Inches(1.0), Inches(1.25), Inches(11.3), Inches(0.4))
    _set_text(tb.text_frame, "FRONTEND  —  React + Tailwind CSS", size=14, bold=True, color=ACCENT_BLUE)
    fe_items = ["Dashboard", "Skill Quiz", "Progress Tracker", "Learning Outcomes", "Job Listings"]
    tb = _add_textbox(slide, Inches(1.2), Inches(1.7), Inches(10.9), Inches(0.8))
    for i, item in enumerate(fe_items):
        sep = "  |  " if i > 0 else ""
        p = tb.text_frame.paragraphs[0] if i == 0 else tb.text_frame.add_paragraph()
        p.text = f"  {item}  " if i == 0 else f"   {item}  "
        p.font.size = Pt(13)
        p.font.color.rgb = GRAY_LIGHT
        p.font.name = "Calibri"
    # Backend box
    be = _add_rounded_rect(slide, Inches(0.8), Inches(3.0), Inches(11.7), Inches(2.2), BG_LIGHT, ACCENT_PURPLE)
    tb = _add_textbox(slide, Inches(1.0), Inches(3.05), Inches(11.3), Inches(0.4))
    _set_text(tb.text_frame, "BACKEND  —  FastAPI + Python + Groq LLM", size=14, bold=True, color=ACCENT_PURPLE)
    be_items = [
        ("Career Decision Agent", "Multi-factor profile analysis", ACCENT_BLUE),
        ("Roadmap Generation Agent", "4-phase personalized learning", ACCENT_GREEN),
        ("Adaptive Roadmap Agent", "Progress-based difficulty adjustment", ACCENT_ORANGE),
        ("Quiz Agent", "Skill assessment & evaluation", ACCENT_PINK),
    ]
    for i, (name, desc, color) in enumerate(be_items):
        y = Inches(3.55 + i * 0.42)
        tb = _add_textbox(slide, Inches(1.3), y, Inches(5), Inches(0.4))
        _set_text(tb.text_frame, f"▸ {name}", size=13, bold=True, color=color)
        tb2 = _add_textbox(slide, Inches(6.5), y, Inches(5.5), Inches(0.4))
        _set_text(tb2.text_frame, desc, size=12, color=GRAY_LIGHT)
    # Database box
    db = _add_rounded_rect(slide, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.4), BG_LIGHT, ACCENT_GREEN)
    tb = _add_textbox(slide, Inches(1.0), Inches(5.55), Inches(11.3), Inches(0.4))
    _set_text(tb.text_frame, "DATABASE  —  Firebase (Auth + Firestore)", size=14, bold=True, color=ACCENT_GREEN)
    tb = _add_textbox(slide, Inches(1.3), Inches(6.0), Inches(10.9), Inches(0.7))
    items = ["User Profiles", "Learning Roadmaps", "Progress Data", "Quiz Results", "Career Decisions"]
    for i, item in enumerate(items):
        p = tb.text_frame.paragraphs[0] if i == 0 else tb.text_frame.add_paragraph()
        p.text = f"  •  {item}"
        p.font.size = Pt(13)
        p.font.color.rgb = GRAY_LIGHT
        p.font.name = "Calibri"


def slide_implementation(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 14)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "⚙️  Implementation Highlights", size=28, bold=True, color=WHITE)
    sections = [
        ("1. Five-Step Psychological Profiling", [
            "Career Clarity Assessment (3 questions → 0-100 score)",
            "Personal Information collection",
            "Skills & Interests enumeration",
            "Goals & Experience capture",
            "Learning Preferences (pace, hours/week)"
        ], ACCENT_BLUE),
        ("2. AI Career Decision Agent", [
            "Processes complete student profile via Groq LLM",
            "Generates: career recommendation, confidence score",
            "Includes reasoning trace and alternative paths",
            "Ultra-fast inference for responsive decisions"
        ], ACCENT_PURPLE),
        ("3. Adaptive Roadmap Mechanism", [
            "Monitors: phase completion, activity recency, streaks",
            "Triggers adaptation when inactivity ≥ 3 days",
            "Adjusts difficulty: beginner → intermediate → advanced",
            "Adds scaffolding resources when progress stalls"
        ], ACCENT_GREEN),
    ]
    for i, (title, items, color) in enumerate(sections):
        y = Inches(1.2 + i * 2.0)
        box = _add_rounded_rect(slide, Inches(0.8), y, Inches(11.7), Inches(1.8), BG_LIGHT)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.08), Inches(1.8))
        bar.fill.solid(); bar.fill.fore_color.rgb = color; bar.line.fill.background()
        tb = _add_textbox(slide, Inches(1.2), y + Inches(0.1), Inches(11), Inches(0.4))
        _set_text(tb.text_frame, title, size=17, bold=True, color=color)
        tb2 = _add_textbox(slide, Inches(1.4), y + Inches(0.5), Inches(10.8), Inches(1.2))
        for j, item in enumerate(items):
            p = tb2.text_frame.paragraphs[0] if j == 0 else tb2.text_frame.add_paragraph()
            p.text = f"  •  {item}"
            p.font.size = Pt(13)
            p.font.color.rgb = GRAY_LIGHT
            p.font.name = "Calibri"


def slide_results(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 15)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "📊  Results & Discussion", size=28, bold=True, color=WHITE)
    findings = [
        ("Psychology theories can be computationally operationalized", "Theory-practice bridge achieved", ACCENT_BLUE),
        ("AI agent produces personalized career decisions", "Scalable alternative to human counseling", ACCENT_GREEN),
        ("Adaptive system adjusts to individual learning pace", "ZPD & Flow Theory effectively implemented", ACCENT_PURPLE),
        ("Skill quiz reveals self-assessment bias", "Dunning-Kruger correction mechanism works", ACCENT_ORANGE),
        ("Multi-factor profiling enhances decision quality", "Holland's model scales through AI", ACCENT_PINK),
    ]
    for i, (finding, implication, color) in enumerate(findings):
        y = Inches(1.1 + i * 1.05)
        box = _add_rounded_rect(slide, Inches(0.8), y, Inches(11.7), Inches(0.9), BG_LIGHT)
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.06), Inches(0.9))
        bar.fill.solid(); bar.fill.fore_color.rgb = color; bar.line.fill.background()
        tb = _add_textbox(slide, Inches(1.2), y + Inches(0.08), Inches(5.5), Inches(0.7))
        _set_text(tb.text_frame, finding, size=14, bold=True, color=WHITE)
        tb2 = _add_textbox(slide, Inches(6.8), y + Inches(0.08), Inches(5.3), Inches(0.7))
        _set_text(tb2.text_frame, implication, size=13, color=GRAY_LIGHT)


def slide_ethics(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 16)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "⚠️  Ethical Considerations & Limitations", size=28, bold=True, color=WHITE)
    # Limitations
    lims = [
        "Quiz validity limited to 5 questions",
        "Self-report bias in interests/goals",
        "No longitudinal outcome tracking",
        "Technology-sector focus only",
        "AI explainability remains partial",
    ]
    box = _add_rounded_rect(slide, Inches(0.8), Inches(1.1), Inches(5.5), Inches(3.5), BG_LIGHT, ACCENT_ORANGE)
    tb = _add_textbox(slide, Inches(1.2), Inches(1.2), Inches(4.8), Inches(0.4))
    _set_text(tb.text_frame, "Current Limitations", size=17, bold=True, color=ACCENT_ORANGE)
    tb2 = _add_textbox(slide, Inches(1.2), Inches(1.7), Inches(4.8), Inches(2.5))
    for j, lim in enumerate(lims):
        p = tb2.text_frame.paragraphs[0] if j == 0 else tb2.text_frame.add_paragraph()
        p.text = f"  {j+1}.  {lim}"
        p.font.size = Pt(14)
        p.font.color.rgb = GRAY_LIGHT
        p.font.name = "Calibri"
    # Ethics table
    ethics = [
        ("Algorithmic Bias", "Discrimination", "Fairness audits"),
        ("Over-Reliance", "Users defer to AI", "Encourage reflection"),
        ("Data Privacy", "Sensitive data", "Encryption, minimal collection"),
        ("Transparency", "Opaque decisions", "Decision trace feature"),
    ]
    box2 = _add_rounded_rect(slide, Inches(6.8), Inches(1.1), Inches(5.7), Inches(3.5), BG_LIGHT, ACCENT_PINK)
    tb = _add_textbox(slide, Inches(7.2), Inches(1.2), Inches(5), Inches(0.4))
    _set_text(tb.text_frame, "Ethical Concerns & Mitigations", size=17, bold=True, color=ACCENT_PINK)
    for i, (issue, risk, mitigation) in enumerate(ethics):
        y = Inches(1.8 + i * 0.7)
        tb = _add_textbox(slide, Inches(7.2), y, Inches(5.0), Inches(0.6))
        _set_text(tb.text_frame, issue, size=13, bold=True, color=WHITE)
        _add_paragraph(tb.text_frame, f"Risk: {risk}  →  {mitigation}", size=11, color=GRAY_LIGHT, space_before=Pt(2))


def slide_future(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 17)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "🚀  Future Work", size=28, bold=True, color=WHITE)
    futures = [
        ("1", "Personality Assessment", "Add MBTI, Big Five, RIASEC instruments", ACCENT_BLUE),
        ("2", "Longitudinal Tracking", "Track career outcomes over months/years", ACCENT_GREEN),
        ("3", "A/B Testing", "Compare against human counselors", ACCENT_PURPLE),
        ("4", "Multi-Domain", "Extend beyond technology careers", ACCENT_ORANGE),
        ("5", "Gamification", "Badges, leaderboards, peer features", ACCENT_PINK),
    ]
    for i, (num, title, desc, color) in enumerate(futures):
        y = Inches(1.2 + i * 1.15)
        box = _add_rounded_rect(slide, Inches(0.8), y, Inches(11.7), Inches(1.0), BG_LIGHT)
        circle = _add_circle(slide, Inches(1.1), y + Inches(0.15), Inches(0.65), color)
        tb = _add_textbox(slide, Inches(1.1), y + Inches(0.18), Inches(0.65), Inches(0.55))
        _set_text(tb.text_frame, num, size=22, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)
        tb = _add_textbox(slide, Inches(2.1), y + Inches(0.12), Inches(3.5), Inches(0.4))
        _set_text(tb.text_frame, title, size=17, bold=True, color=color)
        tb = _add_textbox(slide, Inches(2.1), y + Inches(0.52), Inches(9.5), Inches(0.4))
        _set_text(tb.text_frame, desc, size=13, color=GRAY_LIGHT)


def slide_conclusion(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 18)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "🎓  Conclusion", size=28, bold=True, color=WHITE)
    # Quote box
    box = _add_rounded_rect(slide, Inches(1.5), Inches(1.2), Inches(10.3), Inches(1.5), BG_LIGHT, ACCENT_PURPLE)
    tb = _add_textbox(slide, Inches(2.0), Inches(1.35), Inches(9.3), Inches(1.2))
    _set_text(tb.text_frame, "\"SkillRoute demonstrates that psychological theories, traditionally\napplied in face-to-face counseling, can be effectively translated\ninto computational mechanisms.\"", size=18, color=ACCENT_PURPLE, align=PP_ALIGN.CENTER)
    # Summary
    summaries = [
        ("7 theories → 7 mechanisms", "Each psychology theory mapped to a computational implementation"),
        ("AI as psychological agent", "Not just data processor — performs assessment, diagnosis, treatment planning"),
        ("Scalable career guidance", "Extends human counselor reach through AI-powered personalization"),
    ]
    for i, (title, desc) in enumerate(summaries):
        y = Inches(3.1 + i * 1.1)
        box = _add_rounded_rect(slide, Inches(1.5), y, Inches(10.3), Inches(0.95), BG_LIGHT)
        tb = _add_textbox(slide, Inches(2.0), y + Inches(0.08), Inches(9.3), Inches(0.35))
        _set_text(tb.text_frame, f"  ✓  {title}", size=16, bold=True, color=ACCENT_GREEN)
        tb = _add_textbox(slide, Inches(2.4), y + Inches(0.48), Inches(8.9), Inches(0.35))
        _set_text(tb.text_frame, desc, size=13, color=GRAY_LIGHT)
    # Final quote
    tb = _add_textbox(slide, Inches(1.5), Inches(6.3), Inches(10.3), Inches(0.7))
    _set_text(tb.text_frame, "\"The ultimate promise is not to replace human counselors but to extend their reach.\"", size=16, bold=True, color=GRAY_MED, align=PP_ALIGN.CENTER)


def slide_references(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 19)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "📚  Key References", size=28, bold=True, color=WHITE)
    refs = [
        ("Holland, J. L.", "Career Choice (RIASEC)", "1997", ACCENT_BLUE),
        ("Bandura, A.", "Self-Efficacy Theory", "1977, 1997", ACCENT_GREEN),
        ("Vygotsky, L. S.", "Zone of Proximal Development", "1978", ACCENT_PURPLE),
        ("Deci, E. L. & Ryan, R. M.", "Self-Determination Theory", "1985, 2000", ACCENT_ORANGE),
        ("Kruger, J. & Dunning, D.", "Dunning-Kruger Effect", "1999", ACCENT_PINK),
        ("Locke, E. A. & Latham, G. P.", "Goal Setting Theory", "1990, 2002", RGBColor(0x22,0xD3,0xEE)),
        ("Csikszentmihalyi, M.", "Flow Theory", "1990", RGBColor(0xFB,0xBF,0x24)),
        ("Gati, I. et al.", "Career Decision Difficulties", "1996", GRAY_MED),
        ("Lent, R. W. et al.", "Social Cognitive Career Theory", "1994", GRAY_MED),
        ("Super, D. E.", "Life-Span Career Development", "1990", GRAY_MED),
    ]
    for i, (author, theory, year, color) in enumerate(refs):
        y = Inches(1.1 + i * 0.6)
        # Author
        tb = _add_textbox(slide, Inches(0.8), y, Inches(4.5), Inches(0.5))
        _set_text(tb.text_frame, author, size=13, bold=True, color=color)
        # Theory
        tb = _add_textbox(slide, Inches(5.5), y, Inches(5.5), Inches(0.5))
        _set_text(tb.text_frame, theory, size=13, color=GRAY_LIGHT)
        # Year
        tb = _add_textbox(slide, Inches(11.0), y, Inches(1.5), Inches(0.5))
        _set_text(tb.text_frame, year, size=13, color=GRAY_MED, align=PP_ALIGN.RIGHT)


def slide_qa(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 20)
    # Accent line
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.44), Inches(13.333), Inches(0.06))
    shape.fill.solid(); shape.fill.fore_color.rgb = ACCENT_BLUE; shape.line.fill.background()
    # Question mark
    tb = _add_textbox(slide, Inches(4), Inches(1.5), Inches(5.3), Inches(1.5))
    _set_text(tb.text_frame, "❓", size=80, align=PP_ALIGN.CENTER)
    # Title
    tb = _add_textbox(slide, Inches(2), Inches(3.3), Inches(9.3), Inches(1))
    _set_text(tb.text_frame, "Questions & Discussion", size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    # Subtitle
    tb = _add_textbox(slide, Inches(2), Inches(4.5), Inches(9.3), Inches(0.6))
    _set_text(tb.text_frame, "Thank you!", size=24, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)
    # Contact
    tb = _add_textbox(slide, Inches(3), Inches(5.5), Inches(7.3), Inches(1))
    _set_text(tb.text_frame, "[Your Name]  •  [Your Email]\nSkillRoute AI  •  GitHub: [Your Repository]", size=14, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)


# ── Build Presentation ─────────────────────────────────────────

# Slide 1: Title
slide = prs.slides.add_slide(prs.slide_layouts[6])  # blank
slide_title(slide)

# Slide 2: Problem
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_problem(slide)

# Slide 3: Research Question
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_research_question(slide)

# Slide 4: Solution
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_solution(slide)

# Slide 5: Theories Overview
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_theories_overview(slide)

# Slides 6-12: Individual Theories
theory_data = [
    (6, "🎭", "Holland's RIASEC Model",
     "Individuals succeed when their personality type matches their work environment (Holland, 1997).",
     ["5-step onboarding collects: Interests, Skills, Goals, Education, Pace",
      "AI agent analyzes multi-factor profile → career recommendation",
      "Alternative paths provided for informed decision-making"],
     ACCENT_BLUE,
     'class StudentProfile(BaseModel):\n    interests: str    # RIASEC categories\n    skills: str       # Skill inventory\n    goals: str        # Vocational aspirations'),

    (7, "💪", "Bandura's Self-Efficacy Theory",
     "Self-efficacy is built through mastery experiences and is a primary determinant of motivation (Bandura, 1977, 1997).",
     ["Mastery Experience: AI skill quiz tests actual ability",
      "Calibration: Gap between self-report and quiz score",
      "Growth Evidence: Before/after outcomes dashboard",
      "Feedback: Strengths and areas to improve identified"],
     ACCENT_GREEN,
     'async def evaluate_quiz(questions, user_answers):\n    if percentage >= 80: skill_level = "advanced"\n    elif percentage >= 50: skill_level = "intermediate"\n    else: skill_level = "beginner"'),

    (8, "📈", "Vygotsky's Zone of Proximal Development",
     "Learning is most effective when targeting the zone between independent capability and guided achievement (Vygotsky, 1978).",
     ["Initial skill assessment establishes lower ZPD boundary",
      "Adaptive roadmap raises/lowers upper boundary based on progress",
      "Scaffolding resources bridge gap between current and target state",
      "Dynamic difficulty adjustment maintains optimal challenge"],
     ACCENT_PURPLE,
     'ADAPT_SYSTEM_PROMPT = """Adapt roadmap based on progress:\n- If progressing well: suggest advanced topics\n- If stuck: add remedial resources"""'),

    (9, "🎯", "Self-Determination Theory (SDT)",
     "Intrinsic motivation thrives when three basic psychological needs are met: Autonomy, Competence, Relatedness (Deci & Ryan, 1985, 2000).",
     ["Autonomy: Users control profile, reset path, trigger adaptation",
      "Competence: Skill quiz provides objective mastery feedback",
      "Relatedness: Industry demand data connects to real job market",
      "All three needs addressed → sustained intrinsic motivation"],
     ACCENT_ORANGE,
     'async def analyze_industry_demand(career: str) -> dict:\n    # Connects user to real-world job market\n    # Provides salary, skill demands, job openings'),

    (10, "🪞", "Dunning-Kruger Effect",
     "Unskilled individuals overestimate their competence; skilled individuals underestimate theirs (Kruger & Dunning, 1999).",
     ["User self-reports skills during onboarding (subjective assessment)",
      "AI quiz tests actual understanding with practical questions",
      "Gap between self-report and quiz reveals calibration bias",
      "Roadmap adjusts based on objective skill level, not self-perception"],
     ACCENT_PINK,
     'QUIZ_GENERATE_PROMPT = """\nGiven skills the student claims to know,\ngenerate questions to test ACTUAL skill level.\nQuestions should test real understanding."""'),

    (11, "🎯", "Locke & Latham's Goal Setting Theory",
     "Specific, challenging goals with feedback produce higher performance than vague goals (Locke & Latham, 1990, 2002).",
     ["Specific Goals: Milestones with clear, defined outcomes",
      "Challenging Yet Attainable: AI calibrates difficulty to skill level",
      "Feedback: Progress tracker with %, streaks, completion status",
      "Time-Bound: Phase durations create temporal landmarks",
      "Strategy Support: Curated resources for each milestone"],
     RGBColor(0x22,0xD3,0xEE),
     '{\n  "phase": "Phase 1: Foundations",\n  "duration": "2-3 weeks",\n  "milestones": [{"name": "Python Basics",\n                  "estimated_hours": 15}]}'),

    (12, "🌊", "Csikszentmihalyi's Flow Theory",
     "Flow occurs when challenge matches skill level, producing optimal experience and engagement (Csikszentmihalyi, 1990).",
     ["Challenge-Skill Balance: Adaptive system adjusts difficulty dynamically",
      "Clear Goals: Each milestone has specific, defined outcomes",
      "Immediate Feedback: Progress tracker provides real-time updates",
      "Sense of Control: Users choose when to adapt and what to complete",
      "System aims to keep users in flow zone between boredom and anxiety"],
     RGBColor(0xFB,0xBF,0x24),
     '# Flow balance in adaptive system\nif progress_is_good:\n    increase_challenge()  # Advance to harder topics\nif progress_is_stalled:\n    reduce_challenge()   # Add scaffolding'),
]

for data in theory_data:
    slide = prs.slides.add_slide(prs.slide_layouts[6])
    slide_theory_detail(slide, *data)

# Slide 13: Architecture
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_architecture(slide)

# Slide 14: Implementation
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_implementation(slide)

# Slide 15: Results
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_results(slide)

# Slide 16: Ethics
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_ethics(slide)

# Slide 17: Future Work
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_future(slide)

# Slide 18: Conclusion
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_conclusion(slide)

# Slide 19: References
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_references(slide)

# Slide 20: Q&A
slide = prs.slides.add_slide(prs.slide_layouts[6])
slide_qa(slide)


# ── Save ───────────────────────────────────────────────────────

output_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "SkillRoute_Research_Presentation.pptx")
prs.save(output_path)
print(f"Presentation saved: {output_path}")
print(f"Total slides: {len(prs.slides)}")
