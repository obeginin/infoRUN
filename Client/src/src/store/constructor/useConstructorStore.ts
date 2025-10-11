import { create } from "zustand";
import { createJSONStorage, persist } from "zustand/middleware";
import type { Subject } from "@/src/interface/subject.interface";
import FiltersAPI from "@/src/API/filters";
import { Task } from "@/src/interface/taskNumbers.interface";
import ConstructorAPI from "@/src/API/constructor";

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
  endDialog: boolean;
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
      endDialog: false,

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
          set({ variants: response.variants, loading: false });
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

        try {
          const constructorStorage = localStorage.getItem(
            "constructor-storage"
          );
          if (!constructorStorage) {
            set({ error: "Данные не найдены", loading: false });
            return;
          }

          const storageData = JSON.parse(constructorStorage);

          // ПРАВИЛЬНАЯ ПРОВЕРКА ПОЛЕЙ
          if (!storageData.state.subject || !storageData.state.task) {
            set({ error: "Заполните все поля", loading: false });
            return;
          }

          const task = storageData.state.task.TaskID;
          const subject = storageData.state.subject.ID;
          const variant = storageData.state.variant?.VariantID; // вариант может быть опциональным

          const formData = new FormData();

          // Добавляем обязательные поля
          formData.append("task_id", task.toString());
          formData.append("subtask_number", subject.toString());

          // Добавляем вариант если есть
          if (variant) {
            formData.append("variant_id", variant.toString());
          }

          // Добавляем ответ если есть
          if (get().answer) {
            formData.append("answer", get().answer);
          }

          // Добавляем файлы решения
          get().initialAnswerFiles?.forEach((file) => {
            if (file?.file) {
              formData.append("files_solution", file.file);
            }
          });

          // Добавляем файлы описания
          get().initialDescriptionFiles?.forEach((file) => {
            if (file?.file) {
              formData.append("files_extra", file.file);
            }
          });

          // Создаем blocks и добавляем файлы элементов
          const blocks: Blocks[] = [];
          get().elements.forEach((element, index) => {
            if (element.type === "text") {
              blocks.push({
                type: "text",
                content: element.content || "",
              });
            } else if (element.type === "image" && element.file) {
              formData.append(`files_blocks`, element.file);
              blocks.push({
                type: "image",
                file_index: index,
                content: element.file.name || "",
              });
            }
          });

          // Проверяем что есть хотя бы один блок
          if (blocks.length === 0) {
            set({
              error: "Добавьте хотя бы один элемент задания",
              loading: false,
            });
            return;
          }

          formData.append("blocks", JSON.stringify(blocks));

          // Отправляем на сервер
          await ConstructorAPI.create(token, formData);

          // Очищаем состояние после успешного сохранения
          set({
            success: "Задание успешно сохранено",
            loading: false,
            elements: [],
            subject: null,
            task: null,
            variant: null,
            answer: "",
            initialAnswerFiles: [],
            initialDescriptionFiles: [],
            endDialog: true,
          });

          localStorage.removeItem("constructor-storage");
        } catch (error) {
          set({
            error: "Ошибка при сохранении задания: " + error,
            loading: false,
          });
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
