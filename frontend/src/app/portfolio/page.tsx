"use client";
/**
 * Portfolio Content Generator Page.
 * Includes AI content generation + downloadable HTML/CSS website.
 */
import { useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { portfolioApi } from "@/lib/api";
import toast from "react-hot-toast";

interface PortfolioData {
    about_me: string;
    professional_bio: string;
    linkedin_summary: string;
    project_descriptions: { name: string; description: string }[];
    github_highlights: string;
    history_id?: number;
}

export default function PortfolioPage() {
    const [result, setResult] = useState<PortfolioData | null>(null);
    const [loading, setLoading] = useState(false);
    const [downloading, setDownloading] = useState(false);
    const [activeSection, setActiveSection] = useState("about_me");

    const generate = async () => {
        setLoading(true);
        setResult(null);
        try {
            const res = await portfolioApi.generate();
            setResult(res.data);
            toast.success("Portfolio content generated! 🌐");
        } catch (err: any) {
            toast.error(err.response?.data?.detail || "Generation failed. Fill in your profile first.");
        } finally { setLoading(false); }
    };

    const downloadWebsite = async () => {
        setDownloading(true);
        try {
            const res = await portfolioApi.download();
            // Create a blob and trigger browser download
            const blob = new Blob([res.data], { type: "text/html" });
            const url = window.URL.createObjectURL(blob);
            const a = document.createElement("a");
            a.href = url;
            const cd = res.headers?.["content-disposition"] || "";
            const match = cd.match(/filename="([^"]+)"/);
            a.download = match ? match[1] : "portfolio.html";
            document.body.appendChild(a);
            a.click();
            a.remove();
            window.URL.revokeObjectURL(url);
            toast.success("Portfolio website downloaded! Open the .html file in any browser. 🌐");
        } catch (err: any) {
            toast.error(err.response?.data?.detail || "Download failed.");
        } finally { setDownloading(false); }
    };

    const copyText = (text: string) => {
        navigator.clipboard.writeText(text);
        toast.success("Copied to clipboard!");
    };

    const sections = result ? [
        { key: "about_me", label: "👋 About Me", content: result.about_me },
        { key: "professional_bio", label: "🧑‍💼 Professional Bio", content: result.professional_bio },
        { key: "linkedin_summary", label: "💼 LinkedIn Summary", content: result.linkedin_summary },
        { key: "github_highlights", label: "🐙 GitHub README", content: result.github_highlights },
    ] : [];

    return (
        <DashboardLayout>
            <div className="space-y-6 fade-in">
                <div className="flex flex-col sm:flex-row justify-between items-start sm:items-center gap-4">
                    <div>
                        <h1 className="text-3xl font-bold">🌐 Portfolio Generator</h1>
                        <p style={{ color: "var(--text-secondary)" }}>
                            Generate portfolio content + download a complete website you can host anywhere.
                        </p>
                    </div>
                    <div className="flex gap-3 flex-wrap">
                        <button onClick={generate} className="btn-primary" disabled={loading || downloading}>
                            {loading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Generating...</> : "✨ Generate Content"}
                        </button>
                        <button
                            onClick={downloadWebsite}
                            className="btn-secondary"
                            disabled={loading || downloading}
                            style={{
                                background: "linear-gradient(135deg, #10b981, #059669)",
                                color: "#fff",
                                border: "none",
                                padding: "0.6rem 1.2rem",
                                borderRadius: "10px",
                                fontWeight: 600,
                                cursor: downloading ? "not-allowed" : "pointer",
                                opacity: downloading ? 0.7 : 1,
                            }}
                        >
                            {downloading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Building...</> : "⬇ Download Website"}
                        </button>
                    </div>
                </div>

                {/* Info banner */}
                {!result && !loading && (
                    <div style={{
                        background: "linear-gradient(135deg, rgba(16,185,129,0.1), rgba(6,182,212,0.1))",
                        border: "1px solid rgba(16,185,129,0.3)",
                        borderRadius: "12px",
                        padding: "1rem 1.5rem",
                        display: "flex",
                        alignItems: "flex-start",
                        gap: "1rem",
                    }}>
                        <span style={{ fontSize: "1.5rem" }}>💡</span>
                        <div>
                            <p style={{ fontWeight: 600, marginBottom: "0.25rem" }}>Two ways to use this</p>
                            <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>
                                <strong>✨ Generate Content</strong> — Get AI-written text for About Me, LinkedIn, GitHub README, and project descriptions you can copy/paste.<br />
                                <strong>⬇ Download Website</strong> — Get a complete, beautiful HTML/CSS portfolio site (no code needed!) ready to host on GitHub Pages, Netlify, or Vercel.
                            </p>
                        </div>
                    </div>
                )}

                {loading && (
                    <div className="glass-card p-20 flex flex-col items-center gap-4">
                        <div className="spinner" style={{ width: 56, height: 56 }} />
                        <p style={{ color: "var(--text-secondary)" }}>Gemini AI is crafting your portfolio content...</p>
                    </div>
                )}

                {downloading && (
                    <div className="glass-card p-20 flex flex-col items-center gap-4">
                        <div className="spinner" style={{ width: 56, height: 56, borderColor: "#10b981", borderTopColor: "transparent" }} />
                        <p style={{ color: "var(--text-secondary)" }}>🏗 Building your portfolio website... this takes ~15 seconds</p>
                    </div>
                )}

                {result && !loading && !downloading && (
                    <div className="space-y-4 fade-in">
                        {/* Download prompt banner */}
                        <div style={{
                            background: "linear-gradient(135deg, rgba(16,185,129,0.15), rgba(6,182,212,0.1))",
                            border: "1px solid rgba(16,185,129,0.4)",
                            borderRadius: "12px",
                            padding: "1rem 1.5rem",
                            display: "flex",
                            alignItems: "center",
                            justifyContent: "space-between",
                            gap: "1rem",
                            flexWrap: "wrap",
                        }}>
                            <div>
                                <p style={{ fontWeight: 700, color: "#10b981" }}>✅ Content generated!</p>
                                <p style={{ color: "var(--text-secondary)", fontSize: "0.9rem" }}>
                                    Want a real website? Click "Download Website" to get a full HTML/CSS portfolio you can open, share, or host online.
                                </p>
                            </div>
                            <button
                                onClick={downloadWebsite}
                                disabled={downloading}
                                style={{
                                    background: "linear-gradient(135deg, #10b981, #059669)",
                                    color: "#fff",
                                    border: "none",
                                    padding: "0.7rem 1.4rem",
                                    borderRadius: "10px",
                                    fontWeight: 700,
                                    cursor: "pointer",
                                    whiteSpace: "nowrap",
                                    fontSize: "0.9rem",
                                }}
                            >
                                ⬇ Download .html Website
                            </button>
                        </div>

                        <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
                            {/* Section nav */}
                            <div className="space-y-2">
                                {sections.map(s => (
                                    <button key={s.key} onClick={() => setActiveSection(s.key)}
                                        className={"sidebar-link w-full text-left" + (activeSection === s.key ? " active" : "")}>
                                        {s.label}
                                    </button>
                                ))}
                                <div className="mt-4">
                                    <p className="form-label mb-2">📦 Project Descriptions</p>
                                    {result.project_descriptions.map((p, i) => (
                                        <button key={i} onClick={() => setActiveSection(`project_${i}`)}
                                            className={"sidebar-link w-full text-left text-xs" + (activeSection === `project_${i}` ? " active" : "")}>
                                            {p.name}
                                        </button>
                                    ))}
                                </div>
                            </div>

                            {/* Content display */}
                            <div className="lg:col-span-3 glass-card p-6 space-y-4">
                                {sections.filter(s => s.key === activeSection).map(s => (
                                    <div key={s.key} className="space-y-3">
                                        <div className="flex justify-between items-center">
                                            <h2 className="text-xl font-bold">{s.label}</h2>
                                            <button onClick={() => copyText(s.content)} className="btn-secondary">📋 Copy</button>
                                        </div>
                                        <div className="rounded-xl p-5 text-sm leading-7"
                                            style={{ background: "rgba(15,23,42,0.6)", border: "1px solid var(--border)", whiteSpace: "pre-wrap", color: "var(--text-primary)" }}>
                                            {s.content}
                                        </div>
                                    </div>
                                ))}
                                {result.project_descriptions.map((p, i) => (
                                    activeSection === `project_${i}` && (
                                        <div key={i} className="space-y-3">
                                            <div className="flex justify-between items-center">
                                                <h2 className="text-xl font-bold">📦 {p.name}</h2>
                                                <button onClick={() => copyText(p.description)} className="btn-secondary">📋 Copy</button>
                                            </div>
                                            <div className="rounded-xl p-5 text-sm leading-7"
                                                style={{ background: "rgba(15,23,42,0.6)", border: "1px solid var(--border)", whiteSpace: "pre-wrap", color: "var(--text-primary)" }}>
                                                {p.description}
                                            </div>
                                        </div>
                                    )
                                ))}
                            </div>
                        </div>
                    </div>
                )}

                {!result && !loading && !downloading && (
                    <div className="glass-card p-16 text-center">
                        <div className="text-6xl mb-4">🌐</div>
                        <h3 className="text-xl font-bold mb-2">Generate Your Portfolio</h3>
                        <p style={{ color: "var(--text-secondary)", maxWidth: 500, margin: "0 auto" }}>
                            Click <strong>✨ Generate Content</strong> to get AI-written text sections, or click <strong>⬇ Download Website</strong> to get a complete HTML/CSS portfolio site — no coding required!
                        </p>
                    </div>
                )}
            </div>
        </DashboardLayout>
    );
}
