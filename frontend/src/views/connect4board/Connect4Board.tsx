import React, { useEffect, useState, useReducer, useCallback } from 'react';
import Board from './Board';
import Cell from './Cell';
import { Button } from '@material-ui/core';
import RandomId from '../../utils/RandomId';
import ReceiveReducer from './Reducer';
import Connect4BoardState from './State';
import { Message, MessageType } from './Messages';

const WS_URL = 'ws:/localhost:8000/ws/game';

const START_BOARD = [
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
  [0, 0, 0, 0, 0, 0, 0],
];

interface Connect4BoardProps {
  gameId: string;
}

export default function Connect4Board({ gameId }: Connect4BoardProps) {
  const initialState: Connect4BoardState = {
    board: JSON.parse(JSON.stringify(START_BOARD)),
    isGameStarted: false,
    isYourTurn: false,
    isGameFull: false,
    winner: undefined,
  };

  const [state, dispatch] = useReducer(ReceiveReducer, initialState);

  const [methods, setMethods] = useState({ onClick: (column: number) => {} });

  useEffect(() => {
    const gameUrl = `${WS_URL}/${gameId}/`;

    const ws = new WebSocket(gameUrl);

    ws.onopen = () => {
      console.log(`Connected to ${gameUrl}`);
      ws.send(JSON.stringify({ type: 'user_join', username: 'soslow' }));
    };

    ws.onmessage = evt => {
      const message: Message = JSON.parse(evt.data);
      console.log(message);
      dispatch(message);
    };

    setMethods({
      onClick: (column: number) => {
        ws.send(
          JSON.stringify({ type: MessageType.PLAY_COLUMN, column: column }),
        );
      },
    });

    return () => {
      console.log(`Closing connection to ${gameUrl}}`);
      ws.close();
    };
  }, []);

  return (
    <>
      {state.isGameStarted ? (
        <p>
          {state.isYourTurn ? "It's your turn" : "It's your opponent's turn"}
        </p>
      ) : (
        <p>{state.winner !== undefined ? `${state.winner} won !` : ''}</p>
      )}

      <Board board={state.board} onClick={methods.onClick} />
    </>
  );
}
