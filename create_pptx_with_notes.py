"""
Generate a professional PowerPoint presentation for SkillRoute Research Paper
WITH SPEAKER NOTES for each slide.
Run: python create_pptx_with_notes.py
"""

from pptx import Presentation
from pptx.util import Inches, Pt, Emu
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN, MSO_ANCHOR
from pptx.enum.shapes import MSO_SHAPE
import os

# ── Color Palette ──────────────────────────────────────────────
BG_DARK      = RGBColor(0x0F, 0x17, 0x2A)
BG_LIGHT     = RGBColor(0x1E, 0x29, 0x3B)
ACCENT_BLUE  = RGBColor(0x38, 0xBD, 0xF8)
ACCENT_PURPLE= RGBColor(0xA7, 0x8B, 0xFA)
ACCENT_GREEN = RGBColor(0x4A, 0xDE, 0x80)
ACCENT_ORANGE= RGBColor(0xFB, 0x92, 0x3C)
ACCENT_PINK  = RGBColor(0xF4, 0x72, 0xB6)
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

def _add_notes(slide, notes_text):
    """Add speaker notes to a slide."""
    notes_slide = slide.notes_slide
    notes_tf = notes_slide.notes_text_frame
    notes_tf.text = notes_text


# ── Slide Builders ─────────────────────────────────────────────

def slide_title(slide):
    _set_bg(slide, BG_DARK)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(0), Inches(13.333), Inches(0.06))
    shape.fill.solid(); shape.fill.fore_color.rgb = ACCENT_BLUE; shape.line.fill.background()
    tb = _add_textbox(slide, Inches(1.5), Inches(1.8), Inches(10.3), Inches(1.5))
    _set_text(tb.text_frame, "AI-Powered Career Decision-Making", size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    _add_paragraph(tb.text_frame, "Integrating Psychological Theories into\nPersonalized Learning Platforms", size=28, color=ACCENT_BLUE, align=PP_ALIGN.CENTER, space_before=Pt(12))
    tb2 = _add_textbox(slide, Inches(3), Inches(4.5), Inches(7.3), Inches(1.2))
    _set_text(tb2.text_frame, "[Your Name]", size=20, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)
    _add_paragraph(tb2.text_frame, "Department of Psychology  •  [Your College Name]  •  August 2026", size=14, color=GRAY_MED, align=PP_ALIGN.CENTER, space_before=Pt(8))

    notes = """SPEAKER NOTES — Slide 1 (Title)
================================

Opening Statement:
"Good morning/afternoon everyone. Today I'll be presenting our research on integrating psychological theories into AI-powered career guidance systems."

Key Points to Mention:
• Introduce yourself and your department
• Mention this is an interdisciplinary psychology-computer science project
• Briefly preview the 7 theories you'll discuss
• Set expectations: 20-minute presentation + Q&A

Transition:
"Let me start by explaining the problem we're trying to solve."
"""
    _add_notes(slide, notes)


def slide_problem(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 2)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.4), Inches(8), Inches(0.7))
    _set_text(tb.text_frame, "🎯  The Problem: Career Indecision", size=30, bold=True, color=WHITE)
    box = _add_rounded_rect(slide, Inches(0.8), Inches(1.4), Inches(4), Inches(2.5), BG_LIGHT, ACCENT_BLUE)
    tb = _add_textbox(slide, Inches(1.2), Inches(1.6), Inches(3.2), Inches(2))
    _set_text(tb.text_frame, "80%", size=64, bold=True, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)
    _add_paragraph(tb.text_frame, "of students experience significant\ncareer confusion during education", size=16, color=GRAY_LIGHT, align=PP_ALIGN.CENTER, space_before=Pt(8))
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

    notes = """SPEAKER NOTES — Slide 2 (The Problem)
=======================================

Opening Statement:
"Career indecision is a widespread problem affecting students worldwide."

Key Statistics to Emphasize:
• 80% of students experience significant career confusion (Gati et al., 1996)
• Students waste months learning wrong skills
• Traditional counseling is limited by scalability and availability

Walk Through Each Challenge:
1. "Too many career options → Overwhelm"
   - Students face hundreds of career paths with no clear guidance
   - Decision paralysis is real and documented in psychology literature

2. "Lack of personalized guidance → Generic advice"
   - One-size-fits-all career advice doesn't account for individual differences
   - Each student has unique interests, skills, and learning pace

3. "Rapidly changing industry demands → Outdated information"
   - Career guidance from 5 years ago may be irrelevant today
   - AI can provide real-time market data

4. "No clear learning order → Directionless exploration"
   - Students don't know what to learn first
   - Results in inefficient learning and wasted time

Transition:
"This problem inspired us to build SkillRoute — an AI-powered solution."
"""
    _add_notes(slide, notes)


