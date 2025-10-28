import { create } from "zustand";

interface TimerStore {
  hours: number;
  minutes: number;
  seconds: number;
  isRunning: boolean;
  isTabActive: boolean;
  currentTaskId: number | null;
  setTabActive: (active: boolean) => void;
  startTimer: (
    hours: number,
    minutes: number,
    seconds: number,
    taskId: number
  ) => void;
  stopTimer: () => void;
  tick: () => void;
  loadTimer: () => void;
  resetTimer: () => void;
  setCurrentTask: (taskId: number) => void;
}

export const useTimerStore = create<TimerStore>((set) => ({
  hours: 0,
  minutes: 0,
  seconds: 0,
  isRunning: false,
  isTabActive: false,
  currentTaskId: null,

  setTabActive: (active) => set({ isTabActive: active }),

  setCurrentTask: (taskId) => set({ currentTaskId: taskId }),

  startTimer: (hours, minutes, seconds, taskId) => {
    const existingTimer = localStorage.getItem(`timerEnd_${taskId}`);
    if (existingTimer) return;

    const endTime = new Date();
    endTime.setHours(endTime.getHours() + hours);
    endTime.setMinutes(endTime.getMinutes() + minutes);
    endTime.setSeconds(endTime.getSeconds() + seconds);

    localStorage.setItem(`timerEnd_${taskId}`, endTime.getTime().toString());
    localStorage.setItem("currentTaskId", taskId.toString());

    set({
      hours,
      minutes,
      seconds,
      isRunning: true,
      currentTaskId: taskId,
    });
  },

  loadTimer: () => {
    const taskId = localStorage.getItem("currentTaskId");
    if (!taskId) return;

    const savedEndTime = localStorage.getItem(`timerEnd_${taskId}`);
    if (savedEndTime) {
      const now = new Date();
      const endTime = new Date(parseInt(savedEndTime));
      const diff = endTime.getTime() - now.getTime();

      if (diff > 0) {
        const hours = Math.floor(diff / (1000 * 60 * 60));
        const minutes = Math.floor((diff % (1000 * 60 * 60)) / (1000 * 60));
        const seconds = Math.floor((diff % (1000 * 60)) / 1000);

        set({
          hours,
          minutes,
          seconds,
          isRunning: true,
          currentTaskId: parseInt(taskId),
        });
      }
    }
  },

  resetTimer: () => {
    const taskId = localStorage.getItem("currentTaskId");
    if (taskId) {
      localStorage.removeItem(`timerEnd_${taskId}`);
      localStorage.removeItem("currentTaskId");
    }

    set({
      hours: 0,
      minutes: 0,
      seconds: 0,
      isRunning: false,
      isTabActive: false,
      currentTaskId: null,
    });
  },

  tick: () => {
    set((state) => {
      if (!state.isRunning) return state;
      const { hours, minutes, seconds } = state;
      if (seconds > 0) {
        return { ...state, seconds: seconds - 1 };
      }
      if (minutes > 0) {
        return { ...state, minutes: minutes - 1, seconds: 59 };
      }
      if (hours > 0) {
        return { hours: hours - 1, minutes: 59, seconds: 59 };
      }
      return { ...state, isRunning: false };
    });
  },

  stopTimer: () => {
    set({ isRunning: false });
  },
}));
