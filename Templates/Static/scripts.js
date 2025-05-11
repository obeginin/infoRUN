// scripts.js

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
