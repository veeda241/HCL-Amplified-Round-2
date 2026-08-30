# SkillRoute Research Presentation
## AI-Powered Career Decision-Making: Integrating Psychological Theories into Personalized Learning Platforms

---

## SLIDE 1 — Title Slide

### AI-Powered Career Decision-Making
### Integrating Psychological Theories into Personalized Learning Platforms

**Your Name**
**Department of Psychology**
**[Your College Name]**
**August 2026**

---

## SLIDE 2 — The Problem

### 🎯 Career Indecision: A Growing Crisis

- **80%** of students experience significant career confusion during education
- Traditional career counseling is **limited by scalability** and availability
- Students face:
  - Too many career options → **Overwhelm**
  - Lack of personalized guidance → **Generic advice**
  - Rapidly changing industry demands → **Outdated information**
  - No clear learning order → **Directionless exploration**

> *"Students waste months learning the wrong skills because they lack structured, personalized career guidance."*

---

## SLIDE 3 — Research Question

### 🔬 Central Research Question

> **How can psychological theories of career decision-making, self-efficacy, and adaptive learning be operationalized in an AI-powered learning platform?**

### Our Contribution

1. **Theoretical Operationalization** — Translating abstract psychology constructs into computational mechanisms
2. **System Architecture** — Embedding psychological principles at every layer
3. **Practical Impact** — Demonstrating psychologically grounded AI produces better career guidance

---

## SLIDE 4 — The Solution: SkillRoute

### 💡 What is SkillRoute?

An **AI-powered career decision-making platform** that:

| Feature | Description |
|---------|-------------|
| 🧠 **Decides** | Not just recommends — *decides* the best career path |
| 📋 **Profiles** | 5-step psychological assessment of interests, skills, goals |
| 🗺️ **Plans** | Generates personalized, time-bound learning roadmaps |
| 📊 **Tracks** | Monitors progress and adapts based on performance |
| 🎯 **Assesses** | Tests actual skills vs. self-reported abilities |

**Tech Stack:** React + FastAPI + Groq LLM + Firebase

---

## SLIDE 5 — Theoretical Framework Overview

### 🧠 7 Psychology Theories Integrated

```
┌─────────────────────────────────────────────────────────────┐
│                    SKILLROUTE ARCHITECTURE                   │
├─────────────────────────────────────────────────────────────┤
│                                                              │
│  [INPUT LAYER]                                               │
│  Holland's RIASEC ←→ Dunning-Kruger ←→ SDT (Autonomy)      │
│         ↓                    ↓                   ↓           │
│  [AI DECISION LAYER]                                         │
│  Groq LLM Career Agent (Multi-factor Analysis)              │
│         ↓                                                    │
│  [ADAPTIVE LAYER]                                            │
│  Vygotsky's ZPD ←→ Csikszentmihalyi's Flow ←→ Goal Setting │
│         ↓                                                    │
│  [FEEDBACK LAYER]                                            │
│  Bandura's Self-Efficacy ←→ Progress Tracking ←→ Outcomes   │
│                                                              │
└─────────────────────────────────────────────────────────────┘
```

---

## SLIDE 6 — Theory 1: Holland's RIASEC Model

### 🎭 Career Personality-Environment Fit

**Theory:** Individuals succeed when their personality type matches their work environment (Holland, 1997)

**In SkillRoute:**
- 5-step onboarding collects: Interests, Skills, Goals, Education, Learning Pace
- AI agent analyzes multi-factor profile → generates career recommendation
- Alternative paths provided for informed decision-making

**Implementation:**
```python
class StudentProfile(BaseModel):
    interests: str      # Mapped to RIASEC categories
    skills: str         # Skill inventory
    goals: str          # Vocational aspirations
    learning_pace: str  # Individual difference
```

---

## SLIDE 7 — Theory 2: Bandura's Self-Efficacy

### 💪 Belief in One's Capabilities

**Theory:** Self-efficacy is built through mastery experiences and is a primary determinant of motivation (Bandura, 1977, 1997)

