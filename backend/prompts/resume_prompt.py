"""
Resume Prompt Template — engineered for ATS-optimized output.

Uses strong action verbs, quantified achievements, keyword density,
and a structured format that ATS parsers can reliably extract.
"""


def build_resume_prompt(profile: dict, job_role: str, job_description: str = "") -> str:
    """
    Build the Gemini prompt for ATS-optimized resume generation.

    Args:
        profile: User's complete career profile dict
        job_role: Target job role
        job_description: Optional job description for keyword alignment

    Returns:
        Formatted prompt string
    """
    personal = profile.get("personal_info", {})
    name = personal.get("name", "Candidate")
    email = personal.get("email", "")
    phone = personal.get("phone", "")
    linkedin = personal.get("linkedin", "")
    github = personal.get("github", "")
    location = personal.get("location", "")
    summary = personal.get("summary", "")

    skills = profile.get("skills", [])
    education = profile.get("education", [])
    experience = profile.get("experience", [])
    projects = profile.get("projects", [])
    certifications = profile.get("certifications", [])
    internships = profile.get("internships", [])
    achievements = profile.get("achievements", "")

    # Format sub-sections for the prompt
    skills_str = ", ".join(skills) if skills else "Not provided"
    education_str = _format_education(education)
    experience_str = _format_experience(experience)
    projects_str = _format_projects(projects)
    internships_str = _format_internships(internships)
    certs_str = _format_certs(certifications)

    jd_section = ""
    if job_description:
        jd_section = f"""
JOB DESCRIPTION (Extract and prioritize these keywords in the resume):
---
{job_description[:2000]}
---
"""

    return f"""You are an expert resume writer and ATS optimization specialist.

Your task is to generate a professional, ATS-optimized resume in Markdown format for the following candidate applying for the role of **{job_role}**.

=== CANDIDATE PROFILE ===
Name: {name}
Email: {email}
Phone: {phone}
LinkedIn: {linkedin}
GitHub: {github}
Location: {location}
Professional Summary: {summary}

SKILLS:
{skills_str}

EDUCATION:
{education_str}

WORK EXPERIENCE:
{experience_str}

INTERNSHIPS:
{internships_str}

PROJECTS:
{projects_str}

CERTIFICATIONS:
{certs_str}

ACHIEVEMENTS:
{achievements}
{jd_section}

=== OUTPUT REQUIREMENTS ===
Generate a complete resume in Markdown format following these STRICT rules:

1. **Contact Section**: Name as H1, email | phone | linkedin | github on one line
2. **Professional Summary**: 3-4 lines, keyword-rich, tailored for {job_role}, use first-person narrative
3. **Technical Skills**: Categorized by skill type (Languages, Frameworks, Tools, Databases, etc.)
4. **Work Experience / Internships**: For each role:
   - Company | Role | Duration | Location
   - 3-5 bullet points using STRONG ACTION VERBS (Developed, Architected, Optimized, Reduced, Led, Implemented, Built, Designed, Automated, Improved)
   - QUANTIFY every achievement where possible (e.g., "Reduced API response time by 40%", "Managed team of 5")
   - Use keywords from the job description naturally
5. **Projects**: Name | Tech Stack | GitHub Link
   - 2-3 bullet points describing impact and technology
6. **Education**: Degree | Institution | Year | GPA
7. **Certifications**: Listed cleanly
8. **Achievements / Extra**: Awards, publications, competitions

=== CRITICAL ATS RULES ===
- Use STANDARD section headers (Experience, Education, Skills, Projects — not creative names)
- NO tables, columns, or fancy formatting — plain Markdown only
- NO images, icons, or special characters
- Include exact job title "{job_role}" in the summary
- Spell out acronyms at least once
- Prioritize keywords from the job description
- Action verbs at the START of every bullet point
- NO filler phrases like "responsible for", "worked on", "helped with"
- Every bullet must demonstrate VALUE and IMPACT

Generate the complete resume now:"""


def _format_education(education: list) -> str:
    if not education:
        return "Not provided"
    lines = []
    for e in education:
        line = f"- {e.get('degree', '')} in {e.get('field', '')} | {e.get('institution', '')} | {e.get('year_start', '')}–{e.get('year_end', '')} | GPA: {e.get('gpa', 'N/A')}"
        lines.append(line)
    return "\n".join(lines)


def _format_experience(experience: list) -> str:
    if not experience:
        return "Not provided"
    lines = []
    for e in experience:
        lines.append(f"- {e.get('role', '')} at {e.get('company', '')} ({e.get('duration', '')}): {e.get('description', '')}")
    return "\n".join(lines)


def _format_projects(projects: list) -> str:
    if not projects:
        return "Not provided"
    lines = []
    for p in projects:
        lines.append(f"- {p.get('name', '')} | {p.get('tech_stack', '')} | {p.get('link', '')} — {p.get('description', '')}")
    return "\n".join(lines)


def _format_internships(internships: list) -> str:
    if not internships:
        return "Not provided"
    lines = []
    for i in internships:
        lines.append(f"- {i.get('role', '')} at {i.get('company', '')} ({i.get('duration', '')}): {i.get('description', '')}")
    return "\n".join(lines)


def _format_certs(certifications: list) -> str:
    if not certifications:
        return "Not provided"
    lines = []
    for c in certifications:
        lines.append(f"- {c.get('name', '')} by {c.get('issuer', '')} ({c.get('year', '')})")
    return "\n".join(lines)
