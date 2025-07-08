export default class UserPassword {
  static async changePassword(oldPassword: string, newPassword: string) {
    {
      const response = await fetch(
        `${import.meta.env.VITE_BASE_URL}/home/change-password`,
        {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
          },
          body: JSON.stringify({
            OldPassword: oldPassword,
            NewPassword: newPassword,
          }),
        }
      );
      return response.json();
    }
  }
}
