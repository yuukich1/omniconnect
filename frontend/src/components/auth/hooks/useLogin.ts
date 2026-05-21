import { useState } from 'react';
import { loginSchema } from '@/schemas/auth.schema';
import { api } from '@/lib/api';
import axios from 'axios';

interface UseLoginProps {
  onSuccess: (username: string, token: string) => void;
  onValidationError: () => void;
  onApiError: () => void;
}

export function useLogin({ onSuccess, onValidationError, onApiError }: UseLoginProps) {
  const [username, setUsername] = useState('');
  const [password, setPassword] = useState('');
  const [error, setError] = useState<string | null>(null);
  const [isLoading, setIsLoading] = useState(false);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError(null);

    const validation = loginSchema.safeParse({ username, password });
    if (!validation.success) {
      setError(validation.error.issues[0].message);
      onValidationError();
      return;
    }

    setIsLoading(true);
    try {
      const formData = new URLSearchParams();
      formData.append('username', username.trim());
      formData.append('password', password);

      const response = await api.post('/auth/token', formData, {
        headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      });

      const token = response.data.access_token;

      if (token) {
        onSuccess(username.trim(), token);
      } else {
        setError('Не удалось получить токен доступа');
      }
    } catch (err) {
      onApiError();
      if (axios.isAxiosError(err) && err.response) {
        setError(err.response.data?.detail || 'Неверный логин или пароль');
      } else {
        setError('Сервер недоступен. Проверь FastAPI.');
      }
    } finally {
      setIsLoading(false);
    }
  };

  return {
    username,
    setUsername,
    password,
    setPassword,
    error,
    isLoading,
    handleSubmit
  };
}