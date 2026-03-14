import {
  DEFAULT_SELECTIONS,
  GAME_MODES,
  KEY_TO_DIRECTION,
  MAP_SIZES,
  SPEEDS,
} from "./config.js";
import { GAME_STATUS, SnakeEngine } from "./engine.js";
import { SnakeRenderer } from "./renderer.js";

const modeOptions = document.querySelector("#mode-options");
const mapOptions = document.querySelector("#map-options");
const speedOptions = document.querySelector("#speed-options");

const startButton = document.querySelector("#start-btn");
const pauseButton = document.querySelector("#pause-btn");
const restartButton = document.querySelector("#restart-btn");
const menuButton = document.querySelector("#menu-btn");

const overlay = document.querySelector("#overlay");
const overlayTitle = document.querySelector("#overlay-title");
const overlayMessage = document.querySelector("#overlay-message");
const overlayRestartButton = document.querySelector("#overlay-restart-btn");
const overlayMenuButton = document.querySelector("#overlay-menu-btn");

const modeChip = document.querySelector("#mode-chip");
const mapChip = document.querySelector("#map-chip");
const speedChip = document.querySelector("#speed-chip");
const fruitChip = document.querySelector("#fruit-chip");
const scoreValue = document.querySelector("#score-value");

const touchButtons = Array.from(document.querySelectorAll(".touch-btn"));

const renderer = new SnakeRenderer({
  canvas: document.querySelector("#game-canvas"),
  wrapper: document.querySelector("#board-wrapper"),
});

const selection = {
  modeKey: DEFAULT_SELECTIONS.modeKey,
  mapKey: DEFAULT_SELECTIONS.mapKey,
  speedKey: DEFAULT_SELECTIONS.speedKey,
};

const runtime = {
  engine: null,
  gameState: null,
  rafId: null,
  isPaused: false,
  isRunning: false,
  lastTickAt: 0,
};

function findByKey(list, key) {
  return list.find((item) => item.key === key) ?? list[0];
}

function createOptions({ container, options, selectedKey, onSelect, toLabel }) {
  container.innerHTML = "";

  for (const option of options) {
    const button = document.createElement("button");
    button.type = "button";
    button.className = "option-btn";
    button.textContent = toLabel(option);
    button.dataset.key = option.key;

    if (option.key === selectedKey) {
      button.classList.add("active");
    }

    button.addEventListener("click", () => {
      for (const sibling of container.querySelectorAll(".option-btn")) {
        sibling.classList.remove("active");
      }
      button.classList.add("active");
      onSelect(option.key);
    });

    container.appendChild(button);
  }
}

function syncSummaryChips() {
  const mode = findByKey(GAME_MODES, selection.modeKey);
  const map = findByKey(MAP_SIZES, selection.mapKey);
  const speed = findByKey(SPEEDS, selection.speedKey);

  modeChip.textContent = `Mode: ${mode.label}`;
  mapChip.textContent = `Map: ${map.label} (${map.cols}x${map.rows})`;
  speedChip.textContent = `Vitesse: ${speed.label}`;
  fruitChip.textContent = `Fruits: ${mode.fruitCount}`;
}

function showOverlay({ title, message, showActions = true }) {
  overlayTitle.textContent = title;
  overlayMessage.textContent = message;
  overlayRestartButton.classList.toggle("hidden", !showActions);
  overlayMenuButton.classList.toggle("hidden", !showActions);
  overlay.classList.remove("hidden");
}

function hideOverlay() {
  overlay.classList.add("hidden");
}

function updateScore(state) {
  scoreValue.textContent = String(state?.score ?? 0);
}

function startGame() {
  const mode = findByKey(GAME_MODES, selection.modeKey);
  const map = findByKey(MAP_SIZES, selection.mapKey);

  runtime.engine = new SnakeEngine({
    cols: map.cols,
    rows: map.rows,
    fruitCount: mode.fruitCount,
  });

  runtime.gameState = runtime.engine.reset();
  runtime.isPaused = false;
  runtime.isRunning = true;
  runtime.lastTickAt = performance.now();

  syncSummaryChips();
  updateScore(runtime.gameState);
  hideOverlay();

  if (runtime.rafId === null) {
    runtime.rafId = requestAnimationFrame(loop);
  }
}

function restartCurrentGame() {
  if (!runtime.engine) {
    startGame();
    return;
  }

  runtime.gameState = runtime.engine.reset();
  runtime.isPaused = false;
  runtime.isRunning = true;
  runtime.lastTickAt = performance.now();

  updateScore(runtime.gameState);
  hideOverlay();

  if (runtime.rafId === null) {
    runtime.rafId = requestAnimationFrame(loop);
  }
}

