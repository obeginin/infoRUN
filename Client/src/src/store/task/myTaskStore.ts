import { create } from "zustand";
import { Subject } from "@/src/interface/subject.interface";
import FiltersAPI from "@/src/API/filters";
import SubtaskAPI from "@/src/API/subtask";

export type EditBlock =
  | { type: "text"; content: string }
  | { type: "image"; content: string; file_index?: number; file?: File | null };

export interface HandleEditPayload {
  subtask_id: number;
  subtask_number: number;
  task_id: number;
  variant_id: number;
  answer: null;
  blocks: EditBlock[];
  file_solution?: File | null;
  file_extra?: File | null;
  file_blocks?: File | null;
  comment?: string;
}

interface IData {
  Blocks: IBlock[];
  Comment: string | null;
  Creator: string;
  Description: string;
  DifficultyLevel: number | null;
  Files: [];
  NumberVarinat: number | null;
  SubTaskID: number;
  SubTaskNumber: number;
  SubjectID: number;
  SubjectName: string;
  TaskID: number;
  TaskTitle: string;
  TypeVariant: string | null;
  UploadDate: string;
  VariantID: number;
  VariantName: string;
  YearVariant: number | null;
}

interface IBlock {
  type: string;
  content: string;
}

interface IMyTaskStore {
  loading: boolean;
  task_loading: boolean;
  error: string | null;
  success: string | null;
  subjects: Subject[];
  getSubjects: () => Promise<void>;
  getTask: (student_id: string) => Promise<void>;
  task: IData[];
  currentTask: IData | null;
  setCurrentTask: (task: IData) => void;
  deleteSubtask: (subtask_id: number) => Promise<void>;
  handleEditTask: (payload: HandleEditPayload) => Promise<void>;
  clearError: () => void;
}

export const useMyTaskStore = create<IMyTaskStore>()((set, get) => ({
  loading: false,
  error: null,
  success: null,
  subjects: [],
  task: [],
  currentTask: null,
  task_loading: false,
  getSubjects: async () => {
    set({ loading: true });
    const token = localStorage.getItem("token") || "";
    try {
      const response = await FiltersAPI.getSubjects(token);
      set({ subjects: response.subjects, loading: false });
    } catch (error) {
      set({ error: "Ошибка получения данных" + error, loading: false });
    }
  },

  getTask: async (student_id: string) => {
    set({ task_loading: true });
    const token = localStorage.getItem("token") || "";
    try {
      const response = await SubtaskAPI.getSubtasksCreator(token, student_id);
      set({ task: response.data, task_loading: false });
    } catch (error) {
      set({ error: "Ошибка получения данных" + error, task_loading: false });
    }
  },

  setCurrentTask: (task: IData) => set({ currentTask: task }),

  deleteSubtask: async (subtask_id: number) => {
    set({ loading: true });
    const token = localStorage.getItem("token") || "";
    try {
      const res = await SubtaskAPI.deleteSubtask(token, subtask_id);
      const ok = res?.status === 200 || res?.status === 204;
      if (!ok) set({ error: "Failed to delete subtask", loading: false });
      set((s) => ({
        loading: false,
        success: "Subtask deleted",
        task: s.task.filter((i) => i.SubTaskID !== subtask_id),
      }));
    } catch (error) {
      set({ error: "Failed to delete subtask" + error, loading: false });
    }
  },

  handleEditTask: async (payload: HandleEditPayload) => {
    set({ loading: true, success: null, error: null });
    const token = localStorage.getItem("token") || "";

    try {
      const {
        subtask_number: subtaskNumber,
        task_id: taskId,
        variant_id: variantId,
        answer,
        blocks,
        subtask_id: subtaskId,
        // file_solution: filesSolution,
        // file_extra: filesExtra,
        // file_blocks: filesBlocks,
        // comment,
      } = payload;

      if (!subtaskId) {
        set({ error: "subtaskId обязателен", loading: false });
        return;
      }

      const formData = new FormData();

      formData.append("subtask_id", String(subtaskId));
      if (typeof taskId === "number")
        formData.append("task_id", String(taskId));
      if (typeof subtaskNumber === "number")
        formData.append("subtask_number", String(subtaskNumber));
      if (variantId) formData.append("variant_id", String(variantId));
      if (answer) formData.append("answer", answer);

      // filesSolution?.forEach((f) => f && formData.append("files_solution", f));
      // filesExtra?.forEach((f) => f && formData.append("files_extra", f));

      const outBlocks: EditBlock[] = [];

      blocks.forEach((b, index) => {
        if (b.type === "text") {
          outBlocks.push({ type: "text", content: b.content || "" });
        } else if (b.type === "image") {
          if (b.file) {
            formData.append("files_blocks", b.file);
            outBlocks.push({
              type: "image",
              file_index: index,
              content: b.file.name || "",
            });
          }
        }
      });

      if (outBlocks.length === 0) {
        set({ error: "Добавьте хотя бы один блок", loading: false });
        return;
      }

      formData.append("blocks", JSON.stringify(outBlocks));

      for (const [k, v] of formData.entries()) console.log(k, v);
      await SubtaskAPI.editSubtask(token, subtaskId, formData);

      set({ success: "Задание обновлено", loading: false });

      // опционально обновим currentTask в сторе
      const { currentTask } = get();
      if (currentTask && currentTask.SubTaskID === subtaskId) {
        set({
          currentTask: {
            ...currentTask,
            Blocks: outBlocks.map((b) => ({
              type: b.type,
              content: b.content || "",
            })),
          },
        });
      }
    } catch (error) {
      set({ error: "Ошибка при редактировании: " + error, loading: false });
    }
  },

  clearError: () => set({ error: null }),
}));