def slide_research_question(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 3)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.7))
    _set_text(tb.text_frame, "🔬  Central Research Question", size=30, bold=True, color=WHITE)
    box = _add_rounded_rect(slide, Inches(1.2), Inches(1.5), Inches(10.9), Inches(1.8), BG_LIGHT, ACCENT_PURPLE)
    tb = _add_textbox(slide, Inches(1.6), Inches(1.7), Inches(10.1), Inches(1.4))
    _set_text(tb.text_frame, "\"How can psychological theories of career decision-making,\nself-efficacy, and adaptive learning be operationalized\nin an AI-powered learning platform?\"", size=20, bold=False, color=ACCENT_PURPLE, align=PP_ALIGN.CENTER)
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

    notes = """SPEAKER NOTES — Slide 3 (Research Question)
=============================================

State the Question Clearly:
"Our research asks: How can psychological theories of career decision-making, self-efficacy, and adaptive learning be operationalized in an AI-powered learning platform?"

Explain the Three Contributions:

1. Theoretical Operationalization:
   - "We demonstrate how abstract psychological constructs — like self-efficacy, zone of proximal development, and flow — can be translated into concrete computational mechanisms."
   - "This is the core contribution: bridging theory and practice."

2. System Architecture:
   - "We designed a full-stack system that embeds psychological principles at every layer — from data collection to AI decision-making to feedback delivery."

3. Practical Impact:
   - "We show that psychologically grounded AI systems can produce more meaningful career guidance than purely data-driven approaches."

Transition:
"Let me now explain the solution we built."
"""
    _add_notes(slide, notes)


