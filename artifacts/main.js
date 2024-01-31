/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/define property getters */
/******/ 	(() => {
/******/ 		// define getter functions for harmony exports
/******/ 		__webpack_require__.d = (exports, definition) => {
/******/ 			for(var key in definition) {
/******/ 				if(__webpack_require__.o(definition, key) && !__webpack_require__.o(exports, key)) {
/******/ 					Object.defineProperty(exports, key, { enumerable: true, get: definition[key] });
/******/ 				}
/******/ 			}
/******/ 		};
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/hasOwnProperty shorthand */
/******/ 	(() => {
/******/ 		__webpack_require__.o = (obj, prop) => (Object.prototype.hasOwnProperty.call(obj, prop))
/******/ 	})();
/******/ 	
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
var __webpack_exports__ = {};
// ESM COMPAT FLAG
__webpack_require__.r(__webpack_exports__);

// EXPORTS
__webpack_require__.d(__webpack_exports__, {
  startGame: () => (/* binding */ startGame)
});

;// CONCATENATED MODULE: ./src/config.ts
var hostApi = "http://localhost:5000";


;// CONCATENATED MODULE: ./src/controller.ts
var __awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var __generator = (undefined && undefined.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};

var BASE_URL = hostApi.concat("/api/v1");
var GameController = /** @class */ (function () {
    function GameController() {
    }
    GameController.prototype.getPlayerId = function () {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch(BASE_URL.concat("/new-session-id"), {
                            method: "POST",
                        })];
                    case 1: return [4 /*yield*/, (_a.sent()).json()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    GameController.prototype.getChallengeImage = function (imageId) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch(BASE_URL.concat("/image/".concat(imageId)), {
                            method: "GET",
                        })];
                    case 1: return [4 /*yield*/, (_a.sent()).blob()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    GameController.prototype.getChallenge = function (playerId) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch(BASE_URL.concat("/request-challenge"), {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                player_id: playerId,
                            }),
                        })];
                    case 1: return [4 /*yield*/, (_a.sent()).json()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    GameController.prototype.submitAnswer = function (playerId, challenge_key, answer) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch(BASE_URL.concat("/solve-challenge"), {
                            method: "POST",
                            headers: {
                                "Content-Type": "application/json",
                            },
                            body: JSON.stringify({
                                player_id: playerId,
                                challenge_id: challenge_key,
                                answer: answer,
                            }),
                        })];
                    case 1: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    GameController.prototype.getScore = function (playerId) {
        return __awaiter(this, void 0, void 0, function () {
            return __generator(this, function (_a) {
                switch (_a.label) {
                    case 0: return [4 /*yield*/, fetch(BASE_URL.concat("/score/".concat(playerId)), {
                            method: "GET",
                            headers: {
                                "Content-Type": "application/json",
                            },
                        })];
                    case 1: return [4 /*yield*/, (_a.sent()).json()];
                    case 2: return [2 /*return*/, _a.sent()];
                }
            });
        });
    };
    return GameController;
}());


;// CONCATENATED MODULE: ./src/main.ts
var main_awaiter = (undefined && undefined.__awaiter) || function (thisArg, _arguments, P, generator) {
    function adopt(value) { return value instanceof P ? value : new P(function (resolve) { resolve(value); }); }
    return new (P || (P = Promise))(function (resolve, reject) {
        function fulfilled(value) { try { step(generator.next(value)); } catch (e) { reject(e); } }
        function rejected(value) { try { step(generator["throw"](value)); } catch (e) { reject(e); } }
        function step(result) { result.done ? resolve(result.value) : adopt(result.value).then(fulfilled, rejected); }
        step((generator = generator.apply(thisArg, _arguments || [])).next());
    });
};
var main_generator = (undefined && undefined.__generator) || function (thisArg, body) {
    var _ = { label: 0, sent: function() { if (t[0] & 1) throw t[1]; return t[1]; }, trys: [], ops: [] }, f, y, t, g;
    return g = { next: verb(0), "throw": verb(1), "return": verb(2) }, typeof Symbol === "function" && (g[Symbol.iterator] = function() { return this; }), g;
    function verb(n) { return function (v) { return step([n, v]); }; }
    function step(op) {
        if (f) throw new TypeError("Generator is already executing.");
        while (g && (g = 0, op[0] && (_ = 0)), _) try {
            if (f = 1, y && (t = op[0] & 2 ? y["return"] : op[0] ? y["throw"] || ((t = y["return"]) && t.call(y), 0) : y.next) && !(t = t.call(y, op[1])).done) return t;
            if (y = 0, t) op = [op[0] & 2, t.value];
            switch (op[0]) {
                case 0: case 1: t = op; break;
                case 4: _.label++; return { value: op[1], done: false };
                case 5: _.label++; y = op[1]; op = [0]; continue;
                case 7: op = _.ops.pop(); _.trys.pop(); continue;
                default:
                    if (!(t = _.trys, t = t.length > 0 && t[t.length - 1]) && (op[0] === 6 || op[0] === 2)) { _ = 0; continue; }
                    if (op[0] === 3 && (!t || (op[1] > t[0] && op[1] < t[3]))) { _.label = op[1]; break; }
                    if (op[0] === 6 && _.label < t[1]) { _.label = t[1]; t = op; break; }
                    if (t && _.label < t[2]) { _.label = t[2]; _.ops.push(op); break; }
                    if (t[2]) _.ops.pop();
                    _.trys.pop(); continue;
            }
            op = body.call(thisArg, _);
        } catch (e) { op = [6, e]; y = 0; } finally { f = t = 0; }
        if (op[0] & 5) throw op[1]; return { value: op[0] ? op[1] : void 0, done: true };
    }
};

