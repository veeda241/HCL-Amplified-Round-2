import os
import json
import asyncio
from groq import AsyncGroq


def _get_client():
    api_key = os.getenv("GROQ_API_KEY")
    if not api_key:
        raise ValueError("GROQ_API_KEY environment variable is not set")
    return AsyncGroq(api_key=api_key, timeout=60.0)


# ---------------------------------------------------------------------------
# Fallback resources injected when the AI returns a milestone with no URLs.
# Keys are lowercase keywords that might appear in a milestone name/focus skill.
# ---------------------------------------------------------------------------
FALLBACK_RESOURCES = {
    "python": [
        {"type": "video", "title": "Python for Beginners – Full Course", "url": "https://www.youtube.com/watch?v=rfscVS0vtbw", "duration": "4.5 hours"},
        {"type": "course", "title": "freeCodeCamp – Scientific Computing with Python", "url": "https://www.freecodecamp.org/learn/scientific-computing-with-python/", "duration": "Self-paced"},
        {"type": "documentation", "title": "Official Python Tutorial", "url": "https://docs.python.org/3/tutorial/", "duration": "Self-paced"},
    ],
    "javascript": [
        {"type": "video", "title": "JavaScript Full Course for Beginners", "url": "https://www.youtube.com/watch?v=PkZNo7MFNFg", "duration": "3.5 hours"},
        {"type": "course", "title": "freeCodeCamp – JavaScript Algorithms and Data Structures", "url": "https://www.freecodecamp.org/learn/javascript-algorithms-and-data-structures/", "duration": "Self-paced"},
        {"type": "documentation", "title": "MDN – JavaScript Guide", "url": "https://developer.mozilla.org/en-US/docs/Web/JavaScript/Guide", "duration": "Self-paced"},
    ],
    "react": [
        {"type": "video", "title": "React JS Full Course", "url": "https://www.youtube.com/watch?v=bMknfKXIFA8", "duration": "12 hours"},
        {"type": "documentation", "title": "React Official Tutorial", "url": "https://react.dev/learn/tutorial-tic-tac-toe", "duration": "2 hours"},
        {"type": "course", "title": "freeCodeCamp – Front End Development Libraries", "url": "https://www.freecodecamp.org/learn/front-end-development-libraries/", "duration": "Self-paced"},
    ],
    "html": [
        {"type": "course", "title": "freeCodeCamp – Responsive Web Design", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "duration": "300 hours"},
        {"type": "documentation", "title": "MDN – HTML Basics", "url": "https://developer.mozilla.org/en-US/docs/Learn/Getting_started_with_the_web/HTML_basics", "duration": "1 hour"},
        {"type": "video", "title": "HTML & CSS Crash Course", "url": "https://www.youtube.com/watch?v=916GWv2Qs08", "duration": "1.5 hours"},
    ],
    "css": [
        {"type": "documentation", "title": "MDN – CSS First Steps", "url": "https://developer.mozilla.org/en-US/docs/Learn/CSS/First_steps", "duration": "Self-paced"},
        {"type": "course", "title": "freeCodeCamp – Responsive Web Design", "url": "https://www.freecodecamp.org/learn/2022/responsive-web-design/", "duration": "300 hours"},
        {"type": "video", "title": "CSS Tutorial – Zero to Hero", "url": "https://www.youtube.com/watch?v=1Rs2ND1ryYc", "duration": "6 hours"},
    ],
    "sql": [
        {"type": "video", "title": "SQL Tutorial – Full Database Course", "url": "https://www.youtube.com/watch?v=HXV3zeQKqGY", "duration": "4.5 hours"},
        {"type": "course", "title": "Khan Academy – Intro to SQL", "url": "https://www.khanacademy.org/computing/computer-programming/sql", "duration": "Self-paced"},
        {"type": "documentation", "title": "W3Schools – SQL Tutorial", "url": "https://www.w3schools.com/sql/", "duration": "Self-paced"},
    ],
    "machine learning": [
        {"type": "video", "title": "Machine Learning Course – Stanford / Andrew Ng", "url": "https://www.youtube.com/watch?v=jGwO_UgTS7I", "duration": "10 hours"},
        {"type": "course", "title": "Coursera – Machine Learning Specialization (Audit free)", "url": "https://www.coursera.org/specializations/machine-learning-introduction", "duration": "Self-paced"},
        {"type": "video", "title": "Python Machine Learning Tutorial", "url": "https://www.youtube.com/watch?v=7eh4d6sabA0", "duration": "6 hours"},
    ],
    "data science": [
        {"type": "video", "title": "Data Science Full Course", "url": "https://www.youtube.com/watch?v=ua-CiDNNj30", "duration": "10 hours"},
        {"type": "course", "title": "Kaggle – Intro to Machine Learning", "url": "https://www.kaggle.com/learn/intro-to-machine-learning", "duration": "3 hours"},
        {"type": "course", "title": "freeCodeCamp – Data Analysis with Python", "url": "https://www.freecodecamp.org/learn/data-analysis-with-python/", "duration": "Self-paced"},
    ],
    "django": [
        {"type": "video", "title": "Django Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=rHux0gMZ3Eg", "duration": "6 hours"},
        {"type": "documentation", "title": "Django Official Tutorial", "url": "https://docs.djangoproject.com/en/stable/intro/tutorial01/", "duration": "Self-paced"},
        {"type": "video", "title": "Python Django Web Framework – freeCodeCamp", "url": "https://www.youtube.com/watch?v=F5mRW0jo-U4", "duration": "3.7 hours"},
    ],
    "node": [
        {"type": "video", "title": "Node.js and Express.js – Full Course", "url": "https://www.youtube.com/watch?v=Oe421EPjeBE", "duration": "8 hours"},
        {"type": "documentation", "title": "Node.js Official Docs", "url": "https://nodejs.org/en/learn/getting-started/introduction-to-nodejs", "duration": "Self-paced"},
        {"type": "course", "title": "The Odin Project – NodeJS", "url": "https://www.theodinproject.com/paths/full-stack-javascript/courses/nodejs", "duration": "Self-paced"},
    ],
    "git": [
        {"type": "video", "title": "Git and GitHub for Beginners", "url": "https://www.youtube.com/watch?v=RGOj5yH7evk", "duration": "1 hour"},
        {"type": "documentation", "title": "Pro Git Book (Free)", "url": "https://git-scm.com/book/en/v2", "duration": "Self-paced"},
        {"type": "course", "title": "GitHub Skills – Introduction to GitHub", "url": "https://github.com/skills/introduction-to-github", "duration": "1 hour"},
    ],
    "docker": [
        {"type": "video", "title": "Docker Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=pTFZFxd5hOI", "duration": "2 hours"},
        {"type": "documentation", "title": "Docker Official Get Started Guide", "url": "https://docs.docker.com/get-started/", "duration": "Self-paced"},
        {"type": "video", "title": "Docker and Kubernetes Full Course", "url": "https://www.youtube.com/watch?v=bhBSlnQcq2k", "duration": "10 hours"},
    ],
    "java": [
        {"type": "video", "title": "Java Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=eIrMbAQSU34", "duration": "2.5 hours"},
        {"type": "course", "title": "Coursera – Object Oriented Programming in Java (Audit free)", "url": "https://www.coursera.org/learn/object-oriented-java", "duration": "Self-paced"},
        {"type": "documentation", "title": "Oracle – Java Tutorials", "url": "https://docs.oracle.com/javase/tutorial/", "duration": "Self-paced"},
    ],
    "c++": [
        {"type": "video", "title": "C++ Tutorial for Beginners – Full Course", "url": "https://www.youtube.com/watch?v=vLnPwxZdW4Y", "duration": "4 hours"},
        {"type": "documentation", "title": "cppreference.com", "url": "https://en.cppreference.com/w/", "duration": "Self-paced"},
        {"type": "course", "title": "Coursera – C for Everyone (Audit free)", "url": "https://www.coursera.org/learn/c-for-everyone", "duration": "Self-paced"},
    ],
    "aws": [
        {"type": "video", "title": "AWS Certified Cloud Practitioner – Full Course", "url": "https://www.youtube.com/watch?v=SOTamWNgDKc", "duration": "14 hours"},
        {"type": "course", "title": "AWS Skill Builder – Cloud Practitioner Essentials (Free)", "url": "https://explore.skillbuilder.aws/learn/course/134/aws-cloud-practitioner-essentials", "duration": "6 hours"},
        {"type": "documentation", "title": "AWS Getting Started", "url": "https://aws.amazon.com/getting-started/", "duration": "Self-paced"},
    ],
    "linux": [
        {"type": "video", "title": "Linux Command Line Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=YHFzr-akOas", "duration": "6 hours"},
        {"type": "course", "title": "The Linux Command Line (Free Book)", "url": "https://linuxcommand.org/tlcl.php", "duration": "Self-paced"},
        {"type": "video", "title": "Linux Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=sWbUDq4S6Y8", "duration": "5 hours"},
    ],
    "cybersecurity": [
        {"type": "course", "title": "Google Cybersecurity Certificate (Audit free on Coursera)", "url": "https://www.coursera.org/professional-certificates/google-cybersecurity", "duration": "Self-paced"},
        {"type": "course", "title": "TryHackMe – Pre-Security Path (Free)", "url": "https://tryhackme.com/path/outline/presecurity", "duration": "Self-paced"},
        {"type": "video", "title": "Ethical Hacking Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=3Kq1MIfTWCE", "duration": "15 hours"},
    ],
    "ui": [
        {"type": "video", "title": "UI/UX Design Tutorial – Full Course for Beginners", "url": "https://www.youtube.com/watch?v=c9Wg6Cb_YlU", "duration": "3.5 hours"},
        {"type": "course", "title": "Google UX Design Certificate (Audit free on Coursera)", "url": "https://www.coursera.org/professional-certificates/google-ux-design", "duration": "Self-paced"},
        {"type": "documentation", "title": "Material Design Guidelines", "url": "https://m3.material.io/", "duration": "Self-paced"},
    ],
    "devops": [
        {"type": "video", "title": "DevOps Tutorial for Beginners", "url": "https://www.youtube.com/watch?v=j5Zsa_eOXeY", "duration": "2 hours"},
        {"type": "course", "title": "The Odin Project – DevOps Basics", "url": "https://www.theodinproject.com/", "duration": "Self-paced"},
        {"type": "video", "title": "DevOps CI/CD Full Course – freeCodeCamp", "url": "https://www.youtube.com/watch?v=OXE2a8dqIAI", "duration": "3.4 hours"},
    ],
}

