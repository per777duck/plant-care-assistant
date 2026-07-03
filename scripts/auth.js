const API_BASE =
    window.location.protocol === "file:" ||
    (window.location.port && window.location.port !== "8080")
        ? "http://localhost:8080"
        : "";

window.API_BASE = API_BASE;

window.apiFetch = async function apiFetch(path, options = {}) {
    const headers = new Headers(options.headers || {});
    if (options.body && !headers.has("Content-Type")) {
        headers.set("Content-Type", "application/json");
    }

    return fetch(`${API_BASE}${path}`, {
        credentials: "include",
        ...options,
        headers
    });
};

window.getCurrentUser = async function getCurrentUser() {
    const response = await apiFetch("/auth/me");
    if (response.status === 401) {
        return null;
    }
    if (!response.ok) {
        throw new Error("Не удалось получить данные пользователя");
    }
    return response.json();
};

window.updateAccountButton = async function updateAccountButton() {
    const label = document.querySelector(".account-label");
    if (!label) return;

    try {
        const user = await getCurrentUser();
        label.textContent = user ? user.userName : "Войти";
    } catch (error) {
        console.error(error);
        label.textContent = "Войти";
    }
};
