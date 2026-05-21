'use client';

import Link from 'next/link';
import { usePathname } from 'next/navigation';

export function BottomNav() {
  const pathname = usePathname();

  return (
    <nav className="flex gap-4">
      <Link href="/" className={pathname === '/' ? 'text-black font-bold' : 'text-neutral-400'}>
        Лента
      </Link>
      <Link href="/messages" className={pathname === '/messages' ? 'text-black font-bold' : 'text-neutral-400'}>
        Сообщения
      </Link>
      <Link href="/profile" className={pathname === '/profile' ? 'text-black font-bold' : 'text-neutral-400'}>
        Профиль
      </Link>
    </nav>
  );
}