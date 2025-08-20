export default class FiltersAPI {
    static async getSubjects(token: string) {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/api/subjects`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        return response.json();
    }
}