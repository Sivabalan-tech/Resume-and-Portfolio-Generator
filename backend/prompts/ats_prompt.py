"""
ATS Scoring Prompt — instructs Gemini to score a resume against a job description.
"""

def build_ats_prompt(resume_text: str, job_description: str) -> str:
    return f"""
You are an expert ATS (Applicant Tracking System) simulator and Technical Recruiter.
Analyze the provided RESUME against the JOB DESCRIPTION (JD).

### INPUTS:
1. RESUME:
{resume_text}

2. JOB DESCRIPTION:
{job_description}

### TASK:
1. Provide an ATS Match Score (0-100) based on semantic similarity, technical skills, and experience match.
2. Identify "Matching Keywords": List up to 15 key technical skills or terms found in both.
3. Identify "Missing Keywords": List up to 15 key technical skills or terms found in the JD but missing from the resume.
4. Provide 3-5 Actionable "Improvement Suggestions".

### OUTPUT FORMAT (Strictly follow this):
[SCORE]
(just the number)

[MATCHING]
- Keyword 1
- Keyword 2

[MISSING]
- Keyword 1
- Keyword 2

[SUGGESTIONS]
- Suggestion 1
- Suggestion 2

Keep keywords concise (1-3 words).
"""
