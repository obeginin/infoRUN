import { create } from "zustand";
import type { Task } from "../../../interface/task.interface";
import TasksAPI from "../../../API/tasks";

interface ProfileStore {
  currentTask: Task | null; 
  loading: boolean;
  error: string | null;
  fetchTask: (token: string, id: number) => Promise<void>;
}

export const useProfileStore = create<ProfileStore>((set) => ({
  currentTask: null, 
  loading: false,
  error: null,
  
  fetchTask: async (token: string, id: number) => {
    set({ loading: true, error: null });
    try {
      const response = await TasksAPI.getTask(8, id, token);
      set({ currentTask: response, loading: false });
      console.log("Полученные данные:", response);
    } catch (error) {
      console.error("Ошибка при загрузке:", error);
      set({ error: 'Ошибка загрузки', loading: false });
    }
  },
}));
