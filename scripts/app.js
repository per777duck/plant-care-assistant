async function loadPage(page, button) {
    try {
        const response = await fetch(`../layouts/pages/${page}.html`, { cache: "no-store" });
        const html = await response.text();

        document.getElementById("content").innerHTML = html;

        if (page === "notifications") {
            if (document.getElementById("dynamic-notifications-script")) {
                window.initNotificationsPage?.();
            } else {
                const script = document.createElement("script");
                script.src = "../scripts/notifications.js";
                script.id = "dynamic-notifications-script";
                script.onload = () => window.initNotificationsPage?.();
                document.body.appendChild(script);
            }
        }
        if (page === "catalog") {
            window.loadPlants?.();
        }
        if (page === "favorites") {
            window.initFavoritesPage?.();
        }
        if (page === "myPlants") {
            window.initMyPlantsPage?.();
        }
        if (page === "account") {
            if (document.getElementById("dynamic-account-script")) {
                window.initAccountPage?.();
            } else {
                const script = document.createElement("script");
                script.src = "../scripts/account.js";
                script.id = "dynamic-account-script";
                document.body.appendChild(script);
            }
        }

        document.querySelectorAll("button[data-page]")
            .forEach(btn => btn.classList.remove("active"));

        if (button) {
            button.classList.add("active");
        }
    } catch (error) {
        console.error(`Не удалось загрузить страницу ${page}:`, error);
    }
}

function bindNavigationButtons() {
    document.querySelectorAll("button[data-page]").forEach(btn => {
        btn.addEventListener("click", () => {
            const page = btn.dataset.page;
            if (!page) return;

            loadPage(page, btn);
        });
    });
}

window.onload = () => {
    bindNavigationButtons();
    updateAccountButton();
    const defaultButton = document.querySelector("button[data-page='catalog']");
    loadPage("catalog", defaultButton);
};
