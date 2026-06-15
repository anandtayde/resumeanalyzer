from typing import List
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from utils.analyzer import get_llm


# ─── Pydantic Schemas ──────────────────────────────────────────────────────────

class RewrittenResume(BaseModel):
    rewritten_bullets: List[str] = Field(
        ...,
        description=(
            "A list of powerful, ATS-optimized bullet points that completely rewrite "
            "the candidate's experience and achievements. Each bullet must start with a "
            "strong action verb and include quantified metrics where possible."
        )
    )
    summary_statement: str = Field(
        ...,
        description=(
            "A compelling 3-4 sentence professional summary optimized for the target role, "
            "incorporating key JD keywords naturally."
        )
    )
    key_improvements: List[str] = Field(
        ...,
        description="A brief list of what was specifically improved in the rewrite (e.g., added metrics, stronger verbs)."
    )


class CoverLetter(BaseModel):
    subject_line: str = Field(
        ...,
        description="A compelling email subject line for the cover letter (e.g., 'Experienced SWE | React & Node.js Expert | Application for Senior Engineer')."
    )
    opening_paragraph: str = Field(
        ...,
        description="A strong opening paragraph (2-3 sentences) that hooks the reader, states the target role, and highlights the most relevant credential."
    )
    body_paragraph_1: str = Field(
        ...,
        description="First body paragraph (3-4 sentences) highlighting 2-3 specific technical achievements from the resume that directly match the JD requirements."
    )
    body_paragraph_2: str = Field(
        ...,
        description="Second body paragraph (3-4 sentences) addressing cultural fit, soft skills, and why the candidate is excited about this specific company/role."
    )
    closing_paragraph: str = Field(
        ...,
        description="A confident closing paragraph (2-3 sentences) with a clear call-to-action and professional sign-off."
    )


class LinkedInProfile(BaseModel):
    headline: str = Field(
        ...,
        description=(
            "An optimized LinkedIn headline (max 220 chars) following the pattern: "
            "'[Title] | [Top Skill 1] · [Top Skill 2] | [Value Proposition or Achievement]'. "
            "Rich in keywords for discoverability."
        )
    )
    about_summary: str = Field(
        ...,
        description=(
            "A compelling LinkedIn 'About' section (300-400 words). Start with a hook, "
            "cover expertise and career journey, highlight 2-3 key achievements with metrics, "
            "mention what you're looking for, and end with a call-to-action."
        )
    )
    skills_to_add: List[str] = Field(
        ...,
        description="A list of 10-15 specific skill keywords to add to LinkedIn Skills section for maximum searchability."
    )
    featured_section_ideas: List[str] = Field(
        ...,
        description="3-5 ideas for what to feature in the LinkedIn 'Featured' section (e.g., project links, articles, certifications)."
    )


class SalaryInsight(BaseModel):
    estimated_range_low: int = Field(
        ...,
        description="Conservative low-end salary estimate in USD per year based on the candidate's skills and the target role."
    )
    estimated_range_high: int = Field(
        ...,
        description="Optimistic high-end salary estimate in USD per year based on the candidate's skills and the target role."
    )
    market_demand: str = Field(
        ...,
        description="One of: 'Very High Demand', 'High Demand', 'Moderate Demand', 'Lower Demand' — based on the skills and role."
    )
    negotiation_tips: List[str] = Field(
        ...,
        description="3-5 specific, actionable salary negotiation tips personalized to this candidate's profile and skills."
    )
    in_demand_skills_you_have: List[str] = Field(
        ...,
        description="Skills from the resume that are currently high-value in the market and justify the higher salary range."
    )
    skills_to_add_for_higher_pay: List[str] = Field(
        ...,
        description="3-5 specific skills or certifications that would significantly boost the salary range if acquired."
    )


