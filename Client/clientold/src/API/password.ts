export default class UserPassword {
  static async changePassword(
    oldPassword: string,
    newPassword: string,
    repeat_new_password: string,
    token: string
  ) {
    {
      const response = await fetch(
        `${import.meta.env.VITE_BASE_URL}/api/auth/change-password`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${token}`,
          },
          body: JSON.stringify({
            old_password: oldPassword,
            new_password: newPassword,
            repeat_new_password: repeat_new_password,
          }),
        }
      );
      return response.json();
    }
  }
}
