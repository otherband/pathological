import { hostApi } from "./config";
const BASE_URL = hostApi.concat("/api/v1");

class GameController {
  async getPlayerId(): Promise<object> {
    return await (
      await fetch(BASE_URL.concat("/new-session-id"), {
        method: "POST",
      })
    ).json();
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
  ): Promise<Response> {
    return await fetch(BASE_URL.concat("/solve-challenge"), {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
      },
      body: JSON.stringify({
        player_id: playerId,
        challenge_id: challenge_key,
        answer: answer,
      }),
    });
  }

  async getScore(playerId: string): Promise<object> {
    return await (
      await fetch(BASE_URL.concat(`/score/${playerId}`), {
        method: "GET",
        headers: {
          "Content-Type": "application/json",
        },
      })
    ).json();
  }
}

export { GameController };
