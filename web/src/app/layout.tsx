import { Inter, Source_Sans_Pro } from "next/font/google";
import "../app/globals.css";

const inter = Inter({ subsets: ["latin"], variable: "--font-inter" });
const source = Source_Sans_Pro({ subsets: ["latin"], variable: "--font-sans" });

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
    <html lang="en" className={`${inter.variable} ${source.variable}`}>
      <body className="font-sans bg-background text-foreground antialiased">
        {children}
      </body>
    </html>
  );
}
