'use client';

import React, { useState } from 'react';
import LoginForm from './loginForm';
import RegisterForm from './registerForm';


export default function AuthScreen() {
  const [isLoginMode, setIsLoginMode] = useState(true);

  return (
    <div className="flex min-h-screen items-center justify-center bg-neutral-50 px-4 dark:bg-neutral-950">
      <div className="w-full max-w-md rounded-2xl border border-neutral-200 bg-white p-8 shadow-sm dark:border-neutral-800 dark:bg-neutral-900">
        
        <div className="text-center mb-8">
          <h2 className="text-3xl font-bold tracking-tight text-neutral-900 dark:text-white">
            {isLoginMode ? 'Вход в аккаунт' : 'Создать аккаунт'}
          </h2>
          <p className="mt-2 text-sm text-neutral-500 dark:text-neutral-400">
            {isLoginMode ? 'Используйте свой Email для входа' : 'Заполните данные для регистрации'}
          </p>
        </div>

        {isLoginMode ? (
          <LoginForm onSwitchMode={() => setIsLoginMode(false)} />
        ) : (
          <RegisterForm 
            onSuccess={() => {}}
            onSwitchMode={() => setIsLoginMode(true)} 
          />
        )}

      </div>
    </div>
  );
}