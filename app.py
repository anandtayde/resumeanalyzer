import streamlit as st
import os
import io
import pandas as pd
import altair as alt
from dotenv import load_dotenv

# Import utilities
from utils.parser import parse_resume
from utils.analyzer import analyze_resume_vs_jd, generate_career_guidance
from utils.interview import generate_interview_questions, evaluate_mock_interview

# Load environment variables
load_dotenv()

# Page configuration
st.set_page_config(
    page_title="AI Resume Analyzer & Interview Prep",
    page_icon="💼",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom premium styling using CSS injection
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600;700&family=Inter:wght@300;400;500;600&display=swap');
    
    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }
    h1, h2, h3, h4, h5, h6 {
        font-family: 'Outfit', sans-serif;
        font-weight: 600;
        letter-spacing: -0.5px;
    }
    .main-title {
        font-size: 3rem;
        background: linear-gradient(135deg, #6c5ce7, #a29bfe, #00cec9);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        font-weight: 700;
        margin-bottom: 0.5rem;
    }
    .subtitle {
        color: #b2bec3;
        font-size: 1.1rem;
        margin-bottom: 2rem;
        font-weight: 300;
    }
    .metric-card {
        background: linear-gradient(135deg, #1e1e2f, #2d2d44);
        border: 1px solid #3d3d5c;
        border-radius: 12px;
        padding: 1.5rem;
        text-align: center;
        box-shadow: 0 4px 20px rgba(0,0,0,0.15);
        transition: transform 0.3s ease;
    }
    .metric-card:hover {
        transform: translateY(-5px);
    }
    .metric-score {
        font-size: 4rem;
        font-weight: 700;
        background: linear-gradient(135deg, #00cec9, #6c5ce7);
        -webkit-background-clip: text;
        -webkit-text-fill-color: transparent;
        margin: 0.5rem 0;
    }
    .skills-header {
        font-size: 1.2rem;
        font-weight: 600;
        color: #e2e8f0;
        border-bottom: 2px solid #6c5ce7;
        padding-bottom: 0.5rem;
        margin-bottom: 1rem;
    }
    .skills-pill {
        display: inline-block;
        background-color: #2d3748;
        color: #e2e8f0;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
        border: 1px solid #4a5568;
    }
    .skills-pill-gap {
        display: inline-block;
        background-color: rgba(254, 215, 215, 0.15);
        color: #feb2b2;
        padding: 0.4rem 0.8rem;
        border-radius: 20px;
        font-size: 0.85rem;
        margin: 0.25rem;
        border: 1px solid #feb2b2;
    }
    .suggestion-card {
        background-color: #1a202c;
        border-left: 4px solid #6c5ce7;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
    }
    .gap-card {
        background-color: #1a202c;
        border-left: 4px solid #e53e3e;
        padding: 1rem;
        border-radius: 0 8px 8px 0;
        margin-bottom: 0.8rem;
        font-size: 0.95rem;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize Session States
if "resume_text" not in st.session_state:
    st.session_state.resume_text = ""
if "jd_text" not in st.session_state:
    st.session_state.jd_text = ""
if "analysis_result" not in st.session_state:
    st.session_state.analysis_result = None
if "career_guidance" not in st.session_state:
    st.session_state.career_guidance = None

# Interview states
if "interview_active" not in st.session_state:
    st.session_state.interview_active = False
if "interview_questions" not in st.session_state:
    st.session_state.interview_questions = []
if "current_question_idx" not in st.session_state:
    st.session_state.current_question_idx = 0
if "qa_history" not in st.session_state:
    st.session_state.qa_history = []
if "interview_feedback" not in st.session_state:
    st.session_state.interview_feedback = None

# ----------------- SIDEBAR -----------------
st.sidebar.markdown("### ⚙️ Configuration")

# Gemini API Key Input
gemini_api_key = st.sidebar.text_input(
    "Gemini API Key",
    value=os.getenv("GOOGLE_API_KEY", ""),
    type="password",
    help="Enter your Google Gemini API key to power the analysis. If set in .env (as GOOGLE_API_KEY), it will auto-populate."
)

# Model Selection
model_name = st.sidebar.selectbox(
    "Select Model",
    options=["gemini-2.5-flash", "gemini-2.5-pro"],
    index=0,
    help="gemini-2.5-flash is recommended for general speed and efficiency. gemini-2.5-pro provides deeper evaluations."
)

st.sidebar.markdown("---")
st.sidebar.markdown("### 📄 Resume & Job Description")

# Sample Data Selector
sample_option = st.sidebar.selectbox(
    "Select Sample Data (Optional)",
    options=["Custom Upload / Paste", "Software Engineer Sample", "Product Manager Sample"],
    index=0
)

# Pre-populated samples logic
sample_resume = ""
sample_jd = ""

if sample_option == "Software Engineer Sample":
    try:
        with open("samples/resume_swe.txt", "r") as f:
            sample_resume = f.read()
        with open("samples/jd_swe.txt", "r") as f:
            sample_jd = f.read()
    except FileNotFoundError:
        st.sidebar.warning("Sample files not found yet.")
elif sample_option == "Product Manager Sample":
    try:
        with open("samples/resume_pm.txt", "r") as f:
            sample_resume = f.read()
        with open("samples/jd_pm.txt", "r") as f:
            sample_jd = f.read()
    except FileNotFoundError:
        st.sidebar.warning("Sample files not found yet.")

# Resume Upload
uploaded_file = st.sidebar.file_uploader(
    "Upload Resume (PDF, DOCX, TXT)",
    type=["pdf", "docx", "doc", "txt"],
    disabled=(sample_option != "Custom Upload / Paste")
)

# Parse uploaded file
if sample_option == "Custom Upload / Paste":
    if uploaded_file is not None:
        try:
            st.session_state.resume_text = parse_resume(uploaded_file)
            st.sidebar.success("Resume parsed successfully!")
        except Exception as e:
            st.sidebar.error(f"Error parsing resume: {e}")
    else:
        st.session_state.resume_text = ""
else:
    st.session_state.resume_text = sample_resume
    st.sidebar.success(f"Loaded {sample_option} resume!")

# Job Description Input
if sample_option == "Custom Upload / Paste":
    jd_input = st.sidebar.text_area("Target Job Description", height=200, placeholder="Paste the job description here...")
    st.session_state.jd_text = jd_input
else:
    jd_input = st.sidebar.text_area("Target Job Description", value=sample_jd, height=200)
    st.session_state.jd_text = sample_jd

# ----------------- MAIN PANEL -----------------
st.markdown('<div class="main-title">💼 AI Resume Analyzer & Interview Prep</div>', unsafe_allow_html=True)
st.markdown('<div class="subtitle">Extract gaps, optimize ATS scores, simulate interviews, and receive career coaching using Google Gemini.</div>', unsafe_allow_html=True)

# Require API Key to proceed
if not gemini_api_key:
    st.warning("⚠️ Please provide a Gemini API Key in the sidebar configuration to begin.")
    st.stop()

# Set up tabs
tab1, tab2, tab3, tab4 = st.tabs([
    "📊 Resume Analysis & ATS Match", 
    "💬 Interactive Mock Interview", 
    "📈 Interview Performance Report", 
    "🧭 Career Guidance"
])

# ----------------- TAB 1: RESUME ANALYSIS & ATS MATCH -----------------
with tab1:
    st.header("Resume Analysis & ATS Compatibility")
    
    col1, col2 = st.columns([1, 2])
    
    with col1:
        st.subheader("ATS Match Score")
        analyze_btn = st.button("🚀 Analyze Resume & Match JD", use_container_width=True)
        
        if analyze_btn:
            if not st.session_state.resume_text:
                st.error("Please upload/load a resume in the sidebar first.")
            elif not st.session_state.jd_text:
                st.error("Please enter/load a job description in the sidebar first.")
            else:
                with st.spinner("Analyzing resume against the Job Description... This may take a moment."):
                    try:
                        analysis = analyze_resume_vs_jd(
                            st.session_state.resume_text, 
                            st.session_state.jd_text, 
                            gemini_api_key, 
                            model_name
                        )
                        st.session_state.analysis_result = analysis
                        st.success("Analysis complete!")
                    except Exception as e:
                        st.error(f"Analysis failed: {e}")

        # Render Match Score gauge/visual
        if st.session_state.analysis_result:
            score = st.session_state.analysis_result.match_percentage
            
            # Gauge-like color formatting
            if score >= 80:
                color = "#00cec9" # Cyan / Excellent
                level = "Excellent Fit"
            elif score >= 60:
                color = "#fdcb6e" # Amber / Good Fit
                level = "Moderate Fit"
            else:
                color = "#d63031" # Red / Needs Optimization
                level = "Weak Fit (Needs Work)"
                
            st.markdown(f"""
                <div class="metric-card">
                    <h4>Overall Match Score</h4>
                    <div class="metric-score" style="background: linear-gradient(135deg, {color}, #6c5ce7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                        {score}%
                    </div>
                    <span style="color: {color}; font-weight: 600; font-size: 1.1rem;">{level}</span>
                </div>
            """, unsafe_allow_html=True)
            
            # Simple bar chart visualizing score breakdown
            score_data = pd.DataFrame({
                "Metric": ["Match Score", "Gaps Score"],
                "Percentage": [score, 100 - score]
            })
            chart = alt.Chart(score_data).mark_arc(innerRadius=50).encode(
                theta=alt.Theta(field="Percentage", type="quantitative"),
                color=alt.Color(field="Metric", type="nominal", scale=alt.Scale(range=[color, '#2d3748'])),
                tooltip=["Metric", "Percentage"]
            ).properties(width=200, height=200)
            
            st.altair_chart(chart, use_container_width=True)
        else:
            st.info("Click 'Analyze Resume & Match JD' to generate your ATS score and skill gap overview.")

    with col2:
        if st.session_state.analysis_result:
            result = st.session_state.analysis_result
            
            # Render Extracted Skills
            st.subheader("🔍 Identified Skills")
            col_tech, col_soft = st.columns(2)
            
            with col_tech:
                st.markdown('<div class="skills-header">Technical Skills</div>', unsafe_allow_html=True)
                if result.technical_skills:
                    for skill in result.technical_skills:
                        st.markdown(f'<span class="skills-pill">{skill}</span>', unsafe_allow_html=True)
                else:
                    st.write("*No clear technical skills identified.*")
                    
            with col_soft:
                st.markdown('<div class="skills-header">Soft Skills / Leadership</div>', unsafe_allow_html=True)
                if result.soft_skills:
                    for skill in result.soft_skills:
                        st.markdown(f'<span class="skills-pill">{skill}</span>', unsafe_allow_html=True)
                else:
                    st.write("*No clear soft skills identified.*")
            
            st.markdown("---")
            
            # Render Skills Gaps
            st.subheader("⚠️ Missing Skills & Requirements")
            st.write("These skills are requested in the job description but seem missing or weak in your resume:")
            if result.skills_gaps:
                for gap in result.skills_gaps:
                    st.markdown(f'<div class="gap-card">❌ <strong>{gap}</strong></div>', unsafe_allow_html=True)
            else:
                st.success("🎉 No significant skills gaps found! Your skill set matches the JD core needs perfectly.")
                
            st.markdown("---")
            
            # Render ATS Optimization suggestions
            st.subheader("💡 ATS Optimization Suggestions")
            if result.ats_suggestions:
                for suggestion in result.ats_suggestions:
                    st.markdown(f'<div class="suggestion-card">📌 {suggestion}</div>', unsafe_allow_html=True)
            else:
                st.write("*No specific suggestions generated.*")
        else:
            st.markdown("""
                ### Ready to optimize your resume?
                This tool performs semantic analysis on your resume to evaluate ATS compatibility.
                1. Ensure your resume and job description are loaded in the sidebar.
                2. Click the **Analyze Resume** button.
                3. Review your technical and soft skills breakdown, missing keywords, and actionable rewriting guidelines.
            """)

# ----------------- TAB 2: INTERACTIVE MOCK INTERVIEW -----------------
with tab2:
    st.header("💬 AI Mock Interview Prep")
    st.write("Simulate a live, conversational interview based on your resume and target job description.")
    
    # Check if resume & JD are loaded
    if not st.session_state.resume_text or not st.session_state.jd_text:
        st.info("Please set up a resume and job description in the sidebar to start the mock interview.")
    else:
        # Start or reset interview button
        if not st.session_state.interview_active:
            if st.button("🎯 Start Mock Interview Session", type="primary", use_container_width=True):
                with st.spinner("Generating custom interview questions based on your profile..."):
                    try:
                        questions = generate_interview_questions(
                            st.session_state.resume_text, 
                            st.session_state.jd_text, 
                            gemini_api_key, 
                            model_name
                        )
                        st.session_state.interview_questions = questions
                        st.session_state.current_question_idx = 0
                        st.session_state.qa_history = []
                        st.session_state.interview_feedback = None
                        st.session_state.interview_active = True
                        st.rerun()
                    except Exception as e:
                        st.error(f"Could not generate questions: {e}")
        else:
            col_left, col_right = st.columns([3, 1])
            
            with col_right:
                st.markdown("### 📊 Status Dashboard")
                st.write(f"**Question:** {st.session_state.current_question_idx + 1} of 5")
                progress_val = (st.session_state.current_question_idx) / 5.0
                st.progress(progress_val)
                
                st.markdown("---")
                if st.button("🛑 Force Quit & Evaluate", type="secondary", use_container_width=True):
                    if len(st.session_state.qa_history) > 0:
                        with st.spinner("Evaluating your responses so far..."):
                            try:
                                feedback = evaluate_mock_interview(
                                    st.session_state.qa_history, 
                                    st.session_state.resume_text, 
                                    st.session_state.jd_text, 
                                    gemini_api_key, 
                                    model_name
                                )
                                st.session_state.interview_feedback = feedback
                                st.session_state.interview_active = False
                                st.success("Feedback generated! Check 'Interview Performance Report' tab.")
                            except Exception as e:
                                st.error(f"Evaluation failed: {e}")
                    else:
                        st.session_state.interview_active = False
                        st.rerun()
                        
                if st.button("🔄 Restart Interview", type="secondary", use_container_width=True):
                    st.session_state.interview_active = False
                    st.session_state.interview_questions = []
                    st.session_state.current_question_idx = 0
                    st.session_state.qa_history = []
                    st.session_state.interview_feedback = None
                    st.rerun()

            with col_left:
                # Render the chat sequence
                st.markdown("### 🗣️ Interview Session")
                
                # Show prior Q&A
                for i, qa in enumerate(st.session_state.qa_history):
                    with st.chat_message("assistant", avatar="🤖"):
                        st.write(f"**Q{i+1}:** {qa['question']}")
                    with st.chat_message("user", avatar="👤"):
                        st.write(qa['answer'])
                
                # Show current question
                curr_idx = st.session_state.current_question_idx
                if curr_idx < len(st.session_state.interview_questions):
                    current_q = st.session_state.interview_questions[curr_idx]
                    with st.chat_message("assistant", avatar="🤖"):
                        st.markdown(f"**Question {curr_idx + 1}:** {current_q}")
                        
                    # User response input
                    user_answer = st.chat_input("Type your response here...")
                    
                    if user_answer:
                        # Append to Q&A history
                        st.session_state.qa_history.append({
                            "question": current_q,
                            "answer": user_answer
                        })
                        # Move to next question
                        st.session_state.current_question_idx += 1
                        st.rerun()
                else:
                    # All questions answered
                    st.balloons()
                    st.success("🎉 All 5 questions answered! Click below to evaluate your interview performance and generate your report.")
                    
                    if st.button("📊 Generate My Performance Feedback Report", type="primary", use_container_width=True):
                        with st.spinner("Analyzing your answers and compiling the feedback report..."):
                            try:
                                feedback = evaluate_mock_interview(
                                    st.session_state.qa_history, 
                                    st.session_state.resume_text, 
                                    st.session_state.jd_text, 
                                    gemini_api_key, 
                                    model_name
                                )
                                st.session_state.interview_feedback = feedback
                                st.session_state.interview_active = False
                                st.success("Report successfully generated!")
                                st.rerun()
                            except Exception as e:
                                st.error(f"Evaluation failed: {e}")

# ----------------- TAB 3: INTERVIEW PERFORMANCE REPORT -----------------
with tab3:
    st.header("📈 Interview Performance Report")
    
    if st.session_state.interview_feedback:
        report = st.session_state.interview_feedback
        
        # Display main summary card
        score = report.overall_score
        if score >= 80:
            color = "#00cec9"
            feedback_label = "Excellent Communication & Technical Alignment"
        elif score >= 60:
            color = "#fdcb6e"
            feedback_label = "Good Effort - Some key details missing"
        else:
            color = "#d63031"
            feedback_label = "Requires Improvement - Need more specificity and framework structuring"
            
        st.markdown(f"""
            <div class="metric-card" style="margin-bottom: 2rem;">
                <h4>Overall Interview Score</h4>
                <div class="metric-score" style="background: linear-gradient(135deg, {color}, #6c5ce7); -webkit-background-clip: text; -webkit-text-fill-color: transparent;">
                    {score}/100
                </div>
                <span style="color: {color}; font-weight: 600; font-size: 1.1rem;">{feedback_label}</span>
            </div>
        """, unsafe_allow_html=True)
        
        # Strengths vs Weaknesses columns
        col_st, col_im = st.columns(2)
        with col_st:
            st.markdown('<div class="skills-header">🌟 Strengths Demonstrated</div>', unsafe_allow_html=True)
            for strength in report.strengths:
                st.write(f"- {strength}")
                
        with col_im:
            st.markdown('<div class="skills-header">🚀 Key Areas to Improve</div>', unsafe_allow_html=True)
            for improvement in report.areas_for_improvement:
                st.write(f"- {improvement}")
                
        st.markdown("---")
        
        # Detail review accordions
        st.subheader("🔍 Question-by-Question Detailed Review")
        
        for idx, qa_eval in enumerate(report.qa_evaluations):
            q_title = f"Q{idx+1}: {qa_eval.question[:60]}... (Score: {qa_eval.score}/10)"
            with st.expander(q_title, expanded=(idx==0)):
                st.markdown(f"**Question Asked:** {qa_eval.question}")
                st.markdown(f"**Your Answer:** *{qa_eval.answer}*")
                st.markdown(f"**Score:** `{qa_eval.score}/10`")
                st.info(f"**Feedback:** {qa_eval.feedback}")
                
                with st.container(border=True):
                    st.markdown("**💡 Ideal Model Response (STAR Framework):**")
                    st.write(qa_eval.suggested_answer)
                    
        # Export Report Button
        report_md = f"# Mock Interview Performance Feedback Report\n\n"
        report_md += f"**Overall Score:** {score}/100\n\n"
        report_md += "## Strengths\n"
        for strength in report.strengths:
            report_md += f"- {strength}\n"
        report_md += "\n## Areas for Improvement\n"
        for improvement in report.areas_for_improvement:
            report_md += f"- {improvement}\n"
        report_md += "\n## Detailed Question Breakdown\n\n"
        for idx, qa_eval in enumerate(report.qa_evaluations):
            report_md += f"### Q{idx+1}: {qa_eval.question}\n"
            report_md += f"**Your Answer:** {qa_eval.answer}\n\n"
            report_md += f"**Score:** {qa_eval.score}/10\n\n"
            report_md += f"**Feedback:** {qa_eval.feedback}\n\n"
            report_md += f"**Model Answer:** {qa_eval.suggested_answer}\n\n"
            report_md += "---\n\n"
            
        st.download_button(
            label="📥 Download Detailed Feedback Report (.md)",
            data=report_md,
            file_name="Interview_Feedback_Report.md",
            mime="text/markdown",
            use_container_width=True
        )
    else:
        st.info("Complete the Mock Interview in Tab 2 to generate your personalized feedback report.")

# ----------------- TAB 4: CAREER GUIDANCE -----------------
with tab4:
    st.header("🧭 AI Career Guidance & Upskilling Coach")
    st.write("Understand potential career paths, upskilling roadmaps, and course recommendations based on your resume.")
    
    if not st.session_state.resume_text:
        st.info("Please upload or load your resume in the sidebar first.")
    else:
        career_goals = st.text_area(
            "State your Career Goals & Interests",
            placeholder="e.g. 'I want to transition from backend engineering to DevOps and cloud architecture', or 'I want to reach a Senior Product Manager role at a FinTech startup.'",
            height=120
        )
        
        guidance_btn = st.button("🗺️ Generate Upskilling Roadmap", type="primary", use_container_width=True)
        
        if guidance_btn:
            if not career_goals:
                st.warning("Please type in your career goals or interest areas.")
            else:
                with st.spinner("Generating personalized career advice and upskilling path..."):
                    try:
                        guidance = generate_career_guidance(
                            st.session_state.resume_text,
                            career_goals,
                            gemini_api_key,
                            model_name
                        )
                        st.session_state.career_guidance = guidance
                        st.success("Guidance roadmap generated!")
                    except Exception as e:
                        st.error(f"Failed to generate career guidance: {e}")
                        
        if st.session_state.career_guidance:
            g = st.session_state.career_guidance
            
            # Summary
            st.markdown('<div class="skills-header">📝 Career Strategy Summary</div>', unsafe_allow_html=True)
            st.write(g.summary)
            
            # Target roles & roadmap
            col_r, col_ro = st.columns(2)
            
            with col_r:
                st.markdown('<div class="skills-header">🎯 Recommended Next Roles</div>', unsafe_allow_html=True)
                for role in g.recommended_roles:
                    st.markdown(f'<span class="skills-pill" style="border-color: #00cec9;">🏷️ {role}</span>', unsafe_allow_html=True)
                    
            with col_ro:
                st.markdown('<div class="skills-header">📚 Suggested Certifications & Courses</div>', unsafe_allow_html=True)
                for cert in g.suggested_certifications:
                    st.write(f"🎓 {cert}")
                    
            st.markdown("---")
            
            # Actionable upskilling roadmap steps
            st.markdown('<div class="skills-header">🗺️ Actionable Upskilling Roadmap</div>', unsafe_allow_html=True)
            for idx, step in enumerate(g.upskilling_roadmap):
                st.markdown(f"**Step {idx+1}:** {step}")
        else:
            st.markdown("""
                ### Plan your career path
                Our AI coach scans your experience and details exactly how to transition to your dream job.
                1. Ensure your resume is uploaded in the sidebar.
                2. Input your short-term or long-term career aspirations.
                3. Click **Generate Upskilling Roadmap** to outline recommendations.
            """)
