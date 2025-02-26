document.addEventListener("profilEvent", function() {
    const profilePicture = document.getElementById("profilePicture");
    const pictureInput = document.getElementById("pictureInput");
    const nicknameSpan = document.getElementById("nickname");
    const emailSpan = document.getElementById("email");
    const editProfileBtn = document.getElementById("editProfileBtn");
    const editPasswordBtn = document.getElementById("editPasswordBtn");
    const editProfileForm = document.getElementById("editProfileForm");
    const editPasswordForm = document.getElementById("editPasswordForm");
    const profileForm = document.getElementById("profileForm");
    const passwordForm = document.getElementById("passwordForm");
    const cancelEdit = document.getElementById("cancelEdit");
    const cancelPassword = document.getElementById("cancelPassword");
    const twoFactorBtn = document.getElementById("twoFactorBtn");
    const profileInfo = document.getElementById("profileInfo");

    // Vérification du token
    const token = localStorage.getItem("access_token");
    if (!token) {
        document.getElementById("app").innerHTML = "<p class='text-danger'>Vous devez être connecté pour voir cette page.</p>";
        return;
    }

    // Charger les infos du profil
    function loadProfile() {
        fetch("/api/profil/", {
            headers: { "Authorization": `Bearer ${token}` }
        })
        .then(response => {
            if (!response.ok){
                return response.json().then(err => {throw err;});
            }
            return response.json();
        })
        .then(data => {
            data = data.data;
            nicknameSpan.textContent = data.nickname || data.username;
            emailSpan.textContent = data.email;
            if (data.profil_picture) {
                profilePicture.src = data.profil_picture;
            }
            // twoFactorBtn.textContent = data.check_2fa ? "Désactiver 2FA" : "Activer 2FA";
            
            document.getElementById("newNickname").value = data.nickname || data.username;
            document.getElementById("newEmail").value = data.email;
        })
        .catch(() => {
            showError("Erreur de chargement du profil.");
        });
    }

    // Gestion de la photo de profil
    pictureInput.addEventListener("change", function(e) {
        const file = e.target.files[0];
        if (file) {
            const formData = new FormData();
            formData.append("profil_picture", file);

            fetch("/api/uploadpp/", {
                method: "POST",
                headers: {
                    "Authorization": `Bearer ${token}`,
                    "X-CSRFToken": getCookie("csrftoken"), // Fetch CSRF token from cookies
                },
                body: formData
            })
            .then(response => response.json())
            .then(data => {
                profilePicture.src = data.profil_picture_url;
                showSuccess("Photo de profil mise à jour!");
            })
            .catch(() => {
                showError("Erreur lors du téléchargement de l'image.");
            });
        }
    });

    // Gestion du formulaire de modification du profil
    profileForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const newNickname = document.getElementById("newNickname").value;

        fetch("/api/nickname/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
                "X-CSRFToken": getCookie("csrftoken"), // Fetch CSRF token from cookies
            },
            body: JSON.stringify({ nickname: newNickname })
        })
        .then(response => response.json())
        .then(() => {
            editProfileForm.classList.add("d-none");
            profileInfo.classList.remove("d-none");
            loadProfile();
            showSuccess("Profil mis à jour avec succès!");
        })
        .catch(() => {
            showError("Erreur lors de la mise à jour du profil.");
        });
    });

    // Gestion du formulaire de modification du mot de passe
    passwordForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const currentPassword = document.getElementById("currentPassword").value;
        const newPassword = document.getElementById("newPassword").value;
        const confirmPassword = document.getElementById("confirmPassword").value;

        if (newPassword !== confirmPassword) {
            showError("Les mots de passe ne correspondent pas.");
            return;
        }

        fetch("/api/change_password", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": `Bearer ${token}`,
                "X-CSRFToken": getCookie("csrftoken"), // Fetch CSRF token from cookies
            },
            body: JSON.stringify({
                current_password: currentPassword,
                new_password: newPassword
            })
        })
        .then(response => response.json())
        .then(() => {
            editPasswordForm.classList.add("d-none");
            profileInfo.classList.remove("d-none");
            passwordForm.reset();
            showSuccess("Mot de passe modifié avec succès!");
        })
        .catch(() => {
            showError("Erreur lors de la modification du mot de passe.");
        });
    });

    // Toggle des formulaires
    editProfileBtn.addEventListener("click", function() {
        editProfileForm.classList.remove("d-none");
        editPasswordForm.classList.add("d-none");
        profileInfo.classList.add("d-none");
    });

    editPasswordBtn.addEventListener("click", function() {
        editPasswordForm.classList.remove("d-none");
        editProfileForm.classList.add("d-none");
        profileInfo.classList.add("d-none");
    });

    cancelEdit.addEventListener("click", function() {
        editProfileForm.classList.add("d-none");
        profileInfo.classList.remove("d-none");
    });

    cancelPassword.addEventListener("click", function() {
        editPasswordForm.classList.add("d-none");
        profileInfo.classList.remove("d-none");
        passwordForm.reset();
    });

    // Utilitaires pour afficher les messages
    function showError(message) {
        const alert = createAlert(message, 'danger');
        document.querySelector('.card-body').prepend(alert);
    }

    function showSuccess(message) {
        const alert = createAlert(message, 'success');
        document.querySelector('.card-body').prepend(alert);
    }

    function createAlert(message, type) {
        const alert = document.createElement('div');
        alert.className = `alert alert-${type} alert-dismissible fade show`;
        alert.innerHTML = `
            ${message}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;
        setTimeout(() => alert.remove(), 3000);
        return alert;
    }

    loadProfile();
});

function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== "") {
        const cookies = document.cookie.split(";");
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.startsWith(name + "=")) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}