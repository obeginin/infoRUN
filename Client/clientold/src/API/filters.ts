export default class FiltersAPI {
    static async getSubjects(token: string) {
        const response = await fetch(`${import.meta.env.VITE_BASE_URL}/api/subjects`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
                'Authorization': `Bearer ${token}`
            }
        });
        return response.json();
    }
}