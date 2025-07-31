export default class StudentsAPI {
    static async getStudents() {
        const response = await fetch(`${import.meta.env.VITE_BASE_URL}/students/api`, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json'
            }
        });
        return response.json();
    }
}