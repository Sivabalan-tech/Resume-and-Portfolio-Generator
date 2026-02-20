"use client";
/**
 * Auth Context — manages authentication state across the app.
 * Stores JWT token and user info in localStorage.
 */
import { createContext, useContext, useState, useEffect, ReactNode } from "react";
import { useRouter } from "next/navigation";

interface AuthUser {
    user_id: number;
    email: string;
    full_name: string | null;
    role: "user" | "admin";
    access_token: string;
}

interface AuthContextType {
    user: AuthUser | null;
    login: (userData: AuthUser) => void;
    logout: () => void;
    isAdmin: boolean;
    isLoading: boolean;
}

const AuthContext = createContext<AuthContextType | null>(null);

export function AuthProvider({ children }: { children: ReactNode }) {
    const [user, setUser] = useState<AuthUser | null>(null);
    const [isLoading, setIsLoading] = useState(true);
    const router = useRouter();

    // Restore user from localStorage on mount
    useEffect(() => {
        const stored = localStorage.getItem("auth_user");
        const token = localStorage.getItem("auth_token");
        if (stored && token) {
            try {
                setUser(JSON.parse(stored));
            } catch {
                localStorage.removeItem("auth_user");
                localStorage.removeItem("auth_token");
            }
        }
        setIsLoading(false);
    }, []);

    const login = (userData: AuthUser) => {
        setUser(userData);
        localStorage.setItem("auth_token", userData.access_token);
        localStorage.setItem("auth_user", JSON.stringify(userData));
    };

    const logout = () => {
        setUser(null);
        localStorage.removeItem("auth_token");
        localStorage.removeItem("auth_user");
        router.push("/login");
    };

    return (
        <AuthContext.Provider
            value={{ user, login, logout, isAdmin: user?.role === "admin", isLoading }}
        >
            {children}
        </AuthContext.Provider>
    );
}

export function useAuth() {
    const context = useContext(AuthContext);
    if (!context) throw new Error("useAuth must be used within AuthProvider");
    return context;
}
