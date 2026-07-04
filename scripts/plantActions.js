window.userPlantLists = {
    favorites: new Set(),
    myPlants: new Set()
};

function getApiBase() {
    if (window.API_BASE !== undefined) {
        return window.API_BASE;
    }
    return window.location.protocol === "file:" ||
        (window.location.port && window.location.port !== "8080")
        ? "http://localhost:8080"
        : "";
}

window.formatPlantDate = function formatPlantDate(value) {
    if (!value) return "—";
    return new Date(value).toLocaleDateString("ru-RU");
};

window.renderPlantInfo = function renderPlantInfo(plant, apiBase) {
    const imageSrc = `${apiBase}${plant.imagePath || "/images/plants/default.jpg"}`;
    return `
        <img class="plant-card-image" src="${imageSrc}" alt="${plant.name ?? "Растение"}" loading="lazy">
        <h2>${plant.name ?? "Без названия"}</h2>
        <p><strong>Полив:</strong> ${plant.wateringRecomendation ?? "—"}</p>
        <p><strong>Освещение:</strong> ${plant.lightningRecomendation ?? "—"}</p>
        <p><strong>Пересадка:</strong> ${plant.transferInformation ?? "—"}</p>
        <p><strong>Ядовитость:</strong> ${plant.poisonInformation ?? "—"}</p>
        ${plant.optionalInfoCare ? `<p><strong>Особенности:</strong> ${plant.optionalInfoCare}</p>` : ""}
    `;
};

window.refreshUserPlantLists = async function refreshUserPlantLists() {
    const user = await getCurrentUser();
    if (!user) {
        window.userPlantLists = { favorites: new Set(), myPlants: new Set() };
        return false;
    }

    try {
        const [favoritesResponse, myPlantsResponse] = await Promise.all([
            apiFetch("/favorites"),
            apiFetch("/user-plants")
        ]);

        if (favoritesResponse.ok) {
            const favorites = await favoritesResponse.json();
            window.userPlantLists.favorites = new Set(favorites.map(item => Number(item.plantId)));
        }

        if (myPlantsResponse.ok) {
            const myPlants = await myPlantsResponse.json();
            window.userPlantLists.myPlants = new Set(myPlants.map(item => Number(item.plantId)));
        }

        return true;
    } catch (error) {
        console.error("Не удалось загрузить списки пользователя:", error);
        return false;
    }
};

window.requireAuthMessage = function requireAuthMessage(container, message) {
    if (!container) return;
    container.innerHTML = `
        <div class="auth-required">
            <p>${message}</p>
            <button type="button" class="account-submit" data-page="account">Войти в аккаунт</button>
        </div>
    `;
    container.querySelector("[data-page='account']")?.addEventListener("click", () => {
        const accountButton = document.querySelector("button[data-page='account']");
        loadPage("account", accountButton);
    });
};

window.toggleFavorite = async function toggleFavorite(plantId, button) {
    const user = await getCurrentUser();
    if (!user) {
        alert("Войдите в аккаунт, чтобы добавлять растения в избранное.");
        return;
    }

    const isFavorite = window.userPlantLists.favorites.has(plantId);

    try {
        const response = isFavorite
            ? await apiFetch(`/favorites/${plantId}`, { method: "DELETE" })
            : await apiFetch("/favorites", {
                method: "POST",
                body: JSON.stringify({ plantId })
            });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            alert(data.message || "Не удалось обновить избранное");
            return;
        }

        if (isFavorite) {
            window.userPlantLists.favorites.delete(plantId);
        } else {
            window.userPlantLists.favorites.add(plantId);
        }

        if (button) {
            button.textContent = isFavorite ? "☆ В избранное" : "★ В избранном";
            button.classList.toggle("active", !isFavorite);
        }
    } catch (error) {
        console.error(error);
        alert("Не удалось обновить избранное");
    }
};

window.addToMyPlants = async function addToMyPlants(plantId, button) {
    const user = await getCurrentUser();
    if (!user) {
        alert("Войдите в аккаунт, чтобы добавлять растения в «Мои растения».");
        return;
    }

    if (window.userPlantLists.myPlants.has(Number(plantId))) {
        const myPlantsButton = document.querySelector("button[data-page='myPlants']");
        loadPage("myPlants", myPlantsButton);
        return;
    }

    try {
        const response = await apiFetch("/user-plants", {
            method: "POST",
            body: JSON.stringify({ plantId })
        });

        if (!response.ok) {
            const data = await response.json().catch(() => ({}));
            alert(data.message || "Не удалось добавить растение");
            return;
        }

        window.userPlantLists.myPlants.add(Number(plantId));

        if (button) {
            button.textContent = "✓ В моих растениях";
            button.classList.add("active");
            button.disabled = true;
        }
    } catch (error) {
        console.error(error);
        alert("Не удалось добавить растение");
    }
};

window.buildPlantCardActions = function buildPlantCardActions(plant) {
    const isFavorite = window.userPlantLists.favorites.has(Number(plant.id));
    const inCollection = window.userPlantLists.myPlants.has(Number(plant.id));

    return `
        <div class="plant-card-actions">
            <button type="button" class="plant-action-btn favorite-btn ${isFavorite ? "active" : ""}"
                data-plant-id="${plant.id}">
                ${isFavorite ? "★ В избранном" : "☆ В избранное"}
            </button>
            <button type="button" class="plant-action-btn my-plant-btn ${inCollection ? "active" : ""}"
                data-plant-id="${plant.id}" ${inCollection ? "disabled" : ""}>
                ${inCollection ? "✓ В моих растениях" : "+ Мои растения"}
            </button>
        </div>
    `;
};

window.bindPlantCardActions = function bindPlantCardActions(container) {
    container.querySelectorAll(".favorite-btn").forEach(button => {
        button.addEventListener("click", () => {
            toggleFavorite(Number(button.dataset.plantId), button);
        });
    });

    container.querySelectorAll(".my-plant-btn").forEach(button => {
        button.addEventListener("click", () => {
            addToMyPlants(Number(button.dataset.plantId), button);
        });
    });
};
