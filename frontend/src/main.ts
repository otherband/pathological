import { hostApi } from "./config";
const BASE_URL = hostApi.concat("/api/v1");
let playerId;

async function startGame() {
  playerId = await getPlayerId();
  document
    .getElementById("start-game-div")
    .setAttribute("style", "display: none");
  console.log("hidden");
  startNextChallenge();
  countDown();
}

function startNextChallenge() {
  const challengeDiv: HTMLDivElement = resetChallengeDiv();
  getChallenge().then((challenge) => {
    challengeDiv.setAttribute("style", "display: block");
    challengeDiv.appendChild(createChallengeChoicesDiv(challenge));
  });
}

function resetChallengeDiv() {
  const challengeDiv: HTMLDivElement = document.getElementById(
    "current-challenge-div"
  ) as HTMLDivElement;
  challengeDiv.innerHTML = "";
  return challengeDiv;
}

function createChallengeChoicesDiv(challenge: object): any {
  const div: HTMLElement = document.createElement("div");
  const possibleAnswers: Array<string> = challenge["possible_answers"];
  possibleAnswers.forEach((answer) => {
    div.appendChild(createAnswerDiv(challenge["challenge_id"], answer));
  });
  return div;
}

function createAnswerDiv(challenge: string, answerText: string) {
  const div = document.createElement("div");
  div.appendChild(textDiv(answerText));
  div.appendChild(submitAnswerButton(challenge, answerText));
  return div;
}
function submitAnswerButton(challenge: string, answerText: string): any {
  const button: HTMLButtonElement = document.createElement("button");
  button.onclick = () => {
    submitAnswer(challenge, answerText);
    startNextChallenge();
  };
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

function textDiv(answerText: string): any {
  const textDiv = document.createElement("div");
  textDiv.textContent = answerText;
  return textDiv;
}

function countDown() {
  const timerElement = document.getElementById("game-timer-seconds");
  const remainingSeconds: number =
    Number.parseInt(timerElement.textContent) || 15;
  if (remainingSeconds - 1 <= 0) {
    console.log("Game has ended");
    document
      .getElementById("current-challenge-div")
      .setAttribute("style", "display: none");
    showScore();
  } else {
    timerElement.textContent = (remainingSeconds - 1).toString();
    sleep(1000).then(() => countDown());
  }

}
async function showScore() {
  const scoreDiv = document.getElementById("player-score-div");
  scoreDiv.textContent = await getScore();
}

function sleep(ms) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

async function getScore(): Promise<string> {
  return await (
    await fetch(BASE_URL.concat(`/score/${playerId}`), {
      method: "GET",
      headers: {
        "Content-Type": "application/json",
      },
    })
  ).text();
}

export { startGame };
