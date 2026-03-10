import { Inter } from "next/font/google";
import '../app/globals.css';

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });

export const metadata = {
  title: "SmartSpend AI",
  description: "Transform your spending habits with AI-powered insights and proactive financial coaching."
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${inter.variable}`}> 
      <body className="font-inter bg-background text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}
