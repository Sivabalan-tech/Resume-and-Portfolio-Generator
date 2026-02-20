"use client";
/**
 * Profile Page — multi-section career profile builder.
 * Saves all data to backend as structured JSON.
 */
import { useState, useEffect } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { profileApi } from "@/lib/api";
import toast from "react-hot-toast";

interface ProfileData {
    personal_info: { name: string; email: string; phone: string; linkedin: string; github: string; location: string; website: string; summary: string; };
    skills: string[];
    education: { institution: string; degree: string; field: string; year_start: string; year_end: string; gpa: string; }[];
    experience: { company: string; role: string; duration: string; description: string; location: string; }[];
    projects: { name: string; tech_stack: string; description: string; link: string; }[];
    certifications: { name: string; issuer: string; year: string; link: string; }[];
    internships: { company: string; role: string; duration: string; description: string; }[];
    achievements: string;
}

const emptyProfile: ProfileData = {
    personal_info: { name: "", email: "", phone: "", linkedin: "", github: "", location: "", website: "", summary: "" },
    skills: [],
    education: [{ institution: "", degree: "", field: "", year_start: "", year_end: "", gpa: "" }],
    experience: [],
    projects: [],
    certifications: [],
    internships: [],
    achievements: "",
};

const tabs = ["Personal", "Skills", "Education", "Experience", "Projects", "Certifications", "Internships"];

