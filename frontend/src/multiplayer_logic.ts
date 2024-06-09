import { Socket, io } from "socket.io-client";
import { hostApi } from "./config";
import { multiplayerController } from "./multiplayer_controller";
import { GameStarting } from "../../open-api/generated/pathological-typescript-api/models/GameStarting"
import { GameStarted } from "../../open-api/generated/pathological-typescript-api/models/GameStarted"
import { PlayerJoin } from "../../open-api/generated/pathological-typescript-api/models/PlayerJoin"
import { PlayerLeft } from "../../open-api/generated/pathological-typescript-api/models/PlayerLeft"
import { UpdatePlayersData } from "../../open-api/generated/pathological-typescript-api/models/UpdatePlayersData"
import { PlayerData } from "../../open-api/generated/pathological-typescript-api/models/PlayerData";
import { GameEnded } from "../../open-api/generated/pathological-typescript-api/models/GameEnded";
import { GameController } from "./controller";

const controller = new multiplayerController();
const singlePlayerController = new GameController();
const urlCreator = window.URL || window.webkitURL;

function resetDiv(div: HTMLElement) {
    div.innerHTML = "";
}

export function createMultiplayerGame() {
    initMultiplayerGame(controller.createGame, "Failed to create the game: ", "Successfully created the game")
}

export function joinMultiplayerGame() {
    initMultiplayerGame(
        controller.joinGame,
        "Failed to join game: ",
        "Successfully joined the game!"
    );
}


function initMultiplayerGame(controllerFunction: (gameId: string, playerName: string) => Promise<Response>,
    errorMessagePrefix: string, successfulMessage: string) {


    const form = document.getElementById("start-multiplayer-game-form") as HTMLFormElement;
    const formData = new FormData(form);

    if (!form.checkValidity()) {
        form.reportValidity();
    } else {
        const playerName = formData.get("player-name").toString();
        const lobbyId = formData.get("lobby-id").toString();
        const socket = preInitializeListener(lobbyId, playerName);
        controllerFunction(
            lobbyId,
            playerName
        ).then((response) => {
            const responseDiv = document.getElementById("multiplayer-game-init-error-response-div");
            resetDiv(responseDiv);
            if (response.status != 200) {

                showFailureMessage(response, responseDiv, errorMessagePrefix);
                socket.disconnect();

            } else {

                response.json()
                    .then((responseJson) => {
                        joinLobby();
                        updateLobby(responseJson["game_id"], responseJson);
                        bindButton(socket, lobbyId, playerName);
                    })

            }
        });
    }
}


function showFailureMessage(response: Response, responseDiv: HTMLElement, errorMessagePrefix: string) {
    response.json().then((responseJson) => {
        console.log(`Response JSON: ` + JSON.stringify(responseJson));
        responseDiv.innerText = errorMessagePrefix + responseJson["errorMessage"];
    });
}

function joinLobby() {
    showLobby();
    hideHtmlElement("start-multiplayer-game-div");
}

function preInitializeListener(gameId: string, playerId: string): Socket {
    const socket = io(hostApi, {
        "query": {
            "player_id": playerId,
            "game_id": gameId
        }
    });
    registerListener(
        socket,
        PlayerJoin.name,
        (eventData: PlayerJoin) => {
            if (gameId === eventData.game_id) {
                console.log("Received relevant player join event!");
                console.log("Updating lobby!");
                hideHtmlElement("start-multiplayer-game-div");
                updateLobby(gameId, eventData);
            } else {
                console.log("Received irrelevant player join event!");
            }
        }
    )
    registerListener(
        socket,
        PlayerLeft.name,
        (eventData: PlayerLeft) => {

            if (gameId === eventData.game_id) {
                console.log("Received relevant player left event!");
                console.log("Updating lobby!");
                hideHtmlElement("start-multiplayer-game-div");
                updateLobby(gameId, eventData);
            } else {
                console.log("Received irrelevant player join event!");
            }
        }
    )
    registerListener(
        socket,
        GameStarting.name,
        (eventData: GameStarting) => {
            console.log("Received game starting event...")
            document.getElementById("lobby-info-div").innerText = eventData.message;
        }
    )
    registerListener(
        socket,
        GameStarted.name,
        (evenData: GameStarted) => {
            console.log("Received game started event...");
            hideHtmlElement("multiplayer-lobby-div");
            showGameDiv();

            socket.emit(
                "SubmitAnswer", {
                "game_id": gameId,
                "player_id": playerId,
                "answer_to_previous": ""
            }
            )
        }
    )

    registerListener(
        socket,
        UpdatePlayersData.name,
        (eventData: UpdatePlayersData) => {
            if (eventData.game_id === gameId) {
                console.log(`Received relevant update players data event ${JSON.stringify(eventData)}`)
                let currOtherIndex = 0;
                eventData.connected_players.forEach((pData) => {
                    if (pData.player_id === playerId) {
                        updateThisPlayerDiv(socket, gameId, pData);
                    } else {
                        updateOtherPlayerDiv(currOtherIndex++, pData);
                    }
                })
            } else {
                console.log(`Irrelevant update players data event: ${eventData}`)
            }
        }
    )

    registerListener(socket,
        GameEnded.name,
        (eventData: GameEnded) => {
            hideHtmlElement("multiplayer-game-div");
            const resultDiv = document.getElementById("game-result-div")
            resultDiv.setAttribute("style", "display: block");
            
            eventData.players_ranked.forEach((player) => {
                const div = document.createElement("div");
                div.innerText = `${player.player_id}: ${player.current_score} points`
                resultDiv.appendChild(div);
            })


        }
    )


    return socket;
}

