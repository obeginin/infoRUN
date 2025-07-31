export default class TasksAPI {
  static async getStudentTask(
    id: number,
    token: string,
    limit: number,
    offset: number
  ) {
    const response = await fetch(
      `${
        import.meta.env.VITE_BASE_URL
      }/api/students_subtasks/${id}?limit=${limit}&offset=${offset}`,
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

  static async getAllTasks(id: number, token: string) {
    const response = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/students_subtasks/${id}`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.json()
  }
}
