from unittest import TestCase

from day10 import NavSubsystemParser, InvalidClosingTokenError, Day10, LineCompletion

EXAMPLE_INPUT = '''
[({(<(())[]>[[{[]{<()<>>
[(()[<>])]({[<{<<[]>>(
{([(<{}[<>[]}>{[]{[(<()>
(((({<>}<{<{<>}{[]{[]{}
[[<[([]))<([[{}[[()]]]
[{[{({}]{}}([{[{{{}}([]
{<[[]]>}<{[{[{[]{()[[[]
[<(<(<(<{}))><([]([]()
<{([([[(<>()){}]>(<<{{
<{([{{}}[<[[[<>{}]]]>[]]
'''.strip()

EXPECTED_SCORE_PART_ONE = 26397
EXPECTED_SCORE_PART_TWO = 288957

EXPECTED_INCOMPLETE_LINES = [
    '[({(<(())[]>[[{[]{<()<>>',
    '[(()[<>])]({[<{<<[]>>(',
    '(((({<>}<{<{<>}{[]{[]{}',
    '{<[[]]>}<{[{[{[]{()[[[]',
    '<{([{{}}[<[[[<>{}]]]>[]]'
]


class TestDay10(TestCase):

    def setUp(self) -> None:
        self.sut = Day10(EXAMPLE_INPUT.split("\n"))

    def test_part_one(self):
        self.assertEqual(EXPECTED_SCORE_PART_ONE, self.sut.part_one())

    def test_part_two(self):
        self.assertEqual(EXPECTED_SCORE_PART_TWO, self.sut.part_two())

    def test_only_incomplete_lines_length(self):
        lines = self.sut.only_incomplete_lines()
        print(lines)
        self.assertEqual(5, len(lines))
        lines = [str(line) for line in lines]
        self.assertListEqual(sorted(EXPECTED_INCOMPLETE_LINES), sorted(lines))

    def test_completion_scoring(self):
        self.assertEqual(288957, self.sut.complete_score('}}]])})]'))
        self.assertEqual(5566, self.sut.complete_score(')}>]})'))
        self.assertEqual(1480781, self.sut.complete_score('}}>}>))))'))


class TestNavSubsystemParserChunks(TestCase):

    def test_flattening_single_incomplete_chunk_to_string(self):
        input_str = '['
        sut = NavSubsystemParser.Chunk(input_str)

        self.assertEqual(input_str, str(sut))

    def test_flattening_single_closed_chunk_to_string(self):
        opening_char = '['
        closing_char = ']'
        sut = NavSubsystemParser.Chunk(opening_char)
        sut.close(closing_char)

        self.assertEqual(opening_char + closing_char, str(sut))

    def test_flattening_nested_incomplete_chunks_to_string(self):
        root_opening = '['
        child_opening = '<'
        grand_child_opening = '('

        sut = NavSubsystemParser.Chunk(root_opening)
        child = NavSubsystemParser.Chunk(child_opening)
        grand_child = NavSubsystemParser.Chunk(grand_child_opening)
        child.add_child(grand_child)
        sut.add_child(child)

        self.assertEqual(root_opening + child_opening + grand_child_opening, str(sut))

    def test_flattening_nested_partially_complete_chunks_to_string(self):
        root_opening = '['
        child_opening = '<'
        grand_child_opening = '('
        grand_child_closing = ')'

        sut = NavSubsystemParser.Chunk(root_opening)
        child = NavSubsystemParser.Chunk(child_opening)
        grand_child = NavSubsystemParser.Chunk(grand_child_opening)
        grand_child.close(grand_child_closing)
        child.add_child(grand_child)
        sut.add_child(child)

        self.assertEqual(root_opening + child_opening + grand_child_opening + grand_child_closing, str(sut))

    def test_flattening_example_comple_line(self):
        input_str = '[({(<(())[]>[[{[]{<()<>>'
        self.assertEqual(input_str, str(NavSubsystemParser.parse_line(input_str)))


class TestNavSubsystemParser(TestCase):

    def test_parse_line_with_several_root_chunks(self):
        parsed_line = NavSubsystemParser.parse_line('()[]<>{[]}')
        self.assertEqual(4, len(parsed_line.chunks))

    def test_parse_line_fails_with_example_1(self):
        self.assertRaises(InvalidClosingTokenError, NavSubsystemParser.parse_line, '{([(<{}[<>[]}>{[]{[(<()>')

    def test_parse_line_failure_reports_curly_bracket(self):
        expected_token = '}'
        try:
            NavSubsystemParser.parse_line('{([(<{}[<>[]}>{[]{[(<()>')
        except InvalidClosingTokenError as error:
            print(error)
            self.assertEqual(expected_token, error.token)
        else:
            self.fail('Should raise InvalidClosingTokenError')


class TestLineCompletion(TestCase):
    def test_complete_only_root(self):
        incomplete_root = '{'
        parsed_line = NavSubsystemParser.parse_line(incomplete_root)

        sut = LineCompletion(parsed_line.chunks)
        self.assertEqual('}', sut.complete())

    def test_nested_chunks(self):
        incomplete_line = '[<<>{('
        parsed_line = NavSubsystemParser.parse_line(incomplete_line)

        sut = LineCompletion(parsed_line.chunks)
        self.assertEqual(')}>]', sut.complete())
