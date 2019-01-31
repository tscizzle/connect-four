import boardHelpers as bh

import unittest


class TestBoardHelpers(unittest.TestCase):
    def emptyBoard(self):
        return [[None for _ in range(6)] for _ in range(7)]

    def test_isInBounds(self):
        board = self.emptyBoard()
        self.assertTrue(bh.isInBounds(board, 0, 0))
        self.assertTrue(bh.isInBounds(board, 6, 5))
        self.assertFalse(bh.isInBounds(board, 7, 0))
        self.assertFalse(bh.isInBounds(board, 0, 6))
        self.assertFalse(bh.isInBounds(board, -1, 2))
        self.assertFalse(bh.isInBounds(board, 2, -1))

    def test_getStartsHowManyInARow(self):
        board = self.emptyBoard()
        self.assertEqual(bh.getStartsHowManyInARow(board, 0, 0), 0)
        board[0][0] = 'X'
        self.assertEqual(bh.getStartsHowManyInARow(board, 0, 0), 1)
        board[1][1] = 'X'
        self.assertEqual(bh.getStartsHowManyInARow(board, 1, 1), 2)
        board[2][2] = 'X'
        board[3][3] = 'X'
        self.assertEqual(bh.getStartsHowManyInARow(board, 3, 3), 4)

    def test_isStartsFourInARow(self):
        board = self.emptyBoard()
        self.assertEqual(bh.getStartsHowManyInARow(board, 0, 0), 0)
        board[0][0] = 'X'
        self.assertEqual(bh.getStartsHowManyInARow(board, 0, 0), 1)
        board[1][1] = 'X'
        self.assertEqual(bh.getStartsHowManyInARow(board, 1, 1), 2)
        board[2][2] = 'X'
        board[3][3] = 'X'
        self.assertEqual(bh.getStartsHowManyInARow(board, 3, 3), 4)


if __name__ == '__main__':
    unittest.main()
