"use client";
/**
 * Dashboard Page — overview stats, quick actions, and history.
 * Includes a modal viewer for cover letters and delete functionality.
 */
import { useEffect, useState } from "react";
import Link from "next/link";
import DashboardLayout from "@/components/DashboardLayout";
import { resumeApi, coverLetterApi } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import toast from "react-hot-toast";

interface HistoryItem {
    id: number; job_role: string | null; company_name: string | null;
    generation_type: string; ats_score: number | null; created_at: string;
}

const quickActions = [
    { href: "/resume", label: "Generate Resume", icon: "📄", desc: "ATS-optimized resume" },
    { href: "/cover-letter", label: "Write Cover Letter", icon: "✉️", desc: "Tailored to company" },
    { href: "/ats", label: "Analyze ATS Score", icon: "🎯", desc: "Match vs job description" },
    { href: "/portfolio", label: "Build Portfolio", icon: "🌐", desc: "Portfolio content" },
];

export default function DashboardPage() {
    const { user } = useAuth();
    const [history, setHistory] = useState<HistoryItem[]>([]);
    const [loading, setLoading] = useState(true);

    // Cover letter modal state
    const [modalOpen, setModalOpen] = useState(false);
    const [modalContent, setModalContent] = useState("");
    const [modalTitle, setModalTitle] = useState("");
    const [modalLoading, setModalLoading] = useState(false);

    useEffect(() => {
        loadHistory();
    }, []);

    const loadHistory = () => {
        setLoading(true);
        resumeApi.getHistory().then(r => {
            setHistory(r.data);
            setLoading(false);
        }).catch(() => setLoading(false));
    };

    const viewCoverLetter = async (item: HistoryItem) => {
        setModalTitle(`✉️ Cover Letter — ${item.company_name || ""}${item.job_role ? ` · ${item.job_role}` : ""}`);
        setModalContent("");
        setModalOpen(true);
        setModalLoading(true);
        try {
            const res = await coverLetterApi.getHistoryItem(item.id);
            setModalContent(res.data.cover_letter || "No content found.");
        } catch {
            toast.error("Failed to load cover letter.");
            setModalOpen(false);
        } finally {
            setModalLoading(false);
        }
    };

    const deleteItem = async (id: number) => {
        if (!window.confirm("Are you sure you want to delete this item? This cannot be undone.")) return;

        // Optimistic update
        setHistory(prev => prev.filter(item => item.id !== id));
        toast.success("Item deleted.");

        try {
            await resumeApi.deleteHistoryItem(id);
        } catch (err) {
            toast.error("Failed to delete item.");
            loadHistory(); // Revert on failure
        }
    };

    const copyContent = () => {
        navigator.clipboard.writeText(modalContent);
        toast.success("Copied to clipboard!");
    };

    const resumeCount = history.filter(h => h.generation_type === "resume").length;
    const coverLetterCount = history.filter(h => h.generation_type === "cover_letter").length;
    const avgScore = history.filter(h => h.ats_score).reduce((a, b) => a + (b.ats_score || 0), 0) / (history.filter(h => h.ats_score).length || 1);

    return (
        <DashboardLayout>
            <div className="space-y-8 fade-in">
                {/* Welcome */}
                <div>
                    <h1 className="text-3xl font-bold">Welcome back, <span className="gradient-text">{user?.full_name || "User"}</span> 👋</h1>
                    <p style={{ color: "var(--text-secondary)" }} className="mt-1">Ready to build your next opportunity?</p>
                </div>

                {/* Stats Cards */}
                <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                    {[
                        { label: "Resumes Generated", value: resumeCount, icon: "📄", color: "#6366f1" },
                        { label: "Cover Letters", value: coverLetterCount, icon: "✉️", color: "#8b5cf6" },
                        { label: "Avg ATS Score", value: `${Math.round(avgScore || 0)}%`, icon: "🎯", color: "#10b981" },
                        { label: "Total Generations", value: history.length, icon: "⚡", color: "#f59e0b" },
                    ].map(stat => (
                        <div key={stat.label} className="stat-card">
                            <div style={{ fontSize: "28px", color: stat.color, marginBottom: "8px" }}>{stat.icon}</div>
                            <div className="text-2xl font-bold">{loading ? "—" : stat.value}</div>
                            <div style={{ color: "var(--text-secondary)", fontSize: "13px", marginTop: "4px" }}>{stat.label}</div>
                        </div>
                    ))}
                </div>

                {/* Quick Actions */}
                <div>
                    <h2 className="text-xl font-bold mb-4">Quick Actions</h2>
                    <div className="grid grid-cols-2 md:grid-cols-4 gap-4">
                        {quickActions.map(action => (
                            <Link key={action.href} href={action.href}
                                className="glass-card p-5 group hover:border-indigo-500 transition-all duration-300 block"
                                style={{ textDecoration: "none" }}>
                                <div className="text-3xl mb-3">{action.icon}</div>
                                <div className="font-semibold text-sm group-hover:text-indigo-400 transition-colors">{action.label}</div>
                                <div style={{ color: "var(--text-secondary)", fontSize: "12px", marginTop: "4px" }}>{action.desc}</div>
                            </Link>
                        ))}
                    </div>
                </div>

                {/* Recent History */}
                <div>
                    <h2 className="text-xl font-bold mb-4">Recent Activity</h2>
                    {loading ? (
                        <div className="glass-card p-8 text-center"><div className="spinner mx-auto" /></div>
                    ) : history.length === 0 ? (
                        <div className="glass-card p-12 text-center">
                            <div className="text-5xl mb-4">✨</div>
                            <p className="font-medium">No generations yet — start by building your profile!</p>
                            <Link href="/profile" className="btn-primary mt-4 inline-flex">Go to Profile →</Link>
                        </div>
                    ) : (
                        <div className="glass-card overflow-hidden">
                            <table className="w-full text-sm">
                                <thead>
                                    <tr style={{ borderBottom: "1px solid var(--border)" }}>
                                        {["Type", "Role / Company", "ATS Score", "Date", "Action"].map(h => (
                                            <th key={h} className="text-left px-5 py-3" style={{ color: "var(--text-secondary)", fontWeight: 500 }}>{h}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {history.slice(0, 10).map(item => (
                                        <tr key={item.id} style={{ borderBottom: "1px solid rgba(51,65,85,0.5)" }} className="hover:bg-white/5 transition-colors">
                                            <td className="px-5 py-3">
                                                <span className={`badge badge-${item.generation_type === "resume" ? "indigo" : item.generation_type === "cover_letter" ? "amber" : "green"}`}>
                                                    {item.generation_type === "cover_letter" ? "Cover Letter"
                                                        : item.generation_type === "portfolio" ? "Portfolio"
                                                            : item.generation_type.charAt(0).toUpperCase() + item.generation_type.slice(1)}
                                                </span>
                                            </td>
                                            <td className="px-5 py-3" style={{ color: "var(--text-primary)" }}>
                                                {item.job_role && item.company_name
                                                    ? `${item.job_role} @ ${item.company_name}`
                                                    : item.job_role || item.company_name || "—"}
                                            </td>
                                            <td className="px-5 py-3">
                                                {item.ats_score ? (
                                                    <span className={`badge ${item.ats_score >= 70 ? "badge-green" : item.ats_score >= 50 ? "badge-amber" : "badge-red"}`}>
                                                        {item.ats_score}%
                                                    </span>
                                                ) : "—"}
                                            </td>
                                            <td className="px-5 py-3" style={{ color: "var(--text-secondary)" }}>
                                                {new Date(item.created_at).toLocaleDateString("en-IN", { day: "2-digit", month: "short", year: "numeric" })}
                                            </td>
                                            <td className="px-5 py-3">
                                                <div className="flex gap-2 items-center flex-wrap">
                                                    {/* {item.generation_type === "resume" && (
                                                        <a href={`/api/pdf/history/${item.id}`} target="_blank" rel="noreferrer"
                                                            className="text-xs font-medium text-indigo-400 hover:text-indigo-300 hover:underline transition-colors">
                                                            📥 PDF
                                                        </a>
                                                    )} */}
                                                    {item.generation_type === "cover_letter" && (
                                                        <button
                                                            onClick={() => viewCoverLetter(item)}
                                                            className="text-xs font-medium transition-colors"
                                                            style={{
                                                                color: "#f59e0b",
                                                                background: "rgba(245,158,11,0.1)",
                                                                border: "1px solid rgba(245,158,11,0.3)",
                                                                padding: "2px 10px",
                                                                borderRadius: "6px",
                                                                cursor: "pointer",
                                                            }}
                                                        >
                                                            👁 View
                                                        </button>
                                                    )}
                                                    {/* {item.generation_type === "portfolio" && (
                                                        <a href={`/api/portfolio/download/${item.id}`} target="_blank" rel="noreferrer"
                                                            className="text-xs font-medium text-emerald-400 hover:text-emerald-300 hover:underline transition-colors">
                                                            📥 HTML
                                                        </a>
                                                    )} */}
                                                    <button
                                                        onClick={() => deleteItem(item.id)}
                                                        className="text-xs font-medium transition-colors hover:text-red-400"
                                                        style={{
                                                            color: "rgba(239,68,68,0.7)",
                                                            padding: "2px 6px",
                                                            cursor: "pointer",
                                                        }}
                                                        title="Delete item"
                                                    >
                                                        🗑️
                                                    </button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>

            {/* ── Cover Letter Modal ────────────────────────────────────────────── */}
            {modalOpen && (
                <div
                    style={{
                        position: "fixed", inset: 0, zIndex: 999,
                        background: "rgba(0,0,0,0.7)", backdropFilter: "blur(4px)",
                        display: "flex", alignItems: "center", justifyContent: "center",
                        padding: "1rem",
                    }}
                    onClick={(e) => { if (e.target === e.currentTarget) setModalOpen(false); }}
                >
                    <div style={{
                        background: "#1e293b",
                        border: "1px solid rgba(99,102,241,0.3)",
                        borderRadius: "16px",
                        width: "100%", maxWidth: "700px",
                        maxHeight: "85vh",
                        display: "flex", flexDirection: "column",
                        boxShadow: "0 25px 60px rgba(0,0,0,0.5)",
                    }}>
                        {/* Modal header */}
                        <div style={{
                            padding: "1.2rem 1.5rem",
                            borderBottom: "1px solid rgba(99,102,241,0.2)",
                            display: "flex", alignItems: "center", justifyContent: "space-between",
                        }}>
                            <h3 style={{ fontWeight: 700, fontSize: "1rem" }}>{modalTitle}</h3>
                            <div style={{ display: "flex", gap: "0.75rem", alignItems: "center" }}>
                                {!modalLoading && (
                                    <button onClick={copyContent} className="btn-secondary" style={{ fontSize: "0.8rem", padding: "0.3rem 0.8rem" }}>
                                        📋 Copy
                                    </button>
                                )}
                                <button onClick={() => setModalOpen(false)}
                                    style={{
                                        background: "rgba(255,255,255,0.1)", border: "none", color: "#fff",
                                        width: 28, height: 28, borderRadius: "50%", cursor: "pointer",
                                        fontSize: "1rem", display: "flex", alignItems: "center", justifyContent: "center",
                                    }}>×</button>
                            </div>
                        </div>

                        {/* Modal body */}
                        <div style={{ overflowY: "auto", padding: "1.5rem", flex: 1 }}>
                            {modalLoading ? (
                                <div style={{ display: "flex", justifyContent: "center", padding: "3rem" }}>
                                    <div className="spinner" style={{ width: 40, height: 40 }} />
                                </div>
                            ) : (
                                <pre style={{
                                    whiteSpace: "pre-wrap", lineHeight: 1.8,
                                    fontFamily: "-apple-system, BlinkMacSystemFont, 'Segoe UI', sans-serif",
                                    fontSize: "0.9rem", color: "#e2e8f0",
                                }}>
                                    {modalContent}
                                </pre>
                            )}
                        </div>
                    </div>
                </div>
            )}
        </DashboardLayout>
    );
}
