import random
import sys

from boardHelpers import (
    applyMoveToNewBoard,
    getAvailableColumns,
    getWinner,
    getCenteringMetric,
    getInARowMetric,
    boardStr
)

try:
    BIG_NUM = sys.maxint # Python 2
except AttributeError:
    BIG_NUM = sys.maxsize # Python 3


class Player(object):
    def nextMove(self, board):
        raise Exception('Player subclass must define the nextMove method.')

class Human(Player):
    def nextMove(self, board):
        moveChosen = False
        while not moveChosen:
            print(boardStr(board))
            colIdx = input('Which column?\n')
            try:
                colIdx = int(colIdx)
            except ValueError:
                print('"%s" is not a number.' % colIdx)
            else:
                moveChosen = True
        return colIdx

# Bots

class RandomBot(Player):
    def nextMove(self, board):
        availableCols = getAvailableColumns(board)
        colIdx = random.choice(availableCols)
        return colIdx

class MiniMaxPlayer(Player):
    def __init__(self, maxDepth=4):
        self.maxDepth = maxDepth

class AllOrNothingBot(MiniMaxPlayer):
    def nextMove(self, board):
        return miniMaxMove(self, board, allOrNothingHeuristic)

class CenteringBot(MiniMaxPlayer):
    def nextMove(self, board):
        return miniMaxMove(self, board, centeringHeuristic)

class InARowBot(MiniMaxPlayer):
    def nextMove(self, board):
        return miniMaxMove(self, board, mostInARowHeuristic)

class InARowAllowBlanksBot(MiniMaxPlayer):
    def nextMove(self, board):
        return miniMaxMove(self, board, mostInARowAllowBlanksHeuristic)

# Minimax

def miniMaxMove(player, board, heuristic):
    symbol = player.symbol
    vsSymbol = player.vsSymbol
    maxDepth = player.maxDepth
    colIdxs, _ = miniMax(
        symbol=symbol,
        vsSymbol=vsSymbol,
        board=board,
        heuristic=heuristic,
        maxDepth=maxDepth,
        currentDepth=0
    )
    return random.choice(colIdxs)

def miniMax(symbol, vsSymbol, board, heuristic, maxDepth, currentDepth):
    value = heuristic(symbol, vsSymbol, board)

    if value == 1 or value == -1:
        return None, value
    elif currentDepth == maxDepth:
        return None, value
    else:
        colIdxOptions = getAvailableColumns(board)
        bestOptions = []
        bestValue = -BIG_NUM
        for colIdx in colIdxOptions:
            newBoard = applyMoveToNewBoard(board, colIdx, symbol)
            newDepth = currentDepth + 1
            _, vsValue = miniMax(
                symbol=vsSymbol,
                vsSymbol=symbol,
                board=newBoard,
                heuristic=heuristic,
                maxDepth=maxDepth,
                currentDepth=newDepth
            )
            newValue = -vsValue
            if newValue > bestValue:
                bestOptions = [colIdx]
                bestValue = newValue
            elif newValue == bestValue:
                bestOptions.append(colIdx)
        return bestOptions, bestValue

# Heuristics

def heuristicMaker(nonAbsoluteHeuristic, **kwargs):
    """
    nonAbsoluteHeuristic handles the case when the board has no winner, and
    should return a value such that -1 < value < 1, and such that switching
    symbol and vsSymbol is the same as multiplying by -1.
    heuristicMaker takes this, and combines it with the obvious cases of when
    the board has a winner, and returns 1 for a win and -1 for a loss.
    """
    def heuristic(symbol, vsSymbol, board, **kwargs):
        winningSymbol = getWinner(board)
        if winningSymbol == symbol:
            value = 1
        elif winningSymbol == vsSymbol:
            value = -1
        else:
            value = nonAbsoluteHeuristic(symbol, vsSymbol, board, **kwargs)
        return value
    return heuristic

def allOrNothingHeuristic(symbol, vsSymbol, board):
    return 0
allOrNothingHeuristic = heuristicMaker(allOrNothingHeuristic)

def centeringHeuristic(symbol, vsSymbol, board):
    avgDist = getCenteringMetric(board, symbol)
    vsAvgDist = getCenteringMetric(board, vsSymbol)
    if avgDist is None or vsAvgDist is None:
        value = 0
    elif avgDist == 0 and vsAvgDist == 0:
        value = 0
    else:
        value = 0.9 * (vsAvgDist - avgDist) / (avgDist + vsAvgDist)
    return value
centeringHeuristic = heuristicMaker(centeringHeuristic)

def mostInARowHeuristic(symbol, vsSymbol, board, allowBlanks=False):
    mostInARow, mostInARowFreq = getInARowMetric(board, symbol, allowBlanks)
    vsMostInARow, vsMostInARowFreq = getInARowMetric(board,
                                                     vsSymbol,
                                                     allowBlanks)
    if mostInARow is None or vsMostInARow is None:
        value = 0
    else:
        numCols = len(board)
        numRows = len(board[0])
        numSpaces = float(numCols * numRows)
        mostInARowWithFreq = mostInARow + (mostInARowFreq / numSpaces)
        vsMostInARowWithFreq = vsMostInARow + (vsMostInARowFreq / numSpaces)
        value = 0.9 * ((mostInARowWithFreq - vsMostInARowWithFreq) /
                       (mostInARowWithFreq + vsMostInARowWithFreq))
    return value
mostInARowHeuristic = heuristicMaker(mostInARowHeuristic, allowBlanks=False)
mostInARowAllowBlanksHeuristic = heuristicMaker(mostInARowHeuristic,
                                                allowBlanks=True)
