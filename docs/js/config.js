export const GAME_MODES = [
  {
    key: "classique",
    label: "Classique",
    description: "Un seul fruit simultane.",
    fruitCount: 1,
  },
  {
    key: "multifruit",
    label: "MultiFruit",
    description: "Plusieurs fruits simultanes.",
    fruitCount: 3,
  },
];

export const MAP_SIZES = [
  { key: "tres_petite", label: "Tres-petite", cols: 12, rows: 8 },
  { key: "petite", label: "Petite", cols: 16, rows: 10 },
  { key: "moyenne", label: "Moyenne", cols: 20, rows: 12 },
  { key: "grande", label: "Grande", cols: 28, rows: 16 },
  { key: "tres_grande", label: "Tres grande", cols: 36, rows: 20 },
];

export const SPEEDS = [
  { key: "lent", label: "Lent", tickMs: 220 },
  { key: "normal", label: "Normal", tickMs: 160 },
  { key: "rapide", label: "Rapide", tickMs: 110 },
];

export const DEFAULT_SELECTIONS = {
  modeKey: "classique",
  mapKey: "moyenne",
  speedKey: "normal",
};

export const DIRECTION_VECTORS = {
  up: { x: 0, y: -1 },
  down: { x: 0, y: 1 },
  left: { x: -1, y: 0 },
  right: { x: 1, y: 0 },
};

export const KEY_TO_DIRECTION = {
  ArrowUp: "up",
  ArrowDown: "down",
  ArrowLeft: "left",
  ArrowRight: "right",
  w: "up",
  W: "up",
  z: "up",
  Z: "up",
  s: "down",
  S: "down",
  a: "left",
  A: "left",
  q: "left",
  Q: "left",
  d: "right",
  D: "right",
};
