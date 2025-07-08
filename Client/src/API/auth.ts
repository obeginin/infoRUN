export default class AuthAPI {
    static async login(login: string, password: string) {
        const response = await fetch(`${import.meta.env.VITE_BASE_URL}/home/login`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            },
            body: JSON.stringify({
                Login: login,
                Password: password
            })
        });
        console.log(response.json)
        return response.json();
    }

    static async logout() {
        const response = await fetch(`${import.meta.env.VITE_BASE_URL}/home/logout/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.json();
    }
}