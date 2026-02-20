"use client";
/**
 * Shared Dashboard Layout — sidebar navigation for all authenticated pages.
 */
import Link from "next/link";
import { usePathname, useRouter } from "next/navigation";
import { useAuth } from "@/lib/auth";
import { useEffect } from "react";
import toast from "react-hot-toast";

const navItems = [
    { href: "/dashboard", label: "Dashboard", icon: "📊" },
    { href: "/profile", label: "My Profile", icon: "👤" },
    { href: "/resume", label: "Resume Builder", icon: "📄" },
    { href: "/cover-letter", label: "Cover Letter", icon: "✉️" },
    { href: "/ats", label: "ATS Analyzer", icon: "🎯" },
    { href: "/portfolio", label: "Portfolio", icon: "🌐" },
];

export default function DashboardLayout({ children }: { children: React.ReactNode }) {
    const pathname = usePathname();
    const { user, logout, isLoading } = useAuth();
    const router = useRouter();

    useEffect(() => {
        if (!isLoading && !user) {
            router.push("/login");
        }
    }, [user, isLoading, router]);

    if (isLoading || !user) {
        return (
            <div className="min-h-screen flex items-center justify-center">
                <div className="spinner" style={{ width: 40, height: 40 }} />
            </div>
        );
    }

    return (
        <div className="flex min-h-screen">
            {/* Sidebar */}
            <aside className="fixed top-0 left-0 h-full w-64 flex flex-col z-40"
                style={{ background: "rgba(15,23,42,0.95)", borderRight: "1px solid var(--border)" }}>
                {/* Logo */}
                <div className="p-6 border-b" style={{ borderColor: "var(--border)" }}>
                    <Link href="/dashboard" className="flex items-center gap-3">
                        <div style={{ background: "linear-gradient(135deg,#6366f1,#8b5cf6)", borderRadius: "10px", padding: "8px", fontSize: "18px" }}>🤖</div>
                        <div>
                            <div className="font-bold text-sm gradient-text">AI Resume</div>
                            <div className="text-xs" style={{ color: "var(--text-secondary)" }}>Portfolio Builder</div>
                        </div>
                    </Link>
                </div>

                {/* Nav */}
                <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
                    {navItems.map(item => (
                        <Link key={item.href} href={item.href}
                            className={"sidebar-link" + (pathname === item.href ? " active" : "")}>
                            <span className="text-lg">{item.icon}</span>
                            <span>{item.label}</span>
                        </Link>
                    ))}
                    {user.role === "admin" && (
                        <Link href="/admin"
                            className={"sidebar-link" + (pathname === "/admin" ? " active" : "")}>
                            <span className="text-lg">⚙️</span>
                            <span>Admin Panel</span>
                        </Link>
                    )}
                </nav>

                {/* User Footer */}
                <div className="p-4 border-t" style={{ borderColor: "var(--border)" }}>
                    <div className="flex items-center gap-3 mb-3">
                        <div style={{ width: 36, height: 36, borderRadius: "50%", background: "linear-gradient(135deg,#6366f1,#8b5cf6)", display: "flex", alignItems: "center", justifyContent: "center", fontWeight: "bold", fontSize: "14px" }}>
                            {(user.full_name || user.email)[0].toUpperCase()}
                        </div>
                        <div className="overflow-hidden">
                            <div className="text-sm font-medium truncate">{user.full_name || "User"}</div>
                            <div className="text-xs truncate" style={{ color: "var(--text-secondary)" }}>{user.email}</div>
                        </div>
                    </div>
                    <button onClick={logout} className="btn-secondary w-full justify-center" style={{ fontSize: "13px", padding: "8px" }}>
                        🚪 Sign Out
                    </button>
                </div>
            </aside>

            {/* Main content */}
            <main className="flex-1 ml-64 min-h-screen" style={{ background: "var(--bg-primary)" }}>
                <div className="p-8">
                    {children}
                </div>
            </main>
        </div>
    );
}
