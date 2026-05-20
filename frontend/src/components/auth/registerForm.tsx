'use client';

import React, { useState, useEffect, useRef } from 'react';
import { registerSchema } from '@/schemas/auth.schema';
import { useAuthStore } from '@/store/useAuthStore';
import { api } from '@/lib/api';
import axios from 'axios';
import gsap from 'gsap';

interface RegisterFormProps {
  onSuccess: () => void;
  onSwitchMode: () => void;
}

type Step = 'name' | 'email' | 'password' | 'summary' | 'welcome';

export default function RegisterForm({ onSuccess, onSwitchMode }: RegisterFormProps) {
  const loginGlobal = useAuthStore((state) => state.login);
  
  const [step, setStep] = useState<Step>('name');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const containerRef = useRef<HTMLDivElement>(null);
  const inputRef = useRef<HTMLInputElement>(null);
  const nextBtnRef = useRef<HTMLButtonElement>(null);
  const prevBtnRef = useRef<HTMLButtonElement>(null);
  const summaryRef = useRef<HTMLDivElement>(null);
  const hintRef = useRef<HTMLParagraphElement>(null);
  const welcomeRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    if (step !== 'summary' && step !== 'welcome') {
      inputRef.current?.focus();
    }
  }, [step]);

  useEffect(() => {
    if (hintRef.current && step !== 'welcome') {
      gsap.fromTo(hintRef.current, 
        { opacity: 0, y: -5 },
        { opacity: 1, y: 0, duration: 0.3, ease: 'power2.out' }
      );
    }
  }, [step]);

  useEffect(() => {
    if (step === 'summary' || step === 'welcome') return;
    const value = step === 'name' ? username : step === 'email' ? email : password;
    
    if (value.trim().length > 0) {
      gsap.to(nextBtnRef.current, { opacity: 1, x: 0, pointerEvents: 'auto', duration: 0.2, ease: 'power2.out' });
    } else {
      gsap.to(nextBtnRef.current, { opacity: 0, x: -8, pointerEvents: 'none', duration: 0.15 });
    }
  }, [username, email, password, step]);

  useEffect(() => {
    if (step !== 'name' && step !== 'summary' && step !== 'welcome') {
      gsap.to(prevBtnRef.current, { opacity: 1, x: 0, pointerEvents: 'auto', duration: 0.2 });
    } else {
      gsap.to(prevBtnRef.current, { opacity: 0, x: 8, pointerEvents: 'none', duration: 0.15 });
    }
  }, [step]);

  useEffect(() => {
    if (step === 'summary' && summaryRef.current) {
      gsap.fromTo(summaryRef.current.querySelectorAll('.summary-item'),
        { opacity: 0, y: 15, scale: 0.98 },
        { opacity: 1, y: 0, scale: 1, duration: 0.4, stagger: 0.06, ease: 'power4.out' }
      );
    }
  }, [step]);

  const savedTokenRef = useRef<string | null>(null);

    useEffect(() => {
        if (step === 'welcome' && welcomeRef.current) {
            gsap.fromTo(welcomeRef.current.querySelectorAll('.welcome-item'),
            { opacity: 0, y: 25, scale: 0.96 },
            { 
                opacity: 1, 
                y: 0, 
                scale: 1, 
                duration: 0.6, 
                stagger: 0.15, 
                ease: 'power4.out',
                onComplete: () => {
                gsap.to(containerRef.current, {
                    opacity: 0,
                    scale: 0.98,
                    duration: 0.4,
                    delay: 2,
                    ease: 'power3.inOut',
                    onComplete: () => {
                    if (savedTokenRef.current) {
                        loginGlobal(
                        { id: 'current_user', username: username.trim() }, 
                        savedTokenRef.current
                        );
                    }
                    onSuccess(); 
                    }
                });
                }
            }
            );
        }
    }, [step, onSuccess, username, loginGlobal]);

  const changeStep = (nextStep: Step) => {
    setError(null);
    if (inputRef.current && nextStep !== 'summary' && nextStep !== 'welcome') {
      gsap.to(inputRef.current, {
        opacity: 0,
        x: nextStep === 'password' || (step === 'name' && nextStep === 'email') ? -10 : 10,
        duration: 0.15,
        onComplete: () => {
          setStep(nextStep);
          gsap.fromTo(inputRef.current, 
            { opacity: 0, x: nextStep === 'password' || (step === 'name' && nextStep === 'email') ? 10 : -10 }, 
            { opacity: 1, x: 0, duration: 0.2 }
          );
        }
      });
    } else {
      setStep(nextStep);
    }
  };

  const goNext = () => {
    setError(null);
    if (step === 'name') {
      if (username.trim().length < 3) return setError('Минимум 3 символа'), shake();
      if (username.length > 20) return setError('Максимум 20 символов'), shake();
      changeStep('email');
    } else if (step === 'email') {
      if (!email.includes('@') || email.trim().length < 5) return setError('Некорректный формат email'), shake();
      changeStep('password');
    } else if (step === 'password') {
      if (password.length < 8) return setError('Пароль должен быть от 8 символов'), shake();
      if (password.length > 64) return setError('Пароль слишком длинный (макс. 64)'), shake();
      if (!/\d/.test(password)) return setError('Пароль должен содержать цифру'), shake();
      if (!/[A-ZА-Я]/.test(password)) return setError('Пароль должен содержать заглавную букву'), shake();
      changeStep('summary');
    }
  };

  const shake = () => {
    gsap.to(containerRef.current, {
      x: 6, duration: 0.05, yoyo: true, repeat: 4,
      onComplete: () => gsap.set(containerRef.current, { x: 0 })
    });
  };


    const handleSubmit = async () => {
    setError(null);
    setIsLoading(true);
    try {
        const regResponse = await api.post('/auth/register', {
        email: email.trim(),
        username: username.trim(),
        password: password,
        });

        if (regResponse.status === 200 || regResponse.status === 201) {
        const formData = new URLSearchParams();
        formData.append('username', email.trim()); 
        formData.append('password', password);

        const tokenResponse = await api.post('/auth/token', formData, {
            headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
        });

        const token = tokenResponse.data.access_token;

        if (token) {

            savedTokenRef.current = token;
            
            setStep('welcome');
        } else {
            setError('Аккаунт создан, но не удалось авторизоваться автоматически');
        }
        }
    } catch (err) {
        if (axios.isAxiosError(err) && err.response) {
        setError(err.response.data?.detail || 'Ошибка при регистрации или авто-входе');
        } else {
        setError('Сервер недоступен');
        }
    } finally {
        setIsLoading(false);
    }
    };

  return (
    <div ref={containerRef} className="fixed inset-0 flex flex-col items-center justify-center bg-white dark:bg-black px-6 z-50 select-none overflow-hidden">
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[350px] h-[350px] bg-neutral-200 dark:bg-neutral-800/40 rounded-full blur-[120px] pointer-events-none" />

      {step !== 'summary' && step !== 'welcome' && (
        <div className="w-full max-w-sm mb-4 text-center px-12 sm:px-0">
          <p ref={hintRef} className="text-xs tracking-wide text-neutral-400 dark:text-neutral-500 font-light transition-all">
            {step === 'name' && `Имя пользователя (максимум 20 символов: ${username.length}/20)`}
            {step === 'email' && 'Введите действующий почтовый адрес'}
            {step === 'password' && 'От 8 символов, включая 1 цифру и 1 заглавную букву'}
          </p>
        </div>
      )}

      {step !== 'summary' && step !== 'welcome' && (
        <div className="relative w-full max-w-sm flex items-center justify-center z-10 px-14 sm:px-0">
          <button
            ref={prevBtnRef}
            type="button"
            style={{ opacity: 0, transform: 'translateX(8px)' }}
            onClick={() => changeStep(step === 'password' ? 'email' : 'name')}
            className="absolute left-0 sm:-left-16 h-12 w-12 flex items-center justify-center rounded-full bg-neutral-50 dark:bg-neutral-900 border border-neutral-200 dark:border-neutral-800 text-neutral-500 dark:text-neutral-400 hover:text-neutral-900 dark:hover:text-neutral-100 active:scale-95 transition-all"
          >
            <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2"><path d="M10 12L6 8l4-4"/></svg>
          </button>

          <div className="w-full h-14 relative flex items-center">
            {step === 'name' && (
              <input
                ref={inputRef}
                type="text"
                value={username}
                maxLength={25} 
                placeholder="Как к вам обращаться?"
                onChange={(e) => setUsername(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && username.trim() && goNext()}
                className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1 font-light"
              />
            )}

            {step === 'email' && (
              <input
                ref={inputRef}
                type="email"
                value={email}
                placeholder="Укажите ваш Email"
                onChange={(e) => setEmail(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && email.trim() && goNext()}
                className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1 font-light"
              />
            )}

            {step === 'password' && (
              <input
                ref={inputRef}
                type="password"
                value={password}
                placeholder="Придумайте пароль"
                onChange={(e) => setPassword(e.target.value)}
                onKeyDown={(e) => e.key === 'Enter' && password.trim() && goNext()}
                className="w-full h-12 bg-transparent border-b border-neutral-200 dark:border-neutral-800 text-neutral-950 dark:text-neutral-50 placeholder-neutral-400 dark:placeholder-neutral-600 outline-none text-base transition-colors focus:border-neutral-900 dark:focus:border-neutral-100 py-2 px-1 font-light"
              />
            )}
          </div>

          <button
            ref={nextBtnRef}
            type="button"
            style={{ opacity: 0, transform: 'translateX(-8px)' }}
            onClick={goNext}
            className="absolute right-0 sm:-right-16 h-12 w-12 flex items-center justify-center rounded-full bg-neutral-950 dark:bg-white text-white dark:text-black font-semibold active:scale-95 transition-all"
          >
            <svg width="18" height="18" viewBox="0 0 16 16" fill="none" stroke="currentColor" strokeWidth="2.5"><path d="M6 4l4 4-4 4"/></svg>
          </button>
        </div>
      )}

      {step === 'summary' && (
        <div ref={summaryRef} className="w-full max-w-sm space-y-6 z-10 px-4 sm:px-0">
          <div className="space-y-1 text-center summary-item opacity-0">
            <h2 className="text-3xl font-light tracking-tight text-neutral-900 dark:text-neutral-100">Проверьте данные</h2>
            <p className="text-xs tracking-wide uppercase text-neutral-400 dark:text-neutral-500 font-medium">Всё верно?</p>
          </div>

          <div className="border-t border-b border-neutral-100 dark:border-neutral-900 py-2 space-y-1">
            <div onClick={() => changeStep('name')} className="summary-item opacity-0 flex items-center justify-between px-2 py-3 rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-900/50 cursor-pointer transition-colors group">
              <span className="text-sm text-neutral-400 dark:text-neutral-500 font-light">Никнейм</span>
              <span className="text-base text-neutral-900 dark:text-neutral-100 font-light group-hover:underline underline-offset-4 decoration-neutral-400">{username}</span>
            </div>

            <div onClick={() => changeStep('email')} className="summary-item opacity-0 flex items-center justify-between px-2 py-3 rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-900/50 cursor-pointer transition-colors group">
              <span className="text-sm text-neutral-400 dark:text-neutral-500 font-light">Email</span>
              <span className="text-base text-neutral-900 dark:text-neutral-100 font-light max-w-[180px] sm:max-w-[200px] truncate group-hover:underline underline-offset-4 decoration-neutral-400">{email}</span>
            </div>

            <div onClick={() => changeStep('password')} className="summary-item opacity-0 flex items-center justify-between px-2 py-3 rounded-xl hover:bg-neutral-50 dark:hover:bg-neutral-900/50 cursor-pointer transition-colors group">
              <span className="text-sm text-neutral-400 dark:text-neutral-500 font-light">Пароль</span>
              <span className="text-base text-neutral-400 dark:text-neutral-600 tracking-widest text-xs">••••••••</span>
            </div>
          </div>

          <div className="summary-item opacity-0">
            <button
              type="button"
              onClick={handleSubmit}
              disabled={isLoading}
              className="w-full h-12 rounded-full bg-neutral-950 dark:bg-white text-white dark:text-black font-medium text-sm transition-all hover:opacity-90 active:scale-[0.98] disabled:opacity-40 flex items-center justify-center tracking-wide"
            >
              {isLoading ? <div className="h-4 w-4 animate-spin rounded-full border-2 border-current border-t-transparent" /> : 'Создать аккаунт'}
            </button>
          </div>
        </div>
      )}

      {step === 'welcome' && (
        <div ref={welcomeRef} className="text-center space-y-2 z-10">
          <h1 className="welcome-item opacity-0 text-4xl font-light tracking-tight text-neutral-900 dark:text-neutral-100">
            Добро пожаловать!
          </h1>
          <p className="welcome-item opacity-0 text-sm tracking-wide text-neutral-400 dark:text-neutral-500 font-medium uppercase">
            {username}
          </p>
        </div>
      )}

      {error && step !== 'welcome' && (
        <p className="text-xs text-red-500 font-medium mt-4 absolute transform translate-y-52 sm:translate-y-52 z-20 px-1 text-center">{error}</p>
      )}

      {step !== 'welcome' && (
        <div className="absolute bottom-12 left-1/2 -translate-x-1/2 text-center z-10 w-full">
          <button
            type="button"
            onClick={onSwitchMode}
            className="text-xs tracking-wide text-neutral-500 hover:text-neutral-900 dark:hover:text-neutral-200 transition-colors underline underline-offset-4 decoration-neutral-200 dark:decoration-neutral-800"
          >
            Уже есть аккаунт. <span className="underline underline-offset-4 decoration-neutral-300 dark:decoration-neutral-700">Войти</span>
          </button>
        </div>
      )}

    </div>
  );
}