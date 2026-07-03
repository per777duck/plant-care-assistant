function showMessage(elementId, text, isError = false) {
    const element = document.getElementById(elementId);
    if (!element) return;
    element.textContent = text;
    element.classList.toggle("error", isError);
}

function switchTab(tabName) {
    document.querySelectorAll(".account-tab").forEach(tab => {
        tab.classList.toggle("active", tab.dataset.tab === tabName);
    });
    document.getElementById("login-form").classList.toggle("hidden", tabName !== "login");
    document.getElementById("register-form").classList.toggle("hidden", tabName !== "register");
    showMessage("account-message", "");
}

function formatDate(value) {
    if (!value) return "—";
    return new Date(value).toLocaleString("ru-RU");
}

async function renderAccountPage() {
    const guestCard = document.getElementById("account-guest");
    const profileCard = document.getElementById("account-profile");
    if (!guestCard || !profileCard) return;

    try {
        const user = await getCurrentUser();
        if (!user) {
            guestCard.classList.remove("hidden");
            profileCard.classList.add("hidden");
            return;
        }

        guestCard.classList.add("hidden");
        profileCard.classList.remove("hidden");

        document.getElementById("profile-name").textContent = user.userName;
        document.getElementById("profile-email").textContent = user.email;
        document.getElementById("profile-created").textContent = formatDate(user.createdAt);
        document.getElementById("profile-userName").value = user.userName;
        document.getElementById("profile-email-input").value = user.email;

        await updateAccountButton();
    } catch (error) {
        console.error(error);
        showMessage("account-message", "Не удалось загрузить аккаунт", true);
    }
}

let accountPageInitialized = false;

async function handleLoginSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
        email: form.email.value.trim(),
        password: form.password.value
    };

    try {
        const response = await apiFetch("/auth/login", {
            method: "POST",
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            showMessage("account-message", data.message || "Неверный email или пароль", true);
            return;
        }

        showMessage("account-message", "");
        form.reset();
        await updateAccountButton();
        await renderAccountPage();
    } catch (error) {
        console.error(error);
        showMessage("account-message", "Не удалось войти. Проверьте, что сервер запущен.", true);
    }
}

async function handleRegisterSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
        userName: form.userName.value.trim(),
        email: form.email.value.trim(),
        password: form.password.value
    };

    try {
        const response = await apiFetch("/auth/register", {
            method: "POST",
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            showMessage("account-message", data.message || "Не удалось зарегистрироваться", true);
            return;
        }

        showMessage("account-message", "Аккаунт создан. Теперь войдите.");
        switchTab("login");
        document.querySelector("#login-form input[name='email']").value = payload.email;
    } catch (error) {
        console.error(error);
        showMessage("account-message", "Не удалось зарегистрироваться", true);
    }
}

async function handleProfileSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
        userName: form.userName.value.trim(),
        email: form.email.value.trim()
    };

    try {
        const response = await apiFetch("/users/me", {
            method: "PUT",
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            showMessage("profile-message", data.message || "Не удалось обновить профиль", true);
            return;
        }

        showMessage("profile-message", "Профиль обновлён");
        await renderAccountPage();
    } catch (error) {
        console.error(error);
        showMessage("profile-message", "Не удалось обновить профиль", true);
    }
}

async function handlePasswordSubmit(event) {
    event.preventDefault();
    const form = event.currentTarget;
    const payload = {
        oldPassword: form.oldPassword.value,
        newPassword: form.newPassword.value
    };

    try {
        const response = await apiFetch("/users/me/password", {
            method: "PUT",
            body: JSON.stringify(payload)
        });
        const data = await response.json().catch(() => ({}));
        if (!response.ok) {
            showMessage("profile-message", data.message || "Не удалось сменить пароль", true);
            return;
        }

        form.reset();
        showMessage("profile-message", "Пароль обновлён");
    } catch (error) {
        console.error(error);
        showMessage("profile-message", "Не удалось сменить пароль", true);
    }
}

async function handleLogout() {
    try {
        await apiFetch("/auth/logout", { method: "POST" });
        await updateAccountButton();
        await renderAccountPage();
    } catch (error) {
        console.error(error);
        showMessage("profile-message", "Не удалось выйти", true);
    }
}

window.initAccountPage = function initAccountPage() {
    if (!accountPageInitialized) {
        accountPageInitialized = true;

        document.querySelectorAll(".account-tab").forEach(tab => {
            tab.addEventListener("click", () => switchTab(tab.dataset.tab));
        });

        document.getElementById("login-form")?.addEventListener("submit", handleLoginSubmit);
        document.getElementById("register-form")?.addEventListener("submit", handleRegisterSubmit);
        document.getElementById("profile-form")?.addEventListener("submit", handleProfileSubmit);
        document.getElementById("password-form")?.addEventListener("submit", handlePasswordSubmit);
        document.getElementById("logout-btn")?.addEventListener("click", handleLogout);
    }

    renderAccountPage();
};

window.initAccountPage();