export default function ProfilePage() {
    const [profile, setProfile] = useState<ProfileData>(emptyProfile);
    const [activeTab, setActiveTab] = useState("Personal");
    const [loading, setLoading] = useState(true);
    const [saving, setSaving] = useState(false);
    const [skillInput, setSkillInput] = useState("");

    useEffect(() => {
        profileApi.get().then(r => {
            if (r.data.personal_info) {
                setProfile({
                    personal_info: r.data.personal_info || emptyProfile.personal_info,
                    skills: r.data.skills || [],
                    education: r.data.education?.length ? r.data.education : emptyProfile.education,
                    experience: r.data.experience || [],
                    projects: r.data.projects || [],
                    certifications: r.data.certifications || [],
                    internships: r.data.internships || [],
                    achievements: r.data.achievements || "",
                });
            }
            setLoading(false);
        }).catch(() => setLoading(false));
    }, []);

    const handleSave = async () => {
        setSaving(true);
        try {
            await profileApi.update(profile);
            toast.success("Profile saved! ✅");
        } catch { toast.error("Failed to save profile."); }
        finally { setSaving(false); }
    };

    const updatePersonal = (key: string, val: string) =>
        setProfile(p => ({ ...p, personal_info: { ...p.personal_info, [key]: val } }));

    const addSkill = () => {
        const s = skillInput.trim();
        if (s && !profile.skills.includes(s)) {
            setProfile(p => ({ ...p, skills: [...p.skills, s] }));
            setSkillInput("");
        }
    };

    const removeSkill = (sk: string) =>
        setProfile(p => ({ ...p, skills: p.skills.filter(s => s !== sk) }));

    const addItem = (key: keyof ProfileData, template: object) =>
        setProfile(p => ({ ...p, [key]: [...(p[key] as any[]), template] }));

    const updateItem = (key: keyof ProfileData, idx: number, field: string, val: string) =>
        setProfile(p => ({ ...p, [key]: (p[key] as any[]).map((item, i) => i === idx ? { ...item, [field]: val } : item) }));

    const removeItem = (key: keyof ProfileData, idx: number) =>
        setProfile(p => ({ ...p, [key]: (p[key] as any[]).filter((_, i) => i !== idx) }));

    if (loading) return <DashboardLayout><div className="flex items-center justify-center h-64"><div className="spinner" style={{ width: 40, height: 40 }} /></div></DashboardLayout>;

    return (
        <DashboardLayout>
            <div className="space-y-6 fade-in">
                <div className="flex justify-between items-center">
                    <div>
                        <h1 className="text-3xl font-bold">My Profile</h1>
                        <p style={{ color: "var(--text-secondary)" }}>Fill in your career details — used to generate resumes, cover letters, and portfolio content.</p>
                    </div>
                    <button onClick={handleSave} className="btn-primary" disabled={saving}>
                        {saving ? <><span className="spinner" style={{ width: 16, height: 16 }} /> Saving...</> : "💾 Save Profile"}
                    </button>
                </div>

                {/* Tabs */}
                <div className="flex gap-2 flex-wrap">
                    {tabs.map(tab => (
                        <button key={tab} onClick={() => setActiveTab(tab)}
                            className={activeTab === tab ? "btn-primary" : "btn-secondary"}
                            style={{ padding: "8px 16px", fontSize: "13px" }}>
                            {tab}
                        </button>
                    ))}
                </div>

                <div className="glass-card p-6">
                    {/* Personal Info */}
                    {activeTab === "Personal" && (
                        <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                            {[["name", "Full Name"], ["email", "Email"], ["phone", "Phone"], ["linkedin", "LinkedIn URL"], ["github", "GitHub URL"], ["location", "Location"], ["website", "Personal Website"]].map(([key, label]) => (
                                <div key={key}>
                                    <label className="form-label">{label}</label>
                                    <input className="form-input" value={(profile.personal_info as any)[key]}
                                        onChange={e => updatePersonal(key, e.target.value)} placeholder={label} />
                                </div>
                            ))}
                            <div className="md:col-span-2">
                                <label className="form-label">Professional Summary</label>
                                <textarea className="form-input" rows={4} value={profile.personal_info.summary}
                                    onChange={e => updatePersonal("summary", e.target.value)}
                                    placeholder="Write a 3-4 sentence professional summary..." />
                            </div>
                        </div>
                    )}

                    {/* Skills */}
                    {activeTab === "Skills" && (
                        <div className="space-y-4">
                            <div className="flex gap-3">
                                <input className="form-input" value={skillInput} onChange={e => setSkillInput(e.target.value)}
                                    onKeyDown={e => e.key === "Enter" && addSkill()}
                                    placeholder="Type a skill and press Enter (e.g., Python, React, Machine Learning)" />
                                <button onClick={addSkill} className="btn-primary" style={{ whiteSpace: "nowrap" }}>Add Skill</button>
                            </div>
                            <div className="flex flex-wrap gap-2">
                                {profile.skills.map(sk => (
                                    <div key={sk} className="badge badge-indigo flex items-center gap-2" style={{ padding: "6px 12px" }}>
                                        {sk}
                                        <button onClick={() => removeSkill(sk)} style={{ color: "#818cf8", fontWeight: "bold" }}>×</button>
                                    </div>
                                ))}
                            </div>
                        </div>
                    )}

                    {/* Education */}
                    {activeTab === "Education" && (
                        <div className="space-y-4">
                            {profile.education.map((edu, i) => (
                                <div key={i} className="stat-card space-y-3">
                                    <div className="flex justify-between"><span className="font-medium">Education #{i + 1}</span>
                                        <button onClick={() => removeItem("education", i)} style={{ color: "var(--danger)", fontSize: "12px" }}>Remove</button></div>
                                    <div className="grid grid-cols-2 gap-3">
                                        {[["institution", "Institution"], ["degree", "Degree"], ["field", "Field of Study"], ["year_start", "Start Year"], ["year_end", "End Year"], ["gpa", "GPA"]].map(([k, l]) => (
                                            <div key={k}><label className="form-label">{l}</label>
                                                <input className="form-input" value={edu[k as keyof typeof edu]} onChange={e => updateItem("education", i, k, e.target.value)} placeholder={l} /></div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                            <button onClick={() => addItem("education", { institution: "", degree: "", field: "", year_start: "", year_end: "", gpa: "" })} className="btn-secondary">+ Add Education</button>
                        </div>
                    )}

                    {/* Experience */}
                    {activeTab === "Experience" && (
                        <div className="space-y-4">
                            {profile.experience.map((exp, i) => (
                                <div key={i} className="stat-card space-y-3">
                                    <div className="flex justify-between"><span className="font-medium">Experience #{i + 1}</span>
                                        <button onClick={() => removeItem("experience", i)} style={{ color: "var(--danger)", fontSize: "12px" }}>Remove</button></div>
                                    <div className="grid grid-cols-2 gap-3">
                                        {[["company", "Company"], ["role", "Job Role"], ["duration", "Duration"], ["location", "Location"]].map(([k, l]) => (
                                            <div key={k}><label className="form-label">{l}</label>
                                                <input className="form-input" value={exp[k as keyof typeof exp]} onChange={e => updateItem("experience", i, k, e.target.value)} placeholder={l} /></div>
                                        ))}
                                    </div>
                                    <div><label className="form-label">Description (bullet points, achievements)</label>
                                        <textarea className="form-input" rows={3} value={exp.description} onChange={e => updateItem("experience", i, "description", e.target.value)} /></div>
                                </div>
                            ))}
                            <button onClick={() => addItem("experience", { company: "", role: "", duration: "", description: "", location: "" })} className="btn-secondary">+ Add Experience</button>
                        </div>
                    )}

                    {/* Projects */}
                    {activeTab === "Projects" && (
                        <div className="space-y-4">
                            {profile.projects.map((proj, i) => (
                                <div key={i} className="stat-card space-y-3">
                                    <div className="flex justify-between"><span className="font-medium">Project #{i + 1}</span>
                                        <button onClick={() => removeItem("projects", i)} style={{ color: "var(--danger)", fontSize: "12px" }}>Remove</button></div>
                                    <div className="grid grid-cols-2 gap-3">
                                        {[["name", "Project Name"], ["tech_stack", "Tech Stack"], ["link", "GitHub / Live Link"]].map(([k, l]) => (
                                            <div key={k}><label className="form-label">{l}</label>
                                                <input className="form-input" value={proj[k as keyof typeof proj]} onChange={e => updateItem("projects", i, k, e.target.value)} placeholder={l} /></div>
                                        ))}
                                    </div>
                                    <div><label className="form-label">Description</label>
                                        <textarea className="form-input" rows={2} value={proj.description} onChange={e => updateItem("projects", i, "description", e.target.value)} /></div>
                                </div>
                            ))}
                            <button onClick={() => addItem("projects", { name: "", tech_stack: "", description: "", link: "" })} className="btn-secondary">+ Add Project</button>
                        </div>
                    )}

                    {/* Certifications */}
                    {activeTab === "Certifications" && (
                        <div className="space-y-4">
                            {profile.certifications.map((cert, i) => (
                                <div key={i} className="stat-card space-y-3">
                                    <div className="flex justify-between"><span className="font-medium">Certification #{i + 1}</span>
                                        <button onClick={() => removeItem("certifications", i)} style={{ color: "var(--danger)", fontSize: "12px" }}>Remove</button></div>
                                    <div className="grid grid-cols-2 gap-3">
                                        {[["name", "Certification Name"], ["issuer", "Issuer"], ["year", "Year"], ["link", "Link"]].map(([k, l]) => (
                                            <div key={k}><label className="form-label">{l}</label>
                                                <input className="form-input" value={cert[k as keyof typeof cert]} onChange={e => updateItem("certifications", i, k, e.target.value)} placeholder={l} /></div>
                                        ))}
                                    </div>
                                </div>
                            ))}
                            <button onClick={() => addItem("certifications", { name: "", issuer: "", year: "", link: "" })} className="btn-secondary">+ Add Certification</button>
                        </div>
                    )}

                    {/* Internships */}
                    {activeTab === "Internships" && (
                        <div className="space-y-4">
                            {profile.internships.map((intern, i) => (
                                <div key={i} className="stat-card space-y-3">
                                    <div className="flex justify-between"><span className="font-medium">Internship #{i + 1}</span>
                                        <button onClick={() => removeItem("internships", i)} style={{ color: "var(--danger)", fontSize: "12px" }}>Remove</button></div>
                                    <div className="grid grid-cols-2 gap-3">
                                        {[["company", "Company"], ["role", "Role"], ["duration", "Duration"]].map(([k, l]) => (
                                            <div key={k}><label className="form-label">{l}</label>
                                                <input className="form-input" value={intern[k as keyof typeof intern]} onChange={e => updateItem("internships", i, k, e.target.value)} placeholder={l} /></div>
                                        ))}
                                    </div>
                                    <div><label className="form-label">Description</label>
                                        <textarea className="form-input" rows={2} value={intern.description} onChange={e => updateItem("internships", i, "description", e.target.value)} /></div>
                                </div>
                            ))}
                            <button onClick={() => addItem("internships", { company: "", role: "", duration: "", description: "" })} className="btn-secondary">+ Add Internship</button>
                        </div>
                    )}
                </div>

                {/* Achievements (always visible) */}
                <div className="glass-card p-6">
                    <label className="form-label text-base font-semibold text-white">Achievements & Extra-curriculars</label>
                    <textarea className="form-input mt-2" rows={3} value={profile.achievements}
                        onChange={e => setProfile(p => ({ ...p, achievements: e.target.value }))}
                        placeholder="Awards, competitions, publications, volunteer work..." />
                </div>
            </div>
        </DashboardLayout>
    );
}
