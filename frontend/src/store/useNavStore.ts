import { create } from "zustand";

export type TabType = 'home' | 'search' | 'profile';

interface NavState {
    activeTab: TabType;
    setActiveTab: (tab: TabType) => void;
}

export const useNavStore = create<NavState>((set) => ({
    activeTab: 'home',
    setActiveTab: (tab) => set({ activeTab: tab }),
}));