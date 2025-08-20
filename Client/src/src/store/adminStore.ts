import { create } from "zustand";
import type { IUser } from "@/src/interface/user.interface";
import AdminAPI from "@/src/API/admin";
import StudentsAPI from "@/src/API/students";

interface AdminStore {
  users: IUser[];
  currentUser: IUser | null;
  loading: boolean;
  error: string | null;
  success: string | null;
  fetchUsers: (token: string) => Promise<void>;
  deleteUser: (token: string, id: number) => Promise<void>;
  addNewUser: (
    token: string,
    login: string,
    last_name: string,
    first_name: string,
    email: string,
    phone: string,
    sex: string,
    roleId: number,
    password: string
  ) => Promise<void>;
  reset: () => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  filteredUsers: () => IUser[];
  isVisiblePopup: boolean;
  isVisibleDialogPassword: boolean;
  isVisibleDialogDelete: boolean;
  isVisibleDialogEdit: boolean;
  setVisibleDialogPassword: () => void;
  setVisibleDialogDelete: () => void;
  setVisibleDialogEdit: () => void;
  setVisiblePopup: (user: IUser) => void;
  changePassword: (
    token: string,
    id: number,
    password: string
  ) => Promise<void>;
  editUser: (
    token: string,
    id: number,
    login: string,
    last_name: string,
    first_name: string,
    middle_name: string,
    email: string,
    phone: string,
    sex: string,
    birth_date: Date | string,
    comment: string,
    roleId: number,
    password: string
  ) => Promise<void>;
}

export const useAdminStore = create<AdminStore>((set, get) => ({
  users: [],
  currentUser: null,
  loading: false,
  isVisiblePopup: false,
  isVisibleDialogPassword: false,
  isVisibleDialogDelete: false,
  isVisibleDialogEdit: false,
  error: null,
  success: null,
  searchQuery: "",

  fetchUsers: async (token) => {
    set({ loading: true, error: null });
    try {
      const response = await AdminAPI.getUsers(token);
      set({ users: response, loading: false, success: "Users fetched" });
    } catch (error) {
      set({ error: "Failed to fetch users" + error, loading: false });
    }
  },

  deleteUser: async (token, id) => {
    set({ loading: true });
    try {
      await StudentsAPI.deleteStudent(token, id);
      set((state) => ({
        users: state.users.filter((user) => user.ID !== id),
        loading: false,
        isVisibleDialogDelete: false,
        success: "User deleted",
      }));
    } catch (error) {
      set({ error: "Failed to delete user" + error, loading: false });
    }
  },

  changePassword: async (token, id, password) => {
    set({ loading: true });
    try {
      await AdminAPI.ChangePassword(token, id, password);
      set({
        loading: false,
        isVisibleDialogPassword: false,
        success: "Password changed",
      });
    } catch (error) {
      set({ error: "Failed to change password" + error, loading: false });
    }
  },

  filteredUsers: () => {
    const { users, searchQuery } = get();
    if (!searchQuery.trim()) return users;

    const query = searchQuery.toLowerCase();
    return users.filter(
      (user) =>
        user.ID.toString().includes(query) ||
        user.Email.toLowerCase().includes(query) ||
        user.Login.toLowerCase().includes(query) ||
        (user.First_Name && user.First_Name.toLowerCase().includes(query))
    );
  },

  addNewUser: async (
    token,
    login,
    last_name,
    first_name,
    email,
    phone,
    sex,
    roleId,
    password
  ) => {
    set({ loading: true });
    try {
      await StudentsAPI.addNewUser(
        token,
        login,
        last_name,
        first_name,
        email,
        phone,
        sex,
        roleId,
        password
      );
      set({ loading: false, success: "User added" });
    } catch (error) {
      set({ error: "Failed to add user" + error, loading: false });
    }
  },

  editUser: async (
    token,
    id,
    login,
    last_name,
    first_name,
    middle_name,
    email,
    phone,
    sex,
    birth_date,
    comment,
    roleId,
    password
  ) => {
    set({ loading: true });
    try {
      await StudentsAPI.editUser(
        token,
        id,
        login,
        last_name,
        first_name,
        middle_name,
        email,
        phone,
        sex,
        birth_date as string,
        comment,
        roleId,
        password
      );
      set({
        loading: false,
        success: "User edited",
        isVisibleDialogEdit: false,
      });
      get().fetchUsers(token);
    } catch (error) {
      set({
        error: "Failed to edit user" + error,
        loading: false,
        isVisibleDialogEdit: false,
      });
    }
  },

  setSearchQuery: (query) => set({ searchQuery: query }),

  setVisiblePopup: (user: IUser): void =>
    set({
      isVisiblePopup: !get().isVisiblePopup,
      currentUser: user,
    }),

  setVisibleDialogPassword: (): void =>
    set({
      isVisibleDialogPassword: !get().isVisibleDialogPassword,
      currentUser: get().currentUser,
      isVisiblePopup: false,
    }),

  setVisibleDialogDelete: (): void =>
    set({
      isVisibleDialogDelete: !get().isVisibleDialogDelete,
      currentUser: get().currentUser,
      isVisiblePopup: false,
    }),

  setVisibleDialogEdit: (): void =>
    set({
      isVisibleDialogEdit: !get().isVisibleDialogEdit,
      currentUser: get().currentUser,
      isVisiblePopup: false,
    }),

  reset: () => set({ users: [], error: null }),
}));
