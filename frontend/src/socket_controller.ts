import { Socket, io } from "socket.io-client";
import { hostApi } from "./config";


const CLIENT_JOIN_GAME = "client_join_game"
const NEW_PLAYER_JOINED = "new_player_joined";
const SUCCESSFUL_JOIN = "successful_join";
const LOBBY_DIV = "mutliplayer-lobby-div";


export function sendJoinGameEvent(playerName: string, gameId: string) {

    const socket: Socket = io(hostApi);
    socket.connect();

    registerListeners(gameId, socket);
    showLobbyDiv();

    socket.emit(CLIENT_JOIN_GAME, {
        game_id: gameId,
        player_id: playerName
    })

}

function registerListeners(gameId: string, socket: Socket) {

    socket.once(SUCCESSFUL_JOIN, (event_data: object) => {
        console.log("Recieved successful join event!");
        const gameId = event_data["game_id"];
        registerNewPlayerListener(socket, gameId);
    });
}

function registerNewPlayerListener(socket, gameId: any) {
    socket.on(NEW_PLAYER_JOINED, (event_data: object) => {
        console.log("Reieved new player joined event!");
        if (event_data["game_id"] == gameId) {
            console.log("Game ID matches!");
            const playersList: Array<string> = event_data["all_players"];
            playersList.forEach(player => {
                const listOfPlayers = document.getElementById("connected-players-list");
                resetInnerContent(listOfPlayers);
                listOfPlayers.appendChild(buildPlayerListElement(event_data));
            });
        }
    });
}

function buildPlayerListElement(event_data: object) {
    const newPlayerListElement = document.createElement("li");
    newPlayerListElement.innerText = `Player with ID ${event_data['player_id']}}`;
    return newPlayerListElement;
}

function resetInnerContent(htmlElement: HTMLElement) {
    htmlElement.innerHTML = "";
}

function showLobbyDiv() {
    const lobbyDiv = document.getElementById(LOBBY_DIV);
    lobbyDiv.setAttribute("style", "display: block");
}

