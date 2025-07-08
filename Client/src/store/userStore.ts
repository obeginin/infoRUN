import { create } from "zustand";
import { combine, persist } from "zustand/middleware";
import AuthAPI from "../API/auth";

interface User {
  ID: number;
  Login: string;
  email: string;
  first_name: string;
  last_name: string;
  role_name: string;
}

export const useUserStore = create(
  persist(
    combine(
      {
        user: null as User | null,
        token: null as string | null,
      },
      (set) => ({
        login: async (login: string, password: string) => {
          console.log("store", login, password);
          try {
            const data = await AuthAPI.login(login, password);
            console.log(data);
            set({
              user: data.student,
              token: data.access_token,
            });
            localStorage.setItem("token", data.access_token);
          } catch (error) {
            console.log(error);
          }
        },

        logout: async () => {
          try {
            await AuthAPI.logout();
            set({
              user: null,
              token: null,
            });
            localStorage.removeItem("token");
          } catch (error) {
            console.log(error);
          }
        },
      })
    ),
    {
      name: "user-storage",
    }
  )
);
