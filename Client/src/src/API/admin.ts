export default class AdminAPI {
  static async getUsers(token: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/students`,
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

  static async DeleteUser(token: string, email: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/admin/delete_student?email=${email}`,
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

  static async ChangePassword(token: string, id: number, password: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/admin/students/${id}/change-password`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          new_password: password,
        }),
      }
    );
    return response.json();
  }

  static async adminRoles(token: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/admin/roles`,
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

  static async getStudentLogs(token: string, studentID: number) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/admin/students/${studentID}/logs`,
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

  static async getLogs(token: string, limit: number, offset: number) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/admin/logs?limit=${limit}&offset=${offset}`,
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

  static async getUserLogs(token: string, studentID: number) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/admin/students/${studentID}/logs`,
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

  static async getLogsStudent(token: string, studentID: number) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/admin/students/${studentID}/logs`,
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
