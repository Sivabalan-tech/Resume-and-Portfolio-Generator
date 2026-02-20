import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { AuthProvider } from "@/lib/auth";
import { Toaster } from "react-hot-toast";

const inter = Inter({ subsets: ["latin"] });

export const metadata: Metadata = {
  title: "AI Resume & Portfolio Builder | MCA GenAI Project",
  description:
    "Generate ATS-optimized resumes, cover letters, and portfolio content powered by Gemini AI. Analyze job descriptions, get ATS scores, and export to PDF.",
  keywords: ["resume builder", "AI resume", "ATS optimizer", "portfolio generator", "cover letter"],
};

export default function RootLayout({ children }: { children: React.ReactNode }) {
  return (
    <html lang="en" suppressHydrationWarning>
      <body className={inter.className}>
        <AuthProvider>
          {children}
          <Toaster
            position="top-right"
            toastOptions={{
              style: {
                background: "#1e293b",
                color: "#f1f5f9",
                border: "1px solid #334155",
              },
            }}
          />
        </AuthProvider>
      </body>
    </html>
  );
}
