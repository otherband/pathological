import { hostApi } from "./config";
const BASE_URL = hostApi.concat("/api/v1");
var playerId;

async function startGame() {
  playerId = await getPlayerId();
  document
    .getElementById("start-game-div")
    .setAttribute("style", "display: none");
  console.log("hidden");

  getChallenge().then((challenge) => {
    const challengeDiv: HTMLDivElement = document.getElementById(
      "current-challenge-div"
    ) as HTMLDivElement;
    challengeDiv.setAttribute("style", "display: block");
    challengeDiv.appendChild(createChallengeChoicesDiv(challenge));
  });
}

function createChallengeChoicesDiv(challenge: object): any {
  const div: HTMLElement = document.createElement("div");
  const possibleAnswers: Array<string> = challenge["possible_answers"]
  possibleAnswers.forEach((answer) => {
    const answerDiv = document.createElement("div");
    answerDiv.textContent = answer;
    div.appendChild(answerDiv);
  })
  return div;
}

function createAnswerDiv(challenge: string, answerText: string) {
  const div = document.createElement("div");
  div.textContent = answerText;
  div.appendChild(submitAnswerButton(challenge, answerText));
  return div;
}
function submitAnswerButton(challenge: string, answerText: string): any {
  const button: HTMLButtonElement = document.createElement("button");
  button.onclick = () => submitAnswer(challenge, answerText);
  button.textContent = "Answer!";
  return button;
}

async function getPlayerId(): Promise<string> {
  return await (
    await fetch(BASE_URL.concat("/new-session-id"), {
      method: "POST",
    })
  ).text();
}

async function getChallenge(): Promise<object> {
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

async function submitAnswer(challenge_key, answer): Promise<string> {
  return await (
    await fetch(BASE_URL.concat("/request-challenge"), {
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

export { startGame };
