export default class UserAPI {
    static async getUser() {
        const response = await fetch(`${import.meta.env.VITE_BASE_URL}/home/user`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.json();
    }
}