export enum MessageType {
  START_GAME = 'start_game',
  GAME_FULL = 'game_full',
  USER_JOIN = 'user_join',
  PLAY_COLUMN = 'play_column',
  INVALID_PLAY = 'invalid_play',
  BOARD_STATE = 'board_state',
  YOUR_TURN = 'your_turn',
}

export interface Message {
  type: MessageType;
}

export interface StartGameMessage {
  type: MessageType.START_GAME;
  first_player: boolean;
}

export interface GameFullMessage {
  type: MessageType.GAME_FULL;
}

export interface UserJoinMessage {
  type: MessageType.USER_JOIN;
  username: string;
}

export interface PlayColumnMessage {
  type: MessageType.PLAY_COLUMN;
  column: number;
}

export interface InvalidPlayMessage {
  type: MessageType.INVALID_PLAY;
}

export interface BoardStateMessage {
  type: MessageType.BOARD_STATE;
  board: number[][];
  winner?: number;
}

export interface YourTurnMessage {
  type: MessageType.YOUR_TURN;
}
