from pathlib import Path

from .base import DataStreamSource


BOOK_FOLDER = Path(__file__).parents[3] / 'data' / 'books'

class BookSource(DataStreamSource):
    def __init__(self, book_name: str):
        self.book_path = BOOK_FOLDER / f'{book_name}.txt'

    def __iter__(self):
        with self.book_path.open() as f:
            for line in f:
                yield line.strip()