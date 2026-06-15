<![CDATA[<div align="center">

# 🔥 CareerForge AI

### AI-Powered Resume Intelligence & Career Coaching Platform

[![Python](https://img.shields.io/badge/Python-3.10+-3776AB?style=for-the-badge&logo=python&logoColor=white)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-FF4B4B?style=for-the-badge&logo=streamlit&logoColor=white)](https://streamlit.io)
[![Google Gemini](https://img.shields.io/badge/Google_Gemini-2.5-4285F4?style=for-the-badge&logo=google&logoColor=white)](https://ai.google.dev)
[![LangChain](https://img.shields.io/badge/LangChain-0.2+-1C3C3C?style=for-the-badge&logo=langchain&logoColor=white)](https://langchain.com)

**Analyze resumes · Optimize ATS scores · Simulate interviews · Generate cover letters · Build LinkedIn profiles · Get salary insights**

---

</div>

## 📸 Screenshots

### 🏠 Landing Page & Dashboard — Premium Dark Glassmorphism UI
<p align="center">
  <img src="screenshots/1.png" alt="CareerForge AI Landing Page & Dashboard" width="100%"/>
</p>

> Deep navy-to-indigo gradient background with glassmorphism cards, sidebar navigation, and interactive resume analytics dashboard.

---

### 📊 Resume Analysis & Career Insights
<p align="center">
  <img src="screenshots/2.png" alt="Resume Analysis & Career Insights" width="100%"/>
</p>

> AI-driven ATS matching score, skill extraction, and multi-dimensional analysis with real-time feedback.

---

## 📋 Table of Contents

- [Screenshots](#-screenshots)
- [Overview](#-overview)
- [Features](#-features)
- [Tech Stack](#-tech-stack)
- [Getting Started](#-getting-started)
- [Project Structure](#-project-structure)
- [Usage Guide](#-usage-guide)
- [Configuration](#-configuration)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🧠 Overview

**CareerForge AI** is a comprehensive, AI-powered career intelligence platform that goes far beyond basic resume screening. Built with Google Gemini and LangChain, it provides **7 integrated modules** that help job seekers optimize their resumes, prepare for interviews, craft cover letters, and navigate salary negotiations — all from a single, stunning interface.

Unlike simple ATS checkers, CareerForge AI uses structured output parsing with Pydantic schemas to deliver **consistent, actionable, and deeply personalized** career guidance powered by large language models.

### 🎨 Design Philosophy
- **Dark Glassmorphism** — Frosted glass panels with `backdrop-filter: blur(20px)`
- **Neon Purple Accents** — Ambient glow effects inspired by Linear & Stripe
- **Premium Typography** — Inter + Outfit from Google Fonts
- **Micro-Animations** — Hover lifts, scale transforms, gradient shifts
- **Enterprise-Grade UI** — Behance/Dribbble quality, Apple-level attention to detail

---

## ✨ Features

### 📊 1. Resume Analysis & ATS Match
- **Multi-dimensional scoring** with interactive Plotly radar chart
- Scores across 6 axes: Technical Match, Soft Skills, Formatting, Action Verbs, Metrics Usage, ATS Friendliness
- Extracts technical and soft skills as animated pill tags
- Identifies critical skill gaps vs. the job description
- Provides actionable ATS optimization suggestions

### ✍️ 2. AI Resume Rewriter
- Rewrites every experience bullet with **strong action verbs** and **quantified metrics**
- Generates a tailored professional summary statement
- Lists specific improvements made (before vs. after)
- One-click download of rewritten resume

### 💬 3. Interactive Mock Interview
- Generates **5 custom interview questions** (2 technical, 2 behavioral/STAR, 1 project-specific)
- Real-time chat interface with progress tracking
- Option to end early and evaluate partial responses
- Restart capability for multiple practice sessions

### 📈 4. Interview Performance Report
- **Overall score (0–100)** with color-coded feedback
- Strengths and areas for improvement breakdown
- Question-by-question evaluation with individual scores
- **Model answers** using the STAR framework for every question
- Downloadable detailed feedback report (.md)

### 📝 5. Cover Letter Generator
- **3 tone options**: Formal & Professional, Enthusiastic & Energetic, Concise & Direct
- Structured output: Subject line, Opening, 2 Body paragraphs, Closing
- Directly references JD requirements and resume achievements
- Downloadable as plain text

### 🔗 6. LinkedIn Profile Optimizer
- Generates **SEO-optimized headline** (max 220 chars)
- Writes a compelling **About section** (300–400 words)
- Suggests **10–15 skill keywords** for maximum searchability
- Provides **Featured section ideas** (projects, articles, certifications)
- Downloadable LinkedIn content bundle

### 💰 7. Salary & Career Intelligence (3 Sub-modules)

| Sub-module | What it does |
|------------|-------------|
| **💵 Salary Insights** | Location-aware salary range, market demand, high-value skills, negotiation tips |
| **🧭 Career Roadmap** | AI strategy summary, target roles, upskilling steps, certifications |
| **🧑‍💼 Professional Persona** | Archetype identification, communication style, interview positioning tips |

---

## 🛠 Tech Stack

| Layer | Technology |
|-------|-----------|
| **Frontend** | Streamlit 1.35+ with 400+ lines of custom CSS (glassmorphism, neon glows, animations) |
| **AI Engine** | Google Gemini 2.5 (Flash / Pro) via LangChain |
| **Structured Output** | Pydantic v2 schemas with `with_structured_output()` |
| **Charts** | Plotly (radar charts) |
| **Document Parsing** | PyPDF, docx2txt |
| **Typography** | Google Fonts (Outfit, Inter, JetBrains Mono) |
| **Environment** | python-dotenv for API key management |

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.10+** installed
- A **Google Gemini API Key** — get one free at [Google AI Studio](https://aistudio.google.com/apikey)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/resumeanalyzer.git
   cd resumeanalyzer
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv

   # Windows
   .\venv\Scripts\activate

   # macOS / Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up your API key**
   ```bash
   cp .env.example .env
   ```
   Edit `.env` and add your Gemini API key:
   ```
   GOOGLE_API_KEY=your_api_key_here
   ```

5. **Run the application**
   ```bash
   streamlit run app.py
   ```

6. Open your browser at **http://localhost:8501** 🎉

---

## 📁 Project Structure

```
resumeanalyzer/
├── app.py                  # Main Streamlit application (7 tabs, premium UI)
├── requirements.txt        # Python dependencies
├── .env                    # API keys (git-ignored)
├── .env.example            # Template for environment variables
├── .gitignore              # Git ignore rules
├── README.md               # This file
│
├── utils/
│   ├── __init__.py         # Package initializer
│   ├── analyzer.py         # Resume analysis & career guidance (Pydantic + LangChain)
│   ├── interview.py        # Mock interview generation & evaluation
│   ├── parser.py           # PDF, DOCX, TXT resume parsing
│   └── rewriter.py         # Resume rewriter, cover letter, LinkedIn, salary, persona
│
├── samples/
│   ├── resume_swe.txt      # Sample Software Engineer resume
│   ├── jd_swe.txt          # Sample Software Engineer job description
│   ├── resume_pm.txt       # Sample Product Manager resume
│   └── jd_pm.txt           # Sample Product Manager job description
│
├── screenshots/            # App screenshots for README
│   ├── 1.png
│   └── 2.png
│
└── venv/                   # Virtual environment (git-ignored)
```

---

## 📖 Usage Guide

### Quick Start (with Sample Data)
1. Launch the app with `streamlit run app.py`
2. In the sidebar, select **"Software Engineer Sample"** or **"Product Manager Sample"**
3. Click **🚀 Analyze Resume** in the first tab
4. Explore all 7 tabs!

### With Your Own Resume
1. Select **"Custom Upload / Paste"** in the sidebar
2. Upload your resume (PDF, DOCX, or TXT)
3. Paste the target job description
4. Use any of the 7 modules

### Recommended Workflow
```
Resume Analysis → Resume Rewriter → Cover Letter → LinkedIn Optimizer → Mock Interview → Salary Insights
```

---

## ⚙️ Configuration

### API Key
Set your Google Gemini API key in one of two ways:
- **`.env` file** (recommended): Add `GOOGLE_API_KEY=your_key` to `.env`
- **Sidebar input**: Paste it directly in the app's sidebar

### Model Selection
| Model | Best For |
|-------|----------|
| `gemini-2.5-flash` | Fast responses, general use (recommended) |
| `gemini-2.5-pro` | Deeper analysis, complex evaluations |

---

## 📦 Sample Data

The `samples/` directory includes pre-built resume and job description pairs for quick testing:

| Sample | Resume | Job Description |
|--------|--------|----------------|
| Software Engineer | `resume_swe.txt` | `jd_swe.txt` |
| Product Manager | `resume_pm.txt` | `jd_pm.txt` |

---

## 🤝 Contributing

Contributions are welcome! Here's how:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Commit your changes (`git commit -m 'Add amazing feature'`)
4. Push to the branch (`git push origin feature/amazing-feature`)
5. Open a Pull Request

---

## 📄 License

This project is open source and available under the [MIT License](LICENSE).

---

<div align="center">

**Built with ❤️ using Google Gemini & Streamlit**

⭐ Star this repo if you found it useful!

</div>
]]>
