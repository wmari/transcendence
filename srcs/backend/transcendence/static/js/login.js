document.addEventListener("DOMContentLoaded", function () {
    const loginForm = document.getElementById("loginForm");
    const loginBtn = document.getElementById("loginBtn");
    const logoutBtn = document.getElementById("logoutBtn");
    const loginModal = new bootstrap.Modal(document.getElementById("loginModal"));
    const profilBtn = document.getElementById("profilBtn");
    const gameBtn = document.getElementById("gameBtn");
    const tournamentBtn = document.getElementById("tournamentBtn");

    
    loginForm.addEventListener("submit", function (e) {
        e.preventDefault();
        const username = document.getElementById("username").value;
        const password = document.getElementById("password").value;

        fetch("/api/login/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"), // Fetch CSRF token from cookies
            },
            body: JSON.stringify({username, password})
        })
        .then(response => response.json())
        .then(data => {
            if (data.access) {
                localStorage.setItem("access_token", data.access);
                localStorage.setItem("refresh_token", data.refresh)
                checkLoginStatus();
                loginModal.hide();
            } else {
                document.getElementById("loginError").classList.remove("d-none");
            }
        })
        .catch(() =>{
            document.getElementById("loginError").classList.remove("d-none");
        });
    });
    

    function checkLoginStatus() {
        const token = localStorage.getItem("access_token");
        if (!token) {
            updateUI(false);
            return;
        }
        fetch("/api/user/", { // Endpoint Django pour vérifier le token
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            }
        })
        .then(response => {
            if (response.status === 401) {
                refreshToken();
                throw new Error("Token expiré");
            }
            return response.json();
        })
        .then(data => {
            console.log("Utilisateur connecté :", data);
            updateUI(true);
        })
        .catch(error => {
            console.warn("Non connecté :", error);
            localStorage.removeItem("access_token"); // Supprime le token s'il est invalide
            updateUI(false);
        });
    }

    // Modification à apporter à votre fonction updateUI dans login.js
// Remplacez la fonction updateUI existante par celle-ci:

    function updateUI(isLoggedIn) {
        const registerBtn = document.getElementById("registerBtn");
        const friendsButtonContainer = document.getElementById("friendsButtonContainer");
    
        if (isLoggedIn) {
            loginBtn.classList.add("d-none");
            registerBtn.classList.add("d-none");
            logoutBtn.classList.remove("d-none");   
            profilBtn.classList.remove("d-none");
            gameBtn.classList.remove("d-none");
            tournamentBtn.classList.remove("d-none");
        
            // Afficher la friend list quand on est connecté
            if (friendsButtonContainer) {
                friendsButtonContainer.classList.remove("d-none");
                // Si une fonction loadFriendsList existe (définie dans friendslist.js)
                if (typeof window.loadFriendsList === 'function') {
                    window.loadFriendsList();
                }
            }
        } else {
            loginBtn.classList.remove("d-none");
            registerBtn.classList.remove("d-none");
            logoutBtn.classList.add("d-none");
            profilBtn.classList.add("d-none");
            gameBtn.classList.add("d-none");
            tournamentBtn.classList.add("d-none");
        
            // Cacher la friend list quand on est déconnecté
            if (friendsButtonContainer) {
                friendsButtonContainer.classList.add("d-none");
                const friendsSidebar = document.getElementById("friendsSidebar");
                if (friendsSidebar) {
                    friendsSidebar.classList.add("d-none");
                }
            }
        }
    }
    // rend checkLoginStatus global
    window.checkLoginStatus = checkLoginStatus;
    window.updateUI = updateUI;

    
    
    logoutBtn.addEventListener("click", function () {
        fetch("/api/logout/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "X-CSRFToken": getCookie("csrftoken"), // Fetch CSRF token from cookies
            },
        })
        .then(response => {
            if (!response.ok){
                throw new Error("probably not connected");
            }
            return response.json();
        })
        .then(data => {
                console.log(data.message);
                localStorage.removeItem("access_token");
                localStorage.removeItem("refresh_token");
                checkLoginStatus();
        })
        .catch(error => console.error("Error :", error));
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

    // execute checkLoginStatus au chargement de la page
    checkLoginStatus();
});

