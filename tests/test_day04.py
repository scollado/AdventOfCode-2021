from unittest import TestCase

from day04 import BingoCard, BingoSystem, Day04

INPUT_FILE = """
7,4,9,5,11,17,23,2,0,14,21,24,10,16,13,6,15,25,12,22,18,20,8,19,3,26,1

22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19

 3 15  0  2 22
 9 18 13 17  5
19  8  7 25 23
20 11 10 24  4
14 21 16 12  6

14 21 17 24  4
10 16 15  9 19
18  8 23 26 20
22 11 13  6  5
 2  0 12  3  7
""".lstrip()

TEST_CARD = """
22 13 17 11  0
 8  2 23  4 24
21  9 14 16  7
 6 10  3 18  5
 1 12 20 15 19
""".lstrip()

TEST_CARD_LAST_COLUMN_DRAW = '0,24,7,5,19'
TEST_CARD_SECOND_ROW_DRAW = '8,2,23,4,24'

EXPECTED_WINNING_ROW = 0

EXPECTED_UNCHECKED_SUM = 188
EXPECTED_LAST_DRAWN = 24

EXPECTED_LAST_WINNING_DRAW = 13
EXPECTED_LAST_WINNING_UNCHECKED_SUM = 148


class TestDay04(TestCase):
    def test_part_one(self):
        sut = Day04(INPUT_FILE.split("\n"))
        self.assertEqual(EXPECTED_LAST_DRAWN * EXPECTED_UNCHECKED_SUM, sut.part_one())

    def test_part_two(self):
        pass


class TestBingoCard(TestCase):

    def setUp(self) -> None:
        super().setUp()
        self.sut = BingoCard(
            tuple(
                tuple(int(number) for number in row.strip().split(sep=' ') if number) for row in TEST_CARD.split("\n"))
        )

    def test_draw_known_number(self):
        row, column = self.sut.draw(11)
        self.assertEqual(0, row)
        self.assertEqual(3, column)

    def test_draw_unknown_number(self):
        row, column = self.sut.draw(99)
        self.assertIsNone(row)
        self.assertIsNone(column)

    def test_unchecked_numbers(self):
        drawn_numbers = [
            22, 13, 17, 11, 0,
            8, 2, 23, 4, 24,
            21, 9, 14, 16, 7,
            6, 10, 3, 18, 5,
            1, 12
        ]
        for number in drawn_numbers:
            self.sut.draw(number)

        self.assertTupleEqual((20, 15, 19), self.sut.unchecked_numbers())

    def test_winning_column(self):
        for number in (17, 23, 14, 3, 20):
            self.sut.draw(number)

        self.assertTrue(self.sut.is_winning_column(2))

    def test_winning_row(self):
        for number in [21, 9, 14, 16, 7]:
            self.sut.draw(number)

        self.assertTrue(self.sut.is_winning_row(2))


class TestBingoSystem(TestCase):

    def test_init_with_three_cards(self):
        sut = BingoSystem(INPUT_FILE.split("\n"))
        self.assertEqual(3, len(sut.cards))

    def test_example_draw(self):
        sut = BingoSystem(INPUT_FILE.split("\n"))

        winning_card, last_drawn_number = sut.draw()[0]

        self.assertIsNotNone(winning_card)
        self.assertTrue(winning_card.is_winning_row(EXPECTED_WINNING_ROW))
        self.assertEqual(EXPECTED_LAST_DRAWN, last_drawn_number)
        self.assertEqual(EXPECTED_UNCHECKED_SUM, sum(winning_card.unchecked_numbers()))

    def test_example_draw_last_winning_card(self):
        sut = BingoSystem(INPUT_FILE.split("\n"))

        winning_order = sut.draw()

        self.assertGreater(len(winning_order), 0)
        last_winning_card: BingoCard
        last_winning_card, last_winning_draw = winning_order[-1]
        self.assertEqual(EXPECTED_LAST_WINNING_DRAW, last_winning_draw)
        self.assertEqual(EXPECTED_LAST_WINNING_UNCHECKED_SUM, sum(last_winning_card.unchecked_numbers()))

    def test_draw_with_winning_row(self):
        input_data = f"""{TEST_CARD_SECOND_ROW_DRAW}
        
        {TEST_CARD}
        """

        sut = BingoSystem(input_data.split("\n"))
        winning_card, _ = sut.draw()[0]
        self.assertIsNotNone(winning_card)
        self.assertTrue(winning_card.is_winning_row(1))

    def test_draw_with_winning_column(self):
        input_data = f"""{TEST_CARD_LAST_COLUMN_DRAW}
        
        {TEST_CARD}
        """

        sut = BingoSystem(input_data.split("\n"))
        winning_card, _ = sut.draw()[0]
        self.assertIsNotNone(winning_card)
        self.assertTrue(winning_card.is_winning_column(4))

    def test_draw_without_winning_card(self):
        input_data = f"""0,1,2,3,4
        
        {TEST_CARD}
        """

        sut = BingoSystem(input_data.split("\n"))
        winning_cards = sut.draw()
        self.assertEqual(0, len(winning_cards))
