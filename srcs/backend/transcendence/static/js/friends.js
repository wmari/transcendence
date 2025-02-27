// Sauvegardez ce fichier en tant que friendslist.js et ajoutez-le à votre HTML
document.addEventListener("DOMContentLoaded", function () {
    const friendsButtonContainer = document.getElementById("friendsButtonContainer");
    const toggleFriendsBtn = document.getElementById("toggleFriendsBtn");
    const friendsSidebar = document.getElementById("friendsSidebar");
    const closeFriendsBtn = document.getElementById("closeFriendsBtn");
    const addFriendForm = document.getElementById("addFriendForm");
    const friendAddError = document.getElementById("friendAddError");
    const friendAddSuccess = document.getElementById("friendAddSuccess");
    const onlineFriendsList = document.getElementById("onlineFriendsList");
    const offlineFriendsList = document.getElementById("offlineFriendsList");
    const onlineFriendsCount = document.getElementById("onlineFriendsCount");
    
    // Fonction pour montrer/cacher la friend list
    toggleFriendsBtn.addEventListener("click", function() {
        friendsSidebar.classList.toggle("d-none");
    });
    
    // Fermeture de la friend list
    closeFriendsBtn.addEventListener("click", function() {
        friendsSidebar.classList.add("d-none");
    });
    
    // Ajouter un ami
    addFriendForm.addEventListener("submit", function(e) {
        e.preventDefault();
        const friendUsername = document.getElementById("friendUsername").value;
        
        // Réinitialiser les messages
        friendAddError.classList.add("d-none");
        friendAddSuccess.classList.add("d-none");
        
        const token = localStorage.getItem("access_token");
        if (!token) {
            friendAddError.textContent = "Veuillez vous connecter d'abord.";
            friendAddError.classList.remove("d-none");
            return;
        }
        
        fetch("/api/addfriend/", {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
                "X-CSRFToken": getCookie("csrftoken"),
            },
            body: JSON.stringify({ username: friendUsername })
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || "Erreur lors de l'ajout de l'ami");
                });
            }
            return response.json();
        })
        .then(data => {
            friendAddSuccess.textContent = data.message || "Ami ajouté avec succès!";
            friendAddSuccess.classList.remove("d-none");
            addFriendForm.reset();
            
            // Recharger la liste des amis
            loadFriendsList();
            
            // Masquer le message de succès après 3 secondes
            setTimeout(() => {
                friendAddSuccess.classList.add("d-none");
            }, 3000);
        })
        .catch(error => {
            friendAddError.textContent = error.message;
            friendAddError.classList.remove("d-none");
            
            // Masquer le message d'erreur après 3 secondes
            setTimeout(() => {
                friendAddError.classList.add("d-none");
            }, 3000);
        });
    });
    
    // Fonction pour supprimer un ami
    function removeFriend(friendId, friendElement) {
        const token = localStorage.getItem("access_token");
        if (!token) return;
        
        fetch(`/api/friends/remove/${friendId}/`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json",
                "Authorization": "Bearer " + token,
                "X-CSRFToken": getCookie("csrftoken"),
            }
        })
        .then(response => {
            if (!response.ok) {
                return response.json().then(data => {
                    throw new Error(data.error || "Erreur lors de la suppression de l'ami");
                });
            }
            return response.json();
        })
        .then(data => {
            // Supprimer l'élément de la liste
            friendElement.remove();
            
            // Mettre à jour le compteur d'amis en ligne
            updateOnlineFriendsCount();
            
            // Afficher un message temporaire de succès
            const tempMessage = document.createElement("div");
            tempMessage.className = "alert alert-success position-fixed top-0 start-50 translate-middle-x mt-3";
            tempMessage.style.zIndex = "1050";
            tempMessage.textContent = data.message || "Ami supprimé avec succès!";
            document.body.appendChild(tempMessage);
            
            setTimeout(() => {
                tempMessage.remove();
            }, 3000);
        })
        .catch(error => {
            console.error("Erreur:", error);
            // Afficher un message d'erreur temporaire
            const tempMessage = document.createElement("div");
            tempMessage.className = "alert alert-danger position-fixed top-0 start-50 translate-middle-x mt-3";
            tempMessage.style.zIndex = "1050";
            tempMessage.textContent = error.message;
            document.body.appendChild(tempMessage);
            
            setTimeout(() => {
                tempMessage.remove();
            }, 3000);
        });
    }
    
    // Créer un élément pour chaque ami
    function createFriendElement(friend) {
        const li = document.createElement("li");
        li.className = "list-group-item d-flex justify-content-between align-items-center";
        
        // Ajouter le statut en jeu si nécessaire
        let statusIcon = "";
        if (friend.ingame) {
            statusIcon = '<span class="badge bg-warning ms-2">En jeu</span>';
        }
        
        // Créer l'élément principal avec avatar + nom
        const friendInfo = document.createElement("div");
        friendInfo.className = "d-flex align-items-center";
        
        // Avatar ou image par défaut
        const profilePicUrl = friend.profil_picrture || '/media/PPicture/default.jpg';
        friendInfo.innerHTML = `
            <div class="avatar me-2" style="width: 32px; height: 32px; overflow: hidden; border-radius: 50%;">
                <img src="${profilePicUrl}" alt="${friend.nickname}" style="width: 100%; height: 100%; object-fit: cover;">
            </div>
            <span>${friend.nickname}</span>
            ${statusIcon}
        `;
        
        // Bouton de suppression
        const removeBtn = document.createElement("button");
        removeBtn.className = "btn btn-sm btn-outline-danger";
        removeBtn.innerHTML = '<i class="bi bi-person-dash"></i>';
        removeBtn.title = "Supprimer cet ami";
        
        // Ajouter l'événement de suppression
        removeBtn.addEventListener("click", function() {
            removeFriend(friend.id, li);
        });
        
        // Assembler l'élément
        li.appendChild(friendInfo);
        li.appendChild(removeBtn);
        
        return li;
    }
    
    // Mettre à jour le compteur d'amis en ligne
    function updateOnlineFriendsCount() {
        const onlineCount = onlineFriendsList.querySelectorAll("li").length;
        onlineFriendsCount.textContent = onlineCount;
    }
    
    // Charger la liste des amis
    function loadFriendsList() {
        const token = localStorage.getItem("access_token");
        if (!token) return;
        
        // Afficher des placeholders de chargement
        onlineFriendsList.innerHTML = '<li class="list-group-item text-muted small fst-italic">Chargement...</li>';
        offlineFriendsList.innerHTML = '<li class="list-group-item text-muted small fst-italic">Chargement...</li>';
        
        fetch("/api/getuserfriendlist/", {
            method: "GET",
            headers: {
                "Authorization": "Bearer " + token
            }
        })
        .then(response => {
            if (!response.ok) {
                throw new Error("Erreur lors du chargement des amis");
            }
            return response.json();
        })
        .then(friends => {
            // Vider les listes
            onlineFriendsList.innerHTML = "";
            offlineFriendsList.innerHTML = "";
            
            if (friends.length === 0) {
                onlineFriendsList.innerHTML = '<li class="list-group-item text-muted small fst-italic">Aucun ami en ligne</li>';
                offlineFriendsList.innerHTML = '<li class="list-group-item text-muted small fst-italic">Aucun ami</li>';
            } else {
                let onlineCount = 0;
                let offlineCount = 0;
                
                friends.forEach(friend => {
                    const friendElement = createFriendElement(friend);
                    
                    if (friend.online) {
                        onlineFriendsList.appendChild(friendElement);
                        onlineCount++;
                    } else {
                        offlineFriendsList.appendChild(friendElement);
                        offlineCount++;
                    }
                });
                
                // Ajouter un message si aucun ami n'est en ligne/hors ligne
                if (onlineCount === 0) {
                    onlineFriendsList.innerHTML = '<li class="list-group-item text-muted small fst-italic">Aucun ami en ligne</li>';
                }
                if (offlineCount === 0) {
                    offlineFriendsList.innerHTML = '<li class="list-group-item text-muted small fst-italic">Aucun ami hors ligne</li>';
                }
            }
            
            // Mettre à jour le badge du nombre d'amis en ligne
            updateOnlineFriendsCount();
        })
        .catch(error => {
            console.error("Erreur de chargement des amis:", error);
            onlineFriendsList.innerHTML = '<li class="list-group-item text-danger small">Erreur de chargement</li>';
            offlineFriendsList.innerHTML = '<li class="list-group-item text-danger small">Erreur de chargement</li>';
        });
    }
    
    // Fonction pour obtenir le CSRF token
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
    
    // Mettre à jour la visibilité de la friend list en fonction de la connexion
    function updateFriendsListVisibility(isLoggedIn) {
        if (isLoggedIn) {
            friendsButtonContainer.classList.remove("d-none");
            loadFriendsList();
            
            // Rafraîchir la liste des amis toutes les 30 secondes
            if (!window.friendsListInterval) {
                window.friendsListInterval = setInterval(loadFriendsList, 30000);
            }
        } else {
            friendsButtonContainer.classList.add("d-none");
            friendsSidebar.classList.add("d-none");
            
            // Arrêter le rafraîchissement automatique
            if (window.friendsListInterval) {
                clearInterval(window.friendsListInterval);
                window.friendsListInterval = null;
            }
        }
    }
    
    // Nous n'avons pas besoin de modifier updateUI puisque nous allons utiliser checkLoginStatus de login.js
    
    // Vérifier l'état de connexion initial
    document.addEventListener('DOMContentLoaded', function() {
        // Attendre que checkLoginStatus de login.js soit exécuté
        setTimeout(function() {
            const token = localStorage.getItem("access_token");
            updateFriendsListVisibility(!!token);
        }, 100);
    });
    
    // Écouter les changements de stockage local (déconnexion/connexion)
    window.addEventListener('storage', function(e) {
        if (e.key === 'access_token') {
            updateFriendsListVisibility(!!e.newValue);
        }
    });
});