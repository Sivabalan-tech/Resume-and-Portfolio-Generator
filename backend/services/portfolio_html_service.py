"""
Portfolio HTML Service — generates a complete, self-contained single-page portfolio website.
All CSS is inlined. Zero external dependencies. Fully downloadable and hostable.
"""


def generate_portfolio_html(portfolio: dict, profile: dict) -> str:
    """
    Convert generated portfolio content + user profile into a beautiful
    single-file HTML/CSS portfolio website.

    Args:
        portfolio: dict from generate_portfolio() containing all text sections
        profile:   user profile dict (personal_info, skills, projects, etc.)

    Returns:
        Complete HTML string ready to be saved as .html
    """
    pi = profile.get("personal_info", {})
    name = pi.get("name", "My Portfolio")
    email = pi.get("email", "")
    phone = pi.get("phone", "")
    linkedin = pi.get("linkedin", "")
    github = pi.get("github", "")
    website = pi.get("website", "")
    location = pi.get("location", "")

    skills = profile.get("skills", [])
    projects = portfolio.get("project_descriptions", [])
    about_me = portfolio.get("about_me", "")
    bio = portfolio.get("professional_bio", "")
    linkedin_summary = portfolio.get("linkedin_summary", "")
    github_highlights = portfolio.get("github_highlights", "")

    # ── Skills HTML ──────────────────────────────────────────────────────────
    skills_html = "".join(f'<span class="skill-chip">{s}</span>' for s in skills)

    # ── Projects HTML ─────────────────────────────────────────────────────────
    projects_html = ""
    for i, proj in enumerate(projects):
        p_name = proj.get("name", f"Project {i+1}")
        p_desc = proj.get("description", "")
        # Try to get tech stack and link from profile if available
        profile_projects = profile.get("projects", [])
        tech = ""
        link = ""
        for pp in profile_projects:
            if pp.get("name", "").lower() == p_name.lower():
                tech = pp.get("tech_stack", "")
                link = pp.get("link", "")
                break
        link_html = f'<a href="{link}" target="_blank" class="proj-link">🔗 View Project</a>' if link else ""
        tech_html = f'<p class="proj-tech">🛠 {tech}</p>' if tech else ""
        projects_html += f"""
        <div class="project-card">
            <div class="proj-header">
                <h3>{p_name}</h3>
                {link_html}
            </div>
            {tech_html}
            <p class="proj-desc">{p_desc}</p>
        </div>"""

    # ── Contact links HTML ───────────────────────────────────────────────────
    contacts = []
    if email:    contacts.append(f'<a href="mailto:{email}" class="contact-btn">📧 Email Me</a>')
    if linkedin: contacts.append(f'<a href="{linkedin}" target="_blank" class="contact-btn linkedin">💼 LinkedIn</a>')
    if github:   contacts.append(f'<a href="{github}" target="_blank" class="contact-btn github">🐙 GitHub</a>')
    if website:  contacts.append(f'<a href="{website}" target="_blank" class="contact-btn">🌐 Website</a>')
    contacts_html = "\n".join(contacts)

    meta_info = []
    if location: meta_info.append(f"📍 {location}")
    if phone:    meta_info.append(f"📞 {phone}")
    meta_html = "  |  ".join(meta_info)

    # ── Github section ───────────────────────────────────────────────────────
    github_section = ""
    if github_highlights:
        github_section = f"""
    <section id="github" class="section alt-bg">
        <div class="container">
            <h2 class="section-title">🐙 GitHub Highlights</h2>
            <div class="github-card">
                <pre class="github-text">{github_highlights}</pre>
                {f'<a href="{github}" target="_blank" class="btn-outline">View GitHub Profile →</a>' if github else ""}
            </div>
        </div>
    </section>"""

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{name} — Portfolio</title>
    <style>
        /* ── Reset & Base ─────────────────────────────────── */
        *, *::before, *::after {{ box-sizing: border-box; margin: 0; padding: 0; }}
        :root {{
            --bg: #0f172a;
            --bg2: #1e293b;
            --surface: rgba(30, 41, 59, 0.8);
            --border: rgba(99, 102, 241, 0.2);
            --accent: #6366f1;
            --accent2: #8b5cf6;
            --accent3: #06b6d4;
            --text: #e2e8f0;
            --text2: #94a3b8;
            --green: #10b981;
            --radius: 16px;
        }}
        html {{ scroll-behavior: smooth; }}
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background: var(--bg);
            color: var(--text);
            line-height: 1.7;
        }}

        /* ── Noise texture overlay ────────────────────────── */
        body::before {{
            content: '';
            position: fixed; inset: 0; z-index: -1;
            background: radial-gradient(ellipse at 20% 20%, rgba(99,102,241,0.12) 0%, transparent 60%),
                        radial-gradient(ellipse at 80% 80%, rgba(139,92,246,0.10) 0%, transparent 60%);
        }}

        /* ── Nav ──────────────────────────────────────────── */
        nav {{
            position: fixed; top: 0; width: 100%; z-index: 100;
            background: rgba(15,23,42,0.85);
            backdrop-filter: blur(12px);
            border-bottom: 1px solid var(--border);
            padding: 0 2rem;
            display: flex; align-items: center; justify-content: space-between;
            height: 64px;
        }}
        .nav-brand {{
            font-size: 1.2rem; font-weight: 800;
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .nav-links {{ display: flex; gap: 2rem; list-style: none; }}
        .nav-links a {{
            color: var(--text2); text-decoration: none; font-size: 0.9rem;
            transition: color 0.2s;
        }}
        .nav-links a:hover {{ color: var(--accent); }}

        /* ── Hero ─────────────────────────────────────────── */
        .hero {{
            min-height: 100vh;
            display: flex; align-items: center; justify-content: center;
            text-align: center; padding: 6rem 2rem 4rem;
            position: relative; overflow: hidden;
        }}
        .hero-avatar {{
            width: 100px; height: 100px; border-radius: 50%;
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            display: flex; align-items: center; justify-content: center;
            font-size: 2.5rem; font-weight: 900; margin: 0 auto 1.5rem;
            box-shadow: 0 0 40px rgba(99,102,241,0.4);
            animation: float 3s ease-in-out infinite;
        }}
        @keyframes float {{
            0%, 100% {{ transform: translateY(0); }}
            50% {{ transform: translateY(-10px); }}
        }}
        .hero h1 {{
            font-size: clamp(2.5rem, 6vw, 5rem); font-weight: 900;
            line-height: 1.1; margin-bottom: 1rem;
            background: linear-gradient(135deg, var(--text), var(--accent), var(--accent2));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .hero-meta {{ color: var(--text2); margin-bottom: 1.5rem; font-size: 0.95rem; }}
        .hero-bio {{
            max-width: 650px; margin: 0 auto 2.5rem;
            color: var(--text2); font-size: 1.05rem;
        }}
        .hero-cta {{ display: flex; gap: 1rem; justify-content: center; flex-wrap: wrap; }}
        .btn-primary {{
            background: linear-gradient(135deg, var(--accent), var(--accent2));
            color: #fff; padding: 0.75rem 1.75rem;
            border-radius: 12px; text-decoration: none; font-weight: 600;
            transition: transform 0.2s, box-shadow 0.2s;
            box-shadow: 0 4px 20px rgba(99,102,241,0.3);
        }}
        .btn-primary:hover {{ transform: translateY(-2px); box-shadow: 0 8px 30px rgba(99,102,241,0.5); }}
        .btn-outline {{
            border: 1px solid var(--accent); color: var(--accent);
            padding: 0.75rem 1.75rem; border-radius: 12px; text-decoration: none;
            font-weight: 600; transition: all 0.2s; display: inline-block; margin-top: 1rem;
        }}
        .btn-outline:hover {{ background: var(--accent); color: #fff; }}

        /* ── Section ──────────────────────────────────────── */
        .section {{ padding: 6rem 2rem; }}
        .alt-bg {{ background: rgba(30,41,59,0.4); }}
        .container {{ max-width: 1000px; margin: 0 auto; }}
        .section-title {{
            font-size: 2rem; font-weight: 800; margin-bottom: 0.5rem;
            background: linear-gradient(135deg, var(--text), var(--accent));
            -webkit-background-clip: text; -webkit-text-fill-color: transparent;
            background-clip: text;
        }}
        .section-subtitle {{
            color: var(--text2); margin-bottom: 3rem; font-size: 0.95rem;
        }}

        /* ── About ────────────────────────────────────────── */
        .about-text {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius); padding: 2rem;
            white-space: pre-wrap; line-height: 1.8;
        }}

        /* ── Skills ───────────────────────────────────────── */
        .skills-grid {{ display: flex; flex-wrap: wrap; gap: 0.75rem; }}
        .skill-chip {{
            background: rgba(99,102,241,0.15);
            border: 1px solid rgba(99,102,241,0.3);
            color: #a5b4fc; padding: 0.4rem 1rem;
            border-radius: 999px; font-size: 0.85rem; font-weight: 500;
            transition: all 0.2s;
        }}
        .skill-chip:hover {{
            background: rgba(99,102,241,0.3);
            transform: translateY(-2px);
        }}

        /* ── Projects ─────────────────────────────────────── */
        .projects-grid {{ display: grid; grid-template-columns: repeat(auto-fill, minmax(280px, 1fr)); gap: 1.5rem; }}
        .project-card {{
            background: var(--surface);
            border: 1px solid var(--border);
            border-radius: var(--radius); padding: 1.5rem;
            transition: transform 0.2s, border-color 0.2s, box-shadow 0.2s;
        }}
        .project-card:hover {{
            transform: translateY(-4px);
            border-color: var(--accent);
            box-shadow: 0 8px 30px rgba(99,102,241,0.2);
        }}
        .proj-header {{ display: flex; justify-content: space-between; align-items: flex-start; gap: 1rem; margin-bottom: 0.5rem; }}
        .proj-header h3 {{ font-size: 1rem; font-weight: 700; }}
        .proj-link {{
            color: var(--accent3); font-size: 0.8rem; text-decoration: none;
            white-space: nowrap; border: 1px solid rgba(6,182,212,0.3);
            padding: 0.2rem 0.6rem; border-radius: 6px;
        }}
        .proj-tech {{ color: var(--text2); font-size: 0.8rem; margin-bottom: 0.75rem; }}
        .proj-desc {{ color: var(--text2); font-size: 0.875rem; line-height: 1.6; }}

        /* ── LinkedIn Summary ─────────────────────────────── */
        .linkedin-card {{
            background: linear-gradient(135deg, rgba(10,102,194,0.1), rgba(99,102,241,0.1));
            border: 1px solid rgba(10,102,194,0.3);
            border-radius: var(--radius); padding: 2rem;
        }}
        .linkedin-card p {{ white-space: pre-wrap; line-height: 1.8; color: var(--text2); }}

        /* ── GitHub ───────────────────────────────────────── */
        .github-card {{
            background: rgba(30,41,59,0.8);
            border: 1px solid rgba(99,102,241,0.2);
            border-radius: var(--radius); padding: 2rem;
        }}
        .github-text {{
            font-family: 'Courier New', monospace; font-size: 0.85rem;
            white-space: pre-wrap; color: var(--text2); margin-bottom: 1.5rem;
        }}

        /* ── Contact ──────────────────────────────────────── */
        .contact-btns {{ display: flex; gap: 1rem; flex-wrap: wrap; justify-content: center; margin-top: 2rem; }}
        .contact-btn {{
            display: inline-flex; align-items: center; gap: 0.5rem;
            padding: 0.8rem 1.5rem; border-radius: 12px;
            text-decoration: none; font-weight: 600; font-size: 0.9rem;
            border: 1px solid var(--border); color: var(--text);
            background: var(--surface); transition: all 0.2s;
        }}
        .contact-btn:hover {{ border-color: var(--accent); color: var(--accent); transform: translateY(-2px); }}
        .contact-btn.linkedin {{ border-color: rgba(10,102,194,0.5); }}
        .contact-btn.github {{ border-color: rgba(255,255,255,0.2); }}

        /* ── Footer ───────────────────────────────────────── */
        footer {{
            text-align: center; padding: 2rem;
            border-top: 1px solid var(--border); color: var(--text2); font-size: 0.85rem;
        }}

        /* ── Responsive ───────────────────────────────────── */
        @media (max-width: 640px) {{
            .nav-links {{ display: none; }}
            .hero h1 {{ font-size: 2.2rem; }}
        }}
    </style>
</head>
<body>
    <!-- Navigation -->
    <nav>
        <div class="nav-brand">{name}</div>
        <ul class="nav-links">
            <li><a href="#about">About</a></li>
            <li><a href="#skills">Skills</a></li>
            <li><a href="#projects">Projects</a></li>
            <li><a href="#contact">Contact</a></li>
        </ul>
    </nav>

    <!-- Hero -->
    <section class="hero">
        <div>
            <div class="hero-avatar">{name[0].upper() if name else "👤"}</div>
            <h1>{name}</h1>
            <p class="hero-meta">{meta_html}</p>
            <p class="hero-bio">{bio or about_me}</p>
            <div class="hero-cta">
                {f'<a href="#{{}}" class="btn-primary contact-btn" onclick="document.getElementById(\'contact\').scrollIntoView()" href="#contact">Get In Touch →</a>'.format("") if email else ""}
                {f'<a href="{github}" target="_blank" class="btn-outline">GitHub Profile</a>' if github else ""}
            </div>
        </div>
    </section>

    <!-- About -->
    <section id="about" class="section alt-bg">
        <div class="container">
            <h2 class="section-title">👋 About Me</h2>
            <p class="section-subtitle">Who I am and what I'm passionate about</p>
            <div class="about-text">{about_me}</div>
        </div>
    </section>

    <!-- Skills -->
    <section id="skills" class="section">
        <div class="container">
            <h2 class="section-title">🛠 Technical Skills</h2>
            <p class="section-subtitle">Technologies and tools I work with</p>
            <div class="skills-grid">{skills_html}</div>
        </div>
    </section>

    <!-- Projects -->
    <section id="projects" class="section alt-bg">
        <div class="container">
            <h2 class="section-title">🚀 Projects</h2>
            <p class="section-subtitle">Things I've built</p>
            <div class="projects-grid">{projects_html}</div>
        </div>
    </section>

    <!-- LinkedIn Summary -->
    <section id="linkedin" class="section">
        <div class="container">
            <h2 class="section-title">💼 LinkedIn Summary</h2>
            <p class="section-subtitle">My professional narrative</p>
            <div class="linkedin-card">
                <p>{linkedin_summary}</p>
            </div>
        </div>
    </section>

    {github_section}

    <!-- Contact -->
    <section id="contact" class="section alt-bg">
        <div class="container" style="text-align:center;">
            <h2 class="section-title">📬 Get In Touch</h2>
            <p class="section-subtitle">Open to opportunities and collaborations</p>
            <div class="contact-btns">
                {contacts_html}
            </div>
        </div>
    </section>

    <!-- Footer -->
    <footer>
        <p>© 2026 {name} — Portfolio generated with AI Resume & Portfolio Builder</p>
    </footer>
</body>
</html>"""
