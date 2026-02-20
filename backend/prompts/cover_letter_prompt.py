"""
Cover Letter Prompt Template — professional, tailored, company-specific.
"""


def build_cover_letter_prompt(
    profile: dict,
    company_name: str,
    job_role: str,
    job_description: str,
    hiring_manager: str = "Hiring Manager"
) -> str:
    """
    Build the Gemini prompt for a tailored professional cover letter.
    """
    personal = profile.get("personal_info", {})
    name = personal.get("name", "Candidate")
    email = personal.get("email", "")
    phone = personal.get("phone", "")
    location = personal.get("location", "")
    skills = profile.get("skills", [])
    experience = profile.get("experience", [])
    projects = profile.get("projects", [])

    skills_str = ", ".join(skills[:15]) if skills else "Not provided"
    exp_str = "; ".join([
        f"{e.get('role', '')} at {e.get('company', '')} ({e.get('duration', '')})"
        for e in experience[:3]
    ]) if experience else "Fresher / Entry Level"

    return f"""You are a professional cover letter writer specialized in getting candidates interviews.

Write a compelling, personalized cover letter for:

CANDIDATE:
- Name: {name}
- Email: {email}
- Phone: {phone}
- Location: {location}
- Key Skills: {skills_str}
- Experience: {exp_str}

ROLE DETAILS:
- Applying to: {company_name}
- Position: {job_role}
- Hiring Manager: {hiring_manager}

JOB DESCRIPTION:
---
{job_description[:1500]}
---

COVER LETTER REQUIREMENTS:
1. Professional business letter format (date, address, salutation, body, closing)
2. Opening paragraph: Enthusiastic hook, mention {job_role} and {company_name} by name
3. Second paragraph: 2-3 strongest qualifications that directly match the job description
4. Third paragraph: Specific achievements/projects that demonstrate value (use numbers/metrics)
5. Fourth paragraph: Why {company_name} specifically — show you've researched them
6. Closing: Call to action, thank the reader, professional sign-off

TONE: Professional, confident, enthusiastic — NOT generic or robotic
LENGTH: 4-5 paragraphs, 300-400 words
FORMAT: Plain text (no Markdown headers/bullets)

DO NOT start with "I am writing to apply..." — use a compelling hook instead.
DO NOT use hollow phrases like "I am a hardworking team player".
DO reference specific job requirements from the JD.

Write the complete cover letter:"""
