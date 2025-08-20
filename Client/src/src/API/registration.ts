export default class AuthAPI {
  static async registration(email: string, login: string, password: string, tel: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/register/v2`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          email: email,
          login: login,
          password: password,
          phone: tel
        }),
      }
    );
    return response.json();
  }

  static async confirmEmail() {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/confirm-email`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.json();
  }

  static async confirmToken(token: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/confirm-email`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.json();
  }
}