GENERIC_FALLBACK = [
    {"type": "video", "title": "freeCodeCamp – Full Stack Development", "url": "https://www.youtube.com/c/Freecodecamp", "duration": "Self-paced"},
    {"type": "course", "title": "The Odin Project – Full Stack Path (Free)", "url": "https://www.theodinproject.com/", "duration": "Self-paced"},
    {"type": "course", "title": "Khan Academy – Computing", "url": "https://www.khanacademy.org/computing", "duration": "Self-paced"},
]


def _pick_fallback(text: str) -> list:
    """Return the most relevant fallback resources for the given text."""
    text_lower = text.lower()
    for keyword, resources in FALLBACK_RESOURCES.items():
        if keyword in text_lower:
            return resources
    return GENERIC_FALLBACK


def _ensure_resources(result: dict) -> dict:
    """
    Post-process the roadmap to guarantee every milestone has at least one
    resource with a real (non-empty, http*) URL.
    """
    try:
        roadmap_data = result.get("learning_roadmap", {})
        phases = roadmap_data.get("roadmap", [])
        for phase in phases:
            focus_skills = " ".join(phase.get("focus_skills", []))
            phase_text = phase.get("phase", "") + " " + focus_skills
            for milestone in phase.get("milestones", []):
                resources = milestone.get("resources", [])
                good_resources = [
                    r for r in resources
                    if isinstance(r.get("url"), str) and r["url"].startswith("http")
                ]
                if not good_resources:
                    context = milestone.get("name", "") + " " + phase_text
                    milestone["resources"] = _pick_fallback(context)
                    print(f"DEBUG: Injected fallback resources for milestone '{milestone.get('name')}'")
                else:
                    milestone["resources"] = good_resources
    except Exception as e:
        print(f"Warning: _ensure_resources failed: {e}")
    return result


