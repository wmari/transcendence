document.addEventListener("DOMContentLoaded", function () {
    const registerForm = document.getElementById("registerForm");
    const registerModal = new bootstrap.Modal(document.getElementById("registerModal"));
    const registerError = document.getElementById("registerError");
    const registerSuccess = document.getElementById("registerSuccess");
    
    registerForm.addEventListener("submit", function (e) {
      e.preventDefault();
      const username = document.getElementById("reg_username").value;
      const email = document.getElementById("reg_email").value;
      const password1 = document.getElementById("reg_password").value; // Changé pour correspondre à l'ID HTML
      const password2 = document.getElementById("reg_password_confirm").value; // Changé pour correspondre à l'ID HTML
  
      // Vérification que les mots de passe correspondent
      if (password1 !== password2) {
        registerError.textContent = "Les mots de passe ne correspondent pas.";
        registerError.classList.remove("d-none");
        registerSuccess.classList.add("d-none");
        return;
      }
      
      registerError.classList.add("d-none");
      registerSuccess.classList.add("d-none");
  
      // Obtenir d'abord le token CSRF
      fetch("/api/get-csrf-token/", {
        method: "GET"
      })
      .then(response => response.json())
      .then(data => {
        const csrftoken = data.csrftoken;
        
        // Maintenant faire la requête d'inscription
        return fetch("/api/register/", {
          method: "POST",
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": csrftoken,
          },
          body: JSON.stringify({
            username: username, 
            email: email, 
            password1: password1, // Renommé pour correspondre à ce qu'attend le backend
            password2: password2  // Ajouté car le backend attend ce champ
          })
        });
      })
      .then(response => {
        if (!response.ok) {
          return response.json().then(data => {
            throw new Error(data.error || "Erreur lors de l'inscription");
          });
        }
        return response.json();
      })
      .then(data => {
        console.log("Inscription réussie :", data);
        registerSuccess.textContent = "Inscription réussie. Vous pouvez maintenant vous connecter.";
        registerSuccess.classList.remove("d-none");
        registerForm.reset();
        // Fermeture automatique de la modal après 3 secondes
        setTimeout(() => {
          registerModal.hide();
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
  
    // Fonction pour récupérer le CSRF - gardée mais peut ne pas être nécessaire avec l'approche ci-dessus
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