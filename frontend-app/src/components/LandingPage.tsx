import { ActivePage } from "../ActivePage";

export function LandingPage(props: {
  setActivePage: (activePage: ActivePage) => void;
}) {
  return (
    <>
      <div className="text-center p-2">
        <h1 className="display-4 font-monospace">Pathological!</h1>
        <h4>
          Pathological is a game where doctors compete over image classification
          tasks. <br />
          The winner gets replaced by AI last.
        </h4>
      </div>

      <div className="text-center m-3" id="start-game-div">
        <button
          type="button"
          className="btn btn-danger w-25"
          onClick={() => props.setActivePage(ActivePage.SINGLE_PLAYER)}
        >
          Start Game!
        </button>
        <button
          type="button"
          className="btn btn-danger w-25"
          onClick={() => props.setActivePage(ActivePage.MULTIPLAYER)}
        >
          Start multiplayer game!
        </button>
      </div>
    </>
  );
}
