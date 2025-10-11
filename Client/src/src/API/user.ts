export default class UserAPI {
    static async getUser() {
        const response = await fetch(`${process.env.NEXT_PUBLIC_BASE_URL}/home/user`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.json();
    }
}