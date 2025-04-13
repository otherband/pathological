import { useState } from "react";
import { multiplayerController } from "../multiplayer_controller";
import { GameController } from "../Controller";

const controller = new multiplayerController();
const PLAYER_NAME_INPUT = "multiplayer-player-name-input";
const GAME_NAME_INPUT = "multiplayer-game-name-input";
const FORM_ID = "start-multiplayer-game-form";
const playerNameField = "player-name";
const lobbyIdField = "lobby-id";

enum GameState {
  CREATION,
  LOBBY,
  STARTED,
  ENDED,
}

function StartGameDiv(props: { setGameState: (gameState: GameState) => void }) {
  const [startGameError, setStartGameError] = useState<undefined | string>();

  function startGame(controllerFunction: (gameName: string, playerName: string) => Promise<Response>) {
    const form = document.getElementById(FORM_ID) as HTMLFormElement;
    const formValid = form.checkValidity();
    if (!formValid) {
      form.reportValidity();
    } else {
      const formData = new FormData(form);
      const playerName = formData.get(playerNameField) as string;
      const gameName = formData.get(lobbyIdField) as string;
      controllerFunction(gameName, playerName).then((res) => {
        if (res.status !== 200) {
          res.json().then((resJson) => {
            setStartGameError("Failed to create game: " + resJson["message"]);
          });
        } else {
          props.setGameState(GameState.LOBBY);
        }
      });
    }
  }

  return (
    <div id="start-multiplayer-game-div" className="text-center p-5 w-50 container">
      <form id={FORM_ID} className="form-control p-3 m-3">
        <div className="w-50 container">
          <input name={playerNameField} className="form-control m-1" id={PLAYER_NAME_INPUT} type="text" required />
          <label className="form-label" htmlFor={PLAYER_NAME_INPUT}>
            Player name
          </label>
        </div>
        <div className="w-50 container">
          <input name={lobbyIdField} className="form-control m-1" id={GAME_NAME_INPUT} type="text" required />
          <label className="form-label" htmlFor={GAME_NAME_INPUT}>
            Lobby ID
          </label>
        </div>

        <br />
        <button
          onClick={() => {
            startGame(controller.createGame);
          }}
          className="btn btn-danger m-2"
          type="button"
        >
          Start multiplayer game
        </button>
        <button
          onClick={() => {
            startGame(controller.joinGame);
          }}
          className="btn btn-danger m-2"
          type="button"
        >
          Join multiplayer game
        </button>
      </form>

      {startGameError && <div id="multiplayer-game-init-error-response-div">{startGameError}</div>}
    </div>
  );
}

function MultiplayerGameDiv() {
  return (
    <div id="multiplayer-game-div">
      <div className="container">
        <div className="row">
          <div className="col">
            <div id="rival-placeholder-0"></div>
          </div>
          <div className="col"></div>
          <div className="col">
            <div id="rival-placeholder-1"></div>
          </div>
        </div>
        <div className="row">
          <div className="col"></div>
          <div className="col col-lg-10">
            <div id="this-player-div" className="text-center">
              <h4>
                Score: <span id="this-player-score-span">0</span> | Remaining time:{" "}
                <span id="remaining-time-span"></span>
              </h4>
              <div className="text-center" id="current-challenge-div">
                <img src="path1.jpeg" alt="Current challenge" id="this-player-current-challenge-img" className="w-50" />
              </div>
              <div id="this-player-options">
                <div>
                  <button className="btn btn-danger w-25 m-2">Option A</button>
                </div>
                <div>
                  <button className="btn btn-danger w-25 m-2">Option B</button>
                </div>
                <div>
                  <button className="btn btn-danger w-25 m-2">Option C</button>
                </div>
              </div>
            </div>
          </div>
          <div className="col"></div>
        </div>
        <div className="row">
          <div className="col">
            <div id="rival-placeholder-2"></div>
          </div>
          <div className="col"></div>
          <div className="col">
            <div id="rival-placeholder-3"></div>
          </div>
        </div>
      </div>
    </div>
  );
}

function GameResultsDiv() {
  return (
    <div id="game-result-div" className="text-center">
      <div className="add-results-div">
        <h6>Results</h6>
      </div>
    </div>
  );
}

function MultiplayerLobbyDiv() {
  return (
    <div className="container w-50 justify-content-center" id="multiplayer-lobby-div">
      <div className="border p-5">
        <div className="text-lg-center">
          <h3 id="lobby-game-id-header">SOMETHING</h3>
        </div>
        <h4>Connected players</h4>
        <ul id="connected-players-list"></ul>
        <div id="lobby-info-div" className="border p-4 m-3"></div>
        <button id="start-multiplayer-game-button" className="btn btn-danger m-2" type="button">
          Start multiplayer game
        </button>
      </div>
    </div>
  );
}

export function MultiplayerPage() {
  const [gameState, setGameState] = useState(GameState.CREATION);

  return (
    <>
      <div id="multi-page-background-img-div"></div>
      <div id="header-div" className="text-center p-3">
        <h3>Pathological Multiplayer</h3>
      </div>
      {gameState === GameState.CREATION && <StartGameDiv setGameState={setGameState} />}
      {gameState === GameState.LOBBY && <MultiplayerLobbyDiv />}
      {gameState === GameState.STARTED && <MultiplayerGameDiv />}
      {gameState === GameState.ENDED && <GameResultsDiv />}
    </>
  );
}
