"""
Portfolio Content Prompt — generates structured portfolio content sections.
Uses labeled sections parseable by ai_service._parse_portfolio_sections().
"""


def build_portfolio_prompt(profile: dict) -> str:
    """
    Build the Gemini prompt for portfolio content generation.
    Returns content with labeled sections: [ABOUT_ME], [BIO], [LINKEDIN], [PROJECT:name], [GITHUB]
    """
    personal = profile.get("personal_info", {})
    name = personal.get("name", "Developer")
    summary = personal.get("summary", "")
    github = personal.get("github", "")
    linkedin = personal.get("linkedin", "")

    skills = profile.get("skills", [])
    projects = profile.get("projects", [])
    experience = profile.get("experience", [])
    certifications = profile.get("certifications", [])

    skills_str = ", ".join(skills[:20]) if skills else "Various technologies"

    projects_str = ""
    for p in projects[:6]:
        projects_str += f"\n- {p.get('name', '')}: Tech: {p.get('tech_stack', '')} | Description: {p.get('description', '')} | Link: {p.get('link', '')}"

    exp_str = ""
    for e in experience[:3]:
        exp_str += f"\n- {e.get('role', '')} at {e.get('company', '')} ({e.get('duration', '')}): {e.get('description', '')}"

    project_names = [p.get("name", f"Project {i+1}") for i, p in enumerate(projects[:4])]

    return f"""You are a professional portfolio content writer for software developers.

Generate compelling portfolio website content for:
Name: {name}
Skills: {skills_str}
GitHub: {github}
LinkedIn: {linkedin}
Summary: {summary}
Experience: {exp_str}
Projects: {projects_str}

Generate content in the EXACT format below (keep the labels exactly as shown):

[ABOUT_ME]
Write a 150-200 word "About Me" section in first person. Engaging, professional, mentions top skills, passion for technology, and career goals. Suitable for a portfolio hero section.

[BIO]
Write a 80-100 word professional third-person bio. Like what you'd find on a conference speaker page or LinkedIn "About". Start with the name.

[LINKEDIN]
Write a 200-250 word LinkedIn "About" section in first person. Keyword-rich for recruiters. Include: role, top skills, achievements, and a call to connect.

{_project_sections(project_names)}

[GITHUB]
Write a 100-120 word GitHub profile README introduction. Engaging and technical. Mention primary languages/frameworks, what you build, and where to find the best projects.

Keep all content fresh, specific, and impressive. Avoid generic clichés."""


def _project_sections(project_names: list) -> str:
    """Generate [PROJECT:name] section placeholders for each project."""
    sections = []
    for name in project_names:
        sections.append(f"""[PROJECT:{name}]
Write a 60-80 word project description for "{name}". Cover: what problem it solves, what technologies were used, key features/achievements, and a link if available. Suitable for a portfolio card.""")
    return "\n\n".join(sections)
