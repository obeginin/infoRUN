export default class SubtaskAPI {
  static async getSubtasksCreator(token: string, login: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/subtasks?Creator=${login}&Direction=DESC`,
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

  static async getSubtask(token: string, subtask_id: number) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/subtasks/${subtask_id}`,
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

  static async deleteSubtask(token: string, subtask_id: number) {
    const res = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/subtasks/delete/${subtask_id}`,
      {
        method: "DELETE",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    if (!res.ok) {
      let msg = res.statusText;
      try {
        const j = await res.json();
        msg = j?.message || msg;
      } catch {}
      throw new Error(msg || "Delete failed");
    }
    return { status: res.status };
  }

  static async editSubtask(token: string, subtask_id: number, data: FormData) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/subtasks/update/${subtask_id}`,
      {
        method: "PUT",
        headers: {
          // "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: data,
      }
    );
    return response.json();
  }
}