def slide_solution(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 4)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.4), Inches(10), Inches(0.7))
    _set_text(tb.text_frame, "💡  The Solution: SkillRoute", size=30, bold=True, color=WHITE)
    tb = _add_textbox(slide, Inches(0.8), Inches(1.2), Inches(10), Inches(0.5))
    _set_text(tb.text_frame, "An AI-powered career decision-making & personalized learning platform", size=16, color=GRAY_LIGHT)
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
    box = _add_rounded_rect(slide, Inches(0.8), Inches(5.2), Inches(11.7), Inches(1.5), BG_LIGHT)
    tb = _add_textbox(slide, Inches(1.0), Inches(5.3), Inches(11.3), Inches(1.3))
    _set_text(tb.text_frame, "Tech Stack", size=16, bold=True, color=GRAY_MED)
    techs = [
        ("React + Tailwind", ACCENT_BLUE), ("FastAPI", ACCENT_GREEN),
        ("Groq LLM", ACCENT_PURPLE), ("Firebase", ACCENT_ORANGE),
    ]
    for i, (t, c) in enumerate(techs):
        _add_paragraph(tb.text_frame, f"  •  {t}", size=14, color=c, space_before=Pt(4))

    notes = """SPEAKER NOTES — Slide 4 (The Solution)
========================================

Introduce SkillRoute:
"SkillRoute is an AI-powered career decision-making and personalized learning platform."

Walk Through Each Feature:

1. Decides (not just recommends):
   - "Unlike traditional platforms that suggest courses, SkillRoute DECIDES the best career path for each student."
   - "This is a key differentiator — it's an AI decision-making agent, not just a chatbot."

2. Profiles:
   - "We collect psychological data through a 5-step onboarding process."
   - "This includes interests, skills, goals, education, and learning preferences."

3. Plans:
   - "The system generates personalized, time-bound learning roadmaps."
   - "Each roadmap has 4 phases with specific milestones and resources."

4. Tracks:
   - "We monitor progress and adapt the roadmap based on performance."
   - "This implements Vygotsky's Zone of Proximal Development."

5. Assesses:
   - "The skill quiz tests actual abilities vs. self-reported skills."
   - "This addresses the Dunning-Kruger Effect."

Tech Stack Mention:
"Our tech stack includes React for the frontend, FastAPI for the backend, Groq LLM for AI decisions, and Firebase for authentication and data storage."

Transition:
"Now let me explain the psychological theories underlying this system."
"""
    _add_notes(slide, notes)


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
        bar = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0.8), y, Inches(0.08), Inches(0.72))
        bar.fill.solid(); bar.fill.fore_color.rgb = color; bar.line.fill.background()
        tb = _add_textbox(slide, Inches(1.2), y + Inches(0.08), Inches(4.5), Inches(0.55))
        _set_text(tb.text_frame, name, size=17, bold=True, color=color)
        tb2 = _add_textbox(slide, Inches(5.5), y + Inches(0.08), Inches(5), Inches(0.55))
        _set_text(tb2.text_frame, desc, size=14, color=GRAY_LIGHT)
        badge = _add_rounded_rect(slide, Inches(10.8), y + Inches(0.15), Inches(1.4), Inches(0.4), color)
        tb3 = _add_textbox(slide, Inches(10.8), y + Inches(0.15), Inches(1.4), Inches(0.4))
        _set_text(tb3.text_frame, layer, size=9, bold=True, color=BG_DARK, align=PP_ALIGN.CENTER)

    notes = """SPEAKER NOTES — Slide 5 (Theories Overview)
============================================

Overview Statement:
"Our system integrates 7 major psychological theories from career development, educational psychology, and motivation science."

Walk Through Each Theory Briefly:

1. Holland's RIASEC (INPUT layer):
   - "Holland's theory proposes that career satisfaction depends on personality-environment fit."
   - "We implement this through our 5-step profiling process."

2. Bandura's Self-Efficacy (FEEDBACK layer):
   - "Bandura showed that mastery experiences build self-efficacy."
   - "Our skill quiz and outcomes dashboard provide this feedback."

3. Vygotsky's ZPD (ADAPTIVE layer):
   - "Vygotsky's Zone of Proximal Development says learning is most effective when targeting the zone between what you can do alone and with guidance."
   - "Our adaptive roadmap implements this."

4. Deci & Ryan's SDT (INPUT layer):
   - "Self-Determination Theory identifies three basic needs: autonomy, competence, relatedness."
   - "Our system addresses all three."

5. Dunning-Kruger (ASSESSMENT layer):
   - "The Dunning-Kruger Effect shows that unskilled people overestimate their ability."
   - "Our quiz bridges the gap between self-report and actual skill."

6. Locke & Latham's Goal Setting (STRUCTURE layer):
   - "Goal Setting Theory shows that specific, challenging goals with feedback improve performance."
   - "Our milestone-based roadmap implements this."

7. Csikszentmihalyi's Flow (ADAPTIVE layer):
   - "Flow occurs when challenge matches skill level."
   - "Our adaptive system aims to keep users in this flow zone."

Transition:
"Let me now explain each theory in detail, starting with Holland's RIASEC Model."
"""
    _add_notes(slide, notes)