var gameController = new GameController();
var playerId;
var urlCreator = window.URL || window.webkitURL;
function startGame() {
    return main_awaiter(this, void 0, void 0, function () {
        return main_generator(this, function (_a) {
            switch (_a.label) {
                case 0: return [4 /*yield*/, gameController.getPlayerId()];
                case 1:
                    playerId = (_a.sent())['player_id'];
                    console.log("Received playerId ".concat(playerId));
                    document
                        .getElementById("start-game-div")
                        .setAttribute("style", "display: none");
                    console.log("hidden");
                    startNextChallenge();
                    countDown();
                    return [2 /*return*/];
            }
        });
    });
}
function startNextChallenge() {
    var challengeDiv = resetChallengeDiv();
    gameController.getChallenge(playerId).then(function (challenge) {
        challengeDiv.setAttribute("style", "display: block");
        challengeDiv.appendChild(createChallengeImageDiv(challenge));
        challengeDiv.appendChild(createChallengeChoicesDiv(challenge));
    });
}
function resetChallengeDiv() {
    var challengeDiv = document.getElementById("current-challenge-div");
    challengeDiv.innerHTML = "";
    return challengeDiv;
}
function createChallengeChoicesDiv(challenge) {
    var div = document.createElement("div");
    var possibleAnswers = challenge["possible_answers"];
    possibleAnswers.forEach(function (answer) {
        div.appendChild(createAnswerDiv(challenge["challenge_id"], answer));
    });
    return div;
}
function createAnswerDiv(challenge, answerText) {
    var div = document.createElement("div");
    div.appendChild(submitAnswerButton(challenge, answerText));
    return div;
}
function submitAnswerButton(challenge, answerText) {
    var button = document.createElement("button");
    button.onclick = function () {
        gameController.submitAnswer(playerId, challenge, answerText);
        startNextChallenge();
    };
    button.textContent = answerText;
    button.classList.add("btn", "btn-danger", "w-25", "m-2");
    return button;
}
function textDiv(answerText) {
    var textDiv = document.createElement("div");
    textDiv.textContent = answerText;
    return textDiv;
}
function createChallengeImageDiv(challenge) {
    var imageDiv = document.createElement("div");
    var imageElement = document.createElement("img");
    gameController.getChallengeImage(challenge["image_id"]).then(function (blob) {
        imageElement.src = urlCreator.createObjectURL(blob);
        imageElement.classList.add("challenge-img");
    });
    imageDiv.appendChild(imageElement);
    return imageDiv;
}
function countDown() {
    var timerElement = document.getElementById("game-timer-seconds");
    var remainingSeconds = Number.parseInt(timerElement.textContent) || 15;
    if (remainingSeconds - 1 <= 0) {
        timerElement.textContent = "ZERO ";
        document
            .getElementById("current-challenge-div")
            .setAttribute("style", "display: none");
        showScore();
    }
    else {
        timerElement.textContent = (remainingSeconds - 1).toString();
        sleep(1000).then(function () { return countDown(); });
    }
}
function showScore() {
    return main_awaiter(this, void 0, void 0, function () {
        var scoreDiv, playerScoreResponse, score;
        return main_generator(this, function (_a) {
            switch (_a.label) {
                case 0:
                    scoreDiv = document.getElementById("player-score-div");
                    scoreDiv.classList.add("p-3", "display-2", "text-center");
                    return [4 /*yield*/, gameController.getScore(playerId)];
                case 1:
                    playerScoreResponse = _a.sent();
                    console.log("Fetched response: " + JSON.stringify(playerScoreResponse));
                    score = playerScoreResponse["player_score"];
                    scoreDiv.appendChild(textDiv("Player score: ".concat(score)));
                    return [2 /*return*/];
            }
        });
    });
}
function sleep(ms) {
    return new Promise(function (resolve) { return setTimeout(resolve, ms); });
}


var __webpack_export_target__ = window;
for(var i in __webpack_exports__) __webpack_export_target__[i] = __webpack_exports__[i];
if(__webpack_exports__.__esModule) Object.defineProperty(__webpack_export_target__, "__esModule", { value: true });
/******/ })()
;