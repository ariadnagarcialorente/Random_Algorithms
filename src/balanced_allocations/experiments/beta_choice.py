import random
import numpy as np

from .base_experiment import BaseExperiment
from .choice_runner import choice_runner

class beta_choice(BaseExperiment): 
    def __init__(self, m: int, n_values: list[int], trials: int, b:int):
        super().__init__("beta_choice")
        self.m = m
        self.n_values = n_values
        self.trials = trials
        self.b = b
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
        #Cases 0 and 1
        if (self.b == 0):
            simulation = choice_runner()
            self.results = simulation.ball_simulator(self.m, self.n_values, self.trials, 1)
        if (self.b == 1):
            simulation = choice_runner()
            self.results = simulation.ball_simulator(self.m, self.n_values, self.trials, 2)

        ##MESS OF A FUNCTION BUT WORKS
        for n in self.n_values:

            gaps = [0] * self.trials
            max_load = [0] * self.trials
            
            for trial in range(self.trials):
                loads = [0] * self.m
                for _ in range(n):
                    p = random.random()
                    if (p <= self.b):
                        bin_idx_1 = random.randint(0, self.m-1)
                        bin_idx_2 = random.randint(0, self.m-1)
                        
                        if loads[bin_idx_1] < loads[bin_idx_2]:
                            bin_idx = bin_idx_1
                        elif loads[bin_idx_1] > loads[bin_idx_2]:
                            bin_idx = bin_idx_2
                        else:
                            bin_idx = random.choice([bin_idx_1, bin_idx_2])
                   
                    else: 
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

    def plot(self, save_folder=None, filename=None, use_3d=False):
        for n in self.n_values:
            if n in self.results:
                print(f"Results for n = {n}")
                print(f"Average Gap: {self.results[n]['avg_gap']}")
                print(f"Std Dev Gap: {self.results[n]['std_gap']}")
                print(f"Average Max Load: {self.results[n]['avg_max_load']}")
                print(f"Std Dev Max Load: {self.results[n]['std_max_load']}")
            else:
                print(f"\nNo results found for n = {n}")

        



