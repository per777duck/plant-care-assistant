async function loadPage(page, button) {
    try {
        const response = await fetch(`../layouts/pages/${page}.html`);
        const html = await response.text();

        document.getElementById("content").innerHTML = html;

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
    const defaultButton = document.querySelector("button[data-page='catalog']");
    loadPage("catalog", defaultButton);
};
