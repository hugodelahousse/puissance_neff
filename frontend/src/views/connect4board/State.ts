import Cell from './Cell';

export default interface Connect4BoardState {
  board: Cell[][];
  isYourTurn: boolean;
  winner?: number;
  isGameStarted: boolean;
  isGameFull: boolean;
}
