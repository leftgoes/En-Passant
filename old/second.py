import time
from main import is_enpassant_checkmate


start = time.time()
y = open('pgn/lichess_db_standard_rated_2017-11.pgn', 'r').read()
y = y.splitlines()
i = 0
print(time.time() - start)
for line in y:
    if line[:3] == '1. ':
        if is_enpassant_checkmate(line) is True:
            time_control = y[i - 3][14:-2]
            black_elo = y[i - 8][11:-2]
            white_elo = y[i - 9][11:-2]
            game_time = y[i - 10][10:-2]
            game_date = y[i - 11][10:-2]
            black_username = y[i - 13][8:-2]
            white_username = y[i - 14][8:-2]
            game_link = y[i - 15][7:-2]
            event = y[i - 16][8:-2]
            game_data = game_link + '\t' + game_date + ' ' + game_time + '\t' + white_username + '\t' + black_username + '\t' + white_elo + '\t' + black_elo + '\t' + time_control + '\t' + event + '\t' + line
            print(game_data)
            with open('en passant mates.txt', 'a') as f:
                f.write(game_data + '\n')
    i += 1
print(time.time() - start)
