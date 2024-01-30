import { hostApi } from "./config";
const BASE_URL = hostApi.concat("/api/v1");

class GameController {
  async getPlayerId(): Promise<string> {
    return await (
      await fetch(BASE_URL.concat("/new-session-id"), {
        method: "POST",
      })
    ).text();
  }

  async getChallengeImage(imageId: string): Promise<Blob> {
    return await (
      await fetch(BASE_URL.concat(`/image/${imageId}`), {
        method: "GET",
      })
    ).blob();
  }

  async getChallenge(playerId: string): Promise<object> {
    return await (
      await fetch(BASE_URL.concat("/request-challenge"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          player_id: playerId,
        }),
      })
    ).json();
  }

  async submitAnswer(
    playerId: string,
    challenge_key: string,
    answer: string
  ): Promise<string> {
    return await (
      await fetch(BASE_URL.concat("/solve-challenge"), {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({
          player_id: playerId,
          challenge_key: challenge_key,
          answer: answer,
        }),
      })
    ).text();
  }

  async getScore(playerId: string): Promise<string> {
    return await (
      await fetch(BASE_URL.concat(`/score/${playerId}`), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
    ).text();
  }
}

export { GameController };
