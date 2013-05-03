roguelike chess
===============

Roguelike chess is a simple UCI interface that enables you to play chess in the
terminal using ASCII characters.

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

Caveats & TODO
--------------

You can only play as white.  The Stockfish engine gets 100ms to think.  There
is no way to replay to store the game.

License
-------

GPLv3
