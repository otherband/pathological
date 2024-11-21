import { useEffect, useRef, useState } from "react";
import { GameController } from "../Controller";
import { Challenge } from "../SinglePlayerTypes";

const gameController = new GameController();
const urlCreator = window.URL || window.webkitURL;
const INITIAL_REMAINING_SECONDS = 10;

interface ChallengeWithParsedImage extends Challenge {
  parsedImageBlob: Blob;
}

function ChallengeDiv(props: {
  playerId: string;
  challenge: ChallengeWithParsedImage;
  setCurrentChallenge: (challenge: ChallengeWithParsedImage) => void;
}) {
  const imageUrl = urlCreator.createObjectURL(props.challenge.parsedImageBlob);
  return (
    <>
      <div id="current-challenge-div" style={{ display: "block" }}>
        <div>
          <img className="challenge-img" alt="Challenge" src={imageUrl} />
        </div>
        {props.challenge.possible_answers.map((answer) => {
          return (
            <div>
              <button
                onClick={() => {
                  gameController.submitAnswer(props.playerId, props.challenge.challenge_id, answer);
                  gameController.getChallenge(props.playerId).then((response) => {
                    gameController.getChallengeImage(response.image_id).then((imageBlob) => {
                      props.setCurrentChallenge({
                        challenge_id: response.challenge_id,
                        image_id: response.image_id,
                        possible_answers: response.possible_answers,
                        parsedImageBlob: imageBlob,
                      });
                    });
                  });
                }}
                className="btn btn-danger w-25 m-2"
              >
                {answer}
              </button>
            </div>
          );
        })}
      </div>
    </>
  );
}

export function SinglePlayerPage() {
  var playerId = useRef("");

  const [currentChallenge, setCurrentChallenge] = useState<ChallengeWithParsedImage | undefined>();

  const [remainingSeconds, setRemainingSeconds] = useState(INITIAL_REMAINING_SECONDS);

  const [playerScore, setPlayerScore] = useState<number | undefined>();

  const gameDone = remainingSeconds === 0;

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

        gameController.getChallenge(response.player_id).then((response) => {
          gameController.getChallengeImage(response.image_id).then((imageBlob) => {
            setCurrentChallenge({
              challenge_id: response.challenge_id,
              image_id: response.image_id,
              possible_answers: response.possible_answers,
              parsedImageBlob: imageBlob,
            });
          });
        });
      }
    });
  }, []);

  useEffect(() => {
    if (isReady()) {
      if (remainingSeconds === 0) {
        gameController.getScore(playerId.current).then((playerScore) => {
          setPlayerScore(playerScore.player_score);
        });
        return;
      }

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
        <div className="text-center" id="current-challenge-div">
          {!gameDone && currentChallenge !== undefined && (
            <ChallengeDiv
              playerId={playerId.current}
              setCurrentChallenge={setCurrentChallenge}
              challenge={currentChallenge}
            />
          )}
        </div>
        {gameDone && <div id="player-score-div"> {`Player score: ${playerScore}`} </div>}
        <div
          className="text-center"
          style={{
            display: "flex",
            justifyContent: "center",
          }}
        >
          <div id="game-timer-div" className="text-center border w-25 p-3 display-4">
            Remaining time:
            <span id="game-timer-seconds"> {remainingSeconds} </span>s
          </div>
        </div>
      </div>
    </body>
  );
}
