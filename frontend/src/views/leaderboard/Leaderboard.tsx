import React from 'react';
import { makeStyles } from '@material-ui/core/styles';
import Table from '@material-ui/core/Table';
import TableBody from '@material-ui/core/TableBody';
import TableCell from '@material-ui/core/TableCell';
import TableHead from '@material-ui/core/TableHead';
import TableRow from '@material-ui/core/TableRow';
import Paper from '@material-ui/core/Paper';
import Box from '@material-ui/core/Box';
import IRow from './IRow';

interface LeaderboardProps {
  rows: IRow[];
}

function Leaderboard({ rows }: LeaderboardProps) {
  return (
    <Box width="50%" justifyContent="center" margin="auto" boxShadow={3}>
      <Table>
        <TableHead>
          <TableRow>
            <TableCell>Username</TableCell>
            <TableCell align="right">Wins</TableCell>
            <TableCell align="right">Losses</TableCell>
            <TableCell align="right">Elo</TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {rows.map((player, index) => (
            <TableRow>
              <TableCell>{player.username}</TableCell>
              <TableCell align="right">{player.win}</TableCell>
              <TableCell align="right">{player.loss}</TableCell>
              <TableCell align="right">{player.elo}</TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </Box>
  );
}

export default Leaderboard;
