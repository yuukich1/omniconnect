"use client";

import { useEffect, useState } from "react";

export default function AppInitializer({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);


  if (!mounted) {
    return (
      <div className="flex min-h-screen items-center justify-center bg-neutral-50 dark:bg-neutral-950" />
    );
  }

  return <>{children}</>;
}