import unittest
import move_implementation as mi


class TestGameMoves(unittest.TestCase):
    def test_colorMarbles(self):
        self.assertEqual(mi.colored([[0, 0], [0, 1]], 'W'), True)
        self.assertEqual(mi.colored([[3, 3]], 'B'), False)
        self.assertEqual(mi.colored([[0, 4], [0, 5]], 'W'), False)
        self.assertEqual(mi.colored([[0, 5]], 'X'), False)
        self.assertEqual(mi.colored([[2, 0], [2, 1]], 'E'), False)

    def test_alignedMarbles(self):
        self.assertEqual(mi.chain([[0, 0], [0, 1], [0, 2], [0, 3]]), False)
        self.assertEqual(mi.chain([[0, 0], [0, 2], [1, 3]]), False)
        self.assertEqual(mi.chain([[0, 0], [1, 0], [2, 0]]), False)
        self.assertEqual(mi.chain([[2, 0], [3, 0], [4, 0]]), False)
        self.assertEqual(mi.chain([[0, 5], [0, 6], [0, 7]]), False)
        self.assertEqual(mi.chain([[0, 3], [0, 4], [0, 5]]), False)
        self.assertEqual(mi.chain([[-1, 4], [0, 4], [1, 4]]), False)

    def test_aligned(self):
        self.assertEqual(mi.aligned([1, 1], [-1, -1]), True)
        self.assertEqual(mi.aligned([1, 0], [-1, 0]), True)
        self.assertEqual(mi.aligned([0, 1], [0, -1]), True)
        self.assertEqual(mi.aligned([0, 1], [1, 0]), False)
    
    def test_linemove(self):
        self.assertEqual(mi.lineMove([[0, 0], [1, 1], [2, 2]], "SE")[0], True)
        self.assertEqual(mi.lineMove([[7, 4], [6, 4]], "NE")[0], True)
        self.assertEqual(mi.lineMove([[6, 4]], "NE"), False)
        self.assertEqual(mi.lineMove([[8, 4], [7, 4]], "SW"), False)
        self.assertEqual(mi.lineMove([[1, 5], [2, 5]], "NE"), False)
        self.assertEqual(mi.lineMove([[0, 0], [1, 1]], "SE"), False)
        self.assertEqual(mi.lineMove([[1, 1]], "SW"), False)

    def test_arrowmove(self):
        self.assertEqual(mi.arrowMove([[2, 2], [2, 3], [2, 4]], "SE")[0], True)
        self.assertEqual(mi.arrowMove([[1, 2], [1, 3]], "SW"), False)
        self.assertEqual(mi.arrowMove([[8, 4], [7, 4]], "NW"), False)
        self.assertEqual(mi.arrowMove([[8, 4], [7, 4]], "SE"), False)
    
    def test_solomove(self):
        self.assertEqual(mi.soloMove([[0, 0]], "NW"), False)
        self.assertEqual(mi.soloMove([[2, 2], [1, 1]], "SE"), False)
        self.assertEqual(mi.soloMove([[8, 8]], "SE"), False)
        self.assertEqual(mi.soloMove([[8, 4]], "SW"), False)
        self.assertEqual(mi.soloMove([[0, 4]], "E"), False)
        self.assertEqual(mi.soloMove([[8, 4]], "NW"), False)

    def test_action(self):
        self.assertEqual(mi.action([[8, 5], [7, 5], [6, 5]], "NE", "B")[0], True)
        

    def test_possibleChainFromPoint(self):
        self.assertEqual(mi.possibleChainsFromPoint(2, [2, 3], None, None, [], [], list(mi.moves.values()))[0], True)
        self.assertEqual(mi.possibleChainsFromPoint(3, [0, 0], None, None, [], [], list(mi.moves.values()))[0], True)
        self.assertEqual(mi.possibleChainsFromPoint(3, [2, 3], None, None, [], [], list(mi.moves.values()))[0], True)
        self.assertEqual(mi.possibleChainsFromPoint(0, [2, 3], None, None, [], [], list(mi.moves.values())), False)
        self.assertEqual(mi.possibleChainsFromPoint(4, [2, 3], None, None, [], [], list(mi.moves.values())), False)


if __name__ == '__main__':
    unittest.main()
