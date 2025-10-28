export default class HaelthAPI {
  static async health() {
    {
      const response = await fetch(
        `${process.env.NEXT_PUBLIC_BASE_URL}/api/health`,
        {
          method: "GET",
          headers: {
            "Content-Type": "application/json",
            // Authorization: `Bearer ${token}`,
          },
        }
      );
      return response.json();
    }
  }
}
