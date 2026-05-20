'use client';

import React, { useEffect, useRef, useState } from 'react';
import { useNavStore, TabType } from '@/store/useNavStore';
import { useAuthStore } from '@/store/useAuthStore';
import AuthScreen from '@/components/auth/authScreen';
import gsap from 'gsap';

const HomeScreen = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold tracking-tight">Лента сообщений</h1>
    <p className="text-neutral-500 dark:text-neutral-400">Здесь будут агрегироваться сообщения из твоих мессенджеров.</p>
    <div className="h-32 w-full rounded-2xl bg-neutral-100 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 p-4 animate-pulse" />
  </div>
);

const SearchScreen = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold tracking-tight">Поиск</h1>
    <input 
      type="text" 
      placeholder="Поиск по всем каналам..." 
      className="w-full h-12 px-4 rounded-xl border border-neutral-200 dark:border-neutral-800 bg-white dark:bg-neutral-900 outline-none focus:ring-2 focus:ring-neutral-400"
    />
  </div>
);

const ProfileScreen = () => (
  <div className="space-y-4">
    <h1 className="text-2xl font-bold tracking-tight">Профиль</h1>
    <div className="flex items-center gap-4 border-b border-neutral-200 dark:border-neutral-800 pb-4">
      <div className="h-16 w-16 rounded-full bg-neutral-200 dark:bg-neutral-800" />
      <div>
        <h2 className="font-semibold text-lg">Fullstack Developer</h2>
        <p className="text-sm text-neutral-400">Настройки подключений</p>
      </div>
    </div>
  </div>
);

export default function Home() {

  const isAuthenticated = useAuthStore((state) => state.isAuthenticated);
  const isHydrated = useAuthStore((state) => state.isHydrated);
  const hydrate = useAuthStore((state) => state.hydrate);

  const activeTab = useNavStore((state) => state.activeTab);
  const [displayTab, setDisplayTab] = useState<TabType>(activeTab);
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    hydrate();
  }, [hydrate]);

  useEffect(() => {
    if (!containerRef.current || !isAuthenticated) return; 

    gsap.to(containerRef.current, {
      opacity: 0,
      y: 10,
      duration: 0.2,
      ease: 'power2.in',
      onComplete: () => {
        setDisplayTab(activeTab);
        gsap.fromTo(containerRef.current, 
          { opacity: 0, y: -10 },
          { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }
        );
      }
    });
  }, [activeTab, isAuthenticated]);

  const renderScreen = () => {
    switch (displayTab) {
      case 'home': return <HomeScreen />;
      case 'search': return <SearchScreen />;
      case 'profile': return <ProfileScreen />;
      default: return <HomeScreen />;
    }
  };

  if (!isHydrated) {
    return <div className="min-h-screen bg-neutral-50 dark:bg-neutral-950" />;
  }


  if (!isAuthenticated) {
    return <AuthScreen />;
  }

  return (
    <div className="mx-auto max-w-xl px-4 pt-4 md:pt-8">
      <div ref={containerRef}>
        {renderScreen()}
      </div>
    </div>
  );
}