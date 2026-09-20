 import streamlit as st
New Student Welcome & Campus Guide Portal.

A single-file Streamlit application organised into exactly three tabs:

    1. Welcome Hub             - personalised greeting and the university vision.
    2. Academic Faculties      - Computer Science, Software Engineering, Health Sciences.
    3. Contact & Registration  - orientation steps and a mailto contact form.

Run locally with:

    pip install streamlit
    streamlit run app.py
"""

from __future__ import annotations

import base64
from pathlib import Path
from urllib.parse import quote

import streamlit as st

# ---------------------------------------------------------------------------
# Page configuration (must be the first Streamlit call in the script).
# ---------------------------------------------------------------------------

st.set_page_config(
    page_title="Green Hope University Garowe — New Student Welcome",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="collapsed",
)

# ---------------------------------------------------------------------------
# Institution constants.
# ---------------------------------------------------------------------------

UNIVERSITY = "Green Hope University"
CAMPUS = "Garowe Campus"
CAMPUS_EMAIL = "garowecampus@greenhopeuniversity.edu.so"
CAMPUS_PHONE = "+252 90 000 0000"
CAMPUS_ADDRESS = "Garowe, Nugaal Region, Puntland State, Somalia"
OFFICE_HOURS = "Sunday – Thursday, 8:00 AM – 4:00 PM (EAT)"

HERO_IMAGE = "campus_hero.png"
VISION_IMAGE = "vision_illustration.png"
CREST_IMAGE = "crest.png"

# ---------------------------------------------------------------------------
# Sample data structures.
# ---------------------------------------------------------------------------

VISION_STATEMENT = (
    "To be a leading institution of higher learning in the Horn of Africa, "
    "nurturing ethical, skilled and entrepreneurial graduates who serve their "
    "communities and drive sustainable development across Puntland and beyond."
)

MISSION_STATEMENT = (
    "To deliver accessible, high-quality and practice-oriented education that "
    "equips young Somalis with the technical, analytical and leadership skills "
    "needed to build a prosperous and peaceful society."
)

CORE_VALUES = [
    ("Knowledge", "Academic excellence grounded in curiosity, rigour and lifelong learning."),
    ("Service", "Graduates who give back to their community, region and country."),
    ("Hope", "Opportunity for every student, regardless of background or means."),
]

FACULTIES = [
    {
        "id": "cs",
        "name": "Computer Science",
        "degree": "Bachelor of Science (BSc)",
        "duration": "4 years · 8 semesters",
        "credits": "128 credit hours",
        "visual": "faculty_cs.png",
        "glyph": "💻",
        "tagline": "Build the software, data systems and intelligent products that Somalia's digital economy needs.",
        "description": (
            "The Computer Science programme develops a strong foundation in "
            "algorithms, data structures, systems and software design, then "
            "extends into data science, networking and artificial intelligence. "
            "Students work in well-equipped computer laboratories throughout "
            "their studies and complete a graduation project that solves a real "
            "problem for a local organisation."
        ),
        "courses": [
            "Programming Fundamentals (Python & C++)",
            "Data Structures & Algorithms",
            "Database Systems & SQL",
            "Operating Systems & Computer Networks",
            "Object-Oriented Analysis & Design",
            "Data Science & Machine Learning",
            "Web & Mobile Application Development",
            "Information Security & Cryptography",
            "Software Engineering & Project Management",
            "Final-Year Graduation Project",
        ],
        "careers": [
            "Software Developer / Engineer",
            "Data Analyst / Data Scientist",
            "Database Administrator",
            "Network & Systems Administrator",
            "Cybersecurity Analyst",
            "IT Consultant or Entrepreneur",
        ],
        "skills": ["Python", "SQL", "Git", "Linux", "Machine Learning", "Cloud Basics"],
    },
    {
        "id": "se",
        "name": "Software Engineering",
        "degree": "Bachelor of Science (BSc)",
        "duration": "4 years · 8 semesters",
        "credits": "132 credit hours",
        "visual": "faculty_se.png",
        "glyph": "⚙️",
        "tagline": "Learn to design, build, test and ship reliable software at a professional standard.",
        "description": (
            "Software Engineering applies engineering discipline to the creation "
            "of software systems. The programme emphasises requirements "
            "engineering, architecture, testing, DevOps and agile teamwork. "
            "Students build projects in teams using modern version control and "
            "continuous integration, mirroring how professional software houses "
            "operate, and complete a capstone project delivered to a real client."
        ),
        "courses": [
            "Introduction to Software Engineering",
            "Requirements Engineering & System Design",
            "Software Architecture & Design Patterns",
            "Advanced Programming (Java & JavaScript)",
            "Software Testing, QA & Verification",
            "DevOps, CI/CD & Version Control",
            "Agile Methods & Team Project Management",
            "Mobile & Web Application Engineering",
            "Human-Computer Interaction & UI/UX",
            "Software Engineering Capstone Project",
        ],
        "careers": [
            "Software Engineer / Full-Stack Developer",
            "QA / Test Automation Engineer",
            "DevOps & Cloud Engineer",
            "Mobile Application Developer",
            "Technical Product Manager",
            "Systems Analyst / Solutions Architect",
        ],
        "skills": ["Java", "JavaScript", "Git & CI/CD", "Docker", "Testing", "Agile / Scrum"],
    },
    {
        "id": "hs",
        "name": "Health Sciences",
        "degree": "Bachelor of Science (BSc)",
        "duration": "4 years · 8 semesters",
        "credits": "136 credit hours",
        "visual": "faculty_hs.png",
        "glyph": "🩺",
        "tagline": "Strengthen Somalia's health system with skilled, compassionate and evidence-led practitioners.",
        "description": (
            "The Health Sciences programme combines a rigorous grounding in "
            "biology, anatomy and physiology with public health, epidemiology "
            "and health management. Teaching is delivered through lectures, "
            "practical laboratory sessions and supervised placements with "
            "partner clinics and hospitals in Garowe, preparing graduates for "
            "clinical support, public health and health administration roles."
        ),
        "courses": [
            "Human Anatomy & Physiology",
            "Medical Biochemistry & Microbiology",
            "Public Health & Epidemiology",
            "Primary Health Care & Community Medicine",
            "Pharmacology & Drug Administration",
            "Maternal, Newborn & Child Health",
            "Health Information Systems & Medical Records",
            "Nutrition & Environmental Health",
            "Health Policy, Ethics & Management",
            "Research Methods & Clinical Placement",
        ],
        "careers": [
            "Public Health Officer",
            "Community Health Worker / Programme Officer",
            "Clinical Laboratory Technologist",
            "Health Information / Records Manager",
            "Hospital & Clinic Administrator",
            "NGO / Humanitarian Health Coordinator",
        ],
        "skills": ["Epidemiology", "Clinical Skills", "Health Data", "Community Outreach", "Ethics", "Research"],
    },
]

ORIENTATION_STEPS = [
    {
        "n": 1,
        "title": "Confirm Your Admission",
        "where": "Admissions & Registrar",
        "time": "Day 1 · 30 minutes",
        "desc": (
            "Bring your original secondary school certificate and national ID. "
            "The registrar will verify your documents, confirm your programme and "
            "issue your official admission letter with your student number."
        ),
        "bring": "Secondary school certificate, national ID or passport, 4 passport photographs",
    },
    {
        "n": 2,
        "title": "Pay Tuition & Registration Fees",
        "where": "Finance / Bursar Office",
        "time": "Day 1 · 30 minutes",
        "desc": (
            "Pay your first-semester tuition and one-off registration fee. "
            "Payment can be made by bank transfer or approved mobile money. "
            "Always collect an official receipt — you will need it for step 3."
        ),
        "bring": "Admission letter, payment confirmation, receipt",
    },
    {
        "n": 3,
        "title": "Complete Official Registration",
        "where": "Admissions & Registrar",
        "time": "Day 1–2 · 45 minutes",
        "desc": (
            "Submit your signed admission letter and fee receipt to be entered "
            "into the student register. You will receive your program of study, "
            "academic calendar and your permanent student record number."
        ),
        "bring": "Admission letter, fee receipt, photographs",
    },
    {
        "n": 4,
        "title": "Collect Your Student ID Card",
        "where": "Student Affairs",
        "time": "Day 2 · 20 minutes",
        "desc": (
            "Your student ID card is required for campus access, examinations, "
            "library borrowing and the computer laboratories. Keep it with you at "
            "all times on campus and report any loss immediately."
        ),
        "bring": "Registration slip, 2 passport photographs",
    },
    {
        "n": 5,
        "title": "Activate Your Student Email & Portal",
        "where": "IT Support",
        "time": "Day 2 · 20 minutes",
        "desc": (
            "Set up your university email account and student portal login. All "
            "official announcements, course materials, results and fee statements "
            "are delivered there, so activate it in your first week."
        ),
        "bring": "Student ID number, admission letter",
    },
    {
        "n": 6,
        "title": "Register Your Courses",
        "where": "Academic Advising",
        "time": "Day 3 · 1 hour",
        "desc": (
            "Meet your academic advisor to select and register your first-semester "
            "courses. Your advisor explains prerequisites, credit loads and how to "
            "plan your degree pathway across all eight semesters."
        ),
        "bring": "Program of study, student ID, course catalogue",
    },
    {
        "n": 7,
        "title": "Hostel & Welfare Allocation",
        "where": "Hostel / Welfare Office",
        "time": "Day 3 · 30 minutes",
        "desc": (
            "Students requiring accommodation are allocated a room and issued "
            "bedding and keys. The welfare office also explains the code of "
            "conduct, support services and the emergency contact procedure."
        ),
        "bring": "Student ID, hostel application form, bedding",
    },
    {
        "n": 8,
        "title": "Health Check & Library Card",
        "where": "Health Center, then Library",
        "time": "Day 4 · 40 minutes",
        "desc": (
            "Complete your basic health screening and submit your medical record "
            "to the campus Health Center. Then register at the Library to receive "
            "your borrowing card and orientation on the digital catalogue."
        ),
        "bring": "Student ID, vaccination or medical record",
    },
    {
        "n": 9,
        "title": "Attend Freshman Orientation Week",
        "where": "Student Affairs · Main Auditorium",
        "time": "Day 5 · Full day",
        "desc": (
            "Orientation week introduces the academic calendar, study skills, "
            "campus facilities, student clubs and the university code of conduct. "
            "Attendance is compulsory and is recorded."
        ),
        "bring": "Student ID, notebook, orientation schedule",
    },
    {
        "n": 10,
        "title": "Acknowledge the Student Handbook",
        "where": "Student Affairs",
        "time": "End of week · 15 minutes",
        "desc": (
            "Read and sign the student handbook acknowledgment covering academic "
            "integrity, attendance, examination rules, grievance procedures and "
            "the code of conduct. Your signed form completes enrolment."
        ),
        "bring": "Student ID, signed acknowledgment form",
    },
]

INQUIRY_TEMPLATES = {
    "General enquiry": {
        "subject": "Freshman enquiry — Green Hope University Garowe Campus",
        "body": (
            "Dear Garowe Campus Team,\n\n"
            "My name is {name} and I am joining as a freshman this semester.\n\n"
            "I would like to ask about: [your question here]\n\n"
            "Thank you for your time and guidance.\n\n"
            "Kind regards,\n{name}"
        ),
    },
    "Registration & admission": {
        "subject": "Freshman registration and admission enquiry — Garowe Campus",
        "body": (
            "Dear Admissions & Registrar,\n\n"
            "My name is {name}. I would like to confirm the requirements and "
            "deadlines for freshman registration.\n\n"
            "Specifically I would like to know:\n"
            "1. The exact documents I must bring.\n"
            "2. The registration deadline for this semester.\n"
            "3. Whether I can complete registration remotely.\n\n"
            "Thank you.\n\nKind regards,\n{name}"
        ),
    },
    "Tuition & fees": {
        "subject": "Tuition and fee payment enquiry — Garowe Campus",
        "body": (
            "Dear Finance Office,\n\n"
            "My name is {name}. I would like to request information about the "
            "tuition and registration fees for my programme.\n\n"
            "Please could you confirm:\n"
            "1. The total tuition for the first semester.\n"
            "2. Accepted payment methods, including mobile money and bank transfer.\n"
            "3. Whether an instalment plan is available.\n\n"
            "Thank you for your assistance.\n\nKind regards,\n{name}"
        ),
    },
    "Hostel & accommodation": {
        "subject": "Hostel accommodation enquiry — Garowe Campus",
        "body": (
            "Dear Hostel / Welfare Office,\n\n"
            "My name is {name} and I am an incoming freshman. I would like to "
            "apply for student accommodation.\n\n"
            "Please could you advise:\n"
            "1. Whether rooms are still available for this semester.\n"
            "2. What the room and boarding costs are.\n"
            "3. What I should bring with me.\n\n"
            "Thank you.\n\nKind regards,\n{name}"
        ),
    },
    "Course registration & advising": {
        "subject": "Course registration and academic advising — Garowe Campus",
        "body": (
            "Dear Academic Advising,\n\n"
            "My name is {name}, an incoming freshman. I would like guidance on "
            "registering my first-semester courses.\n\n"
            "Please could you help me with:\n"
            "1. The recommended first-semester course load.\n"
            "2. How to arrange a meeting with my academic advisor.\n"
            "3. Any prerequisites I should complete early.\n\n"
            "Thank you very much.\n\nKind regards,\n{name}"
        ),
    },
    "IT & student portal access": {
        "subject": "Student email and portal activation — Garowe Campus",
        "body": (
            "Dear IT Support,\n\n"
            "My name is {name}. I am having difficulty activating my student "
            "email account and portal login.\n\n"
            "Could you please assist me with:\n"
            "1. Resetting my portal password.\n"
            "2. Confirming my official student email address.\n"
            "3. The recommended way to access course materials online.\n\n"
            "Thank you for your help.\n\nKind regards,\n{name}"
        ),
    },
    "Health & medical records": {
        "subject": "Health check and medical record submission — Garowe Campus",
        "body": (
            "Dear Health Center,\n\n"
            "My name is {name}, a new student on the Garowe Campus. I would like "
            "to complete my required health check.\n\n"
            "Please advise:\n"
            "1. When and where the health screening takes place.\n"
            "2. Which medical or vaccination records I must submit.\n"
            "3. Whether appointments are required.\n\n"
            "Thank you.\n\nKind regards,\n{name}"
        ),
    },
    "Library services": {
        "subject": "Library registration and services — Garowe Campus",
        "body": (
            "Dear Library Team,\n\n"
            "My name is {name}, an incoming freshman. I would like to register "
            "for my library borrowing card.\n\n"
            "Please could you explain:\n"
            "1. How to register and obtain my library card.\n"
            "2. How to access the digital catalogue and e-resources.\n"
            "3. Borrowing rules and opening hours.\n\n"
            "Thank you.\n\nKind regards,\n{name}"
        ),
    },
}

ASSETS_DIR = Path(__file__).parent / "assets"

# ---------------------------------------------------------------------------
# Asset helpers.
# ---------------------------------------------------------------------------


@st.cache_data(show_spinner=False)
def _data_uri(filename: str) -> str:
    """Return a base64 data URI for an image in the assets directory.

    Embedding the images directly keeps the interface fully self-contained and
    removes any dependency on how Streamlit happens to serve static files.
    """
    path = ASSETS_DIR / filename
    if not path.exists():
        return ""
    encoded = base64.b64encode(path.read_bytes()).decode("ascii")
    return f"data:image/png;base64,{encoded}"


def asset_tag(filename: str, alt: str, css_class: str = "") -> str:
    """Return an <img> tag for an asset, or an empty string if it is missing."""
    uri = _data_uri(filename)
    if not uri:
        return ""
    class_attr = f' class="{css_class}"' if css_class else ""
    return f'<img src="{uri}" alt="{alt}"{class_attr}>'


def build_mailto(subject: str, body: str, to: str = CAMPUS_EMAIL) -> str:
    """Build a mailto: URL with a pre-filled subject and body."""
    return f"mailto:{to}?subject={quote(subject)}&body={quote(body)}"


# ---------------------------------------------------------------------------
# Styling.
# ---------------------------------------------------------------------------

CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Fraunces:opsz,wght@9..144,600;9..144,700&family=Plus+Jakarta+Sans:wght@400;500;600;700&display=swap');

:root {
    --ghu-emerald:      #0F5C4A;
    --ghu-emerald-600:  #14795F;
    --ghu-emerald-200:  #CDE7DD;
    --ghu-emerald-050:  #EEF7F3;
    --ghu-gold:         #C9A227;
    --ghu-gold-050:     #FBF4DF;
    --ghu-cream:        #FBF8F3;
    --ghu-white:        #FFFFFF;
    --ghu-ink:          #12211C;
    --ghu-muted:        #5C6B66;
    --ghu-line:         #E4DED2;
    --ghu-radius:       16px;
    --ghu-shadow:       0 1px 2px rgba(18, 33, 28, 0.05), 0 8px 24px rgba(18, 33, 28, 0.05);
}

html, body, [class*="css"] {
    font-family: 'Plus Jakarta Sans', -apple-system, BlinkMacSystemFont, sans-serif;
}

.stApp { background: var(--ghu-cream); }

#MainMenu, footer, header[data-testid="stHeader"] { visibility: hidden; height: 0; }

.block-container {
    padding-top: 1.4rem;
    padding-bottom: 3.5rem;
    max-width: 1220px;
}

/* ---------------------------------------------------------------- Tabs --- */
.stTabs [data-baseweb="tab-list"] {
    gap: 10px;
    background: var(--ghu-white);
    padding: 9px;
    border-radius: 16px;
    border: 1px solid var(--ghu-line);
    box-shadow: var(--ghu-shadow);
    margin-bottom: 1.6rem;
}
.stTabs [data-baseweb="tab"] {
    height: 48px;
    border-radius: 11px;
    padding: 0 22px;
    background: transparent;
    color: var(--ghu-muted);
    font-weight: 600;
    font-size: 0.95rem;
    letter-spacing: 0.01em;
    transition: all 0.18s ease;
}
.stTabs [data-baseweb="tab"]:hover {
    background: var(--ghu-emerald-050);
    color: var(--ghu-emerald);
}
.stTabs [aria-selected="true"] {
    background: var(--ghu-emerald) !important;
    color: var(--ghu-white) !important;
    box-shadow: 0 4px 14px rgba(15, 92, 74, 0.28);
}
.stTabs [data-baseweb="tab-highlight"],
.stTabs [data-baseweb="tab-border"] { display: none; }

/* ---------------------------------------------------------------- Hero --- */
.ghu-hero {
    position: relative;
    border-radius: 22px;
    overflow: hidden;
    background-size: cover;
    background-position: center 65%;
    min-height: 430px;
    display: flex;
    align-items: flex-end;
    box-shadow: 0 18px 48px rgba(18, 33, 28, 0.16);
    margin-bottom: 1.6rem;
}
.ghu-hero::after {
    content: '';
    position: absolute;
    inset: 0;
    background: linear-gradient(180deg, rgba(9, 40, 33, 0.18) 0%, rgba(9, 40, 33, 0.55) 52%, rgba(7, 32, 26, 0.90) 100%);
}
.ghu-hero-inner {
    position: relative;
    z-index: 2;
    padding: 40px 44px 38px;
    width: 100%;
}
.ghu-eyebrow {
    display: inline-block;
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.18em;
    text-transform: uppercase;
    color: var(--ghu-gold);
    background: rgba(255, 255, 255, 0.10);
    border: 1px solid rgba(201, 162, 39, 0.42);
    padding: 6px 14px;
    border-radius: 999px;
    margin-bottom: 18px;
    backdrop-filter: blur(3px);
}
.ghu-hero-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: clamp(2.1rem, 4.4vw, 3.5rem);
    line-height: 1.06;
    font-weight: 700;
    color: #FFFFFF;
    margin: 0 0 6px 0;
    letter-spacing: -0.015em;
}
.ghu-hero-campus {
    font-family: 'Fraunces', Georgia, serif;
    font-size: clamp(1.15rem, 2.1vw, 1.6rem);
    font-weight: 600;
    color: var(--ghu-emerald-200);
    margin-bottom: 16px;
    letter-spacing: 0.01em;
}
.ghu-hero-sub {
    color: rgba(255, 255, 255, 0.90);
    font-size: 1.02rem;
    line-height: 1.65;
    max-width: 660px;
    margin: 0 0 22px 0;
}
.ghu-chips { display: flex; flex-wrap: wrap; gap: 9px; }
.ghu-chip {
    font-size: 0.79rem;
    font-weight: 600;
    color: #FFFFFF;
    background: rgba(255, 255, 255, 0.14);
    border: 1px solid rgba(255, 255, 255, 0.26);
    padding: 7px 14px;
    border-radius: 999px;
    backdrop-filter: blur(3px);
}

/* --------------------------------------------------------------- Cards --- */
.ghu-card {
    background: var(--ghu-white);
    border: 1px solid var(--ghu-line);
    border-radius: var(--ghu-radius);
    padding: 26px 28px;
    box-shadow: var(--ghu-shadow);
    height: 100%;
}
.ghu-card-accent { border-top: 4px solid var(--ghu-emerald); }
.ghu-card-gold   { border-top: 4px solid var(--ghu-gold); }

.ghu-card-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.28rem;
    font-weight: 600;
    color: var(--ghu-ink);
    margin: 0 0 10px 0;
    letter-spacing: -0.01em;
}
.ghu-card-body { color: var(--ghu-muted); font-size: 0.95rem; line-height: 1.72; margin: 0; }

/* ------------------------------------------------------- Section header --- */
.ghu-section-eyebrow {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.17em;
    text-transform: uppercase;
    color: var(--ghu-emerald-600);
    margin-bottom: 7px;
}
.ghu-section-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: clamp(1.55rem, 2.9vw, 2.15rem);
    font-weight: 700;
    color: var(--ghu-ink);
    margin: 0 0 8px 0;
    letter-spacing: -0.015em;
}
.ghu-section-sub {
    color: var(--ghu-muted);
    font-size: 0.98rem;
    line-height: 1.65;
    max-width: 760px;
    margin: 0 0 22px 0;
}

/* ----------------------------------------------------------- Greeting --- */
.ghu-greeting {
    background: linear-gradient(135deg, var(--ghu-emerald) 0%, #0B4A3B 58%, #0A3F33 100%);
    border-radius: var(--ghu-radius);
    padding: 32px 34px;
    color: #FFFFFF;
    box-shadow: 0 14px 36px rgba(15, 92, 74, 0.24);
    position: relative;
    overflow: hidden;
}
.ghu-greeting::before {
    content: '';
    position: absolute;
    top: -70px; right: -50px;
    width: 260px; height: 260px;
    border-radius: 50%;
    background: radial-gradient(circle, rgba(201, 162, 39, 0.26) 0%, rgba(201, 162, 39, 0) 68%);
}
.ghu-greeting-name {
    font-family: 'Fraunces', Georgia, serif;
    font-size: clamp(1.5rem, 3vw, 2.05rem);
    font-weight: 700;
    margin: 0 0 10px 0;
    position: relative;
    z-index: 1;
    color: #FFFFFF;
}
.ghu-greeting-body {
    color: rgba(255, 255, 255, 0.92);
    font-size: 0.98rem;
    line-height: 1.72;
    margin: 0;
    max-width: 720px;
    position: relative;
    z-index: 1;
}

/* --------------------------------------------------------- Vision band --- */
.ghu-vision {
    background: var(--ghu-white);
    border: 1px solid var(--ghu-line);
    border-left: 5px solid var(--ghu-gold);
    border-radius: var(--ghu-radius);
    padding: 30px 34px;
    box-shadow: var(--ghu-shadow);
}
.ghu-vision-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.17em;
    text-transform: uppercase;
    color: var(--ghu-gold);
    margin-bottom: 12px;
}
.ghu-vision-text {
    font-family: 'Fraunces', Georgia, serif;
    font-size: clamp(1.08rem, 1.9vw, 1.34rem);
    line-height: 1.62;
    color: var(--ghu-ink);
    font-weight: 500;
    margin: 0;
}
.ghu-vision-illus {
    width: 100%;
    border-radius: 14px;
    display: block;
    border: 1px solid var(--ghu-line);
}

/* --------------------------------------------------------- Value cards --- */
.ghu-value {
    background: var(--ghu-emerald-050);
    border: 1px solid var(--ghu-emerald-200);
    border-radius: 14px;
    padding: 20px 22px;
    height: 100%;
}
.ghu-value-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.06rem;
    font-weight: 600;
    color: var(--ghu-emerald);
    margin: 0 0 7px 0;
}
.ghu-value-body { color: var(--ghu-muted); font-size: 0.89rem; line-height: 1.62; margin: 0; }

/* -------------------------------------------------------- Quick start --- */
.ghu-qs {
    display: flex;
    gap: 15px;
    align-items: flex-start;
    background: var(--ghu-white);
    border: 1px solid var(--ghu-line);
    border-radius: 14px;
    padding: 17px 19px;
    margin-bottom: 11px;
    box-shadow: 0 1px 2px rgba(18, 33, 28, 0.03);
    transition: transform 0.16s ease, box-shadow 0.16s ease;
}
.ghu-qs:hover {
    transform: translateX(3px);
    box-shadow: 0 6px 18px rgba(18, 33, 28, 0.08);
}
.ghu-qs-num {
    flex: 0 0 34px;
    width: 34px; height: 34px;
    border-radius: 10px;
    background: var(--ghu-emerald);
    color: #FFFFFF;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.92rem;
}
.ghu-qs-text { flex: 1; }
.ghu-qs-title { font-weight: 700; color: var(--ghu-ink); font-size: 0.96rem; margin-bottom: 3px; }
.ghu-qs-body { color: var(--ghu-muted); font-size: 0.885rem; line-height: 1.58; margin: 0; }

/* ------------------------------------------------------------ Faculty --- */
.ghu-fac {
    background: var(--ghu-white);
    border: 1px solid var(--ghu-line);
    border-radius: 18px;
    overflow: hidden;
    box-shadow: var(--ghu-shadow);
    height: 100%;
    display: flex;
    flex-direction: column;
}
.ghu-fac-img { width: 100%; height: 158px; object-fit: cover; display: block; }
.ghu-fac-glyph {
    height: 158px;
    background: linear-gradient(135deg, var(--ghu-emerald-050), var(--ghu-emerald-200));
    display: flex; align-items: center; justify-content: center;
    font-size: 3.4rem;
}
.ghu-fac-body { padding: 24px 26px 26px; display: flex; flex-direction: column; flex: 1; }
.ghu-fac-name {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.34rem;
    font-weight: 700;
    color: var(--ghu-ink);
    margin: 0 0 6px 0;
    letter-spacing: -0.01em;
}
.ghu-fac-tagline {
    color: var(--ghu-emerald-600);
    font-size: 0.895rem;
    font-weight: 600;
    line-height: 1.6;
    margin: 0 0 15px 0;
}
.ghu-meta { display: flex; flex-wrap: wrap; gap: 8px; margin-bottom: 16px; }
.ghu-meta-pill {
    font-size: 0.755rem;
    font-weight: 600;
    color: var(--ghu-emerald);
    background: var(--ghu-emerald-050);
    border: 1px solid var(--ghu-emerald-200);
    padding: 5px 11px;
    border-radius: 999px;
}
.ghu-fac-desc { color: var(--ghu-muted); font-size: 0.9rem; line-height: 1.7; margin: 0 0 18px 0; }
.ghu-mini-label {
    font-size: 0.705rem;
    font-weight: 700;
    letter-spacing: 0.13em;
    text-transform: uppercase;
    color: var(--ghu-gold);
    margin: 0 0 9px 0;
}
.ghu-list { margin: 0 0 18px 0; padding: 0; list-style: none; }
.ghu-list li {
    color: var(--ghu-muted);
    font-size: 0.875rem;
    line-height: 1.55;
    padding: 5px 0 5px 20px;
    position: relative;
}
.ghu-list li::before {
    content: '';
    position: absolute;
    left: 4px; top: 12px;
    width: 6px; height: 6px;
    border-radius: 50%;
    background: var(--ghu-emerald-600);
}
.ghu-skill-row { display: flex; flex-wrap: wrap; gap: 6px; margin-top: auto; }
.ghu-skill {
    font-size: 0.72rem;
    font-weight: 600;
    color: var(--ghu-ink);
    background: var(--ghu-cream);
    border: 1px solid var(--ghu-line);
    padding: 4px 10px;
    border-radius: 7px;
}

/* -------------------------------------------------------------- Steps --- */
.ghu-step {
    background: var(--ghu-white);
    border: 1px solid var(--ghu-line);
    border-left: 4px solid var(--ghu-emerald-600);
    border-radius: 14px;
    padding: 20px 24px;
    margin-bottom: 13px;
    box-shadow: 0 1px 2px rgba(18, 33, 28, 0.04);
}
.ghu-step-head { display: flex; align-items: center; gap: 13px; margin-bottom: 9px; flex-wrap: wrap; }
.ghu-step-num {
    flex: 0 0 32px;
    width: 32px; height: 32px;
    border-radius: 9px;
    background: var(--ghu-gold-050);
    border: 1px solid var(--ghu-gold);
    color: #8A6D0B;
    display: flex; align-items: center; justify-content: center;
    font-weight: 700; font-size: 0.9rem;
}
.ghu-step-title {
    font-family: 'Fraunces', Georgia, serif;
    font-size: 1.09rem;
    font-weight: 600;
    color: var(--ghu-ink);
    margin: 0;
}
.ghu-step-where {
    font-size: 0.745rem;
    font-weight: 600;
    color: var(--ghu-emerald);
    background: var(--ghu-emerald-050);
    border: 1px solid var(--ghu-emerald-200);
    padding: 3px 10px;
    border-radius: 999px;
    margin-left: auto;
}
.ghu-step-time {
    font-size: 0.755rem;
    font-weight: 600;
    color: var(--ghu-muted);
    background: var(--ghu-cream);
    border: 1px solid var(--ghu-line);
    padding: 3px 10px;
    border-radius: 999px;
}
.ghu-step-desc { color: var(--ghu-muted); font-size: 0.905rem; line-height: 1.68; margin: 0 0 9px 0; }
.ghu-step-bring {
    font-size: 0.83rem;
    color: var(--ghu-ink);
    background: var(--ghu-gold-050);
    border-radius: 9px;
    padding: 9px 13px;
    line-height: 1.55;
}

/* ------------------------------------------------------------ Contact --- */
.ghu-primary-contact {
    background: linear-gradient(135deg, var(--ghu-emerald) 0%, #0B4A3B 100%);
    border-radius: var(--ghu-radius);
    padding: 30px 34px;
    color: #FFFFFF;
    box-shadow: 0 14px 36px rgba(15, 92, 74, 0.24);
    margin-bottom: 8px;
}
.ghu-pc-label {
    font-size: 0.72rem;
    font-weight: 700;
    letter-spacing: 0.17em;
    text-transform: uppercase;
    color: var(--ghu-gold);
    margin-bottom: 10px;
}
.ghu-pc-email {
    font-family: 'Fraunces', Georgia, serif;
    font-size: clamp(1.05rem, 2.3vw, 1.62rem);
    font-weight: 700;
    margin: 0 0 14px 0;
    word-break: break-all;
}
.ghu-pc-email a { color: #FFFFFF !important; text-decoration: none; border-bottom: 2px solid rgba(201, 162, 39, 0.6); }
.ghu-pc-email a:hover { border-bottom-color: var(--ghu-gold); }
.ghu-pc-meta { color: rgba(255, 255, 255, 0.85); font-size: 0.875rem; line-height: 1.72; margin: 0; }

.ghu-btn-primary {
    display: inline-block;
    background: var(--ghu-gold);
    color: #2A2205 !important;
    font-weight: 700;
    font-size: 0.93rem;
    padding: 13px 26px;
    border-radius: 11px;
    text-decoration: none !important;
    box-shadow: 0 5px 16px rgba(201, 162, 39, 0.34);
    transition: transform 0.15s ease, box-shadow 0.15s ease;
    border: none;
}
.ghu-btn-primary:hover { transform: translateY(-2px); box-shadow: 0 9px 24px rgba(201, 162, 39, 0.42); }
.ghu-btn-ghost {
    display: inline-block;
    background: var(--ghu-white);
    color: var(--ghu-emerald) !important;
    font-weight: 600;
    font-size: 0.87rem;
    padding: 10px 18px;
    border: 1px solid var(--ghu-emerald-200);
    border-radius: 10px;
    text-decoration: none !important;
    transition: all 0.15s ease;
}
.ghu-btn-ghost:hover { background: var(--ghu-emerald-050); border-color: var(--ghu-emerald-600); }

.ghu-preview {
    background: var(--ghu-cream);
    border: 1px dashed var(--ghu-line);
    border-radius: 12px;
    padding: 16px 18px;
    font-family: 'SFMono-Regular', Menlo, Consolas, monospace;
    font-size: 0.795rem;
    line-height: 1.62;
    color: var(--ghu-muted);
    white-space: pre-wrap;
    word-break: break-word;
    max-height: 250px;
    overflow-y: auto;
}
.ghu-preview-subject { color: var(--ghu-ink); font-weight: 700; margin-bottom: 8px; }

.ghu-dept {
    background: var(--ghu-white);
    border: 1px solid var(--ghu-line);
    border-radius: 13px;
    padding: 17px 19px;
    margin-bottom: 10px;
    display: flex;
    gap: 14px;
    align-items: flex-start;
}
.ghu-dept-icon {
    flex: 0 0 38px; width: 38px; height: 38px;
    border-radius: 10px;
    background: var(--ghu-emerald-050);
    border: 1px solid var(--ghu-emerald-200);
    display: flex; align-items: center; justify-content: center;
    font-size: 1.16rem;
}
.ghu-dept-name { font-weight: 700; color: var(--ghu-ink); font-size: 0.94rem; margin-bottom: 3px; }
.ghu-dept-role { color: var(--ghu-muted); font-size: 0.845rem; line-height: 1.55; margin: 0; }
.ghu-dept-mail { font-size: 0.815rem; margin-top: 5px; }
.ghu-dept-mail a { color: var(--ghu-emerald-600) !important; font-weight: 600; text-decoration: none; }
.ghu-dept-mail a:hover { text-decoration: underline; }

/* -------------------------------------------------------------- Footer --- */
.ghu-footer {
    margin-top: 40px;
    padding: 26px 30px;
    background: var(--ghu-white);
    border: 1px solid var(--ghu-line);
    border-radius: var(--ghu-radius);
    display: flex;
    flex-wrap: wrap;
    gap: 18px;
    align-items: center;
    justify-content: space-between;
}
.ghu-footer-brand { display: flex; align-items: center; gap: 14px; }
.ghu-footer-crest { width: 52px; height: 52px; border-radius: 11px; object-fit: cover; border: 1px solid var(--ghu-line); }
.ghu-footer-name { font-family: 'Fraunces', Georgia, serif; font-weight: 700; color: var(--ghu-ink); font-size: 1.02rem; }
.ghu-footer-sub { color: var(--ghu-muted); font-size: 0.815rem; }
.ghu-footer-contact { text-align: right; }
.ghu-footer-mail a { color: var(--ghu-emerald) !important; font-weight: 700; font-size: 0.925rem; text-decoration: none; }
.ghu-footer-mail a:hover { text-decoration: underline; }
.ghu-footer-note { color: var(--ghu-muted); font-size: 0.775rem; margin-top: 4px; }

/* --------------------------------------------------- Streamlit widgets --- */
.stTextInput input, .stTextArea textarea, .stSelectbox div[data-baseweb="select"] > div {
    border-radius: 10px !important;
    border-color: var(--ghu-line) !important;
    font-family: 'Plus Jakarta Sans', sans-serif !important;
    font-size: 0.925rem !important;
}
.stTextInput input:focus, .stTextArea textarea:focus {
    border-color: var(--ghu-emerald-600) !important;
    box-shadow: 0 0 0 3px rgba(20, 121, 95, 0.13) !important;
}
.stTextInput label, .stTextArea label, .stSelectbox label {
    font-weight: 600 !important;
    font-size: 0.855rem !important;
    color: var(--ghu-ink) !important;
}
hr { border-color: var(--ghu-line); }
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ---------------------------------------------------------------------------
# Session state.
# ---------------------------------------------------------------------------


def init_state() -> None:
    """Initialise every session-state key the application relies on.

    Seeding the keys before any widget is instantiated means the profile fields
    and the contact form survive tab switches and full page reloads within the
    same browser session.
    """
    defaults = {
        "student_name": "",
        "form_name": "",
        "form_subject": INQUIRY_TEMPLATES["General enquiry"]["subject"],
        "form_message": INQUIRY_TEMPLATES["General enquiry"]["body"].format(name="[your name]"),
        "inquiry_template": "General enquiry",
    }
    for key, value in defaults.items():
        if key not in st.session_state:
            st.session_state[key] = value


def display_name() -> str:
    """Return the student's name, falling back to a warm generic greeting."""
    return st.session_state.get("student_name", "").strip()