class PersonaAnalysis(BaseModel):
    persona_title: str = Field(
        ...,
        description="A creative, professional persona archetype title (e.g., 'The Analytical Architect', 'The People-First Leader', 'The Full-Stack Innovator')."
    )
    persona_description: str = Field(
        ...,
        description="A 3-4 sentence description of this professional persona, highlighting their natural working style, strengths, and how they add value."
    )
    communication_style: str = Field(
        ...,
        description="One of: 'Data-Driven & Precise', 'Collaborative & Empathetic', 'Strategic & Visionary', 'Creative & Adaptive', 'Systematic & Detail-Oriented'."
    )
    interview_positioning_tips: List[str] = Field(
        ...,
        description="3-4 tips on how this persona should position themselves in interviews to stand out authentically."
    )
    strengths_to_amplify: List[str] = Field(
        ...,
        description="3-5 unique strengths this persona naturally has that should be highlighted in applications and interviews."
    )


class ResumeScoreBreakdown(BaseModel):
    technical_match: int = Field(..., description="Score 0-100: How well technical skills match the JD requirements.")
    soft_skills_score: int = Field(..., description="Score 0-100: Evidence of teamwork, leadership, communication in resume.")
    formatting_score: int = Field(..., description="Score 0-100: Resume structure, readability, section organization.")
    action_verbs_score: int = Field(..., description="Score 0-100: Strength and variety of action verbs used.")
    metrics_usage_score: int = Field(..., description="Score 0-100: Use of quantifiable achievements (%, $, numbers).")
    ats_friendliness: int = Field(..., description="Score 0-100: ATS compatibility — keyword density, no tables/graphics, clean formatting.")
    overall_score: int = Field(..., description="Weighted overall score 0-100.")
    score_rationale: str = Field(..., description="2-3 sentence explanation of the scoring and what drives the overall score.")


# ─── Functions ─────────────────────────────────────────────────────────────────

def rewrite_resume(resume_text: str, jd_text: str, api_key: str, model_name: str = "gemini-2.5-flash") -> RewrittenResume:
    """
    AI-rewrites the candidate's resume bullets to be ATS-optimized, metrics-driven,
    and perfectly aligned with the target job description.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.4)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a world-class resume writer and career strategist with 20+ years of experience.\n"
            "Your task: Transform the candidate's existing resume into a powerful, ATS-optimized version.\n"
            "Rules:\n"
            "1. Rewrite every bullet point to start with a strong, varied action verb.\n"
            "2. Add quantified metrics where possible (even estimates: 'reduced load time by ~40%').\n"
            "3. Naturally incorporate critical keywords from the job description.\n"
            "4. Keep bullets concise but impactful (1-2 lines max).\n"
            "5. Write a compelling summary section tailored to this specific role.\n"
            "Output at least 10 rewritten bullet points covering the candidate's key experiences."
        )),
        ("user", (
            "Original Resume:\n{resume_text}\n\n"
            "Target Job Description:\n{jd_text}\n\n"
            "Rewrite the resume to be ATS-optimized and perfectly aligned with this job description."
        ))
    ])

    structured_llm = llm.with_structured_output(RewrittenResume)
    chain = prompt | structured_llm

    return chain.invoke({
        "resume_text": resume_text,
        "jd_text": jd_text
    })


def generate_cover_letter(
    resume_text: str,
    jd_text: str,
    tone: str,
    api_key: str,
    model_name: str = "gemini-2.5-flash"
) -> CoverLetter:
    """
    Generates a professional, tailored cover letter based on the resume and JD.
    Tone can be: 'formal', 'enthusiastic', or 'concise'.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.6)

    tone_instructions = {
        "Formal & Professional": "Use formal, polished language. Third-person professional tone. Traditional structure.",
        "Enthusiastic & Energetic": "Show genuine passion and enthusiasm. Use dynamic language. Let personality shine through.",
        "Concise & Direct": "Be extremely direct and efficient. No fluff. Strong statements. Short, punchy sentences."
    }

    tone_guide = tone_instructions.get(tone, tone_instructions["Formal & Professional"])

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            f"You are an expert cover letter writer. Write a compelling, tailored cover letter.\n"
            f"Tone Instruction: {tone_guide}\n"
            "The cover letter must:\n"
            "1. Directly reference specific requirements from the job description.\n"
            "2. Highlight the 2-3 most relevant achievements from the resume with context.\n"
            "3. Demonstrate knowledge of what the role entails.\n"
            "4. Be compelling enough to guarantee an interview call."
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Target Job Description:\n{jd_text}\n\n"
            "Write a structured cover letter in the required format."
        ))
    ])

    structured_llm = llm.with_structured_output(CoverLetter)
    chain = prompt | structured_llm

    return chain.invoke({
        "resume_text": resume_text,
        "jd_text": jd_text
    })


