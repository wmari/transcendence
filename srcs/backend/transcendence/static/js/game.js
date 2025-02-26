document.addEventListener("gameEvent", function(){
    console.log("Game page chargée");

    document.getElementById("soloBtn").addEventListener("click", function (){
        startGame("solo");
    });

    document.getElementById("multiBtn").addEventListener("click", function () {
        startGame("multi");
    });
});

function startGame(mode){
    console.log(`start mode ${mode}`);

    const gameContainer = document.getElementById("gameContainer");
    document.getElementById("loadingMessage").innerHTML = `<p>Chargement du mode <strong>${mode}</strong>...</p>`;

    const script = document.createElement("script");
    script.src = `static/js/${mode}.js`;
    script.defer = true;

    document.querySelectorAll("script[data-game]").forEach(s => s.remove());

    script.dataset.game = "true"; // Marque le script pour le retrouver
    document.body.appendChild(script);
}