function updateLobby(gameId: string, hasAllPlayers: object) {
    const lobbyGameIdHeader = document.getElementById("lobby-game-id-header");
    lobbyGameIdHeader.innerText = gameId;

    const connectPlayersList = document.getElementById("connected-players-list");
    resetDiv(connectPlayersList);
    const allPlayers: Array<object> = hasAllPlayers["connected_players"];
    allPlayers.forEach((player) => {
        connectPlayersList.appendChild(buildPlayerListElement(player));
    })
}

function showLobby() {
    const lobbyDiv = document.getElementById("multiplayer-lobby-div");
    lobbyDiv.setAttribute("style", "display: block");
}

function buildPlayerListElement(player: object) {
    const newPlayerListElement = document.createElement("li");
    newPlayerListElement.innerText = player["player_id"];
    return newPlayerListElement;
}

function bindButton(socket: Socket, lobbyId: string, playerName: string) {
    document.getElementById("start-multiplayer-game-button").onclick = () => {
        socket.emit("StartGame", {
            "game_id": lobbyId,
            "player_id": playerName
        });
    };
}

function hideHtmlElement(elementId: string) {
    document.getElementById(elementId).setAttribute("style", "display: none");
}

function showGameDiv() {
    const gameDiv = document.getElementById("multiplayer-game-div");
    gameDiv.setAttribute("style", "display: block");
}

function registerListener<T>(socket: Socket, eventName: string, eventConsumer: (event: T) => void) {
    console.log(`Registering listener for ${eventName}`)
    socket.on(eventName,
        (event: T) => {
            eventConsumer(event)
        }
    );
}

function updateThisPlayerDiv(socket: Socket, gameId: string, pData: PlayerData) {
    singlePlayerController.getChallengeImage(pData.current_image_id).then((blob) => {
        const imageElement = document.getElementById("this-player-current-challenge-img") as HTMLImageElement
        imageElement.src = urlCreator.createObjectURL(blob);
    });

    document.getElementById("this-player-score-span").textContent = pData.current_score?.toString();
    const allOptionsDiv = document.getElementById("this-player-options");
    allOptionsDiv.innerHTML = "";
    pData.current_challenge_options.forEach((option) => {
        const thisOptionDiv = document.createElement("div");

        const optionButton = document.createElement("button");
        optionButton.classList.add("btn", "btn-danger", "w-25", "m-2");
        optionButton.innerText = option;
        optionButton.onclick = () => {

            socket.emit(
                "SubmitAnswer", {
                "game_id": gameId,
                "player_id": pData.player_id,
                "answer_to_previous": option
            }
            )

        }

        thisOptionDiv.appendChild(optionButton);

        allOptionsDiv.appendChild(thisOptionDiv);
    })

}
function updateOtherPlayerDiv(otherIndex: number, pData: PlayerData) {
    const enemyDiv = document.getElementById(`rival-placeholder-${otherIndex}`);
    enemyDiv.classList.add("text-center")

    resetDiv(enemyDiv);

    const enemyNameHeader = document.createElement("h6");
    enemyNameHeader.innerText = pData.player_id
    enemyDiv.appendChild(enemyNameHeader)

    const playerScoreElement = document.createElement("p");
    playerScoreElement.innerText = `Score: ${pData.current_score}`
    enemyDiv.appendChild(playerScoreElement);

    const imageDiv = document.createElement("img");
    imageDiv.classList.add("w-25")

    singlePlayerController.getChallengeImage(pData.current_image_id).then((blob) => {
        imageDiv.src = urlCreator.createObjectURL(blob);
    });

    enemyDiv.appendChild(imageDiv);

}

