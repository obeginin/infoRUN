// scripts.js


// Кнопка назад back-button при переключении вверх по URL
document.addEventListener("DOMContentLoaded", function () {
    const backButton = document.getElementById("back-button");

    if (backButton) {
        backButton.addEventListener("click", function (event) {
            event.preventDefault();

            const subtasksContainer = document.getElementById("subtasks-container");
            const studentsList = document.getElementById("students-list");

            // Если контейнер с задачами видим — считаем, что можно "откатиться" назад по UI
            if (subtasksContainer && !subtasksContainer.classList.contains("hidden")) {
                subtasksContainer.classList.add("hidden");
                studentsList.classList.remove("hidden");
            } else {
                // Иначе навигация по URL вверх
                const parts = window.location.pathname.split("/").filter(Boolean);
                if (parts.length > 1) {
                    parts.pop();
                    window.location.href = "/" + parts.join("/");
                } else {
                    window.location.href = "/";
                }
            }
        });
    }
});



// Общая функция для загрузки данных для категорий
async function loadTasks() {
    try {
        // Получаем список категорий
        const response = await fetch(`/tasks/api`);
        const tasks = await response.json();
        console.log(tasks); // логирование в консоль

        const container = document.getElementById("task-list");
        container.innerHTML = "";

        if (tasks.length === 0) {
            container.innerHTML = "<p>Категории не найдены.</p>";
            return;
        }

        const ul = document.createElement("ul");

        for (const task of tasks) {
            console.log("task", task);
            const li = document.createElement("li");
            li.innerHTML = `<a href="/tasks/${task.TaskID}"><strong>${task.TaskNumber}: ${task.TaskTitle}</strong></a>`;
            container.appendChild(li);

        };
        container.appendChild(ul);

    } catch (error) {
            console.error("Ошибка при загрузке задач:", error);
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

        // Вешаем обработчики на появившиеся ссылки
        const ul = document.createElement("ul");
        students.forEach(student => {
            const li = document.createElement("li");
            console.log(students);

            // обычная ссылка
            //li.innerHTML = `Студент: <a href="/admin/ListStudents/${student.ID}">${student.Login}</a> - ${student.First_Name} ${student.Last_Name}`;
            // для динамического обновления
            li.innerHTML = `Студент: <a href="#" class="student-link" data-id="${student.ID}">${student.Login}</a> - ${student.First_Name} ${student.Last_Name}`;
            ul.appendChild(li);
        });

        container.appendChild(ul);

        // Загружаем список задач выбранного студента по клику вызывая функцию loadSubtasksForStudent()
        document.getElementById("students-list").addEventListener("click", (e) => {
            if (e.target.classList.contains("student-link")) {
                e.preventDefault();
                const studentID = e.target.dataset.id;

                // Скрываем список студентов и показываем подзадачи
                document.getElementById("students-list").classList.add("hidden");
                document.getElementById("subtasks-container").classList.remove("hidden");

                loadSubtasksForStudent(studentID);
            }

    });
    } catch (error) {
        console.error("Ошибка при загрузке студентов", error);
        document.getElementById("students-list").innerHTML = "<p>Ошибка при загрузке студентов.</p>";
    }
}


async function loadSubtasksForStudent(studentID) {
    try {
        const response = await fetch(`/admin/api/students/${studentID}/subtasks`);
        const subtasks = await response.json();
        console.log(subtasks);
        const container = document.getElementById("subtasks-container");
        container.innerHTML = "";

        if (subtasks.length === 0) {
            container.innerHTML = "<p>Задачи для этого студента не найдены.</p>";
            return;
        }

        const ul = document.createElement("ul");
        subtasks.forEach(subtasks => {
            const li = document.createElement("li");
            li.textContent = `Задача: ${subtasks.SubTaskID} ${subtasks.CompletionStatus}`; // адаптируй под свои поля
            ul.appendChild(li);
        });
        container.appendChild(ul);

    } catch (error) {
        console.error("Ошибка при загрузке задач студента", error);
        document.getElementById("subtasks-container").innerHTML = "<p>Ошибка при загрузке задач.</p>";
    }
}


