from game import Game
from player import (
    Human,
    RandomBot,
    AllOrNothingBot,
    CenteringBot,
    InARowBot,
    InARowAllowBlanksBot,
)


def main():
    players = [
        # AllOrNothingBot(maxDepth=4),
        CenteringBot(maxDepth=4),
        # InARowBot(maxDepth=4),
        # InARowAllowBlanksBot(maxDepth=4),
        # Human(),
        #
        # AllOrNothingBot(maxDepth=4),
        # CenteringBot(maxDepth=4),
        # InARowBot(maxDepth=4),
        # InARowAllowBlanksBot(maxDepth=4),
        Human(),
    ]

    game = Game(players=players)

    while not game.isEnded():
        game.takeTurn(verbose=True, pause=True)

    print(game)
    game.showWhoWon()


if __name__ == "__main__":
    main()
