import { number } from "motion";
import { Nullable } from "primereact/ts-helpers";

export default class TasksAPI {
  static async getStudentTask(
    id: number,
    token: string,
    limit: number,
    offset: number
  ) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/students_subtasks?student_id=${id}&p_limit=${limit}&p_offset=${offset}`,
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
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/students_subtasks?student_id=${id}`,
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
      `${process.env.NEXT_PUBLIC_BASE_URL}
      /api/students_subtasks/${student_id}/StudentTask/${task_id}`,
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

  static async getSelectedTask(
    subject_id: number,
    task_id: number,
    token: string,
    limit?: number,
    offset?: number,
    creator?: string,
    date?: string,
    id?: number
  ) {
    
    const params = new URLSearchParams({
      subject_id: subject_id.toString(),
      task_id: task_id.toString(),
    });

    if (limit !== undefined) params.append("p_limit", limit.toString());
    if (offset !== undefined) params.append("p_offset", offset.toString());
    if (creator !== "" && creator !== undefined) params.append("creator", creator);
    if (date !== null && date !== '1970-01-01') params.append("created_date", date!.toString());
    if (id !== 0 && id !== undefined) params.append("subtask_id", Number(id).toString());

    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/subtasks?${params}`,
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
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/students_subtasks/check-answer/`,
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
