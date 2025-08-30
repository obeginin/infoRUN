import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import type { Subject } from "../interface/subject.interface";
import FiltersAPI from "../API/filters";
import { Task } from "../interface/taskNumbers.interface";
import ConstructorAPI from "../API/constructor";

export type TaskElementType = "text" | "image";

export interface TaskElement {
  id: string;
  type: TaskElementType;
  content?: string;
  file?: File | null;
}

export interface TaskConstructorState {
  elements: TaskElement[];
}

export interface IInitialAnswerFiles {
  id: number;
  file: File | null;
}

export interface Blocks {
  type: string;
  content: string;
  file_index?: number;
}

export interface Variants {
  VariantID: number;
  VariantName: string;
}

interface ConstructorStore {
  loading: boolean;
  error: string | null;
  setError: (error: string | null) => void;
  success: string | null;
  subjects: Subject[];
  subject: Subject | null;
  setSubject: (subject: Subject) => void;
  getSubjects: () => Promise<void>;
  task: Task | null;
  tasks: Task[];
  setTask: (task: Task) => void;
  getTaskNumber: (task_id: number) => Promise<void>;
  getVarinants: () => Promise<void>;
  variants: Variants[];
  variant: Variants | null;
  setVariant: (variant: Variants) => void;
  answer: string;
  setAnswer: (answer: string) => void;
  image: File | null;
  setImage: (image: File | null) => void;
  elements: TaskElement[];
  initialAnswerFiles: IInitialAnswerFiles[];
  initialAnswerFilesAdd: () => void;
  initialAnswerFilesRemove: (id: number) => void;
  updateInitialAnswerFile: (id: number, file: File | null) => void;
  updateInitialDescriptionFile: (id: number, file: File | null) => void;
  initialDescriptionFiles: IInitialAnswerFiles[];
  initialDescriptionFilesAdd: () => void;
  initialDescriptionFilesRemove: (id: number) => void;
  moveElement: (id: string, direction: "up" | "down") => void;
  addElement: (type: TaskElementType) => void;
  updateElement: (id: string, updates: Partial<TaskElement>) => void;
  removeElement: (id: string) => void;
  handleSave: () => Promise<void>;
  clearMessages: () => void;
}

