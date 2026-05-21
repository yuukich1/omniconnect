'use client';

import React, { useEffect, useRef } from 'react';
import gsap from 'gsap';

export default function AnimationTemplate({ children }: { children: React.ReactNode }) {
  const pageRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!pageRef.current) return;

    gsap.fromTo(pageRef.current,
      { opacity: 0, y: 10 },
      { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }
    );
  }, []);

  return (
    <div ref={pageRef} className="w-full">
      {children}
    </div>
  );
}