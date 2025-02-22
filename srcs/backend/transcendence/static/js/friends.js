document.addEventListener("DOMContentLoaded", function () {
    checkLoginStatus();
});

// Vérifie si l'utilisateur est connecté et affiche/cacher la liste d'amis
function checkLoginStatus() {
    const token = localStorage.getItem("access_token");

    if (token) {
        fetchFriendList();
    } else {
        hideFriendList();
    }
}

// Récupère et affiche la liste des amis
function fetchFriendList() {
    fetch('/api/user/', {
        method: 'GET',
        headers: {
            'Authorization': 'Bearer ' + localStorage.getItem('access_token'),
            'Content-Type': 'application/json'
        }
    })
    .then(response => response.json())
    .then(user => {
        if (user.friends) {
            displayFriends(user.friends);
        } else {
            console.error("Erreur avec la liste d'amis.");
        }
    })
    .catch(error => console.error("Erreur lors de la récupération des amis :", error));
}

// Affiche la liste d'amis
function displayFriends(friends) {
    let friendsListContainer = document.getElementById("friends-list");
    
    if (!friendsListContainer) {
        friendsListContainer = document.createElement('div');
        friendsListContainer.id = "friends-list";
        friendsListContainer.style.position = "fixed";
        friendsListContainer.style.top = "50px";
        friendsListContainer.style.right = "10px";
        friendsListContainer.style.width = "250px";
        friendsListContainer.style.backgroundColor = "#f3f3f3";
        friendsListContainer.style.padding = "10px";
        friendsListContainer.style.border = "1px solid #ccc";
        friendsListContainer.style.borderRadius = "5px";
        friendsListContainer.style.boxShadow = "0 4px 8px rgba(0, 0, 0, 0.1)";
        friendsListContainer.style.zIndex = "9999";
        document.body.appendChild(friendsListContainer);
    }

    friendsListContainer.innerHTML = "<h4>Amis</h4>";

    friends.forEach(friend => {
        const friendItem = document.createElement('div');
        friendItem.style.display = "flex";
        friendItem.style.alignItems = "center";
        friendItem.style.marginBottom = "10px";
        friendItem.style.padding = "5px";

        const profilePic = document.createElement('img');
        profilePic.src = friend.profile_picture;
        profilePic.alt = friend.username;
        profilePic.style.width = "40px";
        profilePic.style.height = "40px";
        profilePic.style.borderRadius = "50%";
        profilePic.style.marginRight = "10px";

        const nameStatus = document.createElement('div');
        nameStatus.innerHTML = `<strong>${friend.nickname}</strong> <br> 
                                <span style="color: ${friend.online ? 'green' : 'red'}">
                                    ${friend.online ? 'En ligne' : 'Hors ligne'}
                                </span>`;

        const removeBtn = document.createElement('button');
        removeBtn.textContent = "Supprimer";
        removeBtn.classList.add("btn", "btn-danger", "ms-2");
        removeBtn.onclick = () => removeFriend(friend.id);

        friendItem.appendChild(profilePic);
        friendItem.appendChild(nameStatus);
        friendItem.appendChild(removeBtn);
        friendsListContainer.appendChild(friendItem);
    });
}

// Cacher la liste des amis
function hideFriendList() {
    const friendsListContainer = document.getElementById("friends-list");
    if (friendsListContainer) {
        friendsListContainer.remove();
    }
}

// Supprimer un ami
function removeFriend(friendId) {
    const token = localStorage.getItem("access_token");

    fetch(`/api/friends/remove/${friendId}/`, {
        method: "DELETE",
        headers: {
            "Authorization": "Bearer " + token
        }
    })
    .then(response => {
        if (response.ok) {
            alert("Ami supprimé !");
            fetchFriendList();
        } else {
            alert("Erreur lors de la suppression.");
        }
    });
}
