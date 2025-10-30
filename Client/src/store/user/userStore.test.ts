import { act, renderHook } from '@testing-library/react';
import { useUserStore } from './userStore';
import AuthAPI from '@/API/auth';
import { User } from './user.interface';

// Мокируем AuthAPI
jest.mock('@/API/auth');
const mockedAuthAPI = AuthAPI as jest.Mocked<typeof AuthAPI>;

// Мокируем localStorage
const localStorageMock = {
  getItem: jest.fn(),
  setItem: jest.fn(),
  removeItem: jest.fn(),
};
Object.defineProperty(window, 'localStorage', {
  value: localStorageMock,
});

describe('userStore', () => {
  beforeEach(() => {
    // Очищаем все моки перед каждым тестом
    jest.clearAllMocks();
    // Очищаем состояние store
    useUserStore.setState({
      user: null,
      token: null,
      error: null,
      loading: false,
    });
  });

  describe('initial state', () => {
    it('should have correct initial state', () => {
      const { result } = renderHook(() => useUserStore());
      
      expect(result.current.user).toBeNull();
      expect(result.current.token).toBeNull();
      expect(result.current.error).toBeNull();
      expect(result.current.loading).toBe(false);
    });
  });

  describe('login', () => {
    it('should login successfully with valid credentials', async () => {
      const mockUser = {
        ID: 1,
        Login: 'testuser',
        Email: 'test@example.com',
        First_Name: 'Test',
        Last_name: 'User',
        RoleName: 'Student'
      };
      
      const mockResponse = {
        student: mockUser,
        access_token: 'mock-token-123'
      };

      mockedAuthAPI.loginV2.mockResolvedValue(mockResponse);

      const { result } = renderHook(() => useUserStore());

      await act(async () => {
        await result.current.login('testuser', 'password123');
      });

      expect(result.current.user).toEqual(mockUser);
      expect(result.current.token).toBe('mock-token-123');
      expect(result.current.error).toBeNull();
      expect(result.current.loading).toBe(false);
      expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'mock-token-123');
      expect(mockedAuthAPI.loginV2).toHaveBeenCalledWith('testuser', 'password123');
    });

    it('should handle login error with detail', async () => {
      const mockErrorResponse = {
        detail: {
          error: 'Validation Error',
          message: 'Invalid credentials'
        }
      };

      mockedAuthAPI.loginV2.mockResolvedValue(mockErrorResponse);

      const { result } = renderHook(() => useUserStore());

      await act(async () => {
        await result.current.login('testuser', 'wrongpassword');
      });

      expect(result.current.user).toBeNull();
      expect(result.current.token).toBeNull();
      expect(result.current.error).toEqual({
        error: 'Validation Error',
        message: 'Invalid credentials'
      });
      expect(result.current.loading).toBe(false);
      expect(localStorageMock.setItem).not.toHaveBeenCalled();
    });

    it('should handle login error with missing detail fields', async () => {
      const mockErrorResponse = {
        detail: {
          error: '',
          message: ''
        }
      };

      mockedAuthAPI.loginV2.mockResolvedValue(mockErrorResponse);

      const { result } = renderHook(() => useUserStore());

      await act(async () => {
        await result.current.login('testuser', 'wrongpassword');
      });

      expect(result.current.error).toEqual({
        error: 'Validation Error',
        message: 'Invalid credentials'
      });
    });

    it('should handle login network error', async () => {
      const networkError = new Error('Network error');
      mockedAuthAPI.loginV2.mockRejectedValue(networkError);

      const { result } = renderHook(() => useUserStore());

      await act(async () => {
        await result.current.login('testuser', 'password123');
      });

      expect(result.current.user).toBeNull();
      expect(result.current.token).toBeNull();
      expect(result.current.error).toEqual({
        error: 'Authorization error',
        message: 'Network error'
      });
      expect(result.current.loading).toBe(false);
      expect(localStorageMock.setItem).not.toHaveBeenCalled();
    });

    it('should handle login with non-Error rejection', async () => {
      mockedAuthAPI.loginV2.mockRejectedValue('String error');

      const { result } = renderHook(() => useUserStore());

      await act(async () => {
        await result.current.login('testuser', 'password123');
      });

      expect(result.current.error).toEqual({
        error: 'Authorization error',
        message: 'Authorization error'
      });
    });

    it('should set loading to true during login', async () => {
      let resolvePromise: (value: { student: User; access_token: string }) => void;
      const promise = new Promise<{ student: User; access_token: string }>((resolve) => {
        resolvePromise = resolve;
      });
      
      mockedAuthAPI.loginV2.mockReturnValue(promise);

      const { result } = renderHook(() => useUserStore());

      act(() => {
        result.current.login('testuser', 'password123');
      });

      expect(result.current.loading).toBe(true);

      await act(async () => {
        resolvePromise!({
          student: { ID: 1, Login: 'test', Email: 'test@test.com', First_Name: 'Test', Last_name: 'User', RoleName: 'Student' },
          access_token: 'token'
        });
        await promise;
      });

      expect(result.current.loading).toBe(false);
    });
  });

  describe('logout', () => {
    it('should logout successfully', async () => {
      // Сначала логинимся
      const mockUser = {
        ID: 1,
        Login: 'testuser',
        Email: 'test@example.com',
        First_Name: 'Test',
        Last_name: 'User',
        RoleName: 'Student'
      };
      
      mockedAuthAPI.loginV2.mockResolvedValue({
        student: mockUser,
        access_token: 'mock-token-123'
      });
      mockedAuthAPI.logout.mockResolvedValue(undefined);
      
      localStorageMock.getItem.mockReturnValue('mock-token-123');

      const { result } = renderHook(() => useUserStore());

      // Логинимся
      await act(async () => {
        await result.current.login('testuser', 'password123');
      });

      // Логаутимся
      await act(async () => {
        await result.current.logout();
      });

      expect(result.current.user).toBeNull();
      expect(result.current.token).toBeNull();
      expect(localStorageMock.removeItem).toHaveBeenCalledWith('token');
      expect(mockedAuthAPI.logout).toHaveBeenCalledWith('mock-token-123');
    });

    it('should logout with empty token', async () => {
      mockedAuthAPI.logout.mockResolvedValue(undefined);
      localStorageMock.getItem.mockReturnValue(null);

      const { result } = renderHook(() => useUserStore());

      await act(async () => {
        await result.current.logout();
      });

      expect(mockedAuthAPI.logout).toHaveBeenCalledWith('');
    });

    it('should handle logout error gracefully', async () => {
      mockedAuthAPI.logout.mockRejectedValue(new Error('Logout failed'));
      localStorageMock.getItem.mockReturnValue('mock-token-123');

      const { result } = renderHook(() => useUserStore());

      // Сначала логинимся, чтобы установить состояние
      const mockUser = {
        ID: 1,
        Login: 'test',
        Email: 'test@test.com',
        First_Name: 'Test',
        Last_name: 'User',
        RoleName: 'Student'
      };
      
      mockedAuthAPI.loginV2.mockResolvedValue({
        student: mockUser,
        access_token: 'mock-token-123'
      });

      await act(async () => {
        await result.current.login('test', 'password');
      });

      // Проверяем, что состояние установлено
      expect(result.current.user).toEqual(mockUser);
      expect(result.current.token).toBe('mock-token-123');

      // Теперь тестируем logout с ошибкой
      await act(async () => {
        await result.current.logout();
      });

      // При ошибке logout, состояние НЕ очищается (это текущее поведение кода)
      expect(result.current.user).toEqual(mockUser);
      expect(result.current.token).toBe('mock-token-123');
      expect(localStorageMock.removeItem).not.toHaveBeenCalledWith('token');
    });
  });

  describe('clearError', () => {
    it('should clear error state', async () => {
      const { result } = renderHook(() => useUserStore());

      // Создаем ошибку через неудачный login
      const mockErrorResponse = {
        detail: {
          error: 'Test Error',
          message: 'Test Message'
        }
      };

      mockedAuthAPI.loginV2.mockResolvedValue(mockErrorResponse);

      await act(async () => {
        await result.current.login('testuser', 'wrongpassword');
      });

      expect(result.current.error).toEqual({
        error: 'Test Error',
        message: 'Test Message'
      });

      // Очищаем ошибку
      act(() => {
        result.current.clearError();
      });

      expect(result.current.error).toBeNull();
    });
  });

  describe('persistence', () => {
    it('should persist user data in localStorage', async () => {
      const mockUser = {
        ID: 1,
        Login: 'testuser',
        Email: 'test@example.com',
        First_Name: 'Test',
        Last_name: 'User',
        RoleName: 'Student'
      };
      
      const mockResponse = {
        student: mockUser,
        access_token: 'mock-token-123'
      };

      mockedAuthAPI.loginV2.mockResolvedValue(mockResponse);

      const { result } = renderHook(() => useUserStore());

      await act(async () => {
        await result.current.login('testuser', 'password123');
      });

      // Проверяем, что данные сохраняются в localStorage
      expect(localStorageMock.setItem).toHaveBeenCalledWith('token', 'mock-token-123');
    });
  });

  describe('state updates', () => {
    it('should update user state correctly through login', async () => {
      const { result } = renderHook(() => useUserStore());
      
      const newUser = {
        ID: 2,
        Login: 'newuser',
        Email: 'new@example.com',
        First_Name: 'New',
        Last_name: 'User',
        RoleName: 'Admin'
      };

      mockedAuthAPI.loginV2.mockResolvedValue({
        student: newUser,
        access_token: 'new-token'
      });

      await act(async () => {
        await result.current.login('newuser', 'password');
      });

      expect(result.current.user).toEqual(newUser);
    });

    it('should update token state correctly through login', async () => {
      const { result } = renderHook(() => useUserStore());

      const mockUser = {
        ID: 1,
        Login: 'test',
        Email: 'test@test.com',
        First_Name: 'Test',
        Last_name: 'User',
        RoleName: 'Student'
      };

      mockedAuthAPI.loginV2.mockResolvedValue({
        student: mockUser,
        access_token: 'new-token'
      });

      await act(async () => {
        await result.current.login('test', 'password');
      });

      expect(result.current.token).toBe('new-token');
    });

    it('should update error state correctly through failed login', async () => {
      const { result } = renderHook(() => useUserStore());

      const newError = {
        error: 'New Error',
        message: 'New Message'
      };

      mockedAuthAPI.loginV2.mockResolvedValue({
        detail: newError
      });

      await act(async () => {
        await result.current.login('test', 'wrongpassword');
      });

      expect(result.current.error).toEqual(newError);
    });

    it('should update loading state correctly during login', async () => {
      const { result } = renderHook(() => useUserStore());

      let resolvePromise: (value: { student: User; access_token: string }) => void;
      const promise = new Promise<{ student: User; access_token: string }>((resolve) => {
        resolvePromise = resolve;
      });
      
      mockedAuthAPI.loginV2.mockReturnValue(promise);

      act(() => {
        result.current.login('test', 'password');
      });

      expect(result.current.loading).toBe(true);

      await act(async () => {
        resolvePromise!({
          student: { ID: 1, Login: 'test', Email: 'test@test.com', First_Name: 'Test', Last_name: 'User', RoleName: 'Student' },
          access_token: 'token'
        });
        await promise;
      });

      expect(result.current.loading).toBe(false);
    });
  });
});
