// 1. Справочник (шаблоны) типов уведомлений
const NOTIFICATION_TEMPLATES = {
    water: {
        title: "💧 Время полива",
        textTemplate: (plantName) => `Ваш растение "${plantName}" требует полива. Не забудьте отстоять воду комнатной температуры!`
    },
    feed: {
        title: "☀️ Подкормка",
        textTemplate: (plantName) => `Самое время внести комплексные удобрения для растения "${plantName}". Период активного роста в разгаре.`
    },
    loosen: {
        title: "⛏️ Рыхление почвы",
        textTemplate: (plantName) => `Корням растения "${plantName}" нужен кислород. Аккуратно взрыхлите верхний слой почвы.`
    },
    transplant: {
        title: "🪴 Пересадка",
        textTemplate: (plantName) => `Кажется, горшок стал маловат для "${plantName}". Пора запланировать пересадку в емкость побольше.`
    },
    soil: {
        title: "🌱 Смена земли",
        textTemplate: (plantName) => `Рекомендуется обновить верхний слой грунта или полностью заменить почву у "${plantName}" на свежий субстрат.`
    }
};

window.notificationsArray = [
    { id: 1, title: "💧 Время полива", text: "Ваш Фикус Бенджамина требует полива. Не забудьте отстоять воду комнатной температуры!" },
    { id: 2, title: "🌿 Новинка в справочнике", text: "Мы добавили подробное руководство по уходу за Монстерой Альба. Загляните в раздел «Справочник»." }
];

function renderNotifications() {
    const listContainer = document.getElementById("notifications-list");
    if (!listContainer) return;

    listContainer.innerHTML = "";

    if (window.notificationsArray.length === 0) {
        listContainer.innerHTML = "<p style='text-align: center; color: #999; margin-top: 20px;'>Нет новых уведомлений</p>";
        return;
    }

    window.notificationsArray.forEach(item => {
        const card = document.createElement("div");
        card.className = "notification-card";
        card.setAttribute("data-id", item.id);

        card.innerHTML = `
            <div class="notification-content">
                <h3>${item.title}</h3>
                <p>${item.text}</p>
            </div>
            <button class="close-notification-btn" onclick="deleteNotification(${item.id})">&times;</button>
        `;
        listContainer.appendChild(card);
    });
}

window.addNotification = function(templateType, plantName) {
    const template = NOTIFICATION_TEMPLATES[templateType];
    
    if (!template) {
        console.error(`Шаблон с типом "${templateType}" не найден!`);
        return;
    }

    const newId = Date.now();

    const newNotification = {
        id: newId,
        title: template.title,
        text: template.textTemplate(plantName)
    };

    window.notificationsArray.unshift(newNotification);

    renderNotifications();
    console.log("Добавлено новое уведомление:", newNotification);
};

window.deleteNotification = function(id) {
    window.notificationsArray = window.notificationsArray.filter(item => item.id !== id);

    const card = document.querySelector(`.notification-card[data-id="${id}"]`);
    if (card) {
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';
        setTimeout(() => {
            card.remove();
            if (window.notificationsArray.length === 0) renderNotifications();
        }, 200);
    }
};

window.clearAllNotifications = function() {
    window.notificationsArray = [];
    const cards = document.querySelectorAll('.notification-card');
    cards.forEach(card => {
        card.style.opacity = '0';
        card.style.transform = 'scale(0.95)';
        setTimeout(() => card.remove(), 200);
    });
    setTimeout(() => renderNotifications(), 200);
};

renderNotifications();