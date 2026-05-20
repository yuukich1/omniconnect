'use client';


import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import Navbar from "@/components/navbar";
import AppInitializer from "@/components/auth/AppInit";
import { useAuthStore } from "@/store/useAuthStore";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});


export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isHydrated = useAuthStore((state) => state.isHydrated);

  return (
    <html
      lang="en"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-neutral-50 dark:bg-neutral-950 text-neutral-900 dark:text-neutral-50">
        <AppInitializer>
          {isHydrated && isAuthenticated && <Navbar />}
          
          <main className="min-h-screen pb-20 pt-4 md:pt-24">
            {children}
          </main>
        </AppInitializer>
      </body>
    </html>
  );
}