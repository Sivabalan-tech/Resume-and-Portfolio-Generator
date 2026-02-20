"use client";
/**
 * ATS Analyzer Page — paste a job description and get an ATS match score.
 */
import { useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { atsApi } from "@/lib/api";
import toast from "react-hot-toast";

export default function ATSPage() {
    const [jobDesc, setJobDesc] = useState("");
    const [resumeText, setResumeText] = useState("");
    const [result, setResult] = useState<any>(null);
    const [loading, setLoading] = useState(false);

    const analyze = async () => {
        if (!jobDesc.trim()) { toast.error("Please paste a job description."); return; }
        setLoading(true);
        setResult(null);
        try {
            const res = await atsApi.analyze({ job_description: jobDesc, resume_text: resumeText || undefined });
            setResult(res.data);
            toast.success("Analysis complete! 🎯");
        } catch (err: any) {
            toast.error(err.response?.data?.detail || "ATS analysis failed. Please generate a resume first.");
        } finally { setLoading(false); }
    };

    const scoreColor = result
        ? result.score >= 70 ? "#10b981" : result.score >= 50 ? "#f59e0b" : "#ef4444"
        : "#6366f1";

    return (
        <DashboardLayout>
            <div className="space-y-6 fade-in">
                <div>
                    <h1 className="text-3xl font-bold">🎯 ATS Score Analyzer</h1>
                    <p style={{ color: "var(--text-secondary)" }}>
                        Analyze how well your resume matches a job description using SentenceTransformers semantic similarity.
                    </p>
                </div>

                <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
                    {/* Input */}
                    <div className="glass-card p-6 space-y-4">
                        <h2 className="font-semibold">Job Description *</h2>
                        <textarea className="form-input" rows={10} value={jobDesc} onChange={e => setJobDesc(e.target.value)}
                            placeholder="Paste the target job description here..." />
                        <h2 className="font-semibold">Resume Text (optional)</h2>
                        <textarea className="form-input" rows={4} value={resumeText} onChange={e => setResumeText(e.target.value)}
                            placeholder="Leave blank to use your latest generated resume automatically." />
                        <button onClick={analyze} className="btn-primary w-full justify-center" disabled={loading}>
                            {loading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Analyzing...</> : "🔍 Analyze ATS Match"}
                        </button>
                    </div>

                    {/* Result */}
                    <div className="space-y-4">
                        {loading && (
                            <div className="glass-card p-16 flex flex-col items-center gap-4">
                                <div className="spinner" style={{ width: 48, height: 48 }} />
                                <p style={{ color: "var(--text-secondary)" }}>Computing semantic similarity...</p>
                            </div>
                        )}

                        {result && !loading && (
                            <div className="fade-in space-y-4">
                                {/* Score Ring */}
                                <div className="glass-card p-6 flex flex-col items-center gap-4">
                                    <div className="score-ring pulse" style={{ background: `conic-gradient(${scoreColor} ${result.score}%, rgb(30,41,59) 0%)`, boxShadow: `0 0 30px ${scoreColor}40` }}>
                                        <div style={{ width: 110, height: 110, borderRadius: "50%", background: "var(--bg-secondary)", display: "flex", flexDirection: "column", alignItems: "center", justifyContent: "center" }}>
                                            <span style={{ fontSize: "28px", fontWeight: "800", color: scoreColor }}>{result.score}%</span>
                                            <span style={{ fontSize: "11px", color: "var(--text-secondary)" }}>ATS Match</span>
                                        </div>
                                    </div>
                                    <div className={`badge ${result.score >= 70 ? "badge-green" : result.score >= 50 ? "badge-amber" : "badge-red"}`} style={{ fontSize: "14px", padding: "6px 16px" }}>
                                        {result.score >= 70 ? "✅ Strong Match" : result.score >= 50 ? "⚠️ Partial Match" : "❌ Low Match"}
                                    </div>
                                </div>

                                {/* Keywords */}
                                <div className="glass-card p-5">
                                    <h3 className="font-semibold mb-3 text-green-400">✅ Matching Keywords ({result.matching_keywords.length})</h3>
                                    <div className="flex flex-wrap gap-2">
                                        {result.matching_keywords.map((kw: string) => (
                                            <span key={kw} className="badge badge-green">{kw}</span>
                                        ))}
                                    </div>
                                </div>

                                <div className="glass-card p-5">
                                    <h3 className="font-semibold mb-3 text-red-400">❌ Missing Keywords ({result.missing_keywords.length})</h3>
                                    <div className="flex flex-wrap gap-2">
                                        {result.missing_keywords.map((kw: string) => (
                                            <span key={kw} className="badge badge-red">{kw}</span>
                                        ))}
                                    </div>
                                </div>

                                <div className="glass-card p-5">
                                    <h3 className="font-semibold mb-3">💡 Improvement Suggestions</h3>
                                    <ul className="space-y-2">
                                        {result.improvement_suggestions.map((s: string, i: number) => (
                                            <li key={i} className="flex gap-2 text-sm" style={{ color: "var(--text-secondary)" }}>
                                                <span>→</span><span>{s}</span>
                                            </li>
                                        ))}
                                    </ul>
                                </div>
                            </div>
                        )}
                    </div>
                </div>
            </div>
        </DashboardLayout>
    );
}
