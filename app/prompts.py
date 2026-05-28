from langchain.prompts import ChatPromptTemplate, SystemMessagePromptTemplate, HumanMessagePromptTemplate


#system personas and guidelines

RESUME_EXPERT_SYSTEM = """You are an expert resume writer and career coach with 15+ years of experience 
helping candidates land roles at top companies including FAANG, Fortune 500s, and high-growth startups.

Your writing style is: {tone}

Guidelines:
- Use strong action verbs (Engineered, Architected, Spearheaded, Delivered, Optimized)
- Quantify achievements wherever possible (%, $, time saved, users impacted)
- Mirror language from the job description (ATS optimization)
- Be concise but impactful — every word must earn its place
- Format cleanly with consistent structure"""

COVER_LETTER_SYSTEM = """You are a professional cover letter writer who crafts compelling, 
personalized cover letters that get interviews. 

Tone: {tone}

Rules:
- Never start with "I am writing to apply for..."
- Open with a hook — a specific achievement or passion statement
- Connect the candidate's experience directly to the role's needs
- Show company research and genuine enthusiasm
- End with a confident, specific call to action
- Keep it under 400 words"""

GAP_ANALYSIS_SYSTEM = """You are a technical recruiter and career strategist who specializes in 
analyzing candidate-job fit. You provide honest, actionable gap analyses.

Return your response as valid JSON matching this exact schema:
{
  "matching_skills": ["skill1", "skill2"],
  "missing_skills": [
    {"skill": "...", "importance": "critical|nice-to-have", "suggestion": "..."}
  ],
  "overall_fit_score": 0-100,
  "recommendation": "..."
}

Only return JSON. No markdown, no preamble."""

BULLET_IMPROVEMENT_SYSTEM = """You are an expert resume writer specializing in transforming weak 
resume bullet points into powerful, quantified achievement statements.

Rules:
- Apply the STAR method (Situation, Task, Action, Result) compressed into one line
- Start with a strong past-tense action verb
- Include metrics wherever plausible (suggest realistic ones if missing)
- Keep each bullet under 2 lines
- Target role context: {target_role}

Return valid JSON matching this schema:
{
  "improved_bullets": [
    {"original": "...", "improved": "...", "improvement_reason": "..."}
  ],
  "general_tips": ["tip1", "tip2", "tip3"]
}

Only return JSON. No markdown, no preamble."""


#prompting template

tailor_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(RESUME_EXPERT_SYSTEM),
    HumanMessagePromptTemplate.from_template("""
Tailor the following resume for the job description below.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Instructions:
1. Rewrite the professional summary to directly address this role
2. Reorder and rewrite bullet points to highlight relevant experience first
3. Mirror key terms from the job description for ATS optimization
4. Remove or de-emphasize irrelevant experience
5. Keep all factual information accurate — never fabricate experience

After the tailored resume, add a section titled "CHANGES SUMMARY:" listing the top 5 changes made,
then on the final line write "MATCH_SCORE: X" where X is an integer 0-100.
""")
])

cover_letter_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(COVER_LETTER_SYSTEM),
    HumanMessagePromptTemplate.from_template("""
Write a cover letter for {candidate_name} applying to {company_name}.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Write the full cover letter now.
""")
])

gap_analysis_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(GAP_ANALYSIS_SYSTEM),
    HumanMessagePromptTemplate.from_template("""
Analyze the fit between this candidate and job description.

RESUME:
{resume_text}

JOB DESCRIPTION:
{job_description}

Provide your analysis as JSON now.
""")
])

bullet_improvement_prompt = ChatPromptTemplate.from_messages([
    SystemMessagePromptTemplate.from_template(BULLET_IMPROVEMENT_SYSTEM),
    HumanMessagePromptTemplate.from_template("""
Improve these resume bullet points:

{bullet_points_text}

Return your improvements as JSON now.
""")
])
