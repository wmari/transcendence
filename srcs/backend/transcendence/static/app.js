document.addEventListener("DOMContentLoaded", function () {
    checkLoginStatus();
    navigate("home");
  });
  
  function navigate(page) {
    let content = document.getElementById("content");
  
    fetch(`static/pages/${page}.html`)
      .then(response => response.text())
      .then(html => {
        content.innerHTML = html;
      })
      .catch(error => {
        content.innerHTML = "<h2>Page introuvable</h2>";
      });
  }
// Gérer la soumission du formulaire
document.getElementById('loginForm').addEventListener('submit', function(event) {
  event.preventDefault();
  
  // Récupérer les valeurs des champs
  const username = document.getElementById('username').value;
  const password = document.getElementById('password').value;

  fetch('/api/token/', {
    method: 'POST',
    headers:{
      'Content-Type': 'application/json'
    },
    body: JSON.stringify({
      username: username,
      password: password
    })
  })
  .then(response => response.json())
  .then(data => {
    if (data.access) {
        alert("Connexion réussie !");
        localStorage.setItem('access_token', data.access);
        localStorage.setItem('refresh_token', data.refresh);
        const modal = bootstrap.Modal.getInstance(document.getElementById('loginModal'));
        if (modal) modal.hide();

        checkLoginStatus();
        navigate("home");
    } else {
        alert("Identifiants incorrects !");
    }
  })
  .catch(error => {
    console.error("Erreur : ", error);
    alert("Une erreur est survenue.");
  });
});

// Vérifie si l'utilisateur est connecté
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
      if (!response.ok) {
          throw new Error("Token invalide");
      }
      return response.json();
  })
  .then(data => {
      console.log("Utilisateur connecté :", data);
      updateUI(true, data);
  })
  .catch(error => {
      console.warn("Non connecté :", error);
      localStorage.removeItem("access_token"); // Supprime le token s'il est invalide
      updateUI(false);
  });
}

// Modifie l'affichage selon l'état de connexion
function updateUI(isLoggedIn, user = null) {
  const loginButton = document.getElementById("loginButton");
  const userMenu = document.getElementById("userMenu");

  if (isLoggedIn) {
      loginButton.style.display = "none";
      userMenu.style.display = "block";
      document.getElementById("usernameDisplay").textContent = user.username;
  } else {
      loginButton.style.display = "block";
      userMenu.style.display = "none";
  }
}

// Déconnexion
function logout() {
  localStorage.removeItem("access_token");
  checkLoginStatus();
  navigate("home");
}