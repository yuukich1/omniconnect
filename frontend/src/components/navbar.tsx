'use client';

import React, { useEffect, useRef } from 'react';
import Link from 'next/link';
import { usePathname } from 'next/navigation';
import gsap from 'gsap';
import { Home, MessageSquare, User } from 'lucide-react';

export default function Navbar() {
  const pathname = usePathname();
  const navRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (navRef.current) {
      gsap.fromTo(navRef.current, 
        { y: 20, opacity: 0 }, 
        { y: 0, opacity: 1, duration: 0.6, ease: 'power3.out' }
      );
    }
  }, []);

  const navItems = [
    { href: '/', icon: Home, label: 'Главная' },
    { href: '/messages', icon: MessageSquare, label: 'Сообщения' },
    { href: '/profile', icon: User, label: 'Профиль' },
  ];

  const handleItemClick = (e: React.MouseEvent<HTMLAnchorElement>) => {
    gsap.fromTo(
      e.currentTarget,
      { scale: 0.85 },
      { scale: 1, duration: 0.3, ease: 'back.out(2)' }
    );
  };

  return (
    <div
      ref={navRef} 
      className="fixed bottom-0 left-0 right-0 z-50 flex h-16 items-center justify-between border-t border-neutral-200 bg-white/80 px-6 backdrop-blur-lg dark:border-neutral-800 dark:bg-neutral-900/80 md:top-4 md:bottom-auto md:mx-auto md:max-w-xl md:rounded-full md:border md:h-14"
    >
      <div className="flex w-full items-center justify-around md:justify-between md:gap-8">
        {navItems.map((item) => {
          const Icon = item.icon;
          const isActive = pathname === item.href;

          return (
            <Link
              key={item.href}
              href={item.href}
              onClick={handleItemClick}
              className="relative flex h-12 w-12 items-center justify-center rounded-xl transition-colors duration-200"
              aria-label={item.label}
            >
              <Icon
                size={24}
                strokeWidth={isActive ? 2.5 : 1.5}
                className={`transition-colors duration-200 ${
                  isActive
                    ? 'text-black dark:text-white'
                    : 'text-neutral-400 hover:text-neutral-600 dark:hover:text-neutral-300'
                }`}
              />
              
              {isActive && (
                <span className="absolute bottom-1 h-1 w-1 rounded-full bg-black dark:bg-white md:bottom-0" />
              )}
            </Link>
          );
        })}
      </div>
    </div>
  );
}