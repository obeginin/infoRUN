export default class StudentsAPI {
  static async getStudents() {
    const response = await fetch(
      `${import.meta.env.VITE_BASE_URL}/students/api`,
      {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      }
    );
    return response.json();
  }

  static async deleteStudent(token: string, id: number) {
    const response = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/students/delete_student?id=${id}`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
      }
    );
    return response.json();
  }

  static async addNewUser(
    token: string,
    login: string,
    last_name: string,
    first_name: string,
    email: string,
    phone: string,
    sex: string,
    roleId: number,
    password: string
  ) {
    const response = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/students/new_student`,
      {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          Login: login,
          Last_Name: last_name,
          First_Name: first_name,
          Email: email,
          Phone: phone,
          Sex: sex,
          RoleID: roleId,
          IsActive: true,
          Password: password,
        }),
      }
    );
    return response.json();
  }

  static async editUser(
    token: string,
    id: number,
    login: string,
    last_name: string,
    first_name: string,
    middle_name: string,
    email: string,
    phone: string,
    sex: string,
    birth_date: string,
    comment: string,
    roleId: number,
    password: string
  ) {
    const response = await fetch(
      `${import.meta.env.VITE_BASE_URL}/api/students/edit_student?id=${id}`,
      {
        method: "PATCH",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${token}`,
        },
        body: JSON.stringify({
          Login: login,
          Last_Name: last_name,
          First_Name: first_name,
          Middle_Name: middle_name,
          Email: email,
          Phone: phone,
          Sex: sex,
          BirthDate: birth_date,
          Comment: comment,
          RoleID: roleId,
          IsActive: true,
          Password: password,
        }),
      }
    );
    return response.json();
  }
}
