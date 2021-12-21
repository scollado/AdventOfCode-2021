from unittest import TestCase

from day14 import Day14, Polymer

EXAMPLE_INPUT = '''
NNCB

CH -> B
HH -> N
CB -> H
NH -> C
HB -> C
HC -> B
HN -> C
NN -> C
BH -> H
NC -> B
NB -> B
BN -> B
BB -> N
BC -> B
CC -> N
CN -> C
'''.strip()

EXPECTED_PART_ONE_RESULT = 1588
EXPECTED_PART_TWO_RESULT = 2188189693529


class TestDay14(TestCase):
    def setUp(self) -> None:
        self.sut = Day14(EXAMPLE_INPUT.split("\n"))

    def test_init_successfully(self):
        self.assertEqual(16, len(self.sut.rules))

    def test_example_steps(self):
        polymer = Polymer(self.sut.polymer_template)
        steps = 10
        self.sut.develop_polymer(polymer, steps)
        self.assertEqual(3073, len(polymer))

    def test_part_one(self):
        self.assertEqual(EXPECTED_PART_ONE_RESULT, self.sut.part_one())

    def test_part_two(self):
        self.assertEqual(EXPECTED_PART_TWO_RESULT, self.sut.part_two())


class TestPolymer(TestCase):

    def test_pairs_extraction(self):
        start = 'NNCB'
        sut = Polymer(start)
        expected_pairs = [
            'NN',
            'NC',
            'CB'
        ]
        self.assertListEqual(expected_pairs, list(sut.pairs))