def slide_theory_detail(slide, num, emoji, title, theory_text, implementation_lines, color, code_snippet=""):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, num)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, f"{emoji}  Theory: {title}", size=28, bold=True, color=color)
    box = _add_rounded_rect(slide, Inches(0.8), Inches(1.1), Inches(11.7), Inches(1.3), BG_LIGHT, color)
    tb = _add_textbox(slide, Inches(1.2), Inches(1.2), Inches(10.9), Inches(1.1))
    _set_text(tb.text_frame, "Theory:", size=14, bold=True, color=color)
    _add_paragraph(tb.text_frame, theory_text, size=14, color=GRAY_LIGHT, space_before=Pt(4))
    box2 = _add_rounded_rect(slide, Inches(0.8), Inches(2.7), Inches(11.7), Inches(2.0), BG_LIGHT)
    tb = _add_textbox(slide, Inches(1.2), Inches(2.8), Inches(10.9), Inches(1.8))
    _set_text(tb.text_frame, "In SkillRoute:", size=14, bold=True, color=WHITE)
    for line in implementation_lines:
        _add_paragraph(tb.text_frame, f"  •  {line}", size=14, color=GRAY_LIGHT, space_before=Pt(6))
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
    fe = _add_rounded_rect(slide, Inches(0.8), Inches(1.2), Inches(11.7), Inches(1.5), BG_LIGHT, ACCENT_BLUE)
    tb = _add_textbox(slide, Inches(1.0), Inches(1.25), Inches(11.3), Inches(0.4))
    _set_text(tb.text_frame, "FRONTEND  —  React + Tailwind CSS", size=14, bold=True, color=ACCENT_BLUE)
    fe_items = ["Dashboard", "Skill Quiz", "Progress Tracker", "Learning Outcomes", "Job Listings"]
    tb = _add_textbox(slide, Inches(1.2), Inches(1.7), Inches(10.9), Inches(0.8))
    for i, item in enumerate(fe_items):
        p = tb.text_frame.paragraphs[0] if i == 0 else tb.text_frame.add_paragraph()
        p.text = f"  {item}  " if i == 0 else f"   {item}  "
        p.font.size = Pt(13); p.font.color.rgb = GRAY_LIGHT; p.font.name = "Calibri"
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
    db = _add_rounded_rect(slide, Inches(0.8), Inches(5.5), Inches(11.7), Inches(1.4), BG_LIGHT, ACCENT_GREEN)
    tb = _add_textbox(slide, Inches(1.0), Inches(5.55), Inches(11.3), Inches(0.4))
    _set_text(tb.text_frame, "DATABASE  —  Firebase (Auth + Firestore)", size=14, bold=True, color=ACCENT_GREEN)
    tb = _add_textbox(slide, Inches(1.3), Inches(6.0), Inches(10.9), Inches(0.7))
    items = ["User Profiles", "Learning Roadmaps", "Progress Data", "Quiz Results", "Career Decisions"]
    for i, item in enumerate(items):
        p = tb.text_frame.paragraphs[0] if i == 0 else tb.text_frame.add_paragraph()
        p.text = f"  •  {item}"; p.font.size = Pt(13); p.font.color.rgb = GRAY_LIGHT; p.font.name = "Calibri"

    notes = """SPEAKER NOTES — Slide 13 (System Architecture)
==============================================

Overview:
"Our system has a three-layer architecture: Frontend, Backend, and Database."

Frontend Layer:
- "React with Tailwind CSS for a modern, responsive interface"
- "Key components: Dashboard, Skill Quiz, Progress Tracker, Learning Outcomes, Job Listings"
- "Dark mode design for professional appearance"

Backend Layer:
- "FastAPI with Python for high-performance async API"
- "Four AI agents powered by Groq LLM:"
  1. "Career Decision Agent — analyzes multi-factor profile"
  2. "Roadmap Generation Agent — creates 4-phase learning path"
  3. "Adaptive Roadmap Agent — modifies path based on progress"
  4. "Quiz Agent — generates and evaluates skill assessments"

Database Layer:
- "Firebase for authentication and data storage"
- "Firestore for flexible NoSQL data model"
- "Stores: User profiles, roadmaps, progress data, quiz results, career decisions"

Transition:
"Let me explain the key implementation details."
"""
    _add_notes(slide, notes)


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
            p.text = f"  •  {item}"; p.font.size = Pt(13); p.font.color.rgb = GRAY_LIGHT; p.font.name = "Calibri"

    notes = """SPEAKER NOTES — Slide 14 (Implementation Highlights)
====================================================

Section 1: Five-Step Psychological Profiling
- "Our onboarding collects psychological data in 5 steps"
- "Step 1: Career Clarity Assessment — 3 questions that produce a 0-100 score"
  - "This implements Gati's taxonomy of career decision difficulties"
- "Step 2: Personal Information — name, education level"
- "Step 3: Skills & Interests — open-ended format for ecological validity"
- "Step 4: Goals & Experience — specific career objectives"
- "Step 5: Learning Preferences — time availability and learning pace"
- "This multi-factor profile enables the AI to make nuanced career decisions"

Section 2: AI Career Decision Agent
- "The career decision agent uses Groq LLM for ultra-fast inference"
- "It processes the complete student profile and generates:"
  - "Primary career recommendation with confidence score"
  - "Skill match and market readiness percentages"
  - "Key strengths and identified skill gaps"
  - "Decision trace showing the reasoning process"
  - "Alternative career paths for comparison"
- "This is not just a chatbot — it's an AI decision-making agent"

Section 3: Adaptive Roadmap Mechanism
- "The system monitors three key indicators:"
  1. "Phase completion rate"
  2. "Activity recency (days since last activity)"
  3. "Streak consistency"
- "When inactivity exceeds 3 days and phases remain incomplete, the system suggests adaptation"
- "The adaptation modifies future phases based on performance patterns"
- "This implements Vygotsky's ZPD — adjusting difficulty to match learner capability"

Transition:
"Now let me discuss the results and implications."
"""
    _add_notes(slide, notes)


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

    notes = """SPEAKER NOTES — Slide 15 (Results & Discussion)
===============================================

Key Findings:

1. "Psychology theories can be computationally operationalized"
   - "This is our primary contribution — we've shown the theory-practice bridge is achievable"
   - "Each of the 7 theories maps to a specific computational mechanism"

2. "AI agent produces personalized career decisions"
   - "The Groq LLM processes multi-factor profiles to generate individualized recommendations"
   - "This is scalable — unlike human counseling, it can serve unlimited users"

3. "Adaptive system adjusts to individual learning pace"
   - "Vygotsky's ZPD and Csikszentmihalyi's Flow are effectively implemented"
   - "The system dynamically adjusts difficulty based on progress"

4. "Skill quiz reveals self-assessment bias"
   - "The Dunning-Kruger correction mechanism works"
   - "Users receive objective feedback on their actual skill level"

5. "Multi-factor profiling enhances decision quality"
   - "Holland's model scales through AI"
   - "Multiple factors create a more nuanced career recommendation"

Advantages Over Traditional Counseling:
- Scalable (unlimited users)
- Consistent (algorithmic decisions)
- Accessible (24/7 availability)
- Data-driven (real-time market integration)

Transition:
"Let me address the limitations and ethical considerations."
"""
    _add_notes(slide, notes)


