import { useState, useRef } from 'react';
import { registerSchema } from '@/schemas/auth.schema';
import { api } from '@/lib/api';
import axios from 'axios';
import { Step } from './useRegisterAnimations';

export function useRegister(
  onValidationError: () => void,
  onAutoLoginSuccess: (username: string, token: string) => void
) {
  const [step, setStep] = useState<Step>('name');
  const [username, setUsername] = useState('');
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const savedTokenRef = useRef<string | null>(null);

  const validateCurrentStep = (): string | null => {
    if (step === 'name') {
      const res = registerSchema.shape.username.safeParse(username);
      if (!res.success) return res.error.issues[0].message;
      if (username.length > 20) return 'Максимум 20 символов';
    }
    
    if (step === 'email') {
      const res = registerSchema.shape.email.safeParse(email);
      if (!res.success) return res.error.issues[0].message;
    }
    
    if (step === 'password') {
      const res = registerSchema.shape.password.safeParse(password);
      if (!res.success) return res.error.issues[0].message;
      if (password.length > 64) return 'Пароль слишком длинный (макс. 64)';
      if (!/\d/.test(password)) return 'Пароль должен содержать цифру';
      if (!/[A-ZА-Я]/.test(password)) return 'Пароль должен содержать заглавную букву';
    }
    
    return null;
  };

  const goNext = () => {
    setError(null);
    const validationError = validateCurrentStep();
    
    if (validationError) {
      setError(validationError);
      onValidationError();
      return;
    }

    if (step === 'name') return 'email';
    if (step === 'email') return 'password';
    if (step === 'password') return 'summary';
    return null;
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
        formData.append('username', username.trim()); 
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

  const completeWelcome = () => {
    if (savedTokenRef.current) {
      onAutoLoginSuccess(username.trim(), savedTokenRef.current);
    }
  };

  return {
    step, setStep,
    username, setUsername,
    email, setEmail,
    password, setPassword,
    error, setError,
    isLoading,
    goNext,
    handleSubmit,
    completeWelcome
  };
}