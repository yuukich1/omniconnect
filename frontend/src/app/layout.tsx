import { Geist, Geist_Mono } from "next/font/google";
import "./globals.css";
import AppInitializer from "@/components/auth/AppInit";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata = {
  title: 'OmniConnect',
  description: 'Aggregator space',
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="ru"
      className={`${geistSans.variable} ${geistMono.variable} h-full antialiased`}
    >
      <body suppressHydrationWarning={true} className="min-h-full flex flex-col bg-neutral-50 dark:bg-neutral-950 text-white dark:text-neutral-50">
        <AppInitializer>
          {children}
        </AppInitializer>
        
      </body>
    </html>
  );
}