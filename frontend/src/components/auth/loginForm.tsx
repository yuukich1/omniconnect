'use client';

import React, { useState, useEffect, useRef } from 'react';
import { loginSchema } from '@/schemas/auth.schema';
import { useAuthStore } from '@/store/useAuthStore';
import { api } from '@/lib/api';
import axios from 'axios';
import gsap from 'gsap';

interface LoginFormProps {
  onSwitchMode: () => void;
}

export default function LoginForm({ onSwitchMode }: LoginFormProps) {
  const loginGlobal = useAuthStore((state) => state.login);
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const elementsRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (!elementsRef.current) return;

    gsap.fromTo(
      elementsRef.current.querySelectorAll('.animate-item'),
      { opacity: 0, y: 20, scale: 0.98 },
      { 
        opacity: 1, 
        y: 0, 
        scale: 1,
        duration: 0.5, 
        stagger: 0.07, 
        ease: 'power4.out' 
      }
    );
  }, []);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const validation = loginSchema.safeParse({ email, password });
    if (!validation.success) {
      setError(validation.error.issues[0].message);
      gsap.to(elementsRef.current, { x: 6, duration: 0.05, yoyo: true, repeat: 4, onComplete: () => gsap.set(elementsRef.current, { x: 0 }) });
      return;
    }

    setIsLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', email.trim()); 
      formData.append('password', password);

      const response = await api.post('/auth/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      const token = response.data.access_token;

      if (token) {
        gsap.to(containerRef.current, {
          opacity: 0,
          scale: 0.98,
          duration: 0.25,
          ease: 'power3.in',
          onComplete: () => {
            loginGlobal({ id: 'current_user', username: email.split('@')[0] }, token);
          }
        });
      } else {
        setError('Не удалось получить токен доступа');
      }

    } catch (err) {
      gsap.fromTo(elementsRef.current, { x: -6 }, { x: 0, duration: 0.4, ease: 'elastic.out(1, 0.4)' });
      if (axios.isAxiosError(err) && err.response) {
        setError(err.response.data?.detail || 'Неверный email или пароль');
      } else {
        setError('Сервер недоступен. Проверь FastAPI.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <div 
      ref={containerRef}
      className="fixed inset-0 flex items-center justify-center bg-white dark:bg-black px-6 z-50 overflow-hidden"
    >

      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[350px] h-[350px] bg-neutral-200 dark:bg-neutral-800/40 rounded-full blur-[120px] pointer-events-none" />

      <div 
        ref={elementsRef}
        className="w-full max-w-sm relative z-10"
      >
        <div className="space-y-2 mb-8 text-center animate-item opacity-0">
          <h2 className="text-3xl font-light tracking-tight text-neutral-900 dark:text-neutral-100">
            Вход в аккаунт
          </h2>
          <p className="text-xs tracking-wide uppercase text-neutral-400 dark:text-neutral-500 font-medium">
            Суперапп агрегатор
          </p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-5">
          <div className="animate-item opacity-0 relative">
            <input
              type="text"
              placeholder="Email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
              className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1"
            />
          </div>

          <div className="animate-item opacity-0 relative">
            <input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1"
            />
          </div>

          {error && (
            <p className="text-xs text-red-500 font-medium px-1 pt-1 animate-item ">
              {error}
            </p>
          )}

          <div className="animate-item opacity-0 pt-4">
            <button
              type="submit"
              disabled={isLoading}
              className="w-full h-12 rounded-full bg-neutral-950 dark:bg-white text-white dark:text-black font-medium text-sm transition-all hover:opacity-90 active:scale-[0.98] disabled:opacity-40 flex items-center justify-center tracking-wide"
            >
              {isLoading ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              ) : (
                'Продолжить'
              )}
            </button>
          </div>


          <div className="mt-8 text-center animate-item opacity-1">
            <button
              type="button"
              onClick={onSwitchMode}
              className="text-xs tracking-wide text-neutral-500 hover:text-neutral-300 transition-colors underline underline-offset-4 decoration-neutral-800"
            >
              У меня ещё нет аккаунта. <span className="underline underline-offset-4 decoration-neutral-300 dark:decoration-neutral-700">Создать</span>
            </button>
          </div>
        </form>
      </div>
    </div>
  );
}