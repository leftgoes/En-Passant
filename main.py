import re
from time import perf_counter


numbers = ['king', 'qbishop', 'qknight', 'kcastle', 'qcastle', 'en_passant']


class EnPassant:
    __slots__ = ('path', 'total')

    def __init__(self, path: str, total: int):
        self.path = path
        self.total = total

    @staticmethod
    def round(num: float, length: int) -> str:
        string = str(round(num % 1, length))[1:]
        return str(int(num)) + string + (length - len(string) + 1) * '0'

    @staticmethod
    def progressbar(progress: float, length: int = 30):
        quarters = '_░▒▓█'
        done = int(progress * length)
        return (done * '█' + quarters[round(4 * (length * progress - done))] + int((1 - progress) * length) * '_')[
               :length]

    @staticmethod
    def checkmate(moves) -> int:
        if moves[-5] != '#':  # not checkmate
            return
        elif moves[-8:-5] == 'O-O':
            return 3
        elif moves[-10:-5] == 'O-O-O':
            return 4

        last_move = moves[-9:-4]
        if last_move.replace(' ', '')[0] == 'K':  # King checkmate
            return 0

        last_two = last_move[-3:-1]
        if last_two == '=B':  # Bishop Queen
            return 1
        elif last_two == '=N':  # Knight Queen
            return 2
        elif (last_move[3] == '6' or '3' and last_move[1] == 'x') and (97 <= ord(last_move[0]) <= 104):  # pawn capture on 3rd or 6th rank
            offset = 0
            if moves[-11] == '.':  # previous move was black's move
                offset = 3
                if moves[-14:-12].isnumeric():
                    offset += len(moves[-14:-12].replace(' ', ''))
            if moves[-13 - offset] == ' ' and moves[-12 - offset] == last_move[2] and (
                    (moves[-11 - offset] == '5' and last_move[3] == '6') or (
                    moves[-11 - offset] == '4' and last_move[3] == '3')):  # previous move was pawn moving 2 squared next to pawn delivering checkmate
                return 5

    @staticmethod
    def _get(string: str, key: str, length: int) -> str:
        data = string[string.find(key) + length:]
        return data[:data.find('"')]

    def write(self, path: str):
        print(f'               progress                | elapsed | remaining | found/searched/total\n\r0.00% | {self.progressbar(0)} | {0}s | unknown | 0/0', end='')
        d, game, n, m, start = '[Event', '', 0, 0, perf_counter()
        for i, line in enumerate(open(self.path, encoding="utf-8")):
            if line.startswith('[Ev') and i != 0:
                game_data = [j for j in game.splitlines() if j != '']
                moves = game_data[-1]
                if len(moves) < 10:
                    continue
                checkmate = self.checkmate(re.sub(r'{[^}]*}', '', moves).replace('...', '.'))
                if checkmate is not None:
                    white = self._get(game, 'White', 7)
                    black = self._get(game, 'Black', 7)
                    utc_date = self._get(game, 'UTCDate', 9)
                    utc_time = self._get(game, 'UTCTime', 9)
                    w_elo = self._get(game, 'WhiteElo', 10)
                    b_elo = self._get(game, 'BlackElo', 10)
                    control = self._get(game, 'TimeControl', 13)

                    with open(path, 'a') as f:
                        f.write(f'{checkmate},{game_data[1][27:-2]},{utc_date},{utc_time},{white},{black},{w_elo},{b_elo},{control},{game_data[0][8:-2]},{moves}\n')  # checkmate type, path, date, time, white, black, white elo, black elo, time control, event name, moves
                    m += 1
                n += 1
                game = line
            else:
                game += line
            if i % 250000 == 0:
                progress = n / self.total
                elapsed = perf_counter() - start
                print(f'\r{self.round(100 * progress, 2)}%  {self.progressbar(progress)} | {self.round(elapsed, 2)}s |  {self.round(elapsed / (n + 1) * (self.total - n), 2)}s  | {m}/{n}/{self.total}' + 5 * ' ', end='')


if __name__ == '__main__':
    enpassant = EnPassant(FROM_PATH, TOTAL)
    enpassant.write(TO_PATH)
