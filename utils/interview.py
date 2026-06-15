from typing import List, Dict
from pydantic import BaseModel, Field
from langchain_core.prompts import ChatPromptTemplate
from utils.analyzer import get_llm

class InterviewQuestionsList(BaseModel):
    questions: List[str] = Field(
        ..., 
        description="A list of exactly 5 custom-tailored interview questions for this candidate and role."
    )

class AnswerEvaluation(BaseModel):
    question: str = Field(..., description="The interview question that was asked.")
    answer: str = Field(..., description="The candidate's answer.")
    score: int = Field(..., description="Evaluation score for this answer from 0 (poor) to 10 (excellent).")
    feedback: str = Field(..., description="Constructive feedback for the candidate's response, pointing out what was good and what was missing.")
    suggested_answer: str = Field(..., description="An exemplar or model answer showcasing how to respond using frameworks like STAR (Situation, Task, Action, Result) and incorporating appropriate keywords.")

class InterviewFeedbackReport(BaseModel):
    overall_score: int = Field(
        ..., 
        description="Overall interview performance score, as an integer from 0 to 100."
    )
    strengths: List[str] = Field(
        ..., 
        description="List of key strengths demonstrated by the candidate across all responses (e.g. strong technical expertise, clear structure)."
    )
    areas_for_improvement: List[str] = Field(
        ..., 
        description="List of general areas of improvement (e.g., lack of data/metrics, brief descriptions, weak examples)."
    )
    qa_evaluations: List[AnswerEvaluation] = Field(
        ..., 
        description="Detailed question-by-question evaluations."
    )

def generate_interview_questions(resume_text: str, jd_text: str, api_key: str, model_name: str = "gemini-2.5-flash") -> List[str]:
    """
    Generates 5 personalized interview questions based on the candidate's resume and job description.
    Includes 2 technical, 2 behavioral (STAR-based), and 1 project/experience-specific question.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.7)
    
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are a professional hiring manager and interviewer.\n"
            "Generate 5 high-quality, customized interview questions designed for the candidate's profile "
            "relative to the Target Job Description.\n"
            "Formulate a mix of:\n"
            "- 2 Technical questions exploring specific skills listed in the job description and resume.\n"
            "- 2 Behavioral/Situational questions (using STAR methodology trigger points) checking culture fit and soft skills.\n"
            "- 1 Resume-specific question asking about a particular project or experience mentioned in their resume."
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Target Job Description:\n{jd_text}\n\n"
            "Generate exactly 5 custom interview questions."
        ))
    ])
    
    structured_llm = llm.with_structured_output(InterviewQuestionsList)
    chain = prompt | structured_llm
    
    result = chain.invoke({
        "resume_text": resume_text,
        "jd_text": jd_text
    })
    
    return result.questions

def evaluate_mock_interview(qa_history: List[Dict[str, str]], resume_text: str, jd_text: str, api_key: str, model_name: str = "gemini-2.5-flash") -> InterviewFeedbackReport:
    """
    Evaluates the mock interview transcript.
    Generates a detailed feedback report outlining scores, strengths, improvement points, and suggested answers.
    """
    llm = get_llm(api_key=api_key, model_name=model_name, temperature=0.3)
    
    transcript_text = ""
    for idx, qa in enumerate(qa_history):
        transcript_text += f"Q{idx+1}: {qa['question']}\nA{idx+1}: {qa['answer']}\n\n"
        
    prompt = ChatPromptTemplate.from_messages([
        ("system", (
            "You are an expert Interview Coach and Senior Recruiter.\n"
            "Review the candidate's resume, the job description, and the transcript of the mock interview "
            "(containing questions asked and candidate answers).\n"
            "Evaluate each answer out of 10. Be constructive, pointing out how the answer matches requirements, "
            "and where they could have used better examples (STAR format) or highlighted relevant technical keywords.\n"
            "Provide an overall score out of 100 and identify high-level strengths and weaknesses."
        )),
        ("user", (
            "Candidate Resume:\n{resume_text}\n\n"
            "Target Job Description:\n{jd_text}\n\n"
            "Interview Transcript:\n{transcript_text}\n\n"
            "Please generate the detailed performance feedback report."
        ))
    ])
    
    structured_llm = llm.with_structured_output(InterviewFeedbackReport)
    chain = prompt | structured_llm
    
    return chain.invoke({
        "resume_text": resume_text,
        "jd_text": jd_text,
        "transcript_text": transcript_text
    })
