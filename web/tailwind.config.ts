import { type Config } from "tailwindcss";

export default <Config>{
  content: ["./src/**/*.{js,ts,jsx,tsx,mdx}"],
  theme: {
    extend: {
      colors: {
        background: "var(--color-background)",
        foreground: "var(--color-foreground)",
        card: "var(--color-card)",
        muted: "var(--color-muted)",
        border: "var(--color-border)",
        primary: "var(--color-primary)",
        accent: "var(--color-accent)",
        success: "var(--color-success)",
        warning: "var(--color-warning)"
      },
      borderRadius: {
        radius: "var(--radius)"
      },
      boxShadow: {
        shadow: "var(--shadow)"
      }
    }
  },
  plugins: []
};
