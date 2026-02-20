"use client";
/**
 * Register Page — user registration form.
 */
import { useState } from "react";
import Link from "next/link";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";
import { authApi } from "@/lib/api";

export default function RegisterPage() {
    const [form, setForm] = useState({ email: "", password: "", full_name: "", role: "user" });
    const [loading, setLoading] = useState(false);
    const router = useRouter();

    const handleChange = (e: React.ChangeEvent<HTMLInputElement | HTMLSelectElement>) =>
        setForm(prev => ({ ...prev, [e.target.name]: e.target.value }));

    const handleSubmit = async (e: React.FormEvent) => {
        e.preventDefault();
        if (form.password.length < 6) { toast.error("Password must be at least 6 characters"); return; }
        setLoading(true);
        try {
            await authApi.register(form);
            toast.success("Account created! Please sign in. 🎉");
            router.push("/login");
        } catch (err: any) {
            toast.error(err.response?.data?.detail || "Registration failed.");
        } finally {
            setLoading(false);
        }
    };

    return (
        <div className="min-h-screen flex items-center justify-center px-4" style={{ background: "linear-gradient(135deg,#0f172a,#1e1b4b,#0f172a)" }}>
            <div className="w-full max-w-md fade-in">
                <div className="text-center mb-8">
                    <div className="inline-flex items-center gap-3 mb-4">
                        <div style={{ background: "linear-gradient(135deg,#6366f1,#8b5cf6)", borderRadius: "12px", padding: "10px", fontSize: "24px" }}>🤖</div>
                        <span className="text-2xl font-bold gradient-text">AI Resume Builder</span>
                    </div>
                    <p style={{ color: "var(--text-secondary)" }}>Create your free account</p>
                </div>

                <div className="glass-card p-8">
                    <form onSubmit={handleSubmit} className="space-y-5">
                        <div>
                            <label className="form-label">Full Name</label>
                            <input type="text" name="full_name" className="form-input" placeholder="John Doe"
                                value={form.full_name} onChange={handleChange} />
                        </div>
                        <div>
                            <label className="form-label">Email Address</label>
                            <input type="email" name="email" className="form-input" placeholder="you@example.com"
                                value={form.email} onChange={handleChange} required />
                        </div>
                        <div>
                            <label className="form-label">Password (min. 6 characters)</label>
                            <input type="password" name="password" className="form-input" placeholder="••••••••"
                                value={form.password} onChange={handleChange} required />
                        </div>
                        <div>
                            <label className="form-label">Account Type</label>
                            <select name="role" className="form-input" value={form.role} onChange={handleChange}>
                                <option value="user">User</option>
                                <option value="admin">Admin</option>
                            </select>
                        </div>
                        <button type="submit" className="btn-primary w-full justify-center" style={{ padding: "12px" }} disabled={loading}>
                            {loading ? <><span className="spinner" style={{ width: 18, height: 18 }} /> Creating account...</> : "✨ Create Free Account"}
                        </button>
                    </form>
                    <p className="text-center mt-6" style={{ color: "var(--text-secondary)", fontSize: "14px" }}>
                        Already have an account?{" "}
                        <Link href="/login" style={{ color: "var(--accent-light)" }} className="hover:underline font-medium">Sign in</Link>
                    </p>
                </div>
            </div>
        </div>
    );
}
