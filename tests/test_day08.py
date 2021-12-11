from unittest import TestCase

from day08 import Day08, SegmentWiring, SegmentDisplay, EntryLine

'''
  0:      1:      2:      3:      4:
 aaaa    ....    aaaa    aaaa    ....
b    c  .    c  .    c  .    c  b    c
b    c  .    c  .    c  .    c  b    c
 ....    ....    dddd    dddd    dddd
e    f  .    f  e    .  .    f  .    f
e    f  .    f  e    .  .    f  .    f
 gggg    ....    gggg    gggg    ....

  5:      6:      7:      8:      9:
 aaaa    aaaa    aaaa    aaaa    aaaa
b    .  b    .  .    c  b    c  b    c
b    .  b    .  .    c  b    c  b    c
 dddd    dddd    ....    dddd    dddd
.    f  e    f  .    f  e    f  .    f
.    f  e    f  .    f  e    f  .    f
 gggg    gggg    ....    gggg    gggg

'''

EXAMPLE_INPUT_LINE = "acedgfb cdfbe gcdfa fbcad dab cefabd cdfgeb eafb cagedb ab | cdfeb fcadb cdfeb cdbaf"

EXAMPLE_INPUT = """
be cfbegad cbdgef fgaecd cgeb fdcge agebfd fecdb fabcd edb | fdgacbe cefdb cefbgd gcbe
edbfga begcd cbg gc gcadebf fbgde acbgfd abcde gfcbed gfec | fcgedb cgb dgebacf gc
fgaebd cg bdaec gdafb agbcfd gdcbef bgcad gfac gcb cdgabef | cg cg fdcagb cbg
fbegcd cbd adcefb dageb afcb bc aefdc ecdab fgdeca fcdbega | efabcd cedba gadfec cb
aecbfdg fbg gf bafeg dbefa fcge gcbea fcaegb dgceab fcbdga | gecf egdcabf bgf bfgea
fgeab ca afcebg bdacfeg cfaedg gcfdb baec bfadeg bafgc acf | gebdcfa ecba ca fadegcb
dbcfg fgd bdegcaf fgec aegbdf ecdfab fbedc dacgb gdcebf gf | cefg dcbef fcge gbcadfe
bdfegc cbegaf gecbf dfcage bdacg ed bedf ced adcbefg gebcd | ed bcgafe cdgba cbgef
egadfb cdbfeg cegd fecab cgb gbdefca cg fgcdab egfdb bfceg | gbdfcae bgc cg cgb
gcafb gcf dcaebfg ecagb gf abcdeg gaef cafbge fdbac fegbdc | fgae cfgab fg bagce
""".strip()

EXPECTED_UNIQUE_SEGMENTS_SIZES = 26
EXPECTED_OUTPUT_SUM = 61229


class TestDay08(TestCase):
    def test_part_one(self):
        sut = Day08(EXAMPLE_INPUT.split("\n"))

        self.assertEqual(EXPECTED_UNIQUE_SEGMENTS_SIZES, sut.part_one())

    def test_part_two(self):
        sut = Day08(EXAMPLE_INPUT.split("\n"))
        self.assertEqual(EXPECTED_OUTPUT_SUM, sut.part_two())


class TestSegmentDisplay(TestCase):
    EXEMPLE_WIRING = SegmentWiring(
        top='a', top_right='c', bottom_right='f', bottom='g',
        bottom_left='e', top_left='b', middle='d')

    def setUp(self) -> None:
        super().setUp()

        entry = EntryLine(EXAMPLE_INPUT_LINE)
        self.display = SegmentDisplay(entry.decode_segments_wiring())

    def test_convert_signal_cdfeb(self):
        self.assertEqual('5', self.display.convert_signal('cdfeb'))

    def test_convert_signal_fcadb(self):
        self.assertEqual('3', self.display.convert_signal('fcadb'))

    def test_convert_signal_cdbaf(self):
        self.assertEqual('3', self.display.convert_signal('cdbaf'))

    def test_display_zero(self):
        zero = ''' aaaa 
b    c
b    c
 .... 
e    f
e    f
 gggg '''
        self.assertEqual(zero, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(0))

    def test_display_one(self):
        one = ''' .... 
.    c
.    c
 .... 
.    f
.    f
 .... '''
        self.assertEqual(one, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(1))

    def test_display_two(self):
        two = ''' aaaa 
.    c
.    c
 dddd 
e    .
e    .
 gggg '''
        self.assertEqual(two, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(2))

    def test_display_three(self):
        three = ''' aaaa 
.    c
.    c
 dddd 
.    f
.    f
 gggg '''
        self.assertEqual(three, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(3))

    def test_display_four(self):
        four = ''' .... 
b    c
b    c
 dddd 
.    f
.    f
 .... '''
        self.assertEqual(four, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(4))

    def test_display_five(self):
        five = ''' aaaa 
b    .
b    .
 dddd 
.    f
.    f
 gggg '''
        self.assertEqual(five, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(5))

    def test_display_six(self):
        six = ''' aaaa 
b    .
b    .
 dddd 
e    f
e    f
 gggg '''
        self.assertEqual(six, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(6))

    def test_display_seven(self):
        seven = ''' aaaa 
.    c
.    c
 .... 
.    f
.    f
 .... '''
        self.assertEqual(seven, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(7))

    def test_display_eight(self):
        eight = ''' aaaa 
b    c
b    c
 dddd 
e    f
e    f
 gggg '''
        self.assertEqual(eight, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(8))

    def test_display_nine(self):
        nine = ''' aaaa 
b    c
b    c
 dddd 
.    f
.    f
 gggg '''
        self.assertEqual(nine, SegmentDisplay(self.EXEMPLE_WIRING).display_digit(9))


class TestEntryLine(TestCase):
    EXPECTED_SEGMENT_WIRING = SegmentWiring(
        top='d',
        top_right='a',
        bottom_right='b',
        bottom='c',
        bottom_left='g',
        top_left='e',
        middle='f'
    )

    def test_decode_segment_wiring(self):
        tested_line = EntryLine(EXAMPLE_INPUT_LINE)
        self.assertEqual(self.EXPECTED_SEGMENT_WIRING, tested_line.decode_segments_wiring())

    def test_decode_example_line_output(self):
        tested_line = EntryLine(EXAMPLE_INPUT_LINE)
        self.assertEqual('5353', tested_line.output_value())
