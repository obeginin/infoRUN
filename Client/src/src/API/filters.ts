export default class FiltersAPI {
  static async getSubjects(token: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/subjects`,
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

  static async getTaskNumber(token: string, subject_id: number) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/tasks?subject_id=${subject_id}`,
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

  static async getVariants(token: string) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/variants`,
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
