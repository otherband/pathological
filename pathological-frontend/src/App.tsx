import React, { useState } from "react";
import { GameMode } from "./GameMode";
import "./styles.css";
import { SinglePlayerPage } from "./Pages/SinglePlayer";
import { MultiplayerPage } from "./Pages/Multiplayer";

function TopHalfBackground() {
  return (
    <div
      id="solo-page-background-img-div"
      style={{
        height: "50vh",
        marginTop: "50vh",
      }}
    ></div>
  );
}

function BottomHalfBackground() {
  return (
    <div id="multi-page-background-img-div" style={{ height: "50vh" }}></div>
  );
}

function Intro() {
  return (
    <div className="text-center p-3">
      <h1 className="display-4 font-monospace">Pathological!</h1>
      <h4>
        Pathological is a game where doctors compete over image classification
        tasks. <br />
        The winner gets replaced by AI last.
      </h4>
    </div>
  );
}

function SelectGameModeButton(props: {
  setGameMode: () => void;
  buttonText: string;
  className: string;
}) {
  return (
    <div
      className={"start-game-btn btn btn-danger w-25 " + props.className}
      onClick={(event) => {
        event.stopPropagation();
        props.setGameMode();
      }}
    >
      <div
        style={{
          position: "absolute",
        }}
      >
        <strong>{props.buttonText}</strong>
      </div>
    </div>
  );
}

function SelectGameMode(props: { setGameMode: (mode: GameMode) => void }) {
  return (
    <div className="text-center m-5 p-3" id="start-game-div">
      <SelectGameModeButton
        setGameMode={() => {
          props.setGameMode(GameMode.SINGLE_PLAYER);
        }}
        buttonText={"Start single-player Game 🔬"}
        className="start-game-solo"
      />
      <SelectGameModeButton
        setGameMode={() => {
          props.setGameMode(GameMode.MULTIPLAYER);
        }}
        buttonText={"Start multiplayer game ⚔️"}
        className="start-game-battle"
      />
    </div>
  );
}

function LandingContent(props: { setGameMode: (mode: GameMode) => void }) {
  return (
    <>
      <TopHalfBackground />
      <BottomHalfBackground />
      <Intro />
      <SelectGameMode setGameMode={props.setGameMode} />
    </>
  );
}

function App() {
  const [gameMode, setGameMode] = useState(GameMode.LANDING);
  return (
    <div className="App">
      {GameMode.LANDING === gameMode && (
        <LandingContent setGameMode={setGameMode} />
      )}
      {GameMode.SINGLE_PLAYER === gameMode && <SinglePlayerPage />}
      {GameMode.MULTIPLAYER === gameMode && <MultiplayerPage />}
    </div>
  );
}

export default App;
