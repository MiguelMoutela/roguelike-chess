roguelike chess
===============

Roguelike chess is a simple UCI interface that enables you to play chess in the
terminal using ASCII characters.  I have been testing with the amazing
[Stockfish][1] engine but any UCI compliant engine should work.

Install
-------

    $ git clone git@github.com:honza/roguelike-chess.git
    $ cd rogulelike-chess
    $ git clone git@github.com:mcostalba/Stockfish.git
    $ cd Stockfish/src
    $ make profile-build ARCH=x86-64
    $ cd ../../
    $ cp Stockfish/src/stockfish sf
    $ virtualenv venv
    $ source virtualenv
    $ (venv) git clone git@github.com:niklasf/python-chess.git
    $ (venv) cd python-chess
    $ (venv) python setup.py develop
    $ (venv) cd ..
    $ (venv) python run.py

Screenshot
----------

![chess](http://i.imgur.com/GTDrF89.png)

Options
-------

    -s, --skill   Engine skill: 1-20; Default: 1
    -t, --time    Time per player in minutes; Default 5

Caveats & TODO
--------------

You can only play as white.  There is no way to replay or store the game.

License
-------

GPLv3

[1]: http://stockfishchess.org/
