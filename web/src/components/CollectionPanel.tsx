"use client";
import { useEffect, useState } from "react";
import { fetchItems } from "@/lib/api";
import StatePanel from "@/components/StatePanel";
import { motion } from "framer-motion";
import { ClipboardDocumentListIcon } from "@heroicons/react/24/solid";

export default function CollectionPanel() {
  const [items, setItems] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    async function load() {
      try {
        const data = await fetchItems();
        setItems(data.items);
        setError(null);
      } catch (e:any) {
        setError(e.message || "Failed to load saved items");
      } finally {
        setLoading(false);
      }
    }
    load();
  }, []);

  if (loading || error || items.length === 0) {
    return <StatePanel loading={loading} error={error} empty={items.length === 0 && !loading && !error} />;
  }

  return (
    <section className="bg-card rounded-radius shadow p-6">
      <motion.h2
        className="text-2xl font-semibold text-primary mb-4"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ duration: 0.5 }}
      >
        Your Saved Insights
      </motion.h2>
      <ul className="space-y-3">
        {items.map((item, idx) => (
          <li key={idx} className="flex items-start gap-3">
            <ClipboardDocumentListIcon className="w-5 h-5 text-primary" />
            <div>
              <p className="font-medium">{item.title ?? "Untitled Insight"}</p>
              <p className="text-sm text-muted">{item.summary ?? "No summary provided."}</p>
            </div>
          </li>
        ))}
      </ul>
    </section>
  );
}
