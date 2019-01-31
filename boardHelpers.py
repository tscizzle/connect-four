from collections import defaultdict
import StringIO


def isInBounds(board, colIdx, rowIdx):
    numCols = len(board)
    numRows = len(board[0])
    return 0 <= colIdx < numCols and 0 <= rowIdx < numRows

def getStartsHowManyInARow(board, colIdx, rowIdx, allowBlanks=False):
    symbol = board[colIdx][rowIdx]
    if symbol is None:
        return 0
    bestInARow = 0
    directions = [(1, 0), (1, -1), (0, -1), (-1, -1)]
    for (colStep, rowStep) in directions:
        colCursor = colIdx
        rowCursor = rowIdx
        numInARowSoFar = 0
        while (isInBounds(board, colCursor, rowCursor) and
               (board[colCursor][rowCursor] == symbol or
                (allowBlanks and board[colCursor][rowCursor] is None))):
            if board[colCursor][rowCursor] == symbol:
                numInARowSoFar += 1
            rowCursor = rowCursor + rowStep
            colCursor = colCursor + colStep
        if numInARowSoFar > bestInARow:
            bestInARow = numInARowSoFar
    return bestInARow

def isStartsFourInARow(board, colIdx, rowIdx):
    return getStartsHowManyInARow(board, colIdx, rowIdx) >= 4

def applyMoveToNewBoard(board, colIdx, symbol):
    column = board[colIdx]
    rowIdx = 0
    while rowIdx < len(column):
        if column[rowIdx] is None:
            break
        rowIdx += 1
    newBoard = [
        [symbol if r == rowIdx and c == colIdx else existingSymbol
         for r, existingSymbol in enumerate(column)]
        for c, column in enumerate(board)
    ]
    return newBoard

def getAvailableColumns(board):
    availableCols = []
    for idx, column in enumerate(board):
        if not all(column):
            availableCols.append(idx)
    return availableCols

def getWinner(board):
    numCols = len(board)
    numRows = len(board[0])
    for colIdx in range(numCols):
        for rowIdx in range(numRows):
            if isStartsFourInARow(board, colIdx, rowIdx):
                symbol = board[colIdx][rowIdx]
                return symbol
    return False

def isFull(board):
    return all(all(column) for column in board)

# Heauristic Helpers

def getCenteringMetric(board, symbol):
    middleCol = (len(board) - 1) / 2.0
    dists = [abs(colIdx - middleCol)
             for colIdx, column in enumerate(board) for s in column
             if s == symbol]
    avgDist = sum(dists) / float(len(dists)) if dists else None
    return avgDist

def getInARowMetric(board, symbol, allowBlanks=False):
    inARowCounts = defaultdict(int)
    for colIdx, column in enumerate(board):
        for rowIdx, _ in enumerate(column):
            if board[colIdx][rowIdx] == symbol:
                inARow = getStartsHowManyInARow(board,
                                                colIdx,
                                                rowIdx,
                                                allowBlanks)
                inARowCounts[inARow] += 1
    if len(inARowCounts.keys()) == 0:
        return None, None
    mostInARow = max(inARowCounts.keys())
    mostInARowFreq = inARowCounts[mostInARow]
    return mostInARow, mostInARowFreq

# Printing

def boardStr(board):
    numCols = len(board)
    numRows = len(board[0])
    sio = StringIO.StringIO()
    for rowIdx in reversed(range(numRows)):
        for colIdx in range(numCols):
            symbol = board[colIdx][rowIdx] or '-'
            sio.write(' %s' % symbol)
        sio.write('\n')
    result = sio.getvalue()
    return result
