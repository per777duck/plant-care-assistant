async function loadFavorites() {
    const container = document.getElementById("favorites-container");
    if (!container) return;

    const user = await getCurrentUser();
    if (!user) {
        requireAuthMessage(container, "Войдите в аккаунт, чтобы видеть избранные растения.");
        return;
    }

    const apiBase = getApiBase();

    try {
        const response = await apiFetch("/favorites");
        if (!response.ok) {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }

        const favorites = await response.json();
        window.userPlantLists.favorites = new Set(favorites.map(item => item.plantId));

        if (!favorites.length) {
            container.innerHTML = "<p>Вы ещё не добавили растения в избранное. Откройте справочник и нажмите «В избранное».</p>";
            return;
        }

        container.innerHTML = "";

        favorites.forEach(item => {
            const plant = item.plant;
            const card = document.createElement("article");
            card.className = "plant-card";
            card.innerHTML = `
                ${renderPlantInfo(plant, apiBase)}
                <p class="plant-meta"><strong>Добавлено:</strong> ${formatPlantDate(item.dateAdded)}</p>
                <div class="plant-card-actions">
                    <button type="button" class="plant-action-btn favorite-btn active" data-plant-id="${plant.id}">
                        ★ Убрать из избранного
                    </button>
                </div>
            `;
            container.appendChild(card);
        });

        bindPlantCardActions(container);
    } catch (error) {
        console.error(error);
        container.innerHTML = "<p>Не удалось загрузить избранное.</p>";
    }
}

window.initFavoritesPage = function initFavoritesPage() {
    loadFavorites();
};
