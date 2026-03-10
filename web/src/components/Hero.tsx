"use client";
import { motion } from "framer-motion";
import { ArrowRightIcon } from "@heroicons/react/24/solid";
import { clsx } from "clsx";

export default function Hero() {
  const handleDemo = () => {
    // In a real product this would open the onboarding flow.
    // For demo we simply scroll to the InsightPanel.
    const el = document.getElementById("insight-panel");
    if (el) {
      el.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <section className="text-center py-12 md:py-20">
      <motion.h1
        className="text-4xl md:text-5xl font-bold text-primary mb-4"
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
      >
        SmartSpend AI
      </motion.h1>
      <motion.p
        className="text-lg md:text-xl text-foreground mb-6"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.3, duration: 0.5 }}
      >
        Transform your spending habits with AI‑powered insights and proactive financial coaching.
      </motion.p>
      <motion.button
        onClick={handleDemo}
        className={clsx(
          "inline-flex items-center gap-2 px-6 py-3 bg-accent text-white rounded-radius shadow",
          "hover:bg-accent/90 transition"
        )}
        whileHover={{ scale: 1.03 }}
        whileTap={{ scale: 0.98 }}
      >
        See Your Savings Plan
        <ArrowRightIcon className="w-5 h-5" />
      </motion.button>
    </section>
  );
}
