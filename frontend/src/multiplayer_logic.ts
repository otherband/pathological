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
    hideHtmlElement("start-mutliplayer-game-div");
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
            hideHtmlElement("start-mutliplayer-game-div");
            updateLobby(gameId, eventData);
        } else {
            console.log("Recieved irrelevant player join event!");
        }

    })

    socket.on("player_left_game", (eventData) => {

        if (gameId === eventData["game_id"]) {
            console.log("Recieved relevant player left event!");
            console.log("Updating lobby!");
            hideHtmlElement("start-mutliplayer-game-div");
            updateLobby(gameId, eventData);
        } else {
            console.log("Recieved irrelevant player join event!");
        }
    })


    socket.on("game_starting", (eventData) => {
        console.log("Recieved game starting event...")
        updateLobbyInfoDiv(eventData);
    })

    socket.on("game_started", (eventData) => {
        console.log("Recieved game started event...");
        hideHtmlElement("mutliplayer-lobby-div");
        showGameDiv();
    })

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
    const lobbyDiv = document.getElementById("mutliplayer-lobby-div");
    lobbyDiv.setAttribute("style", "display: block");
}

function buildPlayerListElement(player: object) {
    const newPlayerListElement = document.createElement("li");
    newPlayerListElement.innerText = `Player with ID ${player["player_id"]}`;
    return newPlayerListElement;
}

function bindButton(socket: Socket, lobbyId: string, playerName: string) {
    document.getElementById("start-multiplayer-game-button").onclick = () => {
        socket.emit("start_game", {
            "game_id": lobbyId,
            "player_id": playerName
        });
    };
}

function hideHtmlElement(elementId: string) {
    document.getElementById(elementId).setAttribute("style", "display: none");
}

function updateLobbyInfoDiv(eventData: object) {
    document.getElementById("lobby-info-div").innerText = eventData["message"];
}

function showGameDiv() {
    const gameDiv = document.getElementById("multiplayer-game-div");
    gameDiv.setAttribute("style", "display: block");

}
