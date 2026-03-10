"use client";
import { useEffect, useState } from "react";
import { clsx } from "clsx";

type Stat = {
  label: string;
  value: string;
  icon?: React.ReactNode;
};

export default function StatsStrip() {
  const [stats, setStats] = useState<Stat[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // Mocked data – in a real app this would be fetched from /api/summary
    const timer = setTimeout(() => {
      setStats([
        { label: "Current Balance", value: "$4,320" },
        { label: "Monthly Savings Goal", value: "$500" },
        { label: "AI Accuracy", value: "92%" }
      ]);
      setLoading(false);
    }, 800);
    return () => clearTimeout(timer);
  }, []);

  if (loading) {
    return (
      <div className="flex justify-center py-4">
        <span className="animate-pulse text-muted">Loading stats…</span>
      </div>
    );
  }

  return (
    <section className="grid grid-cols-1 md:grid-cols-3 gap-4">
      {stats.map((s) => (
        <div
          key={s.label}
          className={clsx(
            "p-4 bg-card rounded-radius shadow",
            "flex flex-col items-center"
          )}
        >
          <span className="text-sm text-muted mb-1">{s.label}</span>
          <span className="text-xl font-medium text-primary">{s.value}</span>
        </div>
      ))}
    </section>
  );
}
