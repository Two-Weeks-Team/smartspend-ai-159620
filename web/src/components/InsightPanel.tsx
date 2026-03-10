"use client";
import { useEffect, useState } from "react";
import { categorizeTransactions, Transaction } from "@/lib/api";
import StatePanel from "@/components/StatePanel";
import { motion } from "framer-motion";
import { CheckCircleIcon, ExclamationTriangleIcon } from "@heroicons/react/24/solid";

export default function InsightPanel() {
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [result, setResult] = useState<{ categorized_transactions: { transaction_id: string; category: string }[] } | null>(null);

  // Sample payload representing a tiny bank statement
  const sampleTransactions: Transaction[] = [
    { transaction_id: "t1", amount: 23.45, description: "Starbucks coffee" },
    { transaction_id: "t2", amount: 120.0, description: "Monthly gym membership" },
    { transaction_id: "t3", amount: 45.99, description: "Netflix subscription" }
  ];

  useEffect(() => {
    async function runCategorization() {
      try {
        const data = await categorizeTransactions(sampleTransactions);
        setResult(data);
        setError(null);
      } catch (e:any) {
        setError(e.message || "Unexpected error");
        setResult(null);
      } finally {
        setLoading(false);
      }
    }
    runCategorization();
  }, []);

  if (loading || error || !result) {
    return <StatePanel loading={loading} error={error} empty={!result && !loading && !error} />;
  }

  const savingsOpportunity = result?.categorized_transactions.reduce((acc, cur) => {
    // mock rule: if category includes "subscription" suggest cancel -> $10 savings each
    if (cur.category.toLowerCase().includes("subscription")) {
      return acc + 10;
    }
    return acc;
  }, 0);

  return (
    <section id="insight-panel" className="bg-card rounded-radius shadow p-6">
      <motion.h2
        className="text-2xl font-semibold text-primary mb-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        AI‑Generated Insights
      </motion.h2>
      <ul className="space-y-2">
        {result.categorized_transactions.map((c) => (
          <li key={c.transaction_id} className="flex items-center gap-2">
            <CheckCircleIcon className="w-5 h-5 text-success" />
            <span>{c.transaction_id} – {c.category}</span>
          </li>
        ))}
      </ul>
      <div className="mt-6 p-4 bg-muted rounded-radius">
        <h3 className="text-lg font-medium text-primary mb-2">Quick Recommendation</h3>
        <p>
          Based on your subscriptions, you could save <strong>${savingsOpportunity}</strong> per month by reviewing or canceling low‑value services.
        </p>
        <button className="mt-3 px-4 py-2 bg-primary text-white rounded-radius hover:bg-primary/90 transition">
          Adjust Budget
        </button>
      </div>
    </section>
  );
}
