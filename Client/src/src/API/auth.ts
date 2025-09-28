export default class AuthAPI {
  static async login(login: string, password: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/login`,
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

  static async loginV2(identifier: string, password: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/login/v2`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          identifier: identifier,
          password: password,
        }),
      }
    );
    return response.json();
  }

  static async logout(token: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/logout`,
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

  static async resetPassword(email: string) {
    // ОТПРАВКА ПИСЬМА НА ПОЧТУ ССЫЛКОЙ ДЛЯ СМЕНЫ ПАРОЛЯ
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/password_reset`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          Email: email,
        }),
      }
    );
    return response.json();
  }

  static async resetPasswordWithToken(
    token: string,
    new_password: string,
    repeat_new_password: string
  ) {
    // ДЕЛАЕМ ЗАПРОС КОГДА ОТКРЫТА СТАРНИЦА ИЗ ПИСЬМА
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/auth/password_reset_with_token`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          token: token,
          new_password: new_password,
          repeat_new_password: repeat_new_password,
        }),
      }
    );
    if (response.status === 200) {
      return response.json();
    } else {
      return response.json();
    }
  }
}
