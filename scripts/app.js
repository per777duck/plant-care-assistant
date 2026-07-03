async function loadPage(page, button) {
    try {
        const response = await fetch(`../layouts/pages/${page}.html`);
        const html = await response.text();

        document.getElementById("content").innerHTML = html;

        document.getElementById("dynamic-notifications-script")?.remove();
        document.getElementById("dynamic-catalog-script")?.remove();
        document.getElementById("dynamic-account-script")?.remove();

        if (page === "notifications") {
            const script = document.createElement("script");
            script.src = "../scripts/notifications.js";
            script.id = "dynamic-notifications-script";
            document.body.appendChild(script);
        }
        if (page === "catalog") {
            const runCatalog = () => window.loadPlants?.();
            if (typeof window.loadPlants === "function") {
                runCatalog();
            } else if (!document.getElementById("dynamic-catalog-script")) {
                const script = document.createElement("script");
                script.src = "../scripts/catalog.js";
                script.id = "dynamic-catalog-script";
                script.onload = runCatalog;
                document.body.appendChild(script);
            }
        }
        if (page === "account") {
            const script = document.createElement("script");
            script.src = "../scripts/account.js";
            script.id = "dynamic-account-script";
            document.body.appendChild(script);
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

