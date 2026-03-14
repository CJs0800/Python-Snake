import { DIRECTION_VECTORS } from "./config.js";

export const GAME_STATUS = {
  RUNNING: "running",
  GAME_OVER: "game_over",
  WON: "won",
};

const DIRECTION_KEYS = Object.keys(DIRECTION_VECTORS);

function keyFromPosition(position) {
  return `${position.x},${position.y}`;
}

function positionFromKey(key) {
  const [x, y] = key.split(",").map(Number);
  return { x, y };
}

function isOppositeDirection(current, next) {
  const a = DIRECTION_VECTORS[current];
  const b = DIRECTION_VECTORS[next];
  return a.x === -b.x && a.y === -b.y;
}

function isSamePosition(a, b) {
  return a.x === b.x && a.y === b.y;
}

export class SnakeEngine {
  constructor({ cols, rows, fruitCount, rng = Math.random }) {
    this.cols = cols;
    this.rows = rows;
    this.fruitCount = Math.max(1, fruitCount);
    this._rng = rng;

    this.direction = "right";
    this.pendingDirection = "right";
    this.snake = [];
    this.fruits = new Set();
    this.score = 0;
    this.status = GAME_STATUS.RUNNING;
  }

  reset() {
    const centerY = Math.floor(this.rows / 2);
    const headX = Math.floor(this.cols / 2);

    this.snake = [
      { x: headX, y: centerY },
      { x: headX - 1, y: centerY },
      { x: headX - 2, y: centerY },
    ];

    this.direction = "right";
    this.pendingDirection = "right";
    this.fruits.clear();
    this.score = 0;
    this.status = GAME_STATUS.RUNNING;

    this._refillFruits();
    return this.getState();
  }

  setDirection(directionKey) {
    if (!DIRECTION_KEYS.includes(directionKey)) {
      return;
    }
    if (isOppositeDirection(this.direction, directionKey)) {
      return;
    }
    this.pendingDirection = directionKey;
  }

  step() {
    if (this.status !== GAME_STATUS.RUNNING) {
      return this.getState();
    }

    if (!isOppositeDirection(this.direction, this.pendingDirection)) {
      this.direction = this.pendingDirection;
    }

    const head = this.snake[0];
    const delta = DIRECTION_VECTORS[this.direction];
    const nextHead = {
      x: head.x + delta.x,
      y: head.y + delta.y,
    };

    const willEatFruit = this.fruits.has(keyFromPosition(nextHead));
    const bodyToCheck = willEatFruit ? this.snake : this.snake.slice(0, -1);

    const isOutOfBounds =
      nextHead.x < 0 ||
      nextHead.x >= this.cols ||
      nextHead.y < 0 ||
      nextHead.y >= this.rows;

    if (isOutOfBounds || bodyToCheck.some((part) => isSamePosition(part, nextHead))) {
      this.status = GAME_STATUS.GAME_OVER;
      return this.getState();
    }

    this.snake.unshift(nextHead);

    if (willEatFruit) {
      this.score += 1;
      this.fruits.delete(keyFromPosition(nextHead));
      this._refillFruits();
    } else {
      this.snake.pop();
    }

    if (this.snake.length >= this.cols * this.rows) {
      this.status = GAME_STATUS.WON;
    }

    return this.getState();
  }

  getState() {
    return {
      cols: this.cols,
      rows: this.rows,
      snake: this.snake.map((part) => ({ ...part })),
      fruits: [...this.fruits].map((key) => positionFromKey(key)),
      direction: this.direction,
      score: this.score,
      status: this.status,
      fruitCount: this.fruitCount,
    };
  }

  _refillFruits() {
    while (this.fruits.size < this.fruitCount) {
      const freeCells = this._collectFreeCells();
      if (freeCells.length === 0) {
        this.status = GAME_STATUS.WON;
        return;
      }

      const randomIndex = Math.floor(this._rng() * freeCells.length);
      const fruit = freeCells[randomIndex];
      this.fruits.add(keyFromPosition(fruit));
    }
  }

  _collectFreeCells() {
    const occupied = new Set(this.snake.map((part) => keyFromPosition(part)));
    for (const fruit of this.fruits) {
      occupied.add(fruit);
    }

    const freeCells = [];
    for (let y = 0; y < this.rows; y += 1) {
      for (let x = 0; x < this.cols; x += 1) {
        const key = `${x},${y}`;
        if (!occupied.has(key)) {
          freeCells.push({ x, y });
        }
      }
    }

    return freeCells;
  }
}
