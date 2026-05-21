'use client';

import React from 'react';
import { useAuthStore } from '@/store/useAuthStore';
import { useLoginAnimations } from './hooks/useLoginAnimations';
import { useLogin } from './hooks/useLogin';

interface LoginFormProps {
  onSwitchMode: () => void;
}

export default function LoginForm({ onSwitchMode }: LoginFormProps) {
  const loginGlobal = useAuthStore((state) => state.login);
  
  const { containerRef, elementsRef, shakeValidationError, shakeApiError, animateSuccess } = useLoginAnimations();

  const { username, setUsername, password, setPassword, error, isLoading, handleSubmit } = useLogin({
    onValidationError: shakeValidationError,
    onApiError: shakeApiError,
    onSuccess: (validUsername, token) => {
      animateSuccess(() => {
        loginGlobal({ id: 'current_user', username: validUsername }, token);
      });
    }
  });

  const handleActionSubmit = () => {
    if (isLoading) return;
    const mockEvent = {
      preventDefault: () => {},
      stopPropagation: () => {}
    };
    
    handleSubmit(mockEvent as any);
  };

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (e.key === 'Enter') {
      handleActionSubmit();
    }
  };

  return (
    <div 
      ref={containerRef}
      className="absolute inset-0 flex items-center justify-center bg-white dark:bg-black px-6 z-50 overflow-hidden min-h-full"
    >
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[350px] h-[350px] bg-neutral-200 dark:bg-neutral-800/40 rounded-full blur-[120px] pointer-events-none" />

      <div ref={elementsRef} className="w-full max-w-sm relative z-10">
        <div className="space-y-2 mb-8 text-center animate-item">
          <h2 className="text-3xl font-light tracking-tight text-neutral-900 dark:text-neutral-100">
            Вход в аккаунт
          </h2>
          <p className="text-xs tracking-wide uppercase text-neutral-400 dark:text-neutral-500 font-medium">
            Omniconnect
          </p>
        </div>

        <div className="space-y-5 relative z-20">
          <div className="animate-item relative">
            <input
              type="text"
              placeholder="Логин"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              onKeyDown={handleKeyDown}
              className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1"
            />
          </div>

          <div className="animate-item relative">
            <input
              type="password"
              placeholder="Пароль"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              onKeyDown={handleKeyDown}
              className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1"
            />
          </div>

          {error && (
            <p className="text-xs text-red-500 font-medium px-1 pt-1 animate-item">
              {error}
            </p>
          )}

          <div className="animate-item pt-4 relative z-30">
            <button
              type="button" // Явно указываем button, а не submit
              onClick={handleActionSubmit}
              disabled={isLoading}
              className="w-full h-12 rounded-full bg-neutral-950 dark:bg-white text-white dark:text-black font-medium text-sm transition-all hover:opacity-90 active:scale-[0.98] disabled:opacity-40 flex items-center justify-center tracking-wide cursor-pointer"
            >
              {isLoading ? (
                <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" />
              ) : (
                'Продолжить'
              )}
            </button>
          </div>

          <div className="mt-8 text-center animate-item relative z-30">
            <button
              type="button"
              onClick={(e) => {
                e.preventDefault();
                onSwitchMode();
              }}
              className="text-xs tracking-wide text-neutral-500 hover:text-neutral-300 transition-colors underline underline-offset-4 decoration-neutral-800 cursor-pointer p-2"
            >
              У меня ещё нет аккаунта. <span className="underline underline-offset-4 decoration-neutral-300 dark:decoration-neutral-700">Создать</span>
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}