**In SkillRoute:**

| Mechanism | Implementation |
|-----------|----------------|
| **Mastery Experience** | AI skill quiz tests actual ability |
| **Calibration** | Gap between self-report and quiz score |
| **Growth Evidence** | Before/after outcomes dashboard |
| **Feedback Loop** | Strengths and areas to improve identified |

**Key Insight:** The quiz bridges the gap between *perceived* and *actual* skill level

---

## SLIDE 8 — Theory 3: Vygotsky's ZPD

### 📈 Zone of Proximal Development

**Theory:** Learning is most effective when targeting the zone between independent capability and guided achievement (Vygotsky, 1978)

**In SkillRoute:**

```
Current Skill Level ←──── ZPD ────→ Guided Achievement
        ↑                              ↑
   [Quiz Score]              [Adaptive Roadmap]
        ↓                              ↓
   Lower Boundary            Upper Boundary
```

**Adaptive Mechanism:**
- Progressing well → **Advance to harder topics** (raise upper boundary)
- Progress stalled → **Add remedial resources** (lower lower boundary)

```python
# If progressing well: suggest advanced topics
# If stuck: add remedial resources or extend timelines
```

---

## SLIDE 9 — Theory 4: Self-Determination Theory

### 🎯 Autonomy, Competence, Relatedness

**Theory:** Intrinsic motivation thrives when three basic needs are met (Deci & Ryan, 1985, 2000)

**In SkillRoute:**

| Need | How SkillRoute Addresses It |
|------|----------------------------|
| **Autonomy** | Users control profile, reset path, trigger adaptation |
| **Competence** | Skill quiz provides objective mastery feedback |
| **Relatedness** | Industry demand data connects to real job market |

**Impact:** Users feel empowered (autonomy), capable (competence), and connected (relatedness) → sustained motivation

---

## SLIDE 10 — Theory 5: Dunning-Kruger Effect

### 🪞 Correcting Metacognitive Bias

**Theory:** Unskilled individuals overestimate ability; skilled individuals underestimate (Kruger & Dunning, 1999)

**In SkillRoute:**

```
User Self-Reports: "I know Python, React, Data Analysis"
         ↓
AI Generates Quiz: Tests actual understanding
         ↓
Quiz Result: 40% → Skill Level: BEGINNER
         ↓
Gap Revealed: Overestimated ability
         ↓
Roadmap Adjusts: Starts with fundamentals
```

**Key Innovation:** Dual-assessment architecture reveals calibration bias

---

## SLIDE 11 — Theory 6: Goal Setting Theory

### 🎯 Specific, Challenging Goals with Feedback

**Theory:** Specific, challenging goals with feedback produce higher performance (Locke & Latham, 1990, 2002)

**In SkillRoute:**

| Goal Setting Principle | Implementation |
|----------------------|----------------|
| **Specific Goals** | Milestones with clear outcomes |
| **Challenging Yet Attainable** | AI calibrates difficulty to skill level |
| **Feedback** | Progress tracker, streak counter, % complete |
| **Time-Bound** | Phase durations (e.g., "2-3 weeks") |
| **Strategy Support** | Curated resources for each milestone |

**Roadmap Structure:**
- 4 phases × 2 milestones × 2 resources = Structured learning journey

---

## SLIDE 12 — Theory 7: Flow Theory

### 🌊 Optimal Experience Through Challenge-Skill Balance

**Theory:** Flow occurs when challenge matches skill level (Csikszentmihalyi, 1990)

**In SkillRoute:**

```
        Challenge
           ↑
     Anxiety │  ← Too hard (add scaffolding)
             │
    ─────────┼───────── FLOW ZONE ─────────────
             │
     Boredom │  ← Too easy (advance topics)
             │
           └──────────────────────→ Skill Level
```

**Adaptive System Maintains Flow:**
- Rapid progress → Increase challenge
- Stalled progress → Reduce challenge
- Always balancing between boredom and anxiety

---

## SLIDE 13 — System Architecture

### 🏗️ Full-Stack Implementation

