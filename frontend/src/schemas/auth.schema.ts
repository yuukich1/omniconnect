import { z } from 'zod';

export const loginSchema = z.object({
  username: z.string('Введите корректный логин'),
  password: z.string().min(6, 'Пароль должен быть не менее 6 символов'),
});

export const registerSchema = z.object({
  email: z.string().email('Введите корректный email'),
  username: z.string().min(3, 'Логин должен быть от 3 символов'),
  password: z.string().min(6, 'Пароль должен быть не менее 6 символов'),
});

export type LoginInput = z.infer<typeof loginSchema>;
export type RegisterInput = z.infer<typeof registerSchema>;