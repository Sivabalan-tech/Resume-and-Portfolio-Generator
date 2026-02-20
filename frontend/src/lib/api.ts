/**
 * Axios API client with JWT bearer token interceptor.
 * Reads the token from localStorage and attaches it to every request.
 */
import axios from "axios";

const API_BASE = process.env.NEXT_PUBLIC_API_URL || "http://localhost:8000";

const api = axios.create({
    baseURL: API_BASE,
    headers: {
        "Content-Type": "application/json",
    },
});

// ── Request Interceptor: attach JWT token ────────────────────────────────────
api.interceptors.request.use(
    (config) => {
        if (typeof window !== "undefined") {
            const token = localStorage.getItem("auth_token");
            if (token) {
                config.headers.Authorization = `Bearer ${token}`;
            }
        }
        return config;
    },
    (error) => Promise.reject(error)
);

// ── Response Interceptor: handle 401 (token expired) ─────────────────────────
api.interceptors.response.use(
    (response) => response,
    (error) => {
        if (error.response?.status === 401) {
            if (typeof window !== "undefined") {
                localStorage.removeItem("auth_token");
                localStorage.removeItem("auth_user");
                window.location.href = "/login";
            }
        }
        return Promise.reject(error);
    }
);

export default api;

// ── Typed API Helper Functions ────────────────────────────────────────────────

export const authApi = {
    register: (data: { email: string; password: string; full_name?: string; role?: string }) =>
        api.post("/api/auth/register", data),
    login: (data: { email: string; password: string }) =>
        api.post("/api/auth/login", data),
};

export const profileApi = {
    get: () => api.get("/api/profile"),
    update: (data: object) => api.put("/api/profile", data),
};

export const resumeApi = {
    generate: (data: { job_role: string; job_description?: string; extra_instructions?: string }) =>
        api.post("/api/resume/generate", data),
    getHistory: () => api.get("/api/resume/history"),
    getHistoryItem: (id: number) => api.get(`/api/resume/history/${id}`),
    deleteHistoryItem: (id: number) => api.delete(`/api/resume/history/${id}`),
};

export const coverLetterApi = {
    generate: (data: {
        company_name: string;
        job_role: string;
        job_description: string;
        hiring_manager?: string;
    }) => api.post("/api/cover-letter/generate", data),
    getHistoryItem: (id: number) => api.get(`/api/cover-letter/history/${id}`),
};

export const atsApi = {
    analyze: (data: { job_description: string; resume_text?: string }) =>
        api.post("/api/ats/analyze", data),
};

export const portfolioApi = {
    generate: () => api.post("/api/portfolio/generate"),
    download: () => api.post("/api/portfolio/download", {}, { responseType: "blob" }),
    reDownload: (id: number) => api.get(`/api/portfolio/download/${id}`, { responseType: "blob" }),
};

export const pdfApi = {
    download: (markdown_text: string, filename?: string) =>
        api.post(
            "/api/pdf/download",
            { markdown_text, filename: filename || "resume" },
            { responseType: "blob" }
        ),
    downloadFromHistory: (id: number) =>
        api.get(`/api/pdf/history/${id}`, { responseType: "blob" }),
};

export const adminApi = {
    getUsers: () => api.get("/api/admin/users"),
    getStats: () => api.get("/api/admin/stats"),
    deleteUser: (id: number) => api.delete(`/api/admin/users/${id}`),
};
