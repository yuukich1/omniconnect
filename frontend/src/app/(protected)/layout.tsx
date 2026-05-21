import React from 'react';

export default function ProtectedLayout({ children }: { children: React.ReactNode }) {
  return (
    <div className="dark mx-auto max-w-xl px-4 pt-4 md:pt-8 sequential-layout"
        style={{ colorScheme: 'dark' }}
    >
      {children}
    </div>
  );
}