function pauseOrResume() {
  if (!runtime.gameState || runtime.gameState.status !== GAME_STATUS.RUNNING) {
    return;
  }

  runtime.isPaused = !runtime.isPaused;
  pauseButton.textContent = runtime.isPaused ? "Reprendre" : "Pause";

  if (runtime.isPaused) {
    showOverlay({
      title: "Pause",
      message: "Appuyez sur P ou cliquez sur Reprendre.",
      showActions: false,
    });
  } else {
    hideOverlay();
    runtime.lastTickAt = performance.now();
    if (runtime.rafId === null) {
      runtime.rafId = requestAnimationFrame(loop);
    }
  }
}

function backToHome() {
  runtime.isPaused = true;
  runtime.isRunning = false;
  pauseButton.textContent = "Pause";

  showOverlay({
    title: "Accueil",
    message: 'Choisissez vos options puis cliquez sur "Lancer la partie".',
    showActions: false,
  });
}

function onDirection(direction) {
  if (!runtime.engine || runtime.isPaused) {
    return;
  }
  runtime.engine.setDirection(direction);
}

function loop(timestamp) {
  runtime.rafId = null;

  if (!runtime.gameState) {
    return;
  }

  const speed = findByKey(SPEEDS, selection.speedKey);

  if (
    runtime.isRunning &&
    !runtime.isPaused &&
    runtime.gameState.status === GAME_STATUS.RUNNING
  ) {
    while (timestamp - runtime.lastTickAt >= speed.tickMs) {
      runtime.gameState = runtime.engine.step();
      runtime.lastTickAt += speed.tickMs;
    }
  }

  renderer.render(runtime.gameState);
  updateScore(runtime.gameState);

  if (runtime.gameState.status === GAME_STATUS.GAME_OVER) {
    runtime.isRunning = false;
    runtime.isPaused = true;
    pauseButton.textContent = "Pause";
    showOverlay({
      title: "Partie terminee",
      message: "Collision detectee. Rejouez ou ajustez les options.",
      showActions: true,
    });
  } else if (runtime.gameState.status === GAME_STATUS.WON) {
    runtime.isRunning = false;
    runtime.isPaused = true;
    pauseButton.textContent = "Pause";
    showOverlay({
      title: "Victoire",
      message: "La map est remplie. Bien joue.",
      showActions: true,
    });
  }

  const shouldKeepAnimating =
    runtime.isRunning &&
    !runtime.isPaused &&
    runtime.gameState.status === GAME_STATUS.RUNNING;

  if (shouldKeepAnimating) {
    runtime.rafId = requestAnimationFrame(loop);
  }
}

function setupKeyboardControls() {
  window.addEventListener("keydown", (event) => {
    if (event.key.toLowerCase() === "p") {
      event.preventDefault();
      pauseOrResume();
      return;
    }

    if (event.key.toLowerCase() === "r") {
      event.preventDefault();
      restartCurrentGame();
      return;
    }

    const direction = KEY_TO_DIRECTION[event.key];
    if (direction) {
      event.preventDefault();
      onDirection(direction);
    }
  });
}

function setupTouchControls() {
  for (const button of touchButtons) {
    button.addEventListener("pointerdown", (event) => {
      event.preventDefault();
      onDirection(button.dataset.dir);
    });
  }
}

function setupButtons() {
  startButton.addEventListener("click", startGame);
  pauseButton.addEventListener("click", pauseOrResume);
  restartButton.addEventListener("click", restartCurrentGame);
  menuButton.addEventListener("click", backToHome);

  overlayRestartButton.addEventListener("click", restartCurrentGame);
  overlayMenuButton.addEventListener("click", backToHome);
}

function initOptions() {
  createOptions({
    container: modeOptions,
    options: GAME_MODES,
    selectedKey: selection.modeKey,
    onSelect: (key) => {
      selection.modeKey = key;
      syncSummaryChips();
    },
    toLabel: (mode) => `${mode.label} - ${mode.description}`,
  });

  createOptions({
    container: mapOptions,
    options: MAP_SIZES,
    selectedKey: selection.mapKey,
    onSelect: (key) => {
      selection.mapKey = key;
      syncSummaryChips();
    },
    toLabel: (size) => `${size.label} (${size.cols}x${size.rows})`,
  });

  createOptions({
    container: speedOptions,
    options: SPEEDS,
    selectedKey: selection.speedKey,
    onSelect: (key) => {
      selection.speedKey = key;
      syncSummaryChips();
    },
    toLabel: (speed) => `${speed.label} (${speed.tickMs} ms/tick)`,
  });
}

function bootstrap() {
  initOptions();
  setupButtons();
  setupKeyboardControls();
  setupTouchControls();
  syncSummaryChips();

  const previewMode = findByKey(GAME_MODES, selection.modeKey);
  const previewMap = findByKey(MAP_SIZES, selection.mapKey);
  const preview = new SnakeEngine({
    cols: previewMap.cols,
    rows: previewMap.rows,
    fruitCount: previewMode.fruitCount,
  });
  runtime.gameState = preview.reset();
  renderer.render(runtime.gameState);

  showOverlay({
    title: "Pret ?",
    message: 'Cliquez sur "Lancer la partie" pour commencer.',
    showActions: false,
  });
}

bootstrap();
