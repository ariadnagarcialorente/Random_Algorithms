from pathlib import Path

from .base import DataStreamSource


BOOK_FOLDER = Path(__file__).parents[3] / 'data' / 'books'

class BookSource(DataStreamSource):
    def __init__(self, book_name: str):
        self.book_path = BOOK_FOLDER / f'{book_name}.txt'
        self._length = None  # cache

    def __iter__(self):
        with self.book_path.open() as f:
            for line in f:
                yield line.strip()

    def __len__(self):
        """
        Number of elements in the data stream (lines in the book).
        Computed lazily and cached.
        """
        if self._length is None:
            with self.book_path.open() as f:
                self._length = sum(1 for _ in f)
        return self._length