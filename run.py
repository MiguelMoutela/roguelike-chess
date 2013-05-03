import subprocess
import time
import sys
import chess


START_FEN = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"


def get_board():
    letters = [None, 'a', 'b', 'c', 'd', 'e', 'f', 'g', 'h']
    board = []

    for x in range(1, 9):
        row = []
        for y in range(1, 9):
            row.append(letters[y] + str(x))

        board.append(row)

    return board


BOARD = get_board()


def show_square(s):
    s = str(s)
    if s == 'None':
        return ' '
    else:
        return s


WHITE_TEMPLATE = """

   +-+-+-+-+-+-+-+-+
8  |{a8}|{b8}|{c8}|{d8}|{e8}|{f8}|{g8}|{h8}|
   +-+-+-+-+-+-+-+-+
7  |{a7}|{b7}|{c7}|{d7}|{e7}|{f7}|{g7}|{h7}|
   +-+-+-+-+-+-+-+-+
6  |{a6}|{b6}|{c6}|{d6}|{e6}|{f6}|{g6}|{h6}|
   +-+-+-+-+-+-+-+-+
5  |{a5}|{b5}|{c5}|{d5}|{e5}|{f5}|{g5}|{h5}|
   +-+-+-+-+-+-+-+-+
4  |{a4}|{b4}|{c4}|{d4}|{e4}|{f4}|{g4}|{h4}|
   +-+-+-+-+-+-+-+-+
3  |{a3}|{b3}|{c3}|{d3}|{e3}|{f3}|{g3}|{h3}|
   +-+-+-+-+-+-+-+-+
2  |{a2}|{b2}|{c2}|{d2}|{e2}|{f2}|{g2}|{h2}|
   +-+-+-+-+-+-+-+-+
1  |{a1}|{b1}|{c1}|{d1}|{e1}|{f1}|{g1}|{h1}|
   +-+-+-+-+-+-+-+-+

    a b c d e f g h

"""


def pos_to_str(pos):
    data = {}
    for line in BOARD:
        for p in line:
            x = show_square(pos[p])
            data[p] = x

    return WHITE_TEMPLATE.format(**data)


def fen_to_board(fen):
    pos = chess.Position(fen)
    return pos_to_str(pos)


def get_start_position():
    return chess.Position(START_FEN)


class Engine(object):

    def __init__(self):
        self.engine = subprocess.Popen(
            './sf',
            universal_newlines=True,
            stdin=subprocess.PIPE,
            stdout=subprocess.PIPE,
        )

    def put(self, command):
        self.engine.stdin.write(command+'\n')

        if command == 'stop':
            return self.engine.stdout.readline().strip()

    def stop(self):
        return self.put('stop')

    def get(self):
        self.engine.stdin.write('isready\n')
        while True:
            text = self.engine.stdout.readline().strip()
            if text == 'readyok':
                break
            if text != '':
                continue


def parse_best_move(value):
    return value.split(' ')[1]


def next_move(fen, thinking_time=1000):
    e = Engine()
    e.get()
    e.put('uci')
    e.get()
    e.put('ucinewgame')
    e.get()
    e.put('position fen %s' % fen)
    e.get()
    e.put('go infinite')
    time.sleep(float(thinking_time) / 1000.0)
    e.get()
    v = e.stop()
    e.get()
    e.put('quit')

    return parse_best_move(v)


def main():
    pos = get_start_position()
    print pos_to_str(pos)

    while True:
        move = None

        while not move:
            next_input = raw_input('Your next move in SAN: ')
            try:
                move = pos.get_move_from_san(next_input)
            except ValueError:
                print 'Invalid move, try again'
                move = None

        pos.make_move(move)

        print pos_to_str(pos)

        fen = pos.fen
        n = next_move(fen, thinking_time=100)
        pos.make_move(chess.Move.from_uci(n))

        print pos_to_str(pos)

        if pos.is_check():
            print 'Check!'

        if pos.is_checkmate():
            print 'Checkmate!'
            sys.exit(0)


if __name__ == '__main__':
    main()
