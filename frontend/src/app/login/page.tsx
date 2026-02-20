"use client";
/**
 * Login Page — email/password authentication with JWT.
 */
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { authApi } from "@/lib/api";
import { useAuth } from "@/lib/auth";

export default function LoginPage() {
    const [email, setEmail] = useState("");
    const [password, setPassword] = useState("");
    const [loading, setLoading] = useState(false);
    const { login } = useAuth();
    const router = useRouter();

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        setLoading(true);
        try {
            const res = await authApi.login({ email, password });
            login({
                user_id: res.data.user_id,
                email,
                full_name: res.data.full_name,
                role: res.data.role,
                access_token: res.data.access_token,
            });
            toast.success("Welcome back! 👋");
            router.push(res.data.role === "admin" ? "/admin" : "/dashboard");
        } catch (err: any) {
            toast.error(err.response?.data?.detail || "Login failed. Please check your credentials.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center px-4" style={{ background: "linear-gradient(135deg,#0f172a,#1e1b4b,#0f172a)" }}>
            <div className="w-full max-w-md fade-in">
                {/* Logo */}
                <div className="text-center mb-8">
                    <div className="inline-flex items-center gap-3 mb-4">
                        <div style={{ background: "linear-gradient(135deg,#6366f1,#8b5cf6)", borderRadius: "12px", padding: "10px", fontSize: "24px" }}>🤖</div>
                        <span className="text-2xl font-bold gradient-text">AI Resume Builder</span>
                    </div>
                    <p style={{ color: "var(--text-secondary)" }}>Sign in to your account</p>
                </div>

                {/* Card */}
                <div className="glass-card p-8">
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="form-label">Email Address</label>
                            <input type="email" className="form-input" placeholder="you@example.com"
                                value={email} onChange={e => setEmail(e.target.value)} required />
                        </div>
                        <div>
                            <label className="form-label">Password</label>
                            <input type="password" className="form-input" placeholder="••••••••"
                                value={password} onChange={e => setPassword(e.target.value)} required />
                        </div>
                        <button type="submit" className="btn-primary w-full justify-center" style={{ padding: "12px" }} disabled={loading}>
                            {loading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Signing in...</> : "Sign In →"}
                        </button>
                    </form>
                    <p className="text-center mt-6" style={{ color: "var(--text-secondary)", fontSize: "14px" }}>
                        Don&apos;t have an account?{" "}
                        <Link href="/register" style={{ color: "var(--accent-light)" }} className="hover:underline font-medium">
                            Create one free
                        </Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
