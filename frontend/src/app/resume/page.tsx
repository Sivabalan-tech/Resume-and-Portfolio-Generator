"use client";
/**
 * Resume Generator Page — generate ATS-optimized resume and download as PDF.
 */
import { useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { resumeApi, pdfApi } from "@/lib/api";
import ReactMarkdown from "react-markdown";
import toast from "react-hot-toast";

export default function ResumePage() {
    const [jobRole, setJobRole] = useState("");
    const [jobDesc, setJobDesc] = useState("");
    const [extra, setExtra] = useState("");
    const [result, setResult] = useState<{ markdown: string; id: number } | null>(null);
    const [loading, setLoading] = useState(false);
    const [downloading, setDownloading] = useState(false);

    const generate = async () => {
        if (!jobRole.trim()) { toast.error("Please enter a job role."); return; }
        setLoading(true);
        setResult(null);
        try {
            const res = await resumeApi.generate({ job_role: jobRole, job_description: jobDesc, extra_instructions: extra });
            setResult({ markdown: res.data.resume_markdown, id: res.data.history_id });
            toast.success("Resume generated! ✅");
        } catch (err: any) {
            toast.error(err.response?.data?.detail || "Generation failed. Make sure your profile is filled in.");
        } finally { setLoading(false); }
    };

    const downloadPdf = async () => {
        if (!result) return;
        setDownloading(true);
        try {
            const res = await pdfApi.download(result.markdown, jobRole);
            const url = URL.createObjectURL(res.data);
            const a = document.createElement("a");
            a.href = url;
            a.download = `${jobRole.replace(/\s+/g, "_")}_resume.pdf`;
            a.click();
            URL.revokeObjectURL(url);
            toast.success("PDF downloaded! 📄");
        } catch { toast.error("PDF download failed."); }
        finally { setDownloading(false); }
    };

    return (
        <DashboardLayout>
            <div className="space-y-6 fade-in">
                <div>
                    <h1 className="text-3xl font-bold">Resume Generator</h1>
                    <p style={{ color: "var(--text-secondary)" }}>Generate an ATS-optimized resume tailored to your target job role.</p>
                </div>

                {/* Input Section */}
                <div className="glass-card p-6 space-y-4">
                    <div>
                        <label className="form-label">Target Job Role *</label>
                        <input className="form-input" value={jobRole} onChange={e => setJobRole(e.target.value)}
                            placeholder="e.g., Backend Developer, Data Scientist, ML Engineer" />
                    </div>
                    <div>
                        <label className="form-label">Job Description (optional — improves keyword match)</label>
                        <textarea className="form-input" rows={5} value={jobDesc} onChange={e => setJobDesc(e.target.value)}
                            placeholder="Paste the job description here for better ATS keyword optimization..." />
                    </div>
                    <div>
                        <label className="form-label">Extra Instructions (optional)</label>
                        <input className="form-input" value={extra} onChange={e => setExtra(e.target.value)}
                            placeholder="e.g., Focus on AI/ML experience, include leadership roles, make it 1 page" />
                    </div>
                    <button onClick={generate} className="btn-primary" disabled={loading}>
                        {loading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Generating with AI...</> : "🤖 Generate ATS Resume"}
                    </button>
                </div>

                {/* Result */}
                {loading && (
                    <div className="glass-card p-16 flex flex-col items-center gap-4">
                        <div className="spinner" style={{ width: 48, height: 48 }} />
                        <p style={{ color: "var(--text-secondary)" }}>Gemini AI is crafting your ATS-optimized resume...</p>
                    </div>
                )}

                {result && !loading && (
                    <div className="glass-card p-6 space-y-4 fade-in">
                        <div className="flex justify-between items-center">
                            <h2 className="text-xl font-bold">✅ Your Resume</h2>
                            <div className="flex gap-3">
                                <button onClick={() => { navigator.clipboard.writeText(result.markdown); toast.success("Copied!"); }}
                                    className="btn-secondary">📋 Copy Markdown</button>
                                <button onClick={downloadPdf} className="btn-primary" disabled={downloading}>
                                    {downloading ? <><span className="spinner" style={{ width: 16, height: 16 }} /> Generating PDF...</> : "PDF ↓ Download"}
                                </button>
                            </div>
                        </div>
                        <div className="resume-preview border rounded-xl p-6" style={{ borderColor: "var(--border)", maxHeight: "70vh", overflowY: "auto" }}>
                            <ReactMarkdown>{result.markdown}</ReactMarkdown>
                        </div>
                    </div>
                )}
            </div>
        </DashboardLayout>
    );
}
