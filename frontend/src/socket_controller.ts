import { Socket, io } from "socket.io-client";
import { hostApi } from "./config";


const CLIENT_JOIN_GAME = "client_join_game"
const NEW_PLAYER_JOINED = "notify_join_game";

function getNewPlayerJoinedEventId(gameId: string) {
    return `new_player_joined`
}

function getSuccessfulJoinEventId(gameId: string) {
    return `successful_join`
}

function getStartGameEventId(gameId: string) {
    return `start_game_${gameId}`;
}

export function sendJoinGameEvent(playerName: string, gameId: string) {

    const socket: Socket = io(hostApi);
    socket.connect();

    registerListeners(gameId, socket);
    handleUiElements();

    socket.emit(CLIENT_JOIN_GAME, {
        game_id: gameId,
        player_id: playerName
    })

}

function registerListeners(gameId: string, socket: Socket) {
    const successfulJoinEvent: string = getSuccessfulJoinEventId(gameId);

    console.log(`Registering listener for ${successfulJoinEvent}`)

    socket.on(successfulJoinEvent, (event_data: object) => {
        console.log("Recieved successful join event!");

        
        const gameId = event_data["game_id"];

        socket.on(getNewPlayerJoinedEventId(gameId), (event_data: object) => {
            console.log(`Recieved new player joined event ${JSON.stringify(event_data)}`)
            const listOfPlayers = document.getElementById("connected-players-list");
            const newPlayerListElement = document.createElement("li");
            newPlayerListElement.innerText = `Player with ID ${event_data['player_id']}}`;
            listOfPlayers.appendChild(newPlayerListElement);
        })

        socket.on(getStartGameEventId(gameId), (event_data: object) => {

        })

        // stopListening(socket, successfulJoinEvent);
    });
}

function stopListening(socket: Socket, eventName: string) {
    socket.on(eventName, () => {
    });
}
function handleUiElements() {
    const lobbyDiv = document.getElementById("mutliplayer-lobby-div");
    lobbyDiv.setAttribute("style", "display: block");
}

