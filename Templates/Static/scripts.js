// scripts.js


// Кнопка назад back-button
document.addEventListener("DOMContentLoaded", function () {
    const backButton = document.getElementById("back-button");
    if (backButton) {
        backButton.addEventListener("click", function (event) {
            event.preventDefault(); // предотвращаем переход по href="#"

            const parts = window.location.pathname.split("/").filter(Boolean); // убираем пустые части
            if (parts.length > 1) {
                parts.pop(); // убираем последний сегмент пути
                const parentPath = "/" + parts.join("/");
                window.location.href = parentPath;
            } else {
                // Если остался только "/", возвращаемся на главную
                window.location.href = "/";
            }
        });
    }
});

// Общая функция для загрузки данных для категорий
async function loadData(url, listId) {
    try {
        const response = await fetch(url);
        const data = await response.json();

        const list = document.getElementById(listId);
        list.innerHTML = ""; // Очистить список перед добавлением новых элементов

        data.forEach(item => {
            const li = document.createElement("li");
            li.innerHTML = `<a href="/js/${item.id}"><strong>${item.name}</strong></a>`;
            list.appendChild(li);
        });
    } catch (error) {
        console.error("Ошибка при загрузке данных:", error);
    }
}

// Функция для вывода списка студентов
async function loadStudents() {
    try {
        // Получаем список студентов
        const response = await fetch(`/admin/api/students`);
        const students = await response.json();
        console.log(students); // логирование в консоль

        // Выводим список студентов
        const container = document.getElementById("students-list");
        container.innerHTML = ""; // Очищаем сообщение "Загрузка студентов..."

        if (students.length === 0) {
            container.innerHTML = "<p>Студенты не найдены.</p>";
            return;
        }

        const ul = document.createElement("ul");
        students.forEach(student => {
            const li = document.createElement("li");
            console.log(students);

            li.innerHTML = `Студент: <a href="/admin/ListStudents/${student.ID}">${student.Login}</a> - ${student.First_Name} ${student.Last_Name}`;
            ul.appendChild(li);
        });

        container.appendChild(ul);
    } catch (error) {
        console.error("Ошибка при загрузке студентов", error);
        document.getElementById("students-list").innerHTML = "<p>Ошибка при загрузке студентов.</p>";
    }
}



