import os
import time

if __name__ == '__main__':
    start = time.time()
    print('==============================\nstarting task\n==============================')

    PGN_LENGTH = 18
    PGN_FOLDER = 'pgn'


def s_to_hms(s):
    if s < 0:
        return ValueError
    elif round(s, 1) < 60:
        return str(s) + 's'
    elif round(s) < 3600:
        return time.strftime('%Mm %Ss', time.gmtime(s))
    elif round(s) < 86400:
        return time.strftime('%Hh %Mm %Ss', time.gmtime(s))
    else:
        return ValueError


def is_int(it):
    try:
        int(it)
        return True
    except ValueError:
        return False


def clock_to_normal(clock):
    while True:
        if clock.find('{ [%clk ') != -1:
            clock, second = clock[:clock.find('{ [%clk ')], clock[clock.find('{ [%clk '):]
            clock = clock + second[second.find('} ') + 2:]
        else:
            break
    return clock


def is_enpassant_checkmate(moves):
    if moves[-5] == '#':  # checkmate
        last_move = moves[-9:-4]
        if (last_move[3] == '6' or '3' and last_move[1] == 'x') and (97 <= ord(last_move[0]) <= 104): # pawn capture on 3rd or 6th rank
            offset = 0
            if moves[-11] == '.':  # previous move was black's move
                offset = 3
                if is_int(moves[-14:-12]) == True:
                    offset += len(moves[-14:-12].replace(' ', ''))
            if (moves[-13 - offset] == ' ') and (moves[-12 - offset] == last_move[2]) and ((moves[-11 - offset] == '5' and last_move[3] == '6') or (moves[-11 - offset] == '4' and last_move[3] == '3')): # previous move was pawn moving 2 squared next to pawn delivering checkmate
                return True
    return False


def main():
    all_files = os.listdir(PGN_FOLDER)
    for rel_path in all_files:
        print('==============================\n' + rel_path + '\n==============================')
        lines = []
        for line in open(PGN_FOLDER + '/' + rel_path, 'r'):
            lines.append(line)
        index = 0
        print('==============================\nreadlines finished\n==============================')
        for line in open(PGN_FOLDER + '/' + rel_path, 'r'):
            if line[:3] == '1. ':
                if is_enpassant_checkmate(clock_to_normal(line[:-1])) == True:
                    for i in range(18):
                        try:
                            line_check = lines[index - i]
                            if line_check[:6] == '[Site ':
                                game_link = line_check[7:-3]
                            elif line_check[:9] == '[UTCDate ':
                                game_date = line_check[10:-3]
                            elif line_check[:9] == '[UTCTime ':
                                game_time = line_check[10:-3]
                            elif line_check[:7] == '[White ':
                                white = line_check[8:-3]
                            elif line_check[:7] == '[Black ':
                                black = line_check[8:-3]
                            elif line_check[:10] == '[WhiteElo ':
                                white_elo = line_check[11:-3]
                            elif line_check[:10] == '[BlackElo ':
                                black_elo = line_check[11:-3]
                            elif line_check[:13] == '[TimeControl ':
                                time_control = line_check[14:-3]
                            elif line_check[:7] == '[Event ':
                                event = line_check[8:-3]
                        except IndexError:
                            pass
                    game_data = game_link + '\t' + game_date + ' ' + game_time + '\t' + white + '\t' + black + '\t' + white_elo + '\t' + black_elo + '\t' + time_control + '\t' + event + '\t' + line[:-1]
                    print(game_data)
                    with open('en passant mates.txt', 'a') as f2:
                        f2.write(game_data + '\n')
            index += 1


if __name__ == '__main__':
    main()
    print('==============================\ntask finished\ntime elapsed: ' + s_to_hms(time.time() - start) + '\n==============================')
