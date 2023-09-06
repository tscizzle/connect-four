import time

from boardHelpers import applyMoveToNewBoard, getWinner, isFull, boardStr


class Game(object):
    def __init__(self, players, numCols=7, numRows=6):
        self.numCols = numCols
        self.numRows = numRows
        self.board = [[None for _ in range(numRows)] for _ in range(numCols)]
        self.numMovesSoFar = 0

        self.players = players
        self.players[0].symbol = "X"
        self.players[0].vsSymbol = "O"
        self.players[1].symbol = "O"
        self.players[1].vsSymbol = "X"

    def __str__(self):
        return boardStr(self.board)

    def isEnded(self):
        return getWinner(self.board) or isFull(self.board)

    def showWhoWon(self):
        winningSymbol = getWinner(self.board)
        print("%s wins!" % winningSymbol if winningSymbol else "It was a tie.")

    def nextPlayer(self):
        return self.players[self.numMovesSoFar % len(self.players)]

    def takeTurn(self, verbose=False, pause=False):
        currentPlayer = self.nextPlayer()
        maxCol = len(self.board) - 1
        moveMade = False
        while not moveMade:
            try:
                colIdx = currentPlayer.nextMove(self.board)
                if not 0 <= colIdx <= maxCol:
                    raise MoveOutOfRange
                column = self.board[colIdx]
                if all(column):
                    raise ColumnIsFull
            except MoveOutOfRange:
                print("%s is not from 0 through %s." % (colIdx, maxCol))
            except ColumnIsFull:
                print("Column %s is full." % colIdx)
            else:
                moveMade = True
            if not moveMade:
                time.sleep(1)
        symbol = currentPlayer.symbol

        newBoard = applyMoveToNewBoard(self.board, colIdx, symbol)

        self.board = newBoard
        self.numMovesSoFar += 1

        if verbose:
            print(self)
        if pause:
            input()


class MoveOutOfRange(Exception):
    pass


class ColumnIsFull(Exception):
    pass
