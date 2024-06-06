import { GameController } from "./controller";
import { createMultiplayerGame, joinMultiplayerGame } from "./multiplayer_logic";
import { sendJoinGameEvent } from "./socket_controller";
const gameController: GameController = new GameController();
let playerId: string;
const urlCreator = window.URL || window.webkitURL;

async function startGame() {
  playerId = (await gameController.getPlayerId())['player_id'];
  console.log(`Received playerId ${playerId}`)
  startNextChallenge();
  countDown();
}

function startNextChallenge() {
  const challengeDiv: HTMLDivElement = resetChallengeDiv();
  gameController.getChallenge(playerId).then((challenge) => {
    challengeDiv.setAttribute("style", "display: block");
    challengeDiv.appendChild(createChallengeImageDiv(challenge));
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

function createChallengeChoicesDiv(challenge: object): HTMLDivElement {
  const div: HTMLDivElement = document.createElement("div");
  const possibleAnswers: Array<string> = challenge["possible_answers"];
  possibleAnswers.forEach((answer) => {
    div.appendChild(createAnswerDiv(challenge["challenge_id"], answer));
  });
  return div;
}

function createAnswerDiv(
  challenge: string,
  answerText: string
): HTMLDivElement {
  const div = document.createElement("div");
  div.appendChild(submitAnswerButton(challenge, answerText));
  return div;
}

function submitAnswerButton(
  challenge: string,
  answerText: string
): HTMLButtonElement {
  const button: HTMLButtonElement = document.createElement("button");
  button.onclick = () => {
    gameController.submitAnswer(playerId, challenge, answerText);
    startNextChallenge();
  };
  button.textContent = answerText;
  button.classList.add("btn", "btn-danger", "w-25", "m-2");
  return button;
}

function textDiv(answerText: string): HTMLDivElement {
  const textDiv = document.createElement("div");
  textDiv.textContent = answerText;
  return textDiv;
}

function createChallengeImageDiv(challenge: object): HTMLDivElement {
  const imageDiv = document.createElement("div");
  const imageElement: HTMLImageElement = document.createElement("img");
  gameController.getChallengeImage(challenge["image_id"]).then((blob) => {
    imageElement.src = urlCreator.createObjectURL(blob);
    imageElement.classList.add("challenge-img");
  });
  imageDiv.appendChild(imageElement);
  return imageDiv;
}

function countDown() {
  const timerElement = document.getElementById("game-timer-seconds");
  const remainingSeconds: number =
    Number.parseInt(timerElement.textContent) || 15;
  if (remainingSeconds - 1 <= 0) {
    timerElement.textContent = "ZERO ";
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
  scoreDiv.classList.add("p-3", "display-2", "text-center");
  const playerScoreResponse = await gameController.getScore(playerId);
  console.log("Fetched response: " + JSON.stringify(playerScoreResponse));
  const score = playerScoreResponse["player_score"] as number;
  scoreDiv.appendChild(textDiv(`Player score: ${score}`));
}

function sleep(ms: number): Promise<void> {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

function showStartMultiplayerDiv() {
  document.getElementById("start-mutliplayer-game-div").setAttribute("style", "display: block")
}

export { startGame, createMultiplayerGame, joinMultiplayerGame, showStartMultiplayerDiv };
