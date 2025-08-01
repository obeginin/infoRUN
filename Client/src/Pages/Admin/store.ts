import { create } from "zustand";
import type { IUser } from "../../interface/user.interface";
import AdminAPI from "../../API/admin";

interface AdminStore {
  users: IUser[];
  currentUser: IUser | null;
  loading: boolean;
  error: string | null;
  success: string | null;
  fetchUsers: (token: string) => Promise<void>;
  deleteUser: (token: string, email: string) => Promise<void>;
  reset: () => void;
  searchQuery: string;
  setSearchQuery: (query: string) => void;
  filteredUsers: () => IUser[];
  isVisiblePopup: boolean;
  isVisibleDialogPassword: boolean;
  isVisibleDialogDelete: boolean;
  setVisibleDialogPassword: () => void;
  setVisibleDialogDelete: () => void;
  setVisiblePopup: (user: IUser) => void;
  changePassword: (
    token: string,
    id: number,
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

  deleteUser: async (token, email) => {
    set({ loading: true });
    try {
      await AdminAPI.DeleteUser(token, email);
      set((state) => ({
        users: state.users.filter((user) => user.Email !== email),
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
    set({ isVisibleDialogDelete: !get().isVisibleDialogDelete }),

  reset: () => set({ users: [], error: null }),
}));
