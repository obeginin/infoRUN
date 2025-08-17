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
    return response.json();
  }

  static async getTask(student_id: number, task_id: number, token: string) {
    const response = await fetch(
      `${
        import.meta.env.VITE_BASE_URL
      }/api/students_subtasks/${student_id}/StudentTask/${task_id}`,
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

  static async checkAnswer(
    subtaskId: number,
    studentId: number,
    student_answer: string
  ) {
    const response = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/students_subtasks/check-answer/`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          subtaskId: subtaskId,
          studentId: studentId,
          student_answer: student_answer,
        }),
      }
    );
    return response.json();
  }
}
