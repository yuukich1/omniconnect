import { create } from 'zustand';

interface User {
    id: string;
    username: string;
}

interface AuthState {
    user: User | null;
    token: string | null;
    isAuthenticated: boolean;
    isHydrated: boolean;

    login: (user: User, token: string) => void;
    logout: () => void;
    hydrate: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    token: null,
    isAuthenticated: false,
    isHydrated: false,

    login: (user, token) => {
        try {
            localStorage.setItem('authToken', token);
            localStorage.setItem('user', JSON.stringify(user));

            set({
                user,
                token,
                isAuthenticated: true,
            });
        } catch (error) {
            console.error('Login storage error:', error);
        }
    },

    logout: () => {
        try {
            localStorage.removeItem('authToken');
            localStorage.removeItem('user');
        } catch (error) {
            console.error('Logout storage error:', error);
        }

        set({
            user: null,
            token: null,
            isAuthenticated: false,
        });
    },

    hydrate: async () => {
        try {
            const savedToken = localStorage.getItem('authToken');
            const savedUser = localStorage.getItem('user');

            set({
                token: savedToken,
                user: savedUser ? JSON.parse(savedUser) : null,
                isAuthenticated: !!savedToken,
                isHydrated: true,
            });
        } catch (error) {
            console.error('Hydration error:', error);

            set({
                user: null,
                token: null,
                isAuthenticated: false,
                isHydrated: true,
            });
        }
    },
}));