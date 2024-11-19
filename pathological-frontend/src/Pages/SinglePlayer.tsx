import { useEffect, useRef, useState } from "react";
import { GameController } from "../Controller";
import { Challenge } from "../SinglePlayerTypes";

const gameController = new GameController();
const urlCreator = window.URL || window.webkitURL;
const INITIAL_REMAINING_SECONDS = 10;

interface ChallengeWithParsedImage extends Challenge {
  parsedImageBlob: Blob;
}

function ChallengeDiv(props: { challenge: ChallengeWithParsedImage }) {
  const imageUrl = urlCreator.createObjectURL(props.challenge.parsedImageBlob);
  return (
    <>
      <div id="current-challenge-div" style={{ display: "block" }}>
        <div>
          <img alt="Challenge" src={imageUrl} />
        </div>
        {props.challenge.possible_answers.map((answer) => {
          return (
            <div>
              <button className="btn btn-danger w-25 m-2">{answer}</button>
            </div>
          );
        })}
      </div>
    </>
  );
}

export function SinglePlayerPage() {
  var playerId = useRef("");

  const [currentChallenge, setCurrentChallenge] = useState<
    ChallengeWithParsedImage | undefined
  >();

  const [remainingSeconds, setRemainingSeconds] = useState(
    INITIAL_REMAINING_SECONDS
  );

  const gameDone = remainingSeconds === 0;

  function isReady() {
    return playerId.current !== "";
  }

  // gameController.getChallengeImage(challenge["image_id"]).then((blob) => {
  //   imageElement.src = urlCreator.createObjectURL(blob);
  //   imageElement.classList.add("challenge-img");
  // });

  useEffect(() => {
    gameController.getPlayerId().then((response) => {
      playerId.current = response.player_id;
      if (isReady()) {
        setTimeout(() => {
          setRemainingSeconds(INITIAL_REMAINING_SECONDS - 1);
        }, 1000);

        gameController.getChallenge(response.player_id).then((response) => {
          gameController
            .getChallengeImage(response.image_id)
            .then((imageBlob) => {
              setCurrentChallenge({
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
          {currentChallenge !== undefined && (
            <ChallengeDiv challenge={currentChallenge} />
          )}
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