export const useConstructorStore = create<ConstructorStore>()(
  persist(
    (set, get) => ({
      loading: false,
      error: null,
      success: null,
      subject: null,
      subjects: [],
      task: null,
      variants: [],
      variant: null,
      answer: "",
      image: null,
      tasks: [],
      elements: [],
      initialAnswerFiles: [],
      initialDescriptionFiles: [],

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

      setSubject: (subject: Subject) => {
        set({ subject });
      },

      getTaskNumber: async (task_id: number) => {
        set({ loading: true });
        const token = localStorage.getItem("token") || "";
        try {
          const response = await FiltersAPI.getTaskNumber(token, task_id);
          set({ tasks: response.tasks, loading: false });
        } catch (error) {
          set({ error: "Ошибка получения данных" + error, loading: false });
        }
      },

      setTask: (task: Task) => {
        set({ task });
      },

      getVarinants: async () => {
        set({ loading: true });
        const token = localStorage.getItem("token") || "";
        try {
          const response = await FiltersAPI.getVariants(token);
          set({ variants: response, loading: false });
        } catch (error) {
          set({ error: "Ошибка получения данных" + error, loading: false });
        }
      },

      setVariant: (variant: Variants) => {
        set({ variant });
      },

      setAnswer: (answer: string) => {
        set({ answer });
      },

      setImage: (image: File | null) => {
        set({ image });
      },

      moveElement: (id: string, direction: "up" | "down") => {
        set((state) => ({
          elements: state.elements.map((element) => {
            if (element.id === id) {
              const index = state.elements.indexOf(element);
              if (direction === "up" && index > 0) {
                return state.elements[index - 1];
              } else if (
                direction === "down" &&
                index < state.elements.length - 1
              ) {
                return state.elements[index + 1];
              }
            }
            return element;
          }),
        }));
      },

      addElement: (type: TaskElementType) => {
        console.log(
          get().initialAnswerFiles,
          get().initialDescriptionFiles,
          get().elements
        );
        const newElement: TaskElement = {
          id: Date.now().toString(),
          type: type,
          content: type === "text" ? "" : undefined,
          file: type === "image" ? null : undefined,
        };

        set((state) => ({
          elements: [...state.elements, newElement],
        }));
      },

      initialAnswerFilesAdd: () => {
        const newElement = {
          id: Date.now(),
          file: null,
        };

        set((state) => ({
          initialAnswerFiles: [...state.initialAnswerFiles, newElement],
        }));
      },

      initialDescriptionFilesAdd: () => {
        const newElement = {
          id: Date.now(),
          file: null,
        };
        set((state) => ({
          initialDescriptionFiles: [
            ...state.initialDescriptionFiles,
            newElement,
          ],
        }));
      },

      initialDescriptionFilesRemove: (id: number) => {
        set((state) => ({
          initialDescriptionFiles: state.initialDescriptionFiles.filter(
            (element) => element.id !== id
          ),
        }));
      },

      initialAnswerFilesRemove: (id: number) => {
        set((state) => ({
          initialAnswerFiles: state.initialAnswerFiles.filter(
            (element) => element.id !== id
          ),
        }));
      },

      updateInitialAnswerFile: (id: number, file: File | null) => {
        set((state) => ({
          initialAnswerFiles: state.initialAnswerFiles.map((element) => {
            if (element.id === id) {
              return { ...element, file };
            }
            return element;
          }),
        }));
      },

      updateInitialDescriptionFile: (id: number, file: File | null) => {
        set((state) => ({
          initialDescriptionFiles: state.initialDescriptionFiles.map(
            (element) => {
              if (element.id === id) {
                return { ...element, file };
              }
              return element;
            }
          ),
        }));
      },

      updateElement: (id: string, updates: Partial<TaskElement>) => {
        set((state) => ({
          elements: state.elements.map((element) =>
            element.id === id ? { ...element, ...updates } : element
          ),
        }));
      },

      removeElement: (id: string) => {
        set((state) => ({
          elements: state.elements.filter((element) => element.id !== id),
        }));
      },

      handleSave: async () => {
        set({ loading: true, success: null, error: null });
        const token = localStorage.getItem("token") || "";
        const constructorStorage = localStorage.getItem("constructor-storage");
        const data = JSON.parse(constructorStorage || "");

        if (!data.state.subject || !data.state.task || !data.state.variant_id) {
          set({ error: "Заполните все поля", loading: false });
          return;
        } else {
          const task = data.state.task.TaskID;
          const subject = data.state.subject.ID;
          const variant = data.state.variant.VariantID;

          try {
            const data = new FormData();

            if (get().task?.TaskID) {
              data.append("subtask_number", subject);
            }
            if (get().variant?.VariantID) {
              data.append("variant_id", variant);
            }
            if (get().subject?.ID) {
              data.append("task_id", task);
            }
            if (get().answer) {
              data.append("answer", get().answer);
            }
            if (get().initialAnswerFiles) {
              get().initialAnswerFiles.forEach((file) => {
                if (file.file) {
                  data.append(`files_solution`, file.file);
                }
              });
            }
            if (get().initialDescriptionFiles) {
              get().initialDescriptionFiles.forEach((file) => {
                if (file.file) {
                  data.append(`files`, file.file);
                }
              });
            }

            const blocks: Blocks[] = [];
            get().elements.forEach((element, index) => {
              if (element.type === "text") {
                blocks.push({
                  type: "text",
                  content: element.content || "",
                });
              } else if (element.type === "image" && element.file) {
                // Добавляем файл в FormData
                data.append(`file_${index}`, element.file);

                blocks.push({
                  type: "image",
                  file_index: index,
                  content: element.content || "",
                });
              }
            });

            // Добавляем blocks как JSON строку
            data.append("blocks", JSON.stringify(blocks));

            console.log(data);
            if (
              get().task === null ||
              get().subject === null ||
              blocks.length === 0
            ) {
              set({
                error: "Задание не было сохранено. Проверьте введенные данные",
                loading: false,
              });
            } else {
              await ConstructorAPI.create(token, data);
              set({
                success: "Задание успешно сохранено: ",
                loading: false,
                elements: [],
                subject: null,
                task: null,
                variant: null,
                answer: "",
                initialAnswerFiles: [],
                initialDescriptionFiles: [],
              });
              localStorage.removeItem("constructor-storage");
            }
          } catch (error) {
            set({ error: "Failed to save task" + error, loading: false });
          }
        }
      },

      clearMessages: () => {
        set({ error: null, success: null });
      },
      setError: (error: string | null) => {
        set({ error });
      },
    }),
    {
      name: "constructor-storage",
      storage: createJSONStorage(() => localStorage),
      partialize: (state) => ({
        subject: state.subject,
        task: state.task,
        variant: state.variant,
        answer: state.answer,
      }),
    }
  )
);
