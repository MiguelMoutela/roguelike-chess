import subprocess
from optparse import OptionParser
import sys
import time as _time
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

White time left: {wtime}
Black time left: {btime}

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


def format_time(t):
    return int(float(t) / 1000.0)


def pos_to_str(pos, wtime, btime):
    data = {
        'wtime': format_time(wtime),
        'btime': format_time(btime)
    }

    for line in BOARD:
        for p in line:
            x = show_square(pos[p])
            data[p] = x

    return WHITE_TEMPLATE.format(**data)


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

    def get(self, wait=False):
        if wait:
            self.engine.stdin.write('isready\n')
            while True:
                text = self.engine.stdout.readline().strip()
                if not text.startswith('bestmove'):
                    continue
                else:
                    return text
        else:
            self.engine.stdin.write('isready\n')
            while True:
                text = self.engine.stdout.readline().strip()
                if text == 'readyok':
                    break

    def go(self, wtime, btime):
        start = _time.time()

        self.put('go wtime %s btime %s' % (wtime, btime))
        v = self.get(wait=True)
        ms = (_time.time() - start) * 1000

        self.get()
        self.put('quit')

        return parse_best_move(v), ms


def parse_best_move(value):
    return value.split(' ')[1]


def next_move(fen, skill, wtime, btime):
    e = Engine()
    e.get()
    e.put('uci')
    e.get()
    e.put('ucinewgame')
    e.get()
    e.put('setoption name Skill Level value %s' % skill)
    e.get()
    e.put('position fen %s' % fen)
    e.get()

    return e.go(wtime, btime)


def main(skill, time, **kwargs):
    pos = get_start_position()
    wtime = time * 60 * 1000
    btime = time * 60 * 1000

    print pos_to_str(pos, wtime, btime)

    while True:


        if wtime <= 0:
            print 'White out of time'
            break

        if btime <= 0:
            print 'Black out of time'
            break

        move = None

        while not move:
            start = _time.time()

            next_input = raw_input('Your next move in SAN: ')
            try:
                move = pos.get_move_from_san(next_input)
            except ValueError:
                print 'Invalid move, try again'
                move = None

        ms = (_time.time() - start) * 1000
        wtime -= int(ms)

        pos.make_move(move)

        print pos_to_str(pos, wtime, btime)

        fen = pos.fen
        n, time_taken = next_move(fen, skill, wtime, btime)

        btime -= int(time_taken)
        pos.make_move(chess.Move.from_uci(n))

        print pos_to_str(pos, wtime, btime)

        if pos.is_check():
            print 'Check!'

        if pos.is_checkmate():
            print 'Checkmate!'
            sys.exit(0)


def build_option_parser():
    p = OptionParser('usage: chess [options]')

    p.add_option('-s', '--skill', default=1, action='store', type='int',
            dest='skill', help='Engine skill: 1-20; Default: 1')

    p.add_option('-t', '--time', default=5, action='store', type='int',
            dest='time', help='Time per player in minutes; Default: 5')

    return p


if __name__ == '__main__':
    parser = build_option_parser()
    (options, args) = parser.parse_args()

    try:
        main(skill=options.skill, time=options.time)
    except KeyboardInterrupt:
        print '\nExiting...'
        print 'Thanks for playing!'
