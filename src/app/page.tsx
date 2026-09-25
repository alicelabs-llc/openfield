"use client";

import { useState } from "react";
import { AnimatePresence } from "framer-motion";
import { BootSequence } from "@/components/agent-portal/boot-sequence";
import { AuthRitual } from "@/components/agent-portal/auth-ritual";
import { Dashboard } from "@/components/agent-portal/dashboard";

type Phase = "boot" | "auth" | "dashboard";

export default function Home() {
  const [phase, setPhase] = useState<Phase>("boot");
  const [sessionStart] = useState(() => Date.now());

  return (
    <div className="relative min-h-screen">
      <AnimatePresence mode="wait">
        {phase === "boot" && (
          <BootSequence key="boot" onComplete={() => setPhase("auth")} />
        )}
        {phase === "auth" && (
          <AuthRitual key="auth" onAuthed={() => setPhase("dashboard")} />
        )}
      </AnimatePresence>

      {phase === "dashboard" && <Dashboard sessionStart={sessionStart} />}
    </div>
  );
}
