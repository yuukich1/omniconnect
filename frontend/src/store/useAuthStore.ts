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
    hydrate: () => void;
}

export const useAuthStore = create<AuthState>((set) => ({
    user: null,
    token: null,
    isAuthenticated: false,
    isHydrated: false,


    login: (user, token) => {
        localStorage.setItem('authToken', token);
        localStorage.setItem('user', JSON.stringify(user));
        set({ user, token, isAuthenticated: true });
    },

    logout: () => {
        localStorage.removeItem('authToken');
        localStorage.removeItem('user');
        set({ user: null, token: null, isAuthenticated: false });
    },

    hydrate: () => {
        if (typeof window === 'undefined') return; 
        
        const savedToken = localStorage.getItem('authToken');
        const savedUser = localStorage.getItem('user');


        set({
            token: savedToken,
            user: savedUser ? JSON.parse(savedUser) : null,
            isAuthenticated: !!savedToken,
            isHydrated: true,
        });
    },
}))