def slide_ethics(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 16)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "⚠️  Ethical Considerations & Limitations", size=28, bold=True, color=WHITE)
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
        p.text = f"  {j+1}.  {lim}"; p.font.size = Pt(14); p.font.color.rgb = GRAY_LIGHT; p.font.name = "Calibri"
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

    notes = """SPEAKER NOTES — Slide 16 (Ethics & Limitations)
================================================

Limitations (Be Honest):

1. "Quiz validity limited to 5 questions"
   - "5 questions may not provide sufficient psychometric validity"
   - "Future versions should incorporate validated assessment instruments"

2. "Self-report bias in interests/goals"
   - "Despite the Dunning-Kruger correction, we still rely on self-reported data"
   - "Social desirability bias may affect responses"

3. "No longitudinal outcome tracking"
   - "We don't track career outcomes months or years after guidance"
   - "This limits our ability to evaluate long-term effectiveness"

4. "Technology-sector focus only"
   - "Currently designed for technology careers"
   - "Generalization to other sectors needs testing"

5. "AI explainability remains partial"
   - "While we include a decision trace, the reasoning process is not fully transparent"
   - "This is a known challenge with large language models"

Ethical Concerns & Mitigations:

1. Algorithmic Bias → Fairness audits
   - "We acknowledge the risk of bias in AI recommendations"
   - "Mitigation: Regular fairness audits and diverse training data"

2. Over-Reliance → Encourage reflection
   - "Students may defer too heavily to AI recommendations"
   - "Mitigation: Present alternatives and encourage critical thinking"

3. Data Privacy → Encryption, minimal collection
   - "We collect sensitive psychological data"
   - "Mitigation: Firebase encryption and minimal data collection"

4. Transparency → Decision trace feature
   - "AI decisions may be opaque"
   - "Mitigation: Decision trace shows reasoning steps"

Transition:
"Let me discuss future research directions."
"""
    _add_notes(slide, notes)


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

    notes = """SPEAKER NOTES — Slide 17 (Future Work)
========================================

Present Each Direction:

1. Personality Assessment Integration:
   - "Adding validated instruments like MBTI, Big Five, or RIASEC would enhance psychological depth"
   - "This would provide more structured personality data for the AI agent"

2. Longitudinal Outcome Tracking:
   - "Tracking career outcomes months or years after guidance would enable evaluation of AI decision quality"
   - "This is essential for establishing the system's effectiveness"

3. A/B Testing Against Human Counselors:
   - "Controlled experiments comparing SkillRoute's outcomes with traditional career counseling"
   - "This would provide evidence of comparative effectiveness"

4. Multi-Domain Generalization:
   - "Extending beyond technology careers to healthcare, education, business"
   - "This would broaden the system's impact"

5. Gamification & Social Features:
   - "Adding badges, leaderboards, and peer comparison"
   - "This could enhance motivation through relatedness and competition"

Transition:
"Let me conclude with the key takeaways."
"""
    _add_notes(slide, notes)


