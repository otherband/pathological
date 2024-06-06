import { hostApi } from "./config";

const BASE_URL = hostApi.concat("/api/v1");

class MutliplayerController {
    async createGame(gameId: string, playerId: string) {
        return await (
            await fetch(BASE_URL.concat("/multiplayer/game"), {
                method: "POST",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    player_id: playerId,
                    game_id: gameId
                }),
            })
        ).json();
    }

    async joinGame(gameId: string, playerId: string) {
        return await (
            await fetch(BASE_URL.concat("/multiplayer/game/join"), {
                method: "PUT",
                headers: {
                    "Content-Type": "application/json",
                },
                body: JSON.stringify({
                    player_id: playerId,
                    game_id: gameId
                }),
            })
        ).json();
    }

}