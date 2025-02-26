document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");
    const registerModal = new bootstrap.Modal(document.getElementById("registerModal"));
    const registerError = document.getElementById("registerError");
    const registerSuccess = document.getElementById("registerSuccess");
    
    registerForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const username = document.getElementById("reg_username").value;
        const email = document.getElementById("reg_email").value;
        const password = document.getElementById("reg_password").value;
        const password_confirm = document.getElementById("reg_password_confirm").value;
        
        // Vérification que les mots de passe correspondent
        if (password !== password_confirm) {
            registerError.textContent = "Les mots de passe ne correspondent pas.";
            registerError.classList.remove("d-none");
            registerSuccess.classList.add("d-none");
            return;
        }
        
        // Reset des messages d'erreur/succès
        registerError.classList.add("d-none");
        registerSuccess.classList.add("d-none");
        
        fetch("/api/register/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"), // Fetch CSRF token from cookies
            },
            body: JSON.stringify({username, email, password})
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.message || "Erreur lors de l'inscription");
                });
            }
            return response.json();
        })
        .then(data => {
            console.log("Inscription réussie :", data);
            registerSuccess.textContent = "Inscription réussie. Vous pouvez maintenant vous connecter.";
            registerSuccess.classList.remove("d-none");
            
            // Réinitialisation du formulaire
            registerForm.reset();
            
            // Fermeture automatique de la modal après 3 secondes
            setTimeout(() => {
                registerModal.hide();
                // Optionnel : ouvrir automatiquement la modal de connexion
                const loginModal = new bootstrap.Modal(document.getElementById("loginModal"));
                loginModal.show();
            }, 3000);
        })
        .catch(error => {
            console.error("Erreur d'inscription :", error);
            registerError.textContent = error.message || "Erreur lors de l'inscription.";
            registerError.classList.remove("d-none");
        });
    });
    
    // Fonction pour récupérer le CSRF token (identique à celle du login.js)
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
});