import React from 'react';
import Cell from './Cell';
import LensIcon from '@material-ui/icons/Lens';

interface BoardProps {
  board: Cell[][];
  onClick: (column: number) => void;
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

function Board({ board, onClick }: BoardProps) {
  return (
    <>
      {board.map((row, i) => (
        <div key={i}>
          {row.map((col, j) => (
            <LensIcon
              key={j}
              style={{ color: GetCellColor(col), fontSize: '120px' }}
              onClick={() => onClick(j)}
            />
          ))}
        </div>
      ))}
    </>
  );
}
export default Board;
