export function SinglePlayerPage() {
  return (
    <body>
      <div id="solo-page-background-img-div"></div>
      <div id="header-div" className="text-center p-3">
        <h3>Pathological Single-Player</h3>
      </div>

      <div className="p-3 m-3">
        <div
          className="text-center"
          id="current-challenge-div"
          // style="display: none"
        ></div>
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
            Remaining time: <span id="game-timer-seconds"> 10 </span>s
          </div>
        </div>
      </div>
    </body>
  );
}
