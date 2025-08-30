import { create } from "zustand";
import AuthAPI from "@/src/API/auth";

interface ResetPasswordStore {
  email: string;
  new_password: string;
  repeat_new_password: string;
  error: string | null;
  success: string | null;
  loading: boolean;
  resetPassword: (email: string) => Promise<void>;
  resetPasswordWithToken: (
    token: string,
    new_password: string,
    repeat_new_password: string
  ) => Promise<void>;
  reset: () => void;
}

export const useResetPasswordStore = create<ResetPasswordStore>((set) => ({
  email: "",
  new_password: "",
  repeat_new_password: "",
  error: null,
  success: null,
  loading: false,
  resetPassword: async (email: string) => {
    set({ loading: true });
    try {
      const response = await AuthAPI.resetPassword(email);
      set({ success: response.message, loading: false });
    } catch (error) {
      set({ error: "Failed to reset password" + error, loading: false });
    }
  },
  resetPasswordWithToken: async (
    token: string,
    new_password: string,
    repeat_new_password: string
  ) => {
    set({ loading: true });
    try {
      const response = await AuthAPI.resetPasswordWithToken(
        token,
        new_password,
        repeat_new_password
      );
      set({
        success: "Успешное сброса пароля" + response.message,
        loading: false,
      });
    } catch (error) {
      set({ error: "Ошибка сброса пароля" + error, loading: false });
    }
  },
  reset: () => {
    set({
      email: "",
      new_password: "",
      repeat_new_password: "",
      error: null,
      success: null,
      loading: false,
    });
  },
}));
