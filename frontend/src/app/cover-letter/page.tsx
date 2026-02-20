"use client";
/**
 * Cover Letter Generator Page.
 */
import { useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { coverLetterApi } from "@/lib/api";
import toast from "react-hot-toast";

export default function CoverLetterPage() {
    const [form, setForm] = useState({ company_name: "", job_role: "", job_description: "", hiring_manager: "" });
    const [result, setResult] = useState<string | null>(null);
    const [loading, setLoading] = useState(false);

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLTextAreaElement>) =>
        setForm(p => ({ ...p, [e.target.name]: e.target.value }));

    const generate = async () => {
        if (!form.company_name || !form.job_role || !form.job_description) {
            toast.error("Please fill in company, role, and job description."); return;
        }
        setLoading(true);
        setResult(null);
        try {
            const res = await coverLetterApi.generate(form);
            setResult(res.data.cover_letter);
            toast.success("Cover letter generated! ✉️");
        } catch (err: any) {
            toast.error(err.response?.data?.detail || "Generation failed. Fill in your profile first.");
        } finally { setLoading(false); }
    };

    return (
        <DashboardLayout>
            <div className="space-y-6 fade-in">
                <div>
                    <h1 className="text-3xl font-bold">✉️ Cover Letter Generator</h1>
                    <p style={{ color: "var(--text-secondary)" }}>Generate a tailored, professional cover letter for any company and role.</p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Form */}
                    <div className="glass-card p-6 space-y-4">
                        <div>
                            <label className="form-label">Company Name *</label>
                            <input className="form-input" name="company_name" value={form.company_name} onChange={handleChange} placeholder="Google, Microsoft, Startup X..." />
                        </div>
                        <div>
                            <label className="form-label">Job Role *</label>
                            <input className="form-input" name="job_role" value={form.job_role} onChange={handleChange} placeholder="Software Engineer, Data Analyst..." />
                        </div>
                        <div>
                            <label className="form-label">Hiring Manager Name (optional)</label>
                            <input className="form-input" name="hiring_manager" value={form.hiring_manager} onChange={handleChange} placeholder="John Smith (or leave blank)" />
                        </div>
                        <div>
                            <label className="form-label">Job Description *</label>
                            <textarea className="form-input" rows={8} name="job_description" value={form.job_description} onChange={handleChange}
                                placeholder="Paste the full job description here..." />
                        </div>
                        <button onClick={generate} className="btn-primary w-full justify-center" disabled={loading}>
                            {loading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Generating...</> : "✉️ Generate Cover Letter"}
                        </button>
                    </div>

                    {/* Result */}
                    <div>
                        {loading && (
                            <div className="glass-card p-16 h-full flex flex-col items-center justify-center gap-4">
                                <div className="spinner" style={{ width: 48, height: 48 }} />
                                <p style={{ color: "var(--text-secondary)" }}>Gemini AI is writing your cover letter...</p>
                            </div>
                        )}
                        {result && !loading && (
                            <div className="glass-card p-6 space-y-4 fade-in h-full">
                                <div className="flex justify-between items-center">
                                    <h2 className="font-bold text-xl">✅ Your Cover Letter</h2>
                                    <button onClick={() => { navigator.clipboard.writeText(result); toast.success("Copied!"); }} className="btn-secondary">📋 Copy</button>
                                </div>
                                <div className="rounded-xl p-5 text-sm leading-7 overflow-y-auto" style={{ background: "rgba(15,23,42,0.6)", border: "1px solid var(--border)", maxHeight: "60vh", whiteSpace: "pre-wrap", color: "var(--text-primary)" }}>
                                    {result}
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}
