import { Socket, io } from "socket.io-client";
import { hostApi } from "./config";
import { MutliplayerController } from "./multiplayer_controller";

const controller = new MutliplayerController();

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
                        updateLobby(responseJson["gameId"], responseJson);
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
    hideInitDiv();
}

function preInitializeListener(gameId: string, playerId: string): Socket {
    const socket = io(hostApi, {
        "query": {
            "player_id": playerId,
            "game_id": gameId
        }
    });
    


    socket.on("player_join_event", (eventData) => {

        if (gameId === eventData["game_id"]) {
            console.log("Recieved relevant player join event!");
            console.log("Updating lobby!");
            hideInitDiv();
            updateLobby(gameId, eventData);
        } else {
            console.log("Recieved irrelevant player join event!");
        }

    })

    socket.on("player_left_game", (eventData) => {

        if (gameId === eventData["game_id"]) {
            console.log("Recieved relevant player left event!");
            console.log("Updating lobby!");
            hideInitDiv();
            updateLobby(gameId, eventData);
        } else {
            console.log("Recieved irrelevant player join event!");
        }
    })

    return socket;
}

function updateLobby(gameId: string, hasAllPlayers: object) {
    showLobby();
    const connectPlayersList = document.getElementById("connected-players-list");
    resetDiv(connectPlayersList);
    const allPlayers: Array<string> = hasAllPlayers["connected_players"];
    allPlayers.forEach((playerId) => {
        connectPlayersList.appendChild(buildPlayerListElement(playerId));
    })
}

function showLobby() {
    const lobbyDiv = document.getElementById("mutliplayer-lobby-div");
    lobbyDiv.setAttribute("style", "display: block");
}

function buildPlayerListElement(playerId: string) {
    const newPlayerListElement = document.createElement("li");
    newPlayerListElement.innerText = `Player with ID ${playerId}`;
    return newPlayerListElement;
}


function hideInitDiv() {
    document.getElementById("start-mutliplayer-game-div").setAttribute("style", "display: none");
}

