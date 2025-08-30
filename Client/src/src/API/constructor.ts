export default class ConstructorAPI {
  static async create(token: string, data: FormData) {
    const response = await fetch(
      `${process.env.NEXT_PUBLIC_BASE_URL}/api/subtasks/create/v2`,
      {
        method: "POST",
        headers: {
          Authorization: `Bearer ${token}`,
        },
        body: data,
      }
    );
    return response.json();
  }
}