def generate_linkedin_profile(
    resume_text: str,
    target_role: str,
    api_key: str,
    model_name: str = "gemini-2.5-flash"
) -> LinkedInProfile:
    """
    Generates an optimized LinkedIn headline, 'About' summary,
    skill keywords, and featured section ideas.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.6)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a LinkedIn profile optimization expert and personal branding specialist.\n"
            "Create a powerful LinkedIn presence for this candidate that maximizes recruiter discoverability "
            "and communicates their unique professional brand effectively.\n"
            "The profile must be keyword-rich for LinkedIn's search algorithm while reading naturally and compellingly."
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Target Role / Career Goal:\n{target_role}\n\n"
            "Generate optimized LinkedIn profile components."
        ))
    ])

    structured_llm = llm.with_structured_output(LinkedInProfile)
    chain = prompt | structured_llm

    return chain.invoke({
        "resume_text": resume_text,
        "target_role": target_role
    })


def generate_salary_insights(
    resume_text: str,
    jd_text: str,
    location: str,
    api_key: str,
    model_name: str = "gemini-2.5-flash"
) -> SalaryInsight:
    """
    Generates salary range estimates, market demand analysis, and negotiation tips
    based on the candidate's skills and the target role.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.3)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a senior compensation consultant and HR market analyst.\n"
            "Based on the candidate's resume, target job description, and location, "
            "provide realistic salary range estimates and market insights.\n"
            "Use your knowledge of current technology market rates (2024-2025).\n"
            "Be specific and realistic — not too conservative, not inflated."
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Target Job Description:\n{jd_text}\n\n"
            "Location / Region: {location}\n\n"
            "Provide salary insights and negotiation guidance."
        ))
    ])

    structured_llm = llm.with_structured_output(SalaryInsight)
    chain = prompt | structured_llm

    return chain.invoke({
        "resume_text": resume_text,
        "jd_text": jd_text,
        "location": location
    })


def analyze_persona(
    resume_text: str,
    api_key: str,
    model_name: str = "gemini-2.5-flash"
) -> PersonaAnalysis:
    """
    Identifies the candidate's professional persona archetype based on their resume.
    Provides communication style, positioning tips, and strengths to amplify.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.7)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert organizational psychologist and executive career coach.\n"
            "Analyze the candidate's resume holistically — their career choices, skills, "
            "project types, writing style, and achievements — to identify their professional persona archetype.\n"
            "Be insightful, creative, and deeply personalized. Help them understand their authentic professional brand."
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Identify this candidate's professional persona and provide positioning guidance."
        ))
    ])

    structured_llm = llm.with_structured_output(PersonaAnalysis)
    chain = prompt | structured_llm

    return chain.invoke({"resume_text": resume_text})


def score_resume_breakdown(
    resume_text: str,
    jd_text: str,
    api_key: str,
    model_name: str = "gemini-2.5-flash"
) -> ResumeScoreBreakdown:
    """
    Generates a detailed multi-dimensional score breakdown of the resume
    across 6 key dimensions: technical match, soft skills, formatting,
    action verbs, metrics usage, and ATS friendliness.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.1)

    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a professional resume evaluator and ATS expert.\n"
            "Score the candidate's resume across 6 dimensions. Be critical but fair.\n"
            "Each score is 0-100. The overall_score is a weighted average:\n"
            "- Technical Match: 35% weight\n"
            "- ATS Friendliness: 20% weight\n"
            "- Metrics Usage: 20% weight\n"
            "- Action Verbs: 10% weight\n"
            "- Soft Skills: 10% weight\n"
            "- Formatting: 5% weight\n"
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Target Job Description:\n{jd_text}\n\n"
            "Evaluate and score the resume across all dimensions."
        ))
    ])

    structured_llm = llm.with_structured_output(ResumeScoreBreakdown)
    chain = prompt | structured_llm

    return chain.invoke({
        "resume_text": resume_text,
        "jd_text": jd_text
    })
