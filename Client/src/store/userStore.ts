import { create } from "zustand";
import { combine, persist } from "zustand/middleware";
import AuthAPI from "../API/auth";

interface User {
  ID: number;
  Login: string;
  Email: string;
  First_Name: string;
  Last_name: string;
  RoleName: string;
}


interface ErrorDetail {
  error: string;
  message: string;
}

export const useUserStore = create(
  persist(
    combine(
      {
        user: null as User | null,
        token: null as string | null,
        error: null as ErrorDetail | null,
      },
      (set) => ({
        login: async (login: string, password: string) => {
          try {
            const data = await AuthAPI.login(login, password);
            if (data.detail) {
              set({
                error: {
                  error: data.detail.error || "Validation Error",
                  message: data.detail.message || "Invalid credentials",
                },
              });
              console.log(data.detail);
              return;
            }
            set({
              user: data.student,
              token: data.access_token,
              error: null,
            });
            localStorage.setItem("token", data.access_token);
            console.log(localStorage.getItem("token"));
          } catch (error: unknown) {
            let message = "Authorization error";
            if (error instanceof Error) message = error.message;
            set({
              error: {
                error: "Authorization error",
                message,
              },
            });
            console.log(error);
          }
        },

        logout: async () => {
          try {
            const token = localStorage.getItem("token");
            await AuthAPI.logout(token ? token : "");
            set({
              user: null,
              token: null,
            });
            localStorage.removeItem("token");
          } catch (error) {
            console.log(error);
          }
        },

        clearError: () => set({ error: null }),
      })
    ),
    {
      name: "user-storage",
    }
  )
);