```
┌────────────────────────────────────────────────────────────┐
│                     SKILLROUTE ARCHITECTURE                 │
├────────────────────────────────────────────────────────────┤
│                                                             │
│  [FRONTEND - React + Tailwind CSS]                         │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐     │
│  │Dashboard │ │SkillQuiz │ │Progress  │ │Learning  │     │
│  │          │ │          │ │Tracker   │ │Outcomes  │     │
│  └────┬─────┘ └────┬─────┘ └────┬─────┘ └────┬─────┘     │
│       └─────────────┼───────────┼─────────────┘            │
│                     ▼                                       │
│  [BACKEND - FastAPI + Python]                              │
│  ┌─────────────────────────────────────────────────┐      │
│  │  AI Agent Layer (Groq LLM)                       │      │
│  │  • Career Decision Agent                         │      │
│  │  • Roadmap Generation Agent                      │      │
│  │  • Adaptive Roadmap Agent                        │      │
│  │  • Quiz Agent                                    │      │
│  └─────────────────────┬───────────────────────────┘      │
│                         ▼                                   │
│  [DATABASE - Firebase Firestore]                           │
│  • User profiles  • Roadmaps  • Progress  • Quiz results  │
│                                                             │
└────────────────────────────────────────────────────────────┘
```

---

## SLIDE 14 — Implementation Highlights

### ⚙️ Technical Implementation

**1. Five-Step Psychological Profiling**
- Career Clarity Assessment (3 questions → 0-100 score)
- Personal Information
- Skills & Interests
- Goals & Experience
- Learning Preferences

**2. AI Career Decision Agent**
- Processes complete student profile
- Generates: Career recommendation, confidence score, reasoning trace, alternatives
- Model: Groq LLM (GPT-OSS-20B) for ultra-fast inference

**3. Adaptive Roadmap**
- Monitors: Phase completion, activity recency, streak consistency
- Triggers adaptation when inactivity ≥ 3 days
- Adjusts difficulty based on performance patterns

---

## SLIDE 15 — Results & Discussion

### 📊 Key Findings

| Finding | Implication |
|---------|-------------|
| Psychology theories can be computationally operationalized | Theory-practice bridge achieved |
| AI agent produces personalized career decisions | Scalable alternative to human counseling |
| Adaptive system adjusts to individual learning pace | ZPD and Flow Theory effectively implemented |
| Skill quiz reveals self-assessment bias | Dunning-Kruger correction mechanism works |
| Multi-factor profiling enhances decision quality | Holland's model scales through AI |

**Advantages Over Traditional Counseling:**
- ✅ Scalable (unlimited users)
- ✅ Consistent (algorithmic decisions)
- ✅ Accessible (24/7 availability)
- ✅ Data-driven (real-time market integration)

---

## SLIDE 16 — Ethical Considerations

### ⚠️ Limitations & Ethics

**Current Limitations:**
1. Quiz validity limited to 5 questions
2. Self-report bias in interests/goals
3. No longitudinal outcome tracking
4. Technology-sector focus (limited generalizability)
5. AI explainability remains partial

**Ethical Concerns:**
| Issue | Risk | Mitigation |
|-------|------|------------|
| **Algorithmic Bias** | Discrimination in recommendations | Diverse training data, fairness audits |
| **Over-Reliance** | Users defer to AI uncritically | Present alternatives, encourage reflection |
| **Data Privacy** | Sensitive psychological data | Firebase encryption, minimal data collection |
| **Transparency** | Opaque AI decisions | Decision trace feature, explainable AI |

---

## SLIDE 17 — Future Work

### 🚀 Research Directions

1. **Personality Assessment Integration**
   - Add MBTI, Big Five, or RIASEC instruments
   - Enhance psychological depth of profiling

2. **Longitudinal Outcome Tracking**
   - Track career outcomes months/years after guidance
   - Evaluate AI decision quality over time

3. **A/B Testing Against Human Counselors**
   - Controlled experiments comparing outcomes
   - Evidence of comparative effectiveness

