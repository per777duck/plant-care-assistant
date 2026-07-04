window.loadPlants = async function loadPlants() {
    const container = document.getElementById("plants-container");
    if (!container) return;

    const apiBase = getApiBase();
    container.innerHTML = "<p>Загрузка растений...</p>";

    try {
        await refreshUserPlantLists();

        const response = await fetch(`${apiBase}/plants`);
        if (!response.ok) {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }

        const plants = await response.json();
        if (!plants.length) {
            container.innerHTML = "<p>В справочнике пока нет растений.</p>";
            return;
        }

        container.innerHTML = "";
        container.className = "plants-grid";

        plants.forEach(plant => {
            const card = document.createElement("article");
            card.className = "plant-card";
            card.innerHTML = `
                ${renderPlantInfo(plant, apiBase)}
                ${buildPlantCardActions(plant)}
            `;
            container.appendChild(card);
        });

        bindPlantCardActions(container);
    } catch (error) {
        console.error("Не удалось загрузить растения:", error);
        container.innerHTML = "<p>Не удалось загрузить данные. Проверьте, что сервер запущен.</p>";
    }
};