def _repair_json(content: str) -> str:
    """Try to repair truncated JSON by closing open brackets/braces."""
    # Remove trailing incomplete string value
    content = content.rstrip()
    # If ends with comma or colon, remove it
    if content.endswith(",") or content.endswith(":"):
        content = content[:-1]
    # Count unclosed brackets
    opens = content.count("{") - content.count("}")
    opens_arr = content.count("[") - content.count("]")
    # Close any incomplete string
    if content.count('"') % 2 != 0:
        content += '"'
    # Close open arrays first, then objects
    for _ in range(opens_arr):
        content += "]"
    for _ in range(opens):
        content += "}"
    return content


SYSTEM_PROMPT = """Analyze student profile. Return ONLY raw JSON, no markdown.
{"career_decision":{"career":"<title>","reasoning":"<1-2 sentences>","confidence":<0-100>,"skill_match_percentage":<0-100>,"market_readiness":<0-100>,"industry_demand":"<trending|stable|emerging>","key_strengths":["<short>"],"skill_gaps":["<short>"],"time_to_job_ready":"<X months>","decision_trace":[{"step":"Analysis","detail":"<1 sentence>"},{"step":"Paths","detail":"<1 sentence>"},{"step":"Decision","detail":"<1 sentence>"}],"alternatives":[{"career":"<alt>","match_score":<0-100>,"reason":"<short>"}]},"learning_roadmap":{"duration_months":<num>,"roadmap":[{"phase":"Phase N: <Title>","duration":"X-Y weeks","difficulty":"<beginner|intermediate|advanced>","focus_skills":["s"],"outcomes":["o"],"milestones":[{"name":"<short>","description":"<1 sentence>","estimated_hours":<num>,"resources":[{"type":"<video|course|documentation>","title":"<title>","url":"https://real-url","duration":"Xh"}]}],"prerequisites":["<p>"]}]}}
Rules: 4 phases, 2 milestones each, 2 resources each. URLs must be real (YouTube, freeCodeCamp, MDN, Coursera, Khan Academy, W3Schools, official docs). Keep ALL text fields short."""


