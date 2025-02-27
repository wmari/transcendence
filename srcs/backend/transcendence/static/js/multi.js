console.log("Mode Multijoueur chargé !");


startGameMulti()

function startGameMulti() {

    document.getElementById("game").style.display = "block";
    document.getElementById("loadingMessage").style.display = "none";

    // define elements
    const score1Element = document.getElementById('score1');
    const score2Element = document.getElementById('score2');
    const player1Element = document.getElementById('playerA');
    const player2Element = document.getElementById('playerB');
    const winnerElement = document.getElementById('winScreen');
    const countdownElement = document.getElementById('countdown');
    let turn = localStorage.getItem('turn');
    if (!turn) {
        turn = 1;
        localStorage.setItem('turn', turn);
    }
    else {
        turn++;
        localStorage.setItem('turn', turn);
    }

    // define playground
    const WIDTH = 1000;
    const HEIGHT = 650;
    const fieldWidth = 400, fieldHeight = 200;

    // define camera
    const VIEW_ANGLE = 45;
    const ASPECT = WIDTH / HEIGHT;
    const NEAR = 0.1;
    const FAR = 10000;
    let renderer, scene, camera, pointLightOne, pointLightTwo;


    // define ball
    const RADIUS = 5;
    const SEGMENTS = 16;
    const RINGS = 16;

    // define border
    const barrierThickness = 2;
    const barrierHeight = 5;
    const barrierDepth = fieldHeight;


    // define game elements
    let ball, paddle1, paddle2;
    const paddleWidth = 10, paddleHeight = 10;
    const paddleDepth = 50, paddleQuality = 1;
    let paddle1DirZ = 0, paddle2DirZ = 0, paddleSpeed = 2;
    let ballDirX = -1, ballDirZ = 1, ballSpeed = 1;

    //define score
    let score1 = 0;
    let score2 = 0;
    let player1 = "Player1";
    let player2 = "Player2";
    let winner = 5;

    // define key
    var KEYDOWN = "KeyS", KEYUP = "KeyW", 
    KEYDOWNTWO = "ArrowDown", KEYUPTWO = "ArrowUp";

    var goUpOne = false, goDownOne = false, 
    goUpTwo = false, goDownTwo = false;

    document.addEventListener('keydown', onKeyDown);
    document.addEventListener('keyup', onKeyUp);



    // define game status
    var isRunning = 0;

    player1Element.textContent = player1;
    player2Element.textContent = player2;


    //countdown

    function startCountdown(callback) {
    countdownElement.style.display = 'block';
    let counter = 3;
    countdownElement.textContent = `Starting in ${counter}`;

    const interval = setInterval(() => {
        counter--;
        if (counter > 0) {
            countdownElement.textContent = `Starting in ${counter}`;
        } else {
            clearInterval(interval);
            countdownElement.style.display = 'none';
            callback();
        }
    }, 1000);
    }


    //renderer/camera/scene

    renderer = new THREE.WebGLRenderer({alpha: true});

    camera = new THREE.PerspectiveCamera(
    VIEW_ANGLE,
    ASPECT,
    NEAR,
    FAR
    );

    scene = new THREE.Scene();

    //add camera

    scene.add(camera);
        
    camera.position.set(0, 300, 350);
    camera.lookAt(scene.position);

    //start renderer
    renderer.setSize(WIDTH, HEIGHT);


    // get elem
    const container = document.getElementById('gameCanvas');

    container.appendChild(renderer.domElement);

    //light1
    pointLightOne = new THREE.PointLight(0xF8D898);


    //light position
    pointLightOne.position.set(100, 100, 0);
    pointLightOne.intensity = 1;
    pointLightOne.distance = 0;

    scene.add(pointLightOne);

    //light2
    pointLightTwo = new THREE.PointLight(0xF8D898);

    pointLightTwo.position.set(-100, 100, 0);
    pointLightTwo.intensity = 1;
    pointLightTwo.distance = 0;

    scene.add(pointLightTwo);

    //game model

    //ball

    const sphereMaterial = new THREE.MeshLambertMaterial({ color: 0x303030 });

    ball = new THREE.Mesh(
    new THREE.SphereGeometry(RADIUS, SEGMENTS, RINGS),
    sphereMaterial
    );

    ball.position.set(0, RADIUS, 0);

    scene.add(ball);

    //playground

    //surface

    const planeWidth = fieldWidth, planeHeight = fieldHeight, planeQuality = 32;

    const planeMaterial = new THREE.MeshLambertMaterial({ color: 0xFFD5A1 });

    const plane = new THREE.Mesh(
    new THREE.PlaneGeometry(planeWidth, planeHeight, planeQuality, planeQuality),
    planeMaterial
    );

    plane.rotation.x = -Math.PI / 2;

    plane.position.y = -5;

    scene.add(plane);


    //border

    const barrierMaterial = new THREE.MeshLambertMaterial({ color: 0x444444 });


    //top border
    const topBarrier = new THREE.Mesh(
    new THREE.BoxGeometry(fieldWidth, barrierHeight, barrierThickness),
    barrierMaterial
    );

    topBarrier.position.set(0, barrierHeight / 2, -fieldHeight / 2 - barrierThickness / 2);


    scene.add(topBarrier);


    //bot border
    const bottomBarrier = new THREE.Mesh(
    new THREE.BoxGeometry(fieldWidth, barrierHeight, barrierThickness),
    barrierMaterial
    );

    bottomBarrier.position.set(0, barrierHeight / 2, fieldHeight / 2 + barrierThickness / 2);

    scene.add(bottomBarrier);


    //paddle

    const paddle1Material = new THREE.MeshLambertMaterial({ color: 0x0000FF });
    const paddle2Material = new THREE.MeshLambertMaterial({ color: 0xFF0000 });

    //paddle1

    paddle1 = new THREE.Mesh(
    new THREE.BoxGeometry(
        paddleWidth,
        paddleHeight,
        paddleDepth,
        paddleQuality,
        paddleQuality,
        paddleQuality),
        paddle1Material);

    scene.add(paddle1);

    //paddle2

    paddle2 = new THREE.Mesh(
    new THREE.BoxGeometry(
        paddleWidth,
        paddleHeight,
        paddleDepth,
        paddleQuality,
        paddleQuality,
        paddleQuality),
        paddle2Material);

    scene.add(paddle2);

    //set paddle position

    paddle1.position.x = -fieldWidth / 2 + paddleWidth;
    paddle2.position.x = fieldWidth / 2 - paddleWidth;

    paddle1.position.z = paddleDepth / 2;
    paddle2.position.z = paddleDepth / 2;


    //game

    function ballMovement() {

    ball.position.x += ballDirX * ballSpeed;
    ball.position.z += ballDirZ * ballSpeed;

    if (ball.position.z <= -fieldHeight / 2 + RADIUS || ball.position.z >= fieldHeight / 2 - RADIUS) {
        ballDirZ = -ballDirZ;
    }

    if (ballDirZ > ballSpeed * 2) {
        ballDirZ = ballSpeed * 2;
    } else if (ballDirZ < -ballSpeed * 2) {
        ballDirZ = -ballSpeed * 2;
    }
    }

    function paddelCollide() {

    //paddle1
    if (ball.position.x - RADIUS <= paddle1.position.x + paddleWidth / 2 
        && ball.position.x + RADIUS >= paddle1.position.x - paddleWidth / 2) {
        if (ball.position.z <= paddle1.position.z + paddleDepth / 2 
        && ball.position.z >= paddle1.position.z - paddleDepth / 2) {
        if (ballDirX < 0) {
            ballDirX = -ballDirX;
            let impactPoint = (ball.position.z - paddle1.position.z) / (paddleDepth / 2);
            ballDirZ = impactPoint * ballSpeed / 1.5;
            ballSpeed += 0.1; // Increase ball speed after collision with paddle1
        }
        }
    }

    //paddle2
    if (ball.position.x + RADIUS >= paddle2.position.x - paddleWidth / 2 
        && ball.position.x - RADIUS <= paddle2.position.x + paddleWidth / 2) {
        if (ball.position.z <= paddle2.position.z + paddleDepth / 2 
        && ball.position.z >= paddle2.position.z - paddleDepth / 2) {
        if (ballDirX > 0) {
            ballDirX = -ballDirX;
            let impactPoint = (ball.position.z - paddle2.position.z) / (paddleDepth / 2);
            ballDirZ = impactPoint * ballSpeed / 1.5;
            ballSpeed += 0.1; // Increase ball speed after collision with paddle2
        }
        }
    }
    }

    //paddle movement

    function onKeyDown(event) {

    if (event.code == KEYDOWN) {
        goDownOne = true;
    }
    if (event.code == KEYUP) {
        goUpOne = true;
    } 

    if (event.code == KEYDOWNTWO) {
        goDownTwo = true;
    }
    if (event.code == KEYUPTWO) {
        goUpTwo = true;
    } 
    }

    function onKeyUp(event) {

    if (event.code == KEYDOWN) {
        goDownOne = false;
    }
    if (event.code == KEYUP) {
        goUpOne = false;
    } 

    if (event.code == KEYDOWNTWO) {
        goDownTwo = false;
    }
    if (event.code == KEYUPTWO) {
        goUpTwo = false;
    } 
    }

    function playersMovement() {

    if (goUpOne && paddle1.position.z > -fieldHeight / 2 + paddleDepth / 2 + 2) {
        paddle1.position.z -= paddleSpeed;
    }
    if (goDownOne && paddle1.position.z < fieldHeight / 2 - paddleDepth / 2 - 2) {
        paddle1.position.z += paddleSpeed;
    }

    if (goUpTwo && paddle2.position.z > -fieldHeight / 2 + paddleDepth / 2 + 2) {
        paddle2.position.z -= paddleSpeed;
    }
    if (goDownTwo && paddle2.position.z < fieldHeight / 2 - paddleDepth / 2 - 2) {
        paddle2.position.z += paddleSpeed;
    }

    }

    //score

    function goalManagement() {

    if (ball.position.x >= paddle2.position.x + paddleWidth / 2)
    {
        score1 += 1;
        updateScores();
        resetBall();
    }

    if (ball.position.x <= paddle1.position.x - paddleWidth / 2)
    {
        score2 += 1;
        updateScores();
        resetBall();
    }
    }

    function updateScores() {

    if (score1Element && score2Element) {
        score1Element.textContent = score1;
        score2Element.textContent = score2;
    }

    }


    function resetBall() {
    ballSpeed = 0;
    ballDirZ = 0;
    ball.position.set(0, RADIUS, 0);


    paddle1.position.z = paddleDepth / 2;
    paddle2.position.z = paddleDepth / 2;
    paddle1DirZ = 0;
    paddle2DirZ = 0;

    setTimeout(() => {
        ballDirX = (score1 > score2) ? -1 : 1;
        ballDirZ = Math.random() * 2 - 1;
        ballSpeed = 1;
    }, 2000); 
    }

    function scoreCheck() {

    if (score1 >= winner)
    {
        ballSpeed = 0;
        isRunning = 1;

    }
    else if (score2 >= winner)
    {
        ballSpeed = 0;
        isRunning = 2;
    }
    }


    //game update
    function update() {

    renderer.render(scene, camera);
    
    ballMovement();
    playersMovement();
    paddelCollide();
    goalManagement();
    scoreCheck();

    if (localStorage.getItem('turn') != turn)
        return;

    if (isRunning != 0) {
        let win;
        ballSpeed = 0;
        ball.position.set(0, RADIUS, 0);
        renderer.render(scene, camera);
        if (isRunning == 1) {
        winnerElement.textContent = `Player1 Wins !`;
        win = true;
        }
        else if (isRunning == 2) {
        winnerElement.textContent = `Player2 Wins !`;
        win = false;
        }

        // let data = {
        // 'opponent': 'random',
        // 'win': win,
        // 'my_score': score1,
        // 'opponent_score': score2,
        // };

        // (async () => {
        // try {
        //     let csrfToken = await getCSRFToken(); //appelle la focntion getCSRF
        //     let jwtToken = localStorage.getItem('jwtToken'); //recupere le jwt token
        //     const response = await fetch('/api/game_end/', { //post request to game_end_view
        //     method: 'POST',
        //     headers: {
        //         'Authorization': `Bearer ${jwtToken}`,
        //         'X-CSRFToken': csrfToken,
        //         'Content-Type': 'application/json',
        //     },
        //     credentials: 'include',
        //     body: JSON.stringify(data), //send the data as a json string
        //     });

        //     const respdata = await response.json(); //la reponse est converti en json
        //     if (!response.ok)
        //     console.error(respdata.error);
        // } catch (error) {
        //     console.error('Error during fetching:', error);
        // }
        // })();
        // return;

    }
    requestAnimationFrame(update);
    }

    startCountdown(() => {
    update();
    });
}