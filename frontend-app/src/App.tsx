import React, { useState } from "react";
import { ActivePage } from "./ActivePage";
import { MultiplayerPage } from "./components/MultiplayerPage";
import { SinglePlayerPage } from "./components/SinglePlayerPage";
import { LandingPage } from "./components/LandingPage";

function App() {
  const [activePage, setActivePage] = useState(ActivePage.LANDING);
  return (
    <div className="App">
      {activePage === ActivePage.LANDING && (
        <LandingPage setActivePage={setActivePage} />
      )}
      {activePage === ActivePage.SINGLE_PLAYER && <SinglePlayerPage />}
      {activePage === ActivePage.MULTIPLAYER && <MultiplayerPage />}
    </div>
  );
}

export default App;
