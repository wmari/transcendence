// tournament.js

console.log("tournament.js is loaded and running!");

// Objet global pour stocker l'état du tournoi
let tournament = {
  participants: [],
  bracket: [],
  currentMatchIndex: 0,
  status: "registration"
};

window.initTournamentPage = function() {
  console.log("Init Tournament Page");

  // Sélecteurs
  const formAdd = document.getElementById("add-participant-form");
  const aliasInput = document.getElementById("participant-alias");
  const typeSelect = document.getElementById("participant-type");
  const userSelectContainer = document.getElementById("user-select-container");
  const userSelect = document.getElementById("connected-user-select");
  const participantsList = document.getElementById("participants-list");
  const startBtn = document.getElementById("start-tournament-btn");


  typeSelect.addEventListener("change", () => {
	const type = typeSelect.value;
	if (type === "user") {
		userSelectContainer.style.display = "block";
		aliasInput.style.display = "none";
		aliasInput.removeAttribute("required");
		fetchConnectedUsers();
	} else if (type ==="ia") {
		userSelectContainer.style.display = "none";
		aliasInput.style.display = "block";
		aliasInput.removeAttribute("required");
	} else {
		userSelectContainer.style.display = "none";
		aliasInput.style.display = "block";
		aliasInput.setAttribute("required", "");

	}
});

  // Listener sur le formulaire
  formAdd.addEventListener("submit", (e) => {
    e.preventDefault(); // Empêche le rechargement de la page
    const type = typeSelect.value;
    let participant = {};

    if (type === "guest") {
      const alias = aliasInput.value.trim();
      if (!alias) {
        alert("Veuillez saisir votre nom.");
        return;
      }
      participant = { alias, type };
    } else if (type === "user") {
      const selectedUserId = userSelect.value;
      if (!selectedUserId) {
        alert("Veuillez sélectionner un profil connecté.");
        return;
      }
	  if (tournament.participants.some(p => p.type === "user" && p.userId === selectedUserId)) {
		alert("Cet utilisateur est déjà inscrit au tournoi !");
		return;
	  }
      const selectedUserText = userSelect.options[userSelect.selectedIndex].text;
      participant = { alias: selectedUserText, type, userId: selectedUserId };

	  availableUsers = availableUsers.filter(u => String(u.id) !== selectedUserId);

	  renderUserDropdown();

    } else if (type === "ia") {
      let alias = aliasInput.value.trim();
      if (!alias) {
        const iaCount = tournament.participants.filter(p => p.type === "ia").length;
        alias = "IA-" + (iaCount + 1);
      }
      participant = { alias, type };
    }

    tournament.participants.push(participant);
    formAdd.reset();
    aliasInput.style.display = "block";
    userSelectContainer.style.display = "none";

    updateParticipantsList();
  });

  function updateParticipantsList() {
    participantsList.innerHTML = "";
    tournament.participants.forEach((p) => {
      const li = document.createElement("li");
      li.textContent = `${p.alias} (${p.type})`;
      participantsList.appendChild(li);
    });
    // Activer startBtn si >= 2 participants
    startBtn.disabled = (tournament.participants.length < 2);
  }

  function fetchConnectedUsers() {
    fetch("/api/users/")
      .then(response => response.json())
      .then(users => {
        availableUsers = users;
        usersFetched = true;
        renderUserDropdown();
      })
      .catch(error => {
        console.error("Erreur lors du chargement des utilisateurs connectés", error);
      });
  }

  function renderUserDropdown() {
    userSelect.innerHTML = "";
    const defaultOption = document.createElement("option");
    defaultOption.value = "";
    defaultOption.textContent = "Sélectionnez un profil";
    userSelect.appendChild(defaultOption);

    // On filtre les utilisateurs déjà inscrits
    const alreadyUsedIds = tournament.participants
      .filter(p => p.type === "user")
      .map(p => String(p.userId));

    // On crée une option pour chaque utilisateur non-inscrit
    availableUsers.forEach(user => {
      if (!alreadyUsedIds.includes(String(user.id))) {
        const option = document.createElement("option");
        option.value = user.id;
        option.textContent = user.username;
        userSelect.appendChild(option);
      }
    });
  }

  // Bouton "Démarrer"
  if (startBtn) {
    startBtn.addEventListener("click", () => {
      startTournament();
    });
  }

  // Exemple minimaliste de "startTournament"
  function startTournament() {
    console.log("Starting the tournament!");
    document.getElementById("registration-section").style.display = "none";
    document.getElementById("bracket-section").style.display = "block";
    // ...
  }
}