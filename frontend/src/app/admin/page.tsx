"use client";
/**
 * Admin Dashboard Page — user management and analytics.
 * Admin role required.
 */
import { useEffect, useState } from "react";
import DashboardLayout from "@/components/DashboardLayout";
import { adminApi } from "@/lib/api";
import { useAuth } from "@/lib/auth";
import { useRouter } from "next/navigation";
import toast from "react-hot-toast";

export default function AdminPage() {
    const { user, isAdmin, isLoading } = useAuth();
    const router = useRouter();
    const [users, setUsers] = useState<any[]>([]);
    const [stats, setStats] = useState<any>(null);
    const [loading, setLoading] = useState(true);

    useEffect(() => {
        if (!isLoading && !isAdmin) {
            toast.error("Admin access required.");
            router.push("/dashboard");
        }
    }, [isAdmin, isLoading, router]);

    useEffect(() => {
        if (isAdmin) {
            Promise.all([adminApi.getUsers(), adminApi.getStats()])
                .then(([usersRes, statsRes]) => {
                    setUsers(usersRes.data);
                    setStats(statsRes.data);
                })
                .catch(() => toast.error("Failed to load admin data."))
                .finally(() => setLoading(false));
        }
    }, [isAdmin]);

    const deleteUser = async (id: number, email: string) => {
        if (!confirm(`Delete user ${email}? This cannot be undone.`)) return;
        try {
            await adminApi.deleteUser(id);
            setUsers(users.filter(u => u.id !== id));
            toast.success("User deleted.");
        } catch { toast.error("Failed to delete user."); }
    };

    if (!isAdmin) return null;

    return (
        <DashboardLayout>
            <div className="space-y-8 fade-in">
                <div>
                    <h1 className="text-3xl font-bold">⚙️ Admin Dashboard</h1>
                    <p style={{ color: "var(--text-secondary)" }}>Platform overview and user management.</p>
                </div>

                {/* Stats */}
                {stats && (
                    <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-6 gap-4">
                        {[
                            { label: "Total Users", value: stats.total_users, icon: "👥", color: "#6366f1" },
                            { label: "Resumes Made", value: stats.total_resumes_generated, icon: "📄", color: "#8b5cf6" },
                            { label: "Cover Letters", value: stats.total_cover_letters_generated, icon: "✉️", color: "#ec4899" },
                            { label: "Portfolios", value: stats.total_portfolios_generated, icon: "🌐", color: "#10b981" },
                            { label: "Avg ATS Score", value: `${stats.avg_ats_score}%`, icon: "🎯", color: "#f59e0b" },
                            { label: "New Today", value: stats.new_users_today, icon: "⚡", color: "#06b6d4" },
                        ].map(s => (
                            <div key={s.label} className="stat-card text-center">
                                <div style={{ fontSize: "26px", color: s.color }}>{s.icon}</div>
                                <div className="text-2xl font-bold mt-1">{s.value}</div>
                                <div style={{ color: "var(--text-secondary)", fontSize: "11px" }}>{s.label}</div>
                            </div>
                        ))}
                    </div>
                )}

                {/* Users Table */}
                <div>
                    <h2 className="text-xl font-bold mb-4">All Users ({users.length})</h2>
                    {loading ? (
                        <div className="glass-card p-16 flex items-center justify-center"><div className="spinner" style={{ width: 40, height: 40 }} /></div>
                    ) : (
                        <div className="glass-card overflow-hidden">
                            <table className="w-full text-sm">
                                <thead>
                                    <tr style={{ borderBottom: "1px solid var(--border)" }}>
                                        {["ID", "Email", "Name", "Role", "Profile", "Generations", "Joined", "Actions"].map(h => (
                                            <th key={h} className="text-left px-4 py-3" style={{ color: "var(--text-secondary)", fontWeight: 500, fontSize: "12px" }}>{h}</th>
                                        ))}
                                    </tr>
                                </thead>
                                <tbody>
                                    {users.map(u => (
                                        <tr key={u.id} style={{ borderBottom: "1px solid rgba(51,65,85,0.4)" }} className="hover:bg-white/5">
                                            <td className="px-4 py-3" style={{ color: "var(--text-secondary)" }}>#{u.id}</td>
                                            <td className="px-4 py-3">{u.email}</td>
                                            <td className="px-4 py-3">{u.full_name || "—"}</td>
                                            <td className="px-4 py-3">
                                                <span className={`badge ${u.role === "admin" ? "badge-amber" : "badge-indigo"}`}>{u.role}</span>
                                            </td>
                                            <td className="px-4 py-3">
                                                <span className={`badge ${u.has_profile ? "badge-green" : "badge-red"}`}>{u.has_profile ? "Yes" : "No"}</span>
                                            </td>
                                            <td className="px-4 py-3">{u.resume_count}</td>
                                            <td className="px-4 py-3" style={{ color: "var(--text-secondary)" }}>
                                                {new Date(u.created_at).toLocaleDateString()}
                                            </td>
                                            <td className="px-4 py-3">
                                                {u.id !== user?.user_id && (
                                                    <button onClick={() => deleteUser(u.id, u.email)}
                                                        style={{ color: "var(--danger)", fontSize: "12px", background: "rgba(239,68,68,0.1)", padding: "4px 10px", borderRadius: "6px", border: "1px solid rgba(239,68,68,0.3)" }}>
                                                        Delete
                                                    </button>
                                                )}
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                        </div>
                    )}
                </div>
            </div>
        </DashboardLayout>
    );
}
