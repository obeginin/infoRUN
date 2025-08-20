import { create } from "zustand";

interface ThemeStore {
  isDark: boolean;
  toggleTheme: () => void;
}

export const useThemeStore = create<ThemeStore>((set) => ({
  isDark: false,
  toggleTheme: () => {
    set(() => ({
      isDark: localStorage.getItem("theme") === "dark" ? false : true,
    }));
  },
}));
