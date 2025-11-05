from .base_experiment import BaseExperiment
from .choice_runner import choice_runner

class d_choice(BaseExperiment): 
    def __init__(self, m: int, n_values: list[int], trials: int, d: int):
        super().__init__("d_choice")
        self.m = m
        self.n_values = n_values
        self.trials = trials
        self.d = d
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
        simulation = choice_runner()
        self.results = simulation.ball_simulator(self.m, self.n_values, self.trials, self.d, 1)
    
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

        