def slide_conclusion(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 18)
    tb = _add_textbox(slide, Inches(0.8), Inches(0.3), Inches(10), Inches(0.6))
    _set_text(tb.text_frame, "🎓  Conclusion", size=28, bold=True, color=WHITE)
    box = _add_rounded_rect(slide, Inches(1.5), Inches(1.2), Inches(10.3), Inches(1.5), BG_LIGHT, ACCENT_PURPLE)
    tb = _add_textbox(slide, Inches(2.0), Inches(1.35), Inches(9.3), Inches(1.2))
    _set_text(tb.text_frame, "\"SkillRoute demonstrates that psychological theories, traditionally\napplied in face-to-face counseling, can be effectively translated\ninto computational mechanisms.\"", size=18, color=ACCENT_PURPLE, align=PP_ALIGN.CENTER)
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
    tb = _add_textbox(slide, Inches(1.5), Inches(6.3), Inches(10.3), Inches(0.7))
    _set_text(tb.text_frame, "\"The ultimate promise is not to replace human counselors but to extend their reach.\"", size=16, bold=True, color=GRAY_MED, align=PP_ALIGN.CENTER)

    notes = """SPEAKER NOTES — Slide 18 (Conclusion)
=======================================

Key Takeaways:

1. "7 theories → 7 mechanisms"
   - "Each of the 7 psychology theories we discussed maps to a specific computational implementation"
   - "This is the core contribution of our research"

2. "AI as psychological agent"
   - "SkillRoute's AI is not just a data processor"
   - "It performs functions traditionally attributed to human counselors: assessment, diagnosis, treatment planning, monitoring"

3. "Scalable career guidance"
   - "The system extends human counselor reach through AI-powered personalization"
   - "It can serve unlimited users simultaneously without quality degradation"

Closing Quote:
"The ultimate promise of psychologically grounded AI career guidance is not to replace human counselors but to extend their reach — providing evidence-based, personalized, and scalable career development support to the millions of students worldwide who currently lack access to quality career guidance."

Transition:
"Thank you. I'm happy to take any questions."
"""
    _add_notes(slide, notes)


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
        tb = _add_textbox(slide, Inches(0.8), y, Inches(4.5), Inches(0.5))
        _set_text(tb.text_frame, author, size=13, bold=True, color=color)
        tb = _add_textbox(slide, Inches(5.5), y, Inches(5.5), Inches(0.5))
        _set_text(tb.text_frame, theory, size=13, color=GRAY_LIGHT)
        tb = _add_textbox(slide, Inches(11.0), y, Inches(1.5), Inches(0.5))
        _set_text(tb.text_frame, year, size=13, color=GRAY_MED, align=PP_ALIGN.RIGHT)

    notes = """SPEAKER NOTES — Slide 19 (References)
======================================

Briefly Mention Key Citations:
- "Holland (1997) — Career Choice Theory"
- "Bandura (1977, 1997) — Self-Efficacy Theory"
- "Vygotsky (1978) — Zone of Proximal Development"
- "Deci & Ryan (1985, 2000) — Self-Determination Theory"
- "Kruger & Dunning (1999) — Dunning-Kruger Effect"
- "Locke & Latham (1990, 2002) — Goal Setting Theory"
- "Csikszentmihalyi (1990) — Flow Theory"

Don't Read All — Just Highlight the Main Ones.
"""
    _add_notes(slide, notes)


