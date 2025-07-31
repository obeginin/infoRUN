export default class AuthAPI {
  static async login(login: string, password: string) {
    const response = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/auth/login`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          Login: login,
          Password: password,
        }),
      }
    );
    return response.json();
  }

  static async logout(token: string) {
    const response = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/auth/logout/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.json();
  }
}
