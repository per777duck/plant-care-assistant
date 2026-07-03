function getApiBase() {
    if (window.API_BASE !== undefined) {
        return window.API_BASE;
    }
    return window.location.protocol === "file:" ||
        (window.location.port && window.location.port !== "8080")
        ? "http://localhost:8080"
        : "";
}

window.loadPlants = async function loadPlants() {
    const container = document.getElementById("plants-container");
    if (!container) return;

    const apiBase = getApiBase();

    try {
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

        plants.forEach(plant => {
            const card = document.createElement("article");
            card.className = "plant-card";
            const imageSrc = `${apiBase}${plant.imagePath || "/images/plants/default.jpg"}`;
            card.innerHTML = `
                <img class="plant-card-image" src="${imageSrc}" alt="${plant.name ?? "Растение"}" loading="lazy">
                <h2>${plant.name ?? "Без названия"}</h2>
                <p><strong>Полив:</strong> ${plant.wateringRecomendation ?? "—"}</p>
                <p><strong>Освещение:</strong> ${plant.lightningRecomendation ?? "—"}</p>
                <p><strong>Пересадка:</strong> ${plant.transferInformation ?? "—"}</p>
                <p><strong>Ядовитость:</strong> ${plant.poisonInformation ?? "—"}</p>
                ${plant.optionalInfoCare ? `<p><strong>Особенности:</strong> ${plant.optionalInfoCare}</p>` : ""}
                <button type="button">Подробнее</button>
            `;
            container.appendChild(card);
        });
    } catch (error) {
        console.error("Не удалось загрузить растения:", error);
        container.innerHTML = "<p>Не удалось загрузить данные. Проверьте, что сервер запущен.</p>";
    }
};
