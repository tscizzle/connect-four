"""
To run these tests, from the root directory connect-four/ run

    python3 -m tests.testBoardHelpers

"""


import boardHelpers

import unittest


class TestBoardHelpers(unittest.TestCase):
    def emptyBoard(self):
        return [[None for _ in range(6)] for _ in range(7)]

    def test_isInBounds(self):
        board = self.emptyBoard()
        self.assertTrue(boardHelpers.isInBounds(board, 0, 0))
        self.assertTrue(boardHelpers.isInBounds(board, 6, 5))
        self.assertFalse(boardHelpers.isInBounds(board, 7, 0))
        self.assertFalse(boardHelpers.isInBounds(board, 0, 6))
        self.assertFalse(boardHelpers.isInBounds(board, -1, 2))
        self.assertFalse(boardHelpers.isInBounds(board, 2, -1))

    def test_getStartsHowManyInARow(self):
        board = self.emptyBoard()
        self.assertEqual(boardHelpers.getStartsHowManyInARow(board, 0, 0), 0)
        board[0][0] = "X"
        self.assertEqual(boardHelpers.getStartsHowManyInARow(board, 0, 0), 1)
        board[1][1] = "X"
        self.assertEqual(boardHelpers.getStartsHowManyInARow(board, 1, 1), 2)
        board[2][2] = "X"
        board[3][3] = "X"
        self.assertEqual(boardHelpers.getStartsHowManyInARow(board, 3, 3), 4)

    def test_isStartsFourInARow(self):
        board = self.emptyBoard()
        self.assertEqual(boardHelpers.getStartsHowManyInARow(board, 0, 0), 0)
        board[0][0] = "X"
        self.assertEqual(boardHelpers.getStartsHowManyInARow(board, 0, 0), 1)
        board[1][1] = "X"
        self.assertEqual(boardHelpers.getStartsHowManyInARow(board, 1, 1), 2)
        board[2][2] = "X"
        board[3][3] = "X"
        self.assertEqual(boardHelpers.getStartsHowManyInARow(board, 3, 3), 4)


if __name__ == "__main__":
    unittest.main()
