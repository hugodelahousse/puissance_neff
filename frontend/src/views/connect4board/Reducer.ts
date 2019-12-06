import Connect4BoardState from './State';
import { MessageType, BoardStateMessage, Message } from './Messages';
import Cell from './Cell';

export default function Reducer(
  state: Connect4BoardState,
  action: Message,
): Connect4BoardState {
  switch (action.type) {
    case MessageType.BOARD_STATE:
      const boardStateAction = action as BoardStateMessage;
      return {
        ...state,
        board: boardStateAction.board.reverse(),
        winner: boardStateAction.winner,
        isGameStarted: boardStateAction.winner === undefined,
      };
    case MessageType.GAME_FULL:
      return { ...state, isGameFull: true };
    case MessageType.INVALID_PLAY:
      return { ...state, isYourTurn: true };
    // case MessageType.PLAY_COLUMN:
    //   break;
    case MessageType.START_GAME:
      return { ...state, isGameStarted: true };
    //   return { ...state, isYourTurn: startGameAction.first_player };
    // case MessageType.USER_JOIN:
    //   break;
    case MessageType.YOUR_TURN:
      return { ...state, isYourTurn: true };
  }
  return state;
}
