"use client";
import { motion } from "framer-motion";
import { ExclamationTriangleIcon, ArchiveBoxIcon } from "@heroicons/react/24/outline";

interface Props {
  loading: boolean;
  error: string | null;
  empty: boolean;
}

export default function StatePanel({ loading, error, empty }: Props) {
  if (loading) {
    return (
      <section className="p-6 text-center">
        <motion.div animate={{ rotate: 360 }} transition={{ duration: 1, repeat: Infinity, ease: "linear" }} className="inline-block mx-auto border-4 border-primary rounded-full w-12 h-12" />
        <p className="mt-2 text-muted">Analyzing your transactions…</p>
      </section>
    );
  }

  if (error) {
    return (
      <section className="p-6 text-center text-warning">
        <ExclamationTriangleIcon className="w-12 h-12 mx-auto" />
        <p className="mt-2">{error}</p>
      </section>
    );
  }

  if (empty) {
    return (
      <section className="p-6 text-center text-muted">
        <ArchiveBoxIcon className="w-12 h-12 mx-auto" />
        <p className="mt-2">No data available yet. Upload a bank statement to get started.</p>
      </section>
    );
  }

  return null;
}