def apply_template() -> None:
    """Callback: refill the contact form fields from the selected template.

    Runs on both the inquiry-type change and the form submit, so it always
    re-renders the draft against the name currently typed in the form.
    """
    template = INQUIRY_TEMPLATES[st.session_state["inquiry_template"]]
    typed = st.session_state.get("form_name", "").strip()
    if typed:
        # Keep the Welcome Hub greeting in step with the form field.
        st.session_state["student_name"] = typed
    name = typed or display_name() or "[your name]"
    st.session_state["form_subject"] = template["subject"]
    st.session_state["form_message"] = template["body"].format(name=name)


init_state()

# ---------------------------------------------------------------------------
# Shared UI fragments.
# ---------------------------------------------------------------------------


def section_header(eyebrow: str, title: str, subtitle: str = "") -> None:
    """Render a consistent section heading band."""
    subtitle_html = f'<p class="ghu-section-sub">{subtitle}</p>' if subtitle else ""
    st.markdown(
        f'<div class="ghu-section-eyebrow">{eyebrow}</div>'
        f'<h2 class="ghu-section-title">{title}</h2>'
        f"{subtitle_html}",
        unsafe_allow_html=True,
    )


def render_footer() -> None:
    """Render the campus contact footer shown at the foot of every tab."""
    crest = asset_tag(CREST_IMAGE, "Green Hope University crest", "ghu-footer-crest")
    st.markdown(
        '<div class="ghu-footer">'
        '  <div class="ghu-footer-brand">'
        f"    {crest}"
        "    <div>"
        f'      <div class="ghu-footer-name">{UNIVERSITY}</div>'
        f'      <div class="ghu-footer-sub">{CAMPUS} · {CAMPUS_ADDRESS}</div>'
        "    </div>"
        "  </div>"
        '  <div class="ghu-footer-contact">'
        f'    <div class="ghu-footer-mail"><a href="mailto:{CAMPUS_EMAIL}">{CAMPUS_EMAIL}</a></div>'
        f'    <div class="ghu-footer-note">{OFFICE_HOURS}</div>'
        "  </div>"
        "</div>",
        unsafe_allow_html=True,
    )


