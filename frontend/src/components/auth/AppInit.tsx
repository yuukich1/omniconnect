'use client';

import React, { useEffect, useState } from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import AuthScreen from '@/components/auth/authScreen';
import Navbar from '@/components/navbar';

export default function AppInitializer({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);
  const [hasToken, setHasToken] = useState<boolean | null>(null); // Наше локальное состояние токена
  
  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isHydrated = useAuthStore((state) => state.isHydrated);
  const hydrate = useAuthStore((state) => state.hydrate);
  const logout = useAuthStore((state) => state.logout);

  useEffect(() => {
    hydrate();
    
    const token = localStorage.getItem('authToken');
    setHasToken(!!token); 
    
    if (!token && isAuthenticated) {
      logout();
    }
    
    setMounted(true);
  }, [hydrate, logout, isAuthenticated]);

  useEffect(() => {
    const checkToken = () => {
      const token = localStorage.getItem('authToken');
      const tokenExists = !!token;
      
      if (tokenExists !== hasToken) {
        setHasToken(tokenExists);
        if (!tokenExists) {
          logout();
        }
      }
    };

    const interval = setInterval(checkToken, 1000);
    return () => clearInterval(interval);
  }, [hasToken, logout]);

  if (!mounted || !isHydrated || hasToken === null) {
    return <div className="min-h-screen bg-neutral-950" />;
  }

  if (!isAuthenticated || !hasToken) {
    return <AuthScreen />;
  }

  return (
    <>
      <Navbar />
      <main className="min-h-screen pb-20 pt-4 md:pt-24 bg-neutral-950 text-neutral-50">
        {children}
      </main>
    </>
  );
}