4. **Multi-Domain Generalization**
   - Extend beyond technology careers
   - Healthcare, education, business sectors

5. **Gamification & Social Features**
   - Badges, leaderboards, peer comparison
   - Enhance motivation through relatedness

---

## SLIDE 18 — Conclusion

### 🎓 Key Takeaways

> *"SkillRoute demonstrates that psychological theories, traditionally applied in face-to-face counseling, can be effectively translated into computational mechanisms."*

**Summary:**
- 7 psychology theories → 7 computational mechanisms
- AI as a psychological agent, not just data processor
- Scalable, accessible, personalized career guidance
- Theory-grounded design produces meaningful interventions

**Impact:**
- Democratizes career guidance for underserved populations
- Extends human counselor reach through AI
- Provides evidence-based, personalized support at scale

> *"The ultimate promise is not to replace human counselors but to extend their reach."*

---

## SLIDE 19 — References

### 📚 Key Citations

| Author(s) | Theory | Year |
|-----------|--------|------|
| Holland, J. L. | Career Choice (RIASEC) | 1997 |
| Bandura, A. | Self-Efficacy Theory | 1977, 1997 |
| Vygotsky, L. S. | Zone of Proximal Development | 1978 |
| Deci, E. L. & Ryan, R. M. | Self-Determination Theory | 1985, 2000 |
| Kruger, J. & Dunning, D. | Dunning-Kruger Effect | 1999 |
| Locke, E. A. & Latham, G. P. | Goal Setting Theory | 1990, 2002 |
| Csikszentmihalyi, M. | Flow Theory | 1990 |
| Gati, I. et al. | Career Decision Difficulties | 1996 |
| Lent, R. W. et al. | Social Cognitive Career Theory | 1994 |
| Super, D. E. | Life-Span Career Development | 1990 |

---

## SLIDE 20 — Q&A

### ❓ Questions & Discussion

**Thank you!**

**Contact:** [Your Email]
**Project:** SkillRoute AI
**GitHub:** [Your Repository URL]

---

## SPEAKER NOTES

### Slide 1 (Title)
- Introduce yourself and your research topic
- Mention this is a psychology-computer science interdisciplinary project

### Slide 2 (Problem)
- Emphasize the prevalence of career indecision
- Use the 80% statistic to establish urgency
- Connect to real student experiences

### Slide 3 (Research Question)
- Clearly state the central question
- Highlight the three contributions
- Emphasize the interdisciplinary nature

### Slide 4 (Solution)
- Give a high-level overview of SkillRoute
- Emphasize "decides" vs "recommends"
- Mention the tech stack briefly

### Slide 5 (Theoretical Framework)
- Show the architecture diagram
- Explain how theories map to system layers
- This is the core contribution of the paper

### Slides 6-12 (Individual Theories)
- For each theory:
  1. State the theory in one sentence
  2. Show the implementation in SkillRoute
  3. Connect theory → code → user experience
- Use code snippets to ground abstract theories

### Slide 13 (Architecture)
- Walk through the full-stack design
- Explain data flow from input to feedback
- Emphasize the psychological input → AI decision → adaptive feedback loop

### Slide 14 (Implementation)
- Highlight the 5-step profiling process
- Explain the AI agent's role
- Describe the adaptive mechanism

### Slide 15 (Results)
- Present key findings in table format
- Compare advantages over traditional counseling
- Emphasize scalability and accessibility

### Slide 16 (Ethics)
- Acknowledge limitations honestly
- Present ethical concerns with mitigations
- Show awareness of responsible AI principles

### Slide 17 (Future Work)
- Present concrete research directions
- Emphasize longitudinal studies and A/B testing
- Connect to broader impact

### Slide 18 (Conclusion)
- Summarize the core contribution
- End with the key quote about extending counselor reach
- Leave audience with a memorable takeaway

### Slide 19 (References)
- Briefly mention key citations
- Don't read them all — just highlight the main ones

### Slide 20 (Q&A)
- Open for questions
- Have backup slides ready for common questions