# ---------------------------------------------------------------------------
# Tab 1 — Welcome Hub.
# ---------------------------------------------------------------------------


def render_hero() -> None:
    """Render the campus hero banner."""
    hero_uri = _data_uri(HERO_IMAGE)
    background = f"background-image: url('{hero_uri}');" if hero_uri else "background: linear-gradient(135deg,#0F5C4A,#0A3F33);"
    st.markdown(
        f'<div class="ghu-hero" style="{background}">'
        '  <div class="ghu-hero-inner">'
        '    <span class="ghu-eyebrow">Puntland · Somalia</span>'
        f'    <h1 class="ghu-hero-title">{UNIVERSITY}</h1>'
        f'    <div class="ghu-hero-campus">{CAMPUS}</div>'
        '    <p class="ghu-hero-sub">Welcome to your new academic home. This portal guides every '
        "freshman through arrival, registration and orientation week — everything you need to "
        "begin your studies with confidence.</p>"
        '    <div class="ghu-chips">'
        '      <span class="ghu-chip">🎓 3 Faculties</span>'
        '      <span class="ghu-chip">📚 4-Year Programmes</span>'
        '      <span class="ghu-chip">🌍 English Medium</span>'
        '      <span class="ghu-chip">🤝 Student Support</span>'
        "    </div>"
        "  </div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_greeting() -> None:
    """Render the personalised greeting card."""
    name = display_name()
    if name:
        heading = f"Welcome, {name}! 🎉"
        body = (
            f"We are delighted that you have chosen <strong>{UNIVERSITY}</strong> for your studies "
            f"at our {CAMPUS}. You are now part of a community of scholars, innovators and future "
            "leaders. Begin with the quick-start guide below, then explore your faculty and reach out "
            "to any campus department whenever you need help — we are here for you."
        )
    else:
        heading = "Welcome, future graduate! 🎉"
        body = (
            f"We are delighted that you have chosen <strong>{UNIVERSITY}</strong> for your studies "
            f"at our {CAMPUS}. Enter your name below to personalise this portal, then work through the "
            "quick-start guide, explore your faculty and contact any campus department — we are here for you."
        )
    st.markdown(
        '<div class="ghu-greeting">'
        f'  <div class="ghu-greeting-name">{heading}</div>'
        f'  <p class="ghu-greeting-body">{body}</p>'
        "</div>",
        unsafe_allow_html=True,
    )


def render_name_input() -> None:
    """Personalisation control driving the greeting across the portal."""
    left, right = st.columns([2, 1])
    with left:
        st.text_input(
            "Your full name",
            key="student_name",
            placeholder="e.g. Ayaan Cabdi Warsame",
            help="Your name personalises the welcome message and pre-fills the contact form.",
        )
    with right:
        st.markdown(
            '<div style="height: 29px;"></div>'
            '<div style="color:#5C6B66; font-size:0.815rem; line-height:1.5; padding-top:2px;">'
            "Your name is stored only in this browser session and is never sent anywhere automatically."
            "</div>",
            unsafe_allow_html=True,
        )


def render_vision() -> None:
    """Render the vision statement alongside the learning illustration."""
    left, right = st.columns([1.35, 1])
    with left:
        st.markdown(
            '<div class="ghu-vision">'
            '  <div class="ghu-vision-label">Our Vision</div>'
            f'  <p class="ghu-vision-text">{VISION_STATEMENT}</p>'
            "</div>",
            unsafe_allow_html=True,
        )
    with right:
        illustration = asset_tag(VISION_IMAGE, "Students learning at Green Hope University", "ghu-vision-illus")
        if illustration:
            st.markdown(illustration, unsafe_allow_html=True)


def render_values() -> None:
    """Render the mission statement and core values."""
    st.markdown("<div style='height: 22px;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="ghu-card ghu-card-accent">'
        '  <div class="ghu-card-title">Our Mission</div>'
        f'  <p class="ghu-card-body">{MISSION_STATEMENT}</p>'
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown("<div style='height: 16px;'></div>", unsafe_allow_html=True)
    columns = st.columns(3)
    for column, (title, body) in zip(columns, CORE_VALUES):
        with column:
            st.markdown(
                '<div class="ghu-value">'
                f'  <div class="ghu-value-title">{title}</div>'
                f'  <p class="ghu-value-body">{body}</p>'
                "</div>",
                unsafe_allow_html=True,
            )


QUICK_START = [
    ("Collect your documents", "Bring your secondary school certificate, national ID and four passport photographs."),
    ("Report to Admissions", "Visit the Admissions & Registrar office on day one to confirm your admission letter."),
    ("Settle your fees", "Pay tuition and registration fees at the Finance office and keep your official receipt."),
    ("Get your student ID", "Collect your campus ID card from Student Affairs — you need it for exams and the library."),
    ("Activate your accounts", "Set up your student email and portal login with IT Support in your first week."),
    ("Attend orientation", "Join orientation week, meet your advisor and sign the student handbook acknowledgment."),
]


def render_quick_start() -> None:
    """Render the freshman quick-start guide."""
    left, right = st.columns([1, 1.12])
    with left:
        section_header(
            "Freshman Quick-Start",
            "Your first week, step by step",
            "Follow these six steps during your first days on campus. The full registration and "
            "orientation walkthrough lives in the Contact & Registration tab.",
        )
        for index, (title, body) in enumerate(QUICK_START, start=1):
            st.markdown(
                '<div class="ghu-qs">'
                f'  <div class="ghu-qs-num">{index}</div>'
                '  <div class="ghu-qs-text">'
                f'    <div class="ghu-qs-title">{title}</div>'
                f'    <p class="ghu-qs-body">{body}</p>'
                "  </div>"
                "</div>",
                unsafe_allow_html=True,
            )
    with right:
        st.markdown("<div style='height: 58px;'></div>", unsafe_allow_html=True)
        st.markdown(
            '<div class="ghu-card ghu-card-gold">'
            '  <div class="ghu-card-title">Campus at a glance</div>'
            '  <p class="ghu-card-body">'
            f"    <strong>Campus:</strong> {CAMPUS}<br>"
            f"    <strong>Address:</strong> {CAMPUS_ADDRESS}<br>"
            f"    <strong>Office hours:</strong> {OFFICE_HOURS}<br>"
            f"    <strong>Orientation window:</strong> Orientation week immediately precedes the "
            "start of the semester; attendance is compulsory.<br><br>"
            "    Wherever you are unsure, write to the campus office — every enquiry is answered "
            "within two working days."
            "  </p>"
            "</div>",
            unsafe_allow_html=True,
        )
        st.markdown("<div style='height: 14px;'></div>", unsafe_allow_html=True)
        st.markdown(
            f'<a class="ghu-btn-primary" href="mailto:{CAMPUS_EMAIL}">✉️ Email the campus office</a>',
            unsafe_allow_html=True,
        )


def render_welcome_tab() -> None:
    """Tab 1: Welcome Hub."""
    render_hero()
    render_greeting()
    st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)
    render_name_input()
    st.markdown("<div style='height: 8px;'></div>", unsafe_allow_html=True)
    render_vision()
    render_values()
    st.markdown("<div style='height: 34px;'></div>", unsafe_allow_html=True)
    render_quick_start()
    render_footer()


# ---------------------------------------------------------------------------
# Tab 2 — Academic Faculties.
# ---------------------------------------------------------------------------


def render_faculty_card(faculty: dict) -> None:
    """Render a single faculty card with its programmes, careers and duration."""
    visual = asset_tag(faculty["visual"], f"{faculty['name']} illustration", "ghu-fac-img")
    if not visual:
        visual = f'<div class="ghu-fac-glyph">{faculty["glyph"]}</div>'

    courses = "".join(f"<li>{course}</li>" for course in faculty["courses"])
    careers = "".join(f"<li>{career}</li>" for career in faculty["careers"])
    skills = "".join(f'<span class="ghu-skill">{skill}</span>' for skill in faculty["skills"])

    st.markdown(
        '<div class="ghu-fac">'
        f"  {visual}"
        '  <div class="ghu-fac-body">'
        f'    <h3 class="ghu-fac-name">{faculty["name"]}</h3>'
        f'    <p class="ghu-fac-tagline">{faculty["tagline"]}</p>'
        '    <div class="ghu-meta">'
        f'      <span class="ghu-meta-pill">{faculty["degree"]}</span>'
        f'      <span class="ghu-meta-pill">{faculty["duration"]}</span>'
        f'      <span class="ghu-meta-pill">{faculty["credits"]}</span>'
        "    </div>"
        f'    <p class="ghu-fac-desc">{faculty["description"]}</p>'
        '    <div class="ghu-mini-label">Key Courses</div>'
        f'    <ul class="ghu-list">{courses}</ul>'
        '    <div class="ghu-mini-label">Career Pathways</div>'
        f'    <ul class="ghu-list">{careers}</ul>'
        '    <div class="ghu-mini-label">Core Skills</div>'
        f'    <div class="ghu-skill-row">{skills}</div>'
        "  </div>"
        "</div>",
        unsafe_allow_html=True,
    )


def render_faculties_tab() -> None:
    """Tab 2: Academic Faculties."""
    section_header(
        "Academic Programmes",
        "Our Faculties",
        "Three career-focused faculties, each delivered over four years of full-time study in English. "
        "Every programme combines strong theoretical foundations with laboratory work, team projects "
        "and a final-year capstone delivered with a real partner organisation.",
    )

    for faculty in FACULTIES:
        render_faculty_card(faculty)
        st.markdown("<div style='height: 20px;'></div>", unsafe_allow_html=True)

    st.markdown("<div style='height: 6px;'></div>", unsafe_allow_html=True)
    st.markdown(
        '<div class="ghu-card ghu-card-accent">'
        '  <div class="ghu-card-title">Admission requirements</div>'
        '  <p class="ghu-card-body">'
        "    A completed secondary school certificate with passes in English and Mathematics is required "
        "for all three faculties. Applicants to Health Sciences should also hold a pass in Biology or "
        "Chemistry. All instruction is delivered in English, and a placement assessment is offered during "
        "orientation week for students who wish to strengthen their academic writing and numeracy skills."
        "  </p>"
        "</div>",
        unsafe_allow_html=True,
    )
    render_footer()


# ---------------------------------------------------------------------------
# Tab 3 — Contact & Registration.
# ---------------------------------------------------------------------------


def render_orientation_steps() -> None:
    """Render the numbered registration and orientation walkthrough."""
    section_header(
        "Registration & Orientation Guide",
        "Your step-by-step campus journey",
        "Complete these ten steps to finish your enrolment and begin classes. Steps 1–4 should be "
        "completed in your first two days on campus; the remainder can be spread across orientation week.",
    )

    for step in ORIENTATION_STEPS:
        st.markdown(
            '<div class="ghu-step">'
            '  <div class="ghu-step-head">'
            f'    <div class="ghu-step-num">{step["n"]}</div>'
            f'    <h4 class="ghu-step-title">{step["title"]}</h4>'
            f'    <span class="ghu-step-where">{step["where"]}</span>'
            f'    <span class="ghu-step-time">{step["time"]}</span>'
            "  </div>"
            f'  <p class="ghu-step-desc">{step["desc"]}</p>'
            f'  <div class="ghu-step-bring"><strong>Bring:</strong> {step["bring"]}</div>'
            "</div>",
            unsafe_allow_html=True,
        )


DEPARTMENTS = [
    ("📋", "Admissions & Registrar", "Admission confirmations, document verification and official registration."),
    ("💰", "Finance / Bursar", "Tuition, registration fees, instalment plans and official receipts."),
    ("🤝", "Student Affairs", "Student ID cards, orientation week, clubs and code-of-conduct matters."),
    ("🧭", "Academic Advising", "Course selection, credit loads, prerequisites and degree pathway planning."),
    ("📖", "Library", "Borrowing cards, the digital catalogue and access to electronic resources."),
    ("🖥️", "IT Support", "Student email, portal login, password resets and campus network access."),
    ("🩺", "Health Center", "Health screening, medical records and on-campus first aid."),
    ("🏠", "Hostel / Welfare", "Accommodation allocation, boarding and student welfare support."),
    ("💼", "Career Services", "Internships, graduate placements, CV support and employer links."),
]


def render_departments() -> None:
    """Render the compact campus department directory."""
    st.markdown(
        '<div style="font-size:0.72rem; font-weight:700; letter-spacing:0.16em; '
        'text-transform:uppercase; color:#14795F; margin-bottom:12px;">Campus Departments</div>',
        unsafe_allow_html=True,
    )
    for icon, name, description in DEPARTMENTS:
        st.markdown(
            '<div class="ghu-dept">'
            f'  <div class="ghu-dept-icon">{icon}</div>'
            "  <div>"
            f'    <div class="ghu-dept-name">{name}</div>'
            f'    <p class="ghu-dept-role">{description}</p>'
            f'    <div class="ghu-dept-mail"><a href="mailto:{CAMPUS_EMAIL}">{CAMPUS_EMAIL}</a></div>'
            "  </div>"
            "</div>",
            unsafe_allow_html=True,
        )


def render_contact_form() -> None:
    """Render the interactive contact form that builds a pre-filled mailto link."""
    st.markdown(
        '<div style="font-size:0.72rem; font-weight:700; letter-spacing:0.16em; '
        'text-transform:uppercase; color:#14795F; margin-bottom:12px;">Send an Enquiry</div>',
        unsafe_allow_html=True,
    )

    st.selectbox(
        "Inquiry type (pre-fills the message)",
        options=list(INQUIRY_TEMPLATES.keys()),
        key="inquiry_template",
        on_change=apply_template,
        help="Choosing a template fills the subject and message with a ready-to-send draft.",
    )

    with st.form("contact_form", clear_on_submit=False):
        left, right = st.columns(2)
        with left:
            # Uses its own key: a widget key must be unique across the whole
            # script, and the Welcome Hub already owns "student_name".
            st.text_input(
                "Your full name",
                key="form_name",
                placeholder="e.g. Ayaan Cabdi Warsame",
            )
            st.text_input("Your email address", placeholder="you@example.com")
        with right:
            st.text_input("Phone number (optional)", placeholder="+252 ...")
            st.selectbox(
                "Faculty of interest",
                options=["Not sure yet"] + [faculty["name"] for faculty in FACULTIES],
            )

        st.text_input("Subject", key="form_subject")
        st.text_area("Message", key="form_message", height=230)

        st.form_submit_button(
            "Prepare email draft",
            on_click=apply_template,
            use_container_width=False,
        )

    name = display_name() or "[your name]"
    subject = st.session_state.get("form_subject", "")
    body = st.session_state.get("form_message", "")
    mailto = build_mailto(subject, body)

    st.markdown(
        f'<a class="ghu-btn-primary" href="{mailto}">✉️ Open in your email client</a>',
        unsafe_allow_html=True,
    )
    st.markdown(
        '<div style="color:#5C6B66; font-size:0.8rem; margin-top:10px; line-height:1.6;">'
        f"The button opens your email application addressed to <strong>{CAMPUS_EMAIL}</strong> with the "
        "subject and message above already filled in. Nothing is sent until you press send there."
        "</div>",
        unsafe_allow_html=True,
    )

    with st.expander("Preview the draft email"):
        st.markdown(
            '<div class="ghu-preview">'
            f'<div class="ghu-preview-subject">Subject: {subject}</div>'
            f"{body}"
            "</div>",
            unsafe_allow_html=True,
        )
        st.caption(f"Recipient: {CAMPUS_EMAIL}")
        st.caption(f"Prepared for: {name}")


def render_contact_tab() -> None:
    """Tab 3: Contact & Registration."""
    st.markdown(
        '<div class="ghu-primary-contact">'
        '  <div class="ghu-pc-label">Primary Campus Contact</div>'
        f'  <div class="ghu-pc-email"><a href="mailto:{CAMPUS_EMAIL}">{CAMPUS_EMAIL}</a></div>'
        '  <p class="ghu-pc-meta">'
        f"    {UNIVERSITY} · {CAMPUS}<br>"
        f"    {CAMPUS_ADDRESS}<br>"
        f"    {CAMPUS_PHONE} · {OFFICE_HOURS}"
        "  </p>"
        "</div>",
        unsafe_allow_html=True,
    )
    st.markdown(
        f'<div style="margin: 14px 0 30px 0;">'
        f'<a class="ghu-btn-ghost" href="mailto:{CAMPUS_EMAIL}?subject=Freshman%20enquiry%20—%20Garowe%20Campus">'
        "✉️ Quick email to the campus office</a></div>",
        unsafe_allow_html=True,
    )

    render_orientation_steps()

    st.markdown("<div style='height: 34px;'></div>", unsafe_allow_html=True)
    left, right = st.columns([1, 1.18])
    with left:
        render_departments()
    with right:
        render_contact_form()

    render_footer()


# ---------------------------------------------------------------------------
# Application entry point.
# ---------------------------------------------------------------------------


def main() -> None:
    """Assemble the three tabs and hand control to Streamlit."""
    welcome_tab, faculties_tab, contact_tab = st.tabs(
        ["🏠  Welcome Hub", "🎓  Academic Faculties", "📬  Contact & Registration"]
    )

    with welcome_tab:
        render_welcome_tab()

    with faculties_tab:
        render_faculties_tab()

    with contact_tab:
        render_contact_tab()


if __name__ == "__main__":
    main()
