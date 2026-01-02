import random

class ZipfianGenerator:

    def __init__(self, n_distinct: int, N_length: int, alpha: float, output_file=str):
        self.n_distinct = n_distinct
        self.N_length = N_length
        self.alpha = alpha

        total = 0

        for i in range(1, n_distinct + 1):
            total += 1.0 / (i ** -alpha)
        
        probability = []
        for i in range(1, n_distinct + 1):
            aux = total / (i ** alpha)
            probability.append(aux)
        
        with open(output_file, 'w') as f:
            for i in range(N_length):
                
                string_index = self.sample_from_distribution(probability)
                
                f.write(f"string_{string_index}")
                
                if i < N_length - 1:
                    f.write('\n')

    def sample_from_distribution(self, probability):
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