async def generate_roadmap(profile: dict) -> dict:
    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            client = _get_client()
            response = await client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(profile)}
                ],
                temperature=0.7,
                max_completion_tokens=7000,
                top_p=1,
                stream=False
            )

            content = response.choices[0].message.content
            print(f"DEBUG: Raw content (first 300 chars): {content[:300]}")

            # Strip any accidental markdown wrappers
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            try:
                result = json.loads(content)
                result = _ensure_resources(result)
                return result
            except json.JSONDecodeError:
                # Try to repair truncated JSON by closing open brackets
                repaired = _repair_json(content)
                if repaired:
                    try:
                        result = json.loads(repaired)
                        print("DEBUG: Successfully repaired truncated JSON")
                        result = _ensure_resources(result)
                        return result
                    except json.JSONDecodeError:
                        pass
                print(f"JSON Decode Error. Content: {content[:300]}...")
                raise ValueError("Roadmap agent returned invalid JSON")

        except Exception as e:
            error_type = type(e).__name__
            print(f"Attempt {retry_count + 1} failed: {error_type} - {str(e)}")
            retry_count += 1
            if retry_count >= max_retries:
                raise RuntimeError(
                    f"Failed after {max_retries} attempts. Last error: {error_type} - {str(e)}"
                )
            await asyncio.sleep(2 ** retry_count)


# Concise adapt prompt
ADAPT_SYSTEM_PROMPT = """Adapt the student's learning roadmap based on progress data. Return ONLY raw JSON (no markdown).

Input has current_roadmap and progress (completed_phases, streak_days, days_since_activity).

Return JSON:
{"adaptation_reasoning":"<what changed and why>","duration_months":<num>,"roadmap":[{"phase":"Phase N: ...","duration":"...","difficulty":"<beginner|intermediate|advanced>","focus_skills":["skill"],"outcomes":["outcome"],"milestones":[{"name":"...","description":"...","estimated_hours":<num>,"resources":[{"type":"<video|course|documentation>","title":"...","url":"https://...","duration":"..."}]}]}]}

Rules:
- If progressing well: suggest advanced topics or speed up
- If stuck: add remedial resources or extend timelines
- Keep structure consistent, modify future phases
- Every resource URL must start with https:// and be real"""


async def adapt_roadmap(current_data: dict) -> dict:
    progress = current_data.get("progress", {})
    last_active = progress.get("last_activity_date")
    days_since_activity = 0

    if last_active:
        from datetime import datetime
        try:
            last_date = datetime.fromisoformat(last_active).date()
            days_since_activity = (datetime.utcnow().date() - last_date).days
        except (ValueError, TypeError):
            days_since_activity = 0

    input_data = {
        "current_roadmap": current_data.get("learning_roadmap"),
        "progress": {
            **progress,
            "days_since_activity": days_since_activity,
        }
    }

    max_retries = 3
    retry_count = 0

    while retry_count < max_retries:
        try:
            client = _get_client()
            response = await client.chat.completions.create(
                model="openai/gpt-oss-20b",
                messages=[
                    {"role": "system", "content": ADAPT_SYSTEM_PROMPT},
                    {"role": "user", "content": json.dumps(input_data)}
                ],
                temperature=0.7,
                max_completion_tokens=7000,
                top_p=1,
                stream=False
            )

            content = response.choices[0].message.content
            content = content.strip()
            if content.startswith("```json"):
                content = content[7:]
            elif content.startswith("```"):
                content = content[3:]
            if content.endswith("```"):
                content = content[:-3]
            content = content.strip()

            try:
                result = json.loads(content)
                result = _ensure_resources({"learning_roadmap": result})
                return result.get("learning_roadmap", result)
            except json.JSONDecodeError:
                print(f"JSON Decode Error in adapt_roadmap. Content: {content[:100]}...")
                return current_data.get("learning_roadmap")

        except Exception as e:
            error_type = type(e).__name__
            print(f"Attempt {retry_count + 1} failed in adapt_roadmap: {error_type} - {str(e)}")
            retry_count += 1
            if retry_count >= max_retries:
                return current_data.get("learning_roadmap")
            await asyncio.sleep(2 ** retry_count)

    return current_data.get("learning_roadmap")
