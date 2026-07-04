function buildMyPlantCard(item, apiBase) {    const plant = item.plant;
    const card = document.createElement("article");
    card.className = "my-plant-card";
    card.dataset.id = item.id;

    card.innerHTML = `
        <div class="my-plant-card-header">
            ${renderPlantInfo(plant, apiBase)}
        </div>
        <p class="plant-meta"><strong>Добавлено:</strong> ${formatPlantDate(item.dateAdded)}</p>
        <form class="my-plant-form">
            <label>
                Заметки
                <textarea name="notes" rows="3" placeholder="Где стоит, особенности ухода...">${item.notes ?? ""}</textarea>
            </label>
            <label>
                Напоминание о поливе (дней)
                <input type="number" name="wateringReminderDays" min="1" placeholder="Например, 7"
                    value="${item.wateringReminderDays ?? ""}">
            </label>
            <label>
                Напоминание о пересадке (дней)
                <input type="number" name="transferReminderDays" min="1" placeholder="Например, 365"
                    value="${item.transferReminderDays ?? ""}">
            </label>
            <label>
                Последний полив
                <input type="date" name="lastWateredAt" value="${item.lastWateredAt ?? ""}">
            </label>
            <label>
                Последняя пересадка
                <input type="date" name="lastTransferredAt" value="${item.lastTransferredAt ?? ""}">
            </label>
            <div class="my-plant-form-actions">
                <button type="submit" class="plant-action-btn">Сохранить</button>
                <button type="button" class="plant-action-btn danger remove-my-plant-btn">Удалить</button>
            </div>
            <p class="my-plant-message"></p>
        </form>
    `;

    const form = card.querySelector(".my-plant-form");
    form.addEventListener("submit", event => handleMyPlantSave(event, item.id));
    card.querySelector(".remove-my-plant-btn").addEventListener("click", () => handleMyPlantRemove(item.id, plant.id, card));

    return card;
}

async function handleMyPlantSave(event, id) {
    event.preventDefault();
    const form = event.currentTarget;
    const message = form.querySelector(".my-plant-message");

    const payload = {
        notes: form.notes.value.trim(),
        wateringReminderDays: form.wateringReminderDays.value ? Number(form.wateringReminderDays.value) : null,
        transferReminderDays: form.transferReminderDays.value ? Number(form.transferReminderDays.value) : null,
        lastWateredAt: form.lastWateredAt.value || null,
        lastTransferredAt: form.lastTransferredAt.value || null
    };

    try {
        const response = await apiFetch(`/user-plants/${id}`, {
            method: "PUT",
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));

        if (!response.ok) {
            message.textContent = data.message || "Не удалось сохранить";
            message.classList.add("error");
            return;
        }

        message.textContent = "Сохранено";
        message.classList.remove("error");
    } catch (error) {
        console.error(error);
        message.textContent = "Ошибка сохранения";
        message.classList.add("error");
    }
}

async function handleMyPlantRemove(id, plantId, card) {
    if (!confirm("Удалить растение из вашей коллекции?")) {
        return;
    }

    try {
        const response = await apiFetch(`/user-plants/${id}`, { method: "DELETE" });
        if (!response.ok) {
            alert("Не удалось удалить растение");
            return;
        }

        window.userPlantLists.myPlants.delete(plantId);
        card.remove();
    } catch (error) {
        console.error(error);
        alert("Не удалось удалить растение");
    }
}

async function loadMyPlants() {
    const container = document.getElementById("my-plants-container");
    if (!container) return;

    const user = await getCurrentUser();
    if (!user) {
        requireAuthMessage(container, "Войдите в аккаунт, чтобы вести список своих растений.");
        return;
    }

    const apiBase = getApiBase();

    try {
        const response = await apiFetch("/user-plants");
        if (!response.ok) {
            throw new Error(`Ошибка сервера: ${response.status}`);
        }

        const items = await response.json();
        window.userPlantLists.myPlants = new Set(items.map(item => Number(item.plantId)));

        if (!items.length) {
            container.innerHTML = "<p>У вас пока нет растений. Добавьте их из справочника кнопкой «Мои растения».</p>";
            return;
        }

        container.innerHTML = "";
        items.forEach(item => container.appendChild(buildMyPlantCard(item, apiBase)));
    } catch (error) {
        console.error(error);
        container.innerHTML = "<p>Не удалось загрузить ваши растения.</p>";
    }
}

window.initMyPlantsPage = function initMyPlantsPage() {
    loadMyPlants();
};
