from typing import List
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_core.prompts import ChatPromptTemplate

# Define Pydantic schemas for structured output
class ResumeAnalysisResult(BaseModel):
    match_percentage: int = Field(
        ..., 
        description="Percentage match between resume and job description, as an integer from 0 to 100."
    )
    technical_skills: List[str] = Field(
        ..., 
        description="Technical skills, programming languages, tools, frameworks or methodologies found in the resume."
    )
    soft_skills: List[str] = Field(
        ..., 
        description="Soft skills, leadership qualities, teamwork, communication, and management skills found in the resume."
    )
    skills_gaps: List[str] = Field(
        ..., 
        description="Critical skills, tools, or experiences listed in the job description that are missing from the resume."
    )
    ats_suggestions: List[str] = Field(
        ..., 
        description="Concrete, actionable recommendations for optimizing the resume to improve ATS compatibility (e.g., adding specific keywords, framing achievements with metrics, modifying section titles)."
    )

class CareerGuidanceResult(BaseModel):
    summary: str = Field(
        ..., 
        description="A personalized summary of the career guidance, highlighting strengths and defining a career trajectory."
    )
    recommended_roles: List[str] = Field(
        ..., 
        description="3 to 5 target job roles that the candidate is well-suited for or can transition into."
    )
    upskilling_roadmap: List[str] = Field(
        ..., 
        description="A step-by-step roadmap indicating skills they need to learn next and technical concepts they should master."
    )
    suggested_certifications: List[str] = Field(
        ..., 
        description="Specific industry certifications, courses, or training paths (e.g. AWS, Coursera, Scrum Master) that would boost their profile."
    )

def get_llm(api_key: str, model_name: str = "gemini-2.5-flash", temperature: float = 0.2) -> ChatGoogleGenerativeAI:
    """Initializes and returns a ChatGoogleGenerativeAI client with the user's API key."""
    return ChatGoogleGenerativeAI(
        google_api_key=api_key,
        model=model_name,
        temperature=temperature
    )

def analyze_resume_vs_jd(resume_text: str, jd_text: str, api_key: str, model_name: str = "gemini-2.5-flash") -> ResumeAnalysisResult:
    """
    Analyzes a resume against a job description.
    Extracts match percentage, skills, gaps, and ATS optimization suggestions.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.1)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert HR Specialist, Recruiter, and Applicant Tracking System (ATS) optimization expert.\n"
            "Analyze the candidate's resume in the context of the job description provided.\n"
            "Be critical but constructive. Evaluate how well the resume content aligns with the core requirements of the job description."
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Target Job Description:\n{jd_text}\n\n"
            "Analyze the resume against the job description and fill out the required schema fields."
        ))
    ])
    
    # Bind structured output schema
    structured_llm = llm.with_structured_output(ResumeAnalysisResult)
    chain = prompt | structured_llm
    
    return chain.invoke({
        "resume_text": resume_text,
        "jd_text": jd_text
    })

def generate_career_guidance(resume_text: str, career_goals: str, api_key: str, model_name: str = "gemini-2.5-flash") -> CareerGuidanceResult:
    """
    Generates personalized career guidance and upskilling roadmaps
    based on the resume and user's stated career goals.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.5)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a professional AI Career Coach and Mentor.\n"
            "Review the candidate's resume and understand their current skills, experience level, and background.\n"
            "Then, look at their target career goals or interest areas and design a personalized upskilling plan, "
            "recommending roles and action items."
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Stated Career Goals / Area of Interest:\n{career_goals}\n\n"
            "Generate structured career guidance recommendations."
        ))
    ])
    
    structured_llm = llm.with_structured_output(CareerGuidanceResult)
    chain = prompt | structured_llm
    
    return chain.invoke({
        "resume_text": resume_text,
        "career_goals": career_goals
    })
