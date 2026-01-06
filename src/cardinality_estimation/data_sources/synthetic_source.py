from pathlib import Path
import random

from .base import DataStreamSource


BOOK_FOLDER = Path(__file__).parents[3] / 'data' / 'generated'

class Synthetic_source(DataStreamSource):
    def __init__(self, n_distinct: int, N_length: int, alpha: float, output_file: str):
        self.n_distinct = n_distinct
        self.N_length = N_length
        self.alpha = alpha
        self.output_path = BOOK_FOLDER / output_file
        self._length = None  # cache
        
        self.output_path.parent.mkdir(parents=True, exist_ok=True)
        
        self._generate_file()

    def _generate_file(self):
        
        sum_term = 0.0
        for i in range(1, self.n_distinct + 1):
            sum_term += i ** (-self.alpha)

        c_n = 1.0 / sum_term

        cumulative_prob = []
        cumulative = 0.0
        for i in range(1, self.n_distinct + 1):
            prob = c_n / (i ** self.alpha)
            cumulative += prob
            cumulative_prob.append(cumulative)
        
        # Generate strings according to Zipfian distribution
        with open(self.output_path, 'w') as f:
            for i in range(self.N_length):
                string_index = self._sample_from_distribution(cumulative_prob)
                f.write(f"string_{string_index}")
                if i < self.N_length - 1:
                    f.write('\n')
    

    def _sample_from_distribution(self, probability):
        random_value = random.random()

        left = 0
        right = len(probability) - 1
        
        while left < right:
            mid = (left + right) // 2
            if random_value < probability[mid]:
                right = mid
            else:
                left = mid + 1
        
        return left

    def __iter__(self):
        with self.output_path.open() as f:
            for line in f:
                yield line.strip()

    def __len__(self):
        """
        Number of elements in the data stream (lines in the book).
        Computed lazily and cached.
        """
        if self._length is None:
            with self.output_path.open() as f:
                self._length = sum(1 for _ in f)
        return self._length