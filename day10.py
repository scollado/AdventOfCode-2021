from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from aocutils.aoc import Exercise
from aocutils.file import get_input_data_filepath

t_PAREN_OPEN = '('
t_PAREN_CLOSE = ')'
t_SQRB_OPEN = '['
t_SQRB_CLOSE = ']'
t_CRLY_OPEN = '{'
t_CRLY_CLOSE = '}'
t_LT_OPEN = '<'
t_GT_CLOSE = '>'

VALID_TOKENS = (
    t_PAREN_OPEN,
    t_PAREN_CLOSE,
    t_SQRB_OPEN,
    t_SQRB_CLOSE,
    t_CRLY_OPEN,
    t_CRLY_CLOSE,
    t_LT_OPEN,
    t_GT_CLOSE,
)


class InvalidTokenError(Exception):
    def __init__(self, token: str, position: int = None) -> None:
        self.token = token

        message = f'Invalid token: {token}'

        if position is not None:
            self.position = position
            message += f' at position {str(position)}'

        super().__init__(message)


class InvalidClosingTokenError(Exception):

    def __init__(self, chunk: NavSubsystemParser.Chunk, token: str, position: int = None) -> None:
        self.chunk = chunk
        self.token = token
        self.expected_token = NavSubsystemParser.CLOSING_TOKENS[chunk.opening_token]
        message = f'Invalid closing token {token}'
        if position is not None:
            self.position = position
            message += f' at position {position}'
        message += f'. Expected token: {self.expected_token}'

        super(InvalidClosingTokenError, self).__init__(message)


class ChunkAlreadyClosedError(Exception):
    pass


class NavSubsystemParser:
    OPENING_TOKENS = {t_PAREN_OPEN, t_SQRB_OPEN, t_CRLY_OPEN, t_LT_OPEN}
    CLOSING_TOKENS = {
        t_PAREN_OPEN: t_PAREN_CLOSE,
        t_SQRB_OPEN: t_SQRB_CLOSE,
        t_CRLY_OPEN: t_CRLY_CLOSE,
        t_LT_OPEN: t_GT_CLOSE
    }

    class Chunk:

        def __init__(self, opening_token: str) -> None:
            if opening_token not in NavSubsystemParser.OPENING_TOKENS:
                raise InvalidTokenError(opening_token)

            self.opening_token = opening_token
            self.closing_token: Optional[NavSubsystemParser.Chunk] = None
            self.parent: Optional[NavSubsystemParser.Chunk] = None
            self.children: list[NavSubsystemParser.Chunk] = []

        def __repr__(self) -> str:
            string_repr = self.opening_token

            for child in self.children:
                string_repr += str(child)

            if self.is_closed():
                string_repr += self.closing_token

            return string_repr

        def close(self, closing_token: str):
            if NavSubsystemParser.CLOSING_TOKENS[self.opening_token] != closing_token:
                raise InvalidClosingTokenError(self, closing_token)
            if self.closing_token is not None:
                raise ChunkAlreadyClosedError

            self.closing_token = closing_token

        def is_closed(self):
            return self.closing_token is not None

        def add_child(self, child: NavSubsystemParser.Chunk):
            if self.is_closed():
                raise ChunkAlreadyClosedError
            child.parent = self
            self.children.append(child)

    @dataclass(repr=False)
    class ParsedLine:

        def __init__(self, chunks: list[NavSubsystemParser.Chunk]) -> None:
            self.chunks = chunks

        def __repr__(self) -> str:
            return ''.join([str(chunk) for chunk in self.chunks])

    @classmethod
    def parse_line(cls, line: str) -> NavSubsystemParser.ParsedLine:
        chunks: list[cls.Chunk] = []
        current_chunk: Optional[cls.Chunk] = None
        for pos, char in enumerate(line):
            if char not in VALID_TOKENS:
                continue

            if current_chunk is None:
                current_chunk = cls.Chunk(char)
                chunks.append(current_chunk)
                continue

            if char in cls.OPENING_TOKENS:
                new_chunk = cls.Chunk(char)
                current_chunk.add_child(new_chunk)
                current_chunk = new_chunk

            if char in list(cls.CLOSING_TOKENS.values()):
                try:
                    current_chunk.close(char)
                except InvalidClosingTokenError as chunk_error:
                    raise InvalidClosingTokenError(
                        chunk=chunk_error.chunk,
                        token=chunk_error.token,
                        position=pos
                    ) from chunk_error

                current_chunk = current_chunk.parent

        return NavSubsystemParser.ParsedLine(chunks)


class LineCompletion:

    def __init__(self, input_chunks: list[NavSubsystemParser.Chunk]) -> None:
        self.input_chunks = input_chunks

    def complete(self):
        completion = ''
        for chunk in reversed(self.input_chunks):
            completion += self._complete_chunk(chunk)
        return completion

    def _complete_chunk(self, chunk: NavSubsystemParser.Chunk) -> str:
        completion = ''
        if chunk.is_closed():
            return completion

        for child in reversed(chunk.children):
            completion += self._complete_chunk(child)

        completion += NavSubsystemParser.CLOSING_TOKENS[chunk.opening_token]
        return completion


class Day10(Exercise):
    PARSING_SCORING_TABLE = {
        t_PAREN_CLOSE: 3,
        t_SQRB_CLOSE: 57,
        t_CRLY_CLOSE: 1197,
        t_GT_CLOSE: 25137
    }

    COMPLETION_SCORING_TABLE = ')]}>'

    def part_one(self) -> int:
        score = 0

        for line in self.input_data:
            try:
                NavSubsystemParser.parse_line(line.strip())
            except InvalidClosingTokenError as closing_error:
                if closing_error.token in set(self.PARSING_SCORING_TABLE.keys()):
                    score += self.PARSING_SCORING_TABLE[closing_error.token]
                else:
                    print(f'Unknown invalid closing token: {closing_error.token}')

        return score

    def part_two(self) -> int:

        incomplete_lines = self.only_incomplete_lines()

        completions = [LineCompletion(line.chunks).complete() for line in incomplete_lines]
        completions_scores = sorted([self.complete_score(completion) for completion in completions])

        return completions_scores[len(completions_scores) // 2]

    def only_incomplete_lines(self) -> list[NavSubsystemParser.ParsedLine]:
        incomplete_lines: list[NavSubsystemParser.ParsedLine] = []
        for line in self.input_data:
            try:
                parsed_line = NavSubsystemParser.parse_line(line.strip())
            except InvalidClosingTokenError:
                continue
            else:
                incomplete_lines.append(parsed_line)
        return incomplete_lines

    def complete_score(self, completion: str) -> int:
        line_score = 0
        for char in completion:
            line_score *= 5
            line_score += 1 + self.COMPLETION_SCORING_TABLE.index(char)
        return line_score


if __name__ == '__main__':
    inputfile_path = get_input_data_filepath(__file__)
    with open(inputfile_path) as input_file:
        exercise = Day10(input_file.readlines())
        exercise.solve_all()
