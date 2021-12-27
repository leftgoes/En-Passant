from datetime import datetime
import re
import os
from time import perf_counter

from input import NUMBERS


class PGN:
    __slots__ = ('data_path', 'log_path')

    def __init__(self, data_path: str, log_path: str):
        self.data_path = data_path
        self.log_path = log_path

    @staticmethod
    def _get(game_data: list[str,], key: str, length: int) -> str:
        for s in game_data:
            if s.startswith(key):
                return s[length:-2]

    @staticmethod
    def checkmate(moves: str) -> int:
        if moves[-5] != '#':  # not checkmate
            return
        elif moves[-10:-5] == 'O-O-O':  # queen-side castle mate
            return 4
        elif moves[-8:-5] == 'O-O':  # king-side castle mate
            return 3

        last_move = moves[-9:-4]
        if last_move.replace(' ', '')[0] == 'K':  # King checkmate
            return 0

        last_two = last_move[-3:-1]
        if last_two == '=B':  # Bishop Queen
            return 1
        elif last_two == '=N':  # Knight Queen
            return 2
        elif (last_move[3] == '6' or '3' and last_move[1] == 'x') and (
                97 <= ord(last_move[0]) <= 104):  # pawn capture on 3rd or 6th rank
            offset = 0
            if moves[-11] == '.':  # previous move was black's move
                offset = 3
                if moves[-14:-12].replace(' ', '').isnumeric():
                    offset += len(moves[-14:-12].replace(' ', ''))
            if moves[-13 - offset] == ' ' and moves[-12 - offset] == last_move[2] and (
                    (moves[-11 - offset] == '5' and last_move[3] == '6') or (
                    moves[-11 - offset] == '4' and last_move[3] == '3')):  # previous move was pawn moving 2 squared next to pawn delivering checkmate
                return 5

    @staticmethod
    def progressbar(progress: float, length: int = 30) -> str:
        quarters = '_░▒▓█'
        done = int(progress * length)
        return (done * '█' + quarters[round(4 * (length * progress - done))] + int((1 - progress) * length) * '_')[
               :length]

    @staticmethod
    def round(num: float, length: int) -> str:
        string = str(round(num % 1, length))[1:]
        return str(int(num)) + string + (length - len(string) + 1) * '0'

    @staticmethod
    def s2hms(s: int) -> str:
        h = int(s / 3600)
        s -= 3600 * h
        m = int(s / 60)
        s -= 60 * m
        return f'{h}:{"0" if m < 10 else ""}{m}:{"0" if s < 10 else ""}{int(s)}'

    def folder(self, folder: str, path: str, total: list[int, ]):  # analyze entire folder
        i = 0
        for pgn in os.listdir(folder):
            if not file.endswith('.pgn'):
                continue
            self.get(folder + '\\' + pgn, total[i])
            i += 1

    def get(self, path: str, total: str = None):  # analyze pgn
        d, game, n = '[Event', [], 0
        start, occurrences = perf_counter(), [0 for _ in NUMBERS]

        if not os.path.isfile(self.data_path):
            with open(self.data_path, 'a') as f:
                f.write('number,path,date,time,white,black,white elo,black elo,time control,event,moves')
        print(f'\n{path!r}\n{100 * "-"}\n{15 * " "}progress{15 * " "}| elapsed | remaining | games\n{100 * "-"}\n\r0.00% | {self.progressbar(0)} | 0:00:00 |  unknown  | 0/0/0/0/0/0//0//{total}', end='')

        for i, line in enumerate(open(path, encoding="utf-8")):
            if (line.startswith('[Ev') and i != 0) or n == total - 1:
                game = list(filter(lambda a: a != '', game))
                moves = game[-1]

                if len(moves) < 10:
                    continue

                checkmate = self.checkmate(re.sub(' {[^}]*}', '', moves).replace('...', '.').replace('?', '').replace('!', ''))
                if checkmate is not None:
                    occurrences[checkmate] += 1
                    white = self._get(game, '[White', 8)
                    black = self._get(game, '[Black', 8)
                    utc_date = self._get(game, '[UTCDate', 10)
                    utc_time = self._get(game, '[UTCTime', 10)
                    w_elo = self._get(game, '[WhiteElo', 11)
                    b_elo = self._get(game, '[BlackElo', 11)
                    control = self._get(game, '[TimeControl', 14)

                    with open(self.data_path, 'a') as f:
                        f.write(f'\n{checkmate},{game[1][27:-2]},{utc_date},{utc_time},{white},{black},{w_elo},{b_elo},{control},{game[0][8:-2]},{moves}')  # checkmate type, path, date, time, white, black, white elo, black elo, time control, event name, moves
                n += 1
                game = [line[:-1]]
            else:
                game.append(line[:-1])

            if i % 250000 == 0:
                progress = n / total
                elapsed = perf_counter() - start
                print(f'\r{self.round(100 * progress, 2)}%  {self.progressbar(progress)} | {self.s2hms(elapsed)} |  {self.s2hms(elapsed / (n + 1) * (total - n))}  | {"/".join([str(o) for o in occurrences])}//{n}//{total}' + 5 * ' ', end='')
        print(f'\r100.0% {self.progressbar(1)} | {self.s2hms(perf_counter() - start)} |  0:00:00  | {"/".join([str(i) for i in occurrences])}//{n}//{total}' + 15 * ' ', end='')

        if not os.path.isfile(self.log_path):
            with open(self.log_path, 'a') as f:
                f.write('datetime,month,bytes,elapsed,games detected,games total,' + ','.join(NUMBERS))
        with open(self.log_path, 'a') as f:
            f.write(f'\n{datetime.now().strftime("%Y-%m-%d %H:%M:%S")},{path[-11:-4]},{os.stat(path).st_size},{round(perf_counter() - start, 3)},{n},{total},{",".join([str(i) for i in occurrences])}')


if __name__ == '__main__':
    enpassant = PGN(TO_CSV, TO_LOG)
    enpassant.get(DATA_CSV, TOTAL_GAMES)