def slide_qa(slide):
    _set_bg(slide, BG_DARK)
    _add_slide_number(slide, 20)
    shape = slide.shapes.add_shape(MSO_SHAPE.RECTANGLE, Inches(0), Inches(7.44), Inches(13.333), Inches(0.06))
    shape.fill.solid(); shape.fill.fore_color.rgb = ACCENT_BLUE; shape.line.fill.background()
    tb = _add_textbox(slide, Inches(4), Inches(1.5), Inches(5.3), Inches(1.5))
    _set_text(tb.text_frame, "❓", size=80, align=PP_ALIGN.CENTER)
    tb = _add_textbox(slide, Inches(2), Inches(3.3), Inches(9.3), Inches(1))
    _set_text(tb.text_frame, "Questions & Discussion", size=40, bold=True, color=WHITE, align=PP_ALIGN.CENTER)
    tb = _add_textbox(slide, Inches(2), Inches(4.5), Inches(9.3), Inches(0.6))
    _set_text(tb.text_frame, "Thank you!", size=24, color=ACCENT_BLUE, align=PP_ALIGN.CENTER)
    tb = _add_textbox(slide, Inches(3), Inches(5.5), Inches(7.3), Inches(1))
    _set_text(tb.text_frame, "[Your Name]  •  [Your Email]\nSkillRoute AI  •  GitHub: [Your Repository]", size=14, color=GRAY_LIGHT, align=PP_ALIGN.CENTER)

    notes = """SPEAKER NOTES — Slide 20 (Q&A)
================================

Closing Statement:
"Thank you for your attention. I'm happy to take any questions."

Prepared for Common Questions:

Q: "How is this different from Coursera/Udemy?"
A: "They offer courses. We decide WHICH course and WHEN to take it, tailored to YOUR profile."

Q: "What if the AI suggests a wrong career?"
A: "The user can adjust preferences anytime, and the AI re-evaluates. It's adaptive, not one-time."

Q: "Can this scale?"
A: "Firebase + Vercel + Groq handle thousands of concurrent users on free tier."

Q: "How do you make money?"
A: "Freemium model — premium features like resume builder, mock interviews, mentor matching."

Q: "What about ethical concerns with AI making career decisions?"
A: "We present alternatives and encourage reflection. The AI suggests — the user decides."

Q: "How do you validate the AI's career recommendations?"
A: "This is a limitation we acknowledge. Future work includes longitudinal tracking and A/B testing against human counselors."
"""
    _add_notes(slide, notes)


# ── Build Presentation ─────────────────────────────────────────

# Slide 1: Title
slide = prs.slides.add_slide(prs.slide_layouts[6])
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
print(f"Speaker notes added to all slides")
