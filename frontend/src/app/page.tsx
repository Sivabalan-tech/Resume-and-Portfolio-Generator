"use client";
/**
 * Landing Page — hero section, features, and call-to-action.
 * Public page (no auth required).
 */
import Link from "next/link";
import { useAuth } from "@/lib/auth";

const features = [
  { icon: "🤖", title: "AI Resume Generator", desc: "ATS-optimized resumes tailored to each job role using Gemini AI." },
  { icon: "📄", title: "Cover Letter Writer", desc: "Company-specific cover letters that stand out from the crowd." },
  { icon: "📊", title: "ATS Score Analyzer", desc: "SentenceTransformers-powered semantic similarity scoring." },
  { icon: "🔍", title: "Skill Gap Analysis", desc: "Identify missing keywords and skills for any job description." },
  { icon: "🌐", title: "Portfolio Generator", desc: "Professional bio, project descriptions, and LinkedIn summaries." },
  { icon: "📑", title: "PDF Export", desc: "Download your resume as a beautifully formatted PDF instantly." },
];

export default function LandingPage() {
  const { user } = useAuth();

  return (
    <div className="min-h-screen" style={{ background: "linear-gradient(135deg, #0f172a 0%, #1e1b4b 50%, #0f172a 100%)" }}>
      {/* Navbar */}
      <nav className="fixed top-0 w-full z-50" style={{ background: "rgba(15,23,42,0.8)", backdropFilter: "blur(12px)", borderBottom: "1px solid rgba(99,102,241,0.2)" }}>
        <div className="max-w-7xl mx-auto px-6 py-4 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div style={{ background: "linear-gradient(135deg,#6366f1,#8b5cf6)", borderRadius: "10px", padding: "8px", fontSize: "20px" }}>🤖</div>
            <span className="font-bold text-lg gradient-text">AI Resume Builder</span>
          </div>
          <div className="flex gap-3">
            {user ? (
              <Link href="/dashboard" className="btn-primary">Go to Dashboard →</Link>
            ) : (
              <>
                <Link href="/login" className="btn-secondary">Login</Link>
                <Link href="/register" className="btn-primary">Get Started Free →</Link>
              </>
            )}
          </div>
        </div>
      </nav>

      {/* Hero */}
      <section className="pt-36 pb-24 px-6 text-center">
        <div className="max-w-4xl mx-auto space-y-6 fade-in">
          <div className="badge badge-indigo mx-auto" style={{ width: "fit-content" }}>✨ Powered by Gemini AI + SentenceTransformers</div>
          <h1 className="text-5xl md:text-7xl font-black leading-tight">
            Build Your Dream Resume<br />
            <span className="gradient-text">in Seconds with AI</span>
          </h1>
          <p className="text-xl" style={{ color: "var(--text-secondary)" }}>
            Generate ATS-optimized resumes, tailored cover letters, portfolio content, and get real-time
            job description analysis — all powered by cutting-edge Generative AI.
          </p>
          <div className="flex gap-4 justify-center flex-wrap">
            <Link href="/register" className="btn-primary" style={{ fontSize: "16px", padding: "14px 32px" }}>
              🚀 Start Building Free
            </Link>
            <Link href="/login" className="btn-secondary" style={{ fontSize: "16px", padding: "14px 32px" }}>
              Sign In →
            </Link>
          </div>
          {/* Stats row */}
          <div className="flex gap-8 justify-center pt-6 flex-wrap">
            {[["10x", "Faster Resume Writing"], ["95%", "ATS Pass Rate"], ["100%", "AI Powered"]].map(([v, l]) => (
              <div key={l} className="text-center">
                <div className="text-3xl font-black gradient-text">{v}</div>
                <div className="text-sm" style={{ color: "var(--text-secondary)" }}>{l}</div>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* Features Grid */}
      <section className="py-20 px-6" id="features">
        <div className="max-w-6xl mx-auto">
          <h2 className="text-4xl font-bold text-center mb-4">Everything You Need to <span className="gradient-text">Get Hired</span></h2>
          <p className="text-center mb-12" style={{ color: "var(--text-secondary)" }}>One platform. All the AI tools to land your dream job.</p>
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
            {features.map((f) => (
              <div key={f.title} className="glass-card p-6 group hover:border-indigo-500 transition-all duration-300" style={{ cursor: "default" }}>
                <div className="text-4xl mb-4">{f.icon}</div>
                <h3 className="text-lg font-bold mb-2">{f.title}</h3>
                <p style={{ color: "var(--text-secondary)", fontSize: "14px" }}>{f.desc}</p>
              </div>
            ))}
          </div>
        </div>
      </section>

      {/* CTA */}
      <section className="py-20 px-6 text-center">
        <div className="glass-card max-w-2xl mx-auto p-12" style={{ background: "linear-gradient(135deg, rgba(99,102,241,0.15), rgba(139,92,246,0.15))" }}>
          <h2 className="text-3xl font-bold mb-4">Ready to Build Your Career?</h2>
          <p className="mb-8" style={{ color: "var(--text-secondary)" }}>Join thousands of professionals using AI to get hired faster.</p>
          <Link href="/register" className="btn-primary" style={{ fontSize: "16px", padding: "14px 32px" }}>
            ✨ Create Free Account
          </Link>
        </div>
      </section>

      {/* Footer */}
      <footer className="py-8 text-center border-t" style={{ borderColor: "var(--border)", color: "var(--text-secondary)", fontSize: "14px" }}>
        <p>© 2026 AI Resume & Portfolio Builder — Final Year MCA (Generative AI) Project</p>
      </footer>
    </div>
  );
}
