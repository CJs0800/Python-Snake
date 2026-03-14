const BOARD_PADDING = 16;

function roundedRect(ctx, x, y, width, height, radius) {
  const r = Math.min(radius, width / 2, height / 2);
  ctx.beginPath();
  ctx.moveTo(x + r, y);
  ctx.arcTo(x + width, y, x + width, y + height, r);
  ctx.arcTo(x + width, y + height, x, y + height, r);
  ctx.arcTo(x, y + height, x, y, r);
  ctx.arcTo(x, y, x + width, y, r);
  ctx.closePath();
}

export class SnakeRenderer {
  constructor({ canvas, wrapper }) {
    this.canvas = canvas;
    this.wrapper = wrapper;
    this.ctx = canvas.getContext("2d");

    this.cellSize = 20;
    this.cols = 20;
    this.rows = 12;

    this._resizeObserver = new ResizeObserver(() => {
      this._resizeCanvas(this.cols, this.rows);
    });
    this._resizeObserver.observe(this.wrapper);

    this._resizeCanvas(this.cols, this.rows);
  }

  render(state) {
    if (state.cols !== this.cols || state.rows !== this.rows) {
      this._resizeCanvas(state.cols, state.rows);
    }

    this._drawBoard(state);
    this._drawFruits(state);
    this._drawSnake(state);
  }

  _resizeCanvas(cols, rows) {
    this.cols = cols;
    this.rows = rows;

    const wrapperRect = this.wrapper.getBoundingClientRect();
    const availableWidth = Math.max(280, wrapperRect.width - 20);
    const availableHeight = Math.max(260, window.innerHeight * 0.56);

    const cellSize = Math.floor(
      Math.min(
        (availableWidth - BOARD_PADDING * 2) / cols,
        (availableHeight - BOARD_PADDING * 2) / rows,
      ),
    );

    this.cellSize = Math.max(10, cellSize);

    const cssWidth = cols * this.cellSize + BOARD_PADDING * 2;
    const cssHeight = rows * this.cellSize + BOARD_PADDING * 2;

    const dpr = window.devicePixelRatio || 1;
    this.canvas.style.width = `${cssWidth}px`;
    this.canvas.style.height = `${cssHeight}px`;
    this.canvas.width = Math.floor(cssWidth * dpr);
    this.canvas.height = Math.floor(cssHeight * dpr);

    this.ctx.setTransform(dpr, 0, 0, dpr, 0, 0);
    this.ctx.imageSmoothingEnabled = true;
  }

  _cellRect(position) {
    const x = BOARD_PADDING + position.x * this.cellSize;
    const y = BOARD_PADDING + position.y * this.cellSize;
    return { x, y, size: this.cellSize };
  }

  _drawBoard(state) {
    const { ctx } = this;
    const boardWidth = state.cols * this.cellSize;
    const boardHeight = state.rows * this.cellSize;

    ctx.clearRect(0, 0, this.canvas.width, this.canvas.height);

    roundedRect(ctx, BOARD_PADDING - 4, BOARD_PADDING - 4, boardWidth + 8, boardHeight + 8, 14);
    ctx.fillStyle = "#adc86a";
    ctx.fill();

    for (let y = 0; y < state.rows; y += 1) {
      for (let x = 0; x < state.cols; x += 1) {
        const cellX = BOARD_PADDING + x * this.cellSize;
        const cellY = BOARD_PADDING + y * this.cellSize;
        ctx.fillStyle = (x + y) % 2 === 0 ? "#cde08c" : "#b8d66f";
        ctx.fillRect(cellX, cellY, this.cellSize, this.cellSize);
      }
    }
  }

  _drawFruits(state) {
    const { ctx } = this;

    for (const fruit of state.fruits) {
      const cell = this._cellRect(fruit);
      const centerX = cell.x + cell.size / 2;
      const centerY = cell.y + cell.size / 2;
      const radius = Math.max(3, cell.size * 0.27);

      ctx.beginPath();
      ctx.arc(centerX, centerY, radius, 0, Math.PI * 2);
      ctx.fillStyle = "#da4f31";
      ctx.fill();

      ctx.beginPath();
      ctx.arc(centerX + radius * 0.33, centerY - radius * 0.35, radius * 0.34, 0, Math.PI * 2);
      ctx.fillStyle = "#ffddc8";
      ctx.fill();
    }
  }

  _drawSnake(state) {
    const { ctx } = this;

    for (let index = state.snake.length - 1; index >= 0; index -= 1) {
      const segment = state.snake[index];
      const cell = this._cellRect(segment);

      const inset = index === 0 ? 2 : 2.5;
      roundedRect(
        ctx,
        cell.x + inset,
        cell.y + inset,
        cell.size - inset * 2,
        cell.size - inset * 2,
        index === 0 ? 6 : 5,
      );
      ctx.fillStyle = index === 0 ? "#4c7f1f" : "#659f2a";
      ctx.fill();
    }

    this._drawHeadEyes(state);
  }

  _drawHeadEyes(state) {
    const head = state.snake[0];
    const cell = this._cellRect(head);
    const { ctx } = this;

    const centerX = cell.x + cell.size / 2;
    const centerY = cell.y + cell.size / 2;
    const eyeRadius = Math.max(1.6, cell.size * 0.08);

    const offsets = {
      up: [
        { x: -cell.size * 0.16, y: -cell.size * 0.15 },
        { x: cell.size * 0.16, y: -cell.size * 0.15 },
      ],
      down: [
        { x: -cell.size * 0.16, y: cell.size * 0.15 },
        { x: cell.size * 0.16, y: cell.size * 0.15 },
      ],
      left: [
        { x: -cell.size * 0.15, y: -cell.size * 0.16 },
        { x: -cell.size * 0.15, y: cell.size * 0.16 },
      ],
      right: [
        { x: cell.size * 0.15, y: -cell.size * 0.16 },
        { x: cell.size * 0.15, y: cell.size * 0.16 },
      ],
    };

    const eyeOffsets = offsets[state.direction] || offsets.right;

    for (const eye of eyeOffsets) {
      ctx.beginPath();
      ctx.arc(centerX + eye.x, centerY + eye.y, eyeRadius, 0, Math.PI * 2);
      ctx.fillStyle = "#eef9d6";
      ctx.fill();

      ctx.beginPath();
      ctx.arc(centerX + eye.x, centerY + eye.y, eyeRadius * 0.45, 0, Math.PI * 2);
      ctx.fillStyle = "#294015";
      ctx.fill();
    }
  }
}
