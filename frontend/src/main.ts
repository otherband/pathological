import { GameController } from "./controller";
const gameController = new GameController();
let playerId;

async function startGame() {
  playerId = await gameController.getPlayerId();
  document
    .getElementById("start-game-div")
    .setAttribute("style", "display: none");
  console.log("hidden");
  startNextChallenge();
  countDown();
}

function startNextChallenge() {
  const challengeDiv: HTMLDivElement = resetChallengeDiv();
  gameController.getChallenge(playerId).then((challenge) => {
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
    gameController.submitAnswer(playerId, challenge, answerText);
    startNextChallenge();
  };
  button.textContent = "Answer!";
  return button;
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
  scoreDiv.textContent = await gameController.getScore(playerId);
}

function sleep(ms: number) {
  return new Promise((resolve) => setTimeout(resolve, ms));
}

export { startGame };
