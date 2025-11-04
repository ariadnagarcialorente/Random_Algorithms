import random
import numpy as np

from .base_experiment import BaseExperiment

class OneChoice: 
    def __init__(self, m: int, n_values: list[int], trials: int):
        super().__init__("one_choice")
        self.m = m
        self.n_values = n_values
        self.trials = trials
        self.results = {}  
        '''
            results{
                n: {
                For the study of the gap:
                    avg_gap,
                    std_gap,
                    gap_values,
                For the study of the load;
                    max_loads_values,
                    avg_max_load,
                    std_max_load
                }
                for n in n_values
            }
        '''
        #self.max_load = [] substituted by results
        #self.gap= []  substituted by results

    def run(self):

        for n in self.n_values:
            gaps = [0] * self.trials
            max_load = [0] * self.trials
            for trial in range(self.trials):
                loads = [0] * self.m
                for _ in range(n):
                    bin_idx = random.randint(0, self.m-1)
                    loads[bin_idx] += 1
                max_load[trial] = max(loads)
                gaps[trial] = max_load[trial] - n/self.m
            self.results[n] = {
                'avg_gap' : np.mean(gaps),
                'std_gap' : np.std(gaps),
                'gap_values' : gaps,
                'max_loads_values' : max_load,
                'avg_max_load' : np.mean(max_load),
                'std_max_load' : np.std(max_load)
            } 

        



