import React from 'react';
import Board from './Board';
import Cell from './Cell';

const startBoard = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
];

interface Connect4BoardProps {}
interface Connect4BoardState {
  board: Cell[][];
}

class Connect4Board extends React.Component<
  Connect4BoardProps,
  Connect4BoardState
> {
  constructor(props: Connect4BoardProps) {
    super(props);
    this.state = { board: JSON.parse(JSON.stringify(startBoard)) };
  }

  render() {
    return <Board board={this.state.board} />;
  }
}

export default Connect4Board;
