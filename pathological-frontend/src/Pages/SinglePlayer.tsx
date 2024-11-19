import { useCallback, useEffect, useRef, useState } from "react";
import { GameController } from "../Controller";

const gameController = new GameController();
const INITIAL_REMAINING_SECONDS = 10;

export function SinglePlayerPage() {
  var playerId = useRef("");

  const [currentChallenge, setCurrentChallenge] = useState();

  const [remainingSeconds, setRemainingSeconds] = useState(
    INITIAL_REMAINING_SECONDS
  );

  function isReady() {
    return playerId.current !== "";
  }

  useEffect(() => {
    gameController.getPlayerId().then((response) => {
      playerId.current = response.player_id;
      if (isReady()) {
        setTimeout(() => {
          setRemainingSeconds(INITIAL_REMAINING_SECONDS - 1);
        }, 1000);
      }
    });
  }, []);

  useEffect(() => {
    if (isReady()) {
      setTimeout(() => {
        setRemainingSeconds((remaining) => remaining - 1);
      }, 1000);
    }
  }, [remainingSeconds]);

  return (
    <body>
      <div id="header-div" className="text-center p-3">
        <h3>Pathological Single-Player</h3>
      </div>
      <div className="p-3 m-3">
        <div className="text-center" id="current-challenge-div"></div>
        <div id="player-score-div"></div>

        <div
          className="text-center"
          style={{
            display: "flex",
            justifyContent: "center",
          }}
        >
          <div
            id="game-timer-div"
            className="text-center border w-25 p-3 display-4"
          >
            Remaining time:
            <span id="game-timer-seconds"> {remainingSeconds} </span>s
          </div>
        </div>
      </div>
    </body>
  );
}
