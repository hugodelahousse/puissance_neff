import React from 'react';
import Cell from './Cell';
import LensIcon from '@material-ui/icons/Lens';

interface BoardProps {
  board: Cell[][];
}

function GetCellColor(cell: Cell): string {
  switch (cell) {
    case Cell.Red: {
      return 'red';
    }
    case Cell.Yellow: {
      return 'yellow';
    }
    default: {
      return 'white';
    }
  }
}

function Board({ board }: BoardProps) {
  return (
    <>
      {board.map((row, i) => (
        <div>
          {row.map((col, j) => (
            <LensIcon style={{ color: GetCellColor(col), fontSize: '120px' }} />
          ))}
        </div>
      ))}
    </>
  );
}
export default Board;
