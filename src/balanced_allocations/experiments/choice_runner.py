import random
import numpy as np


class choice_runner:
    def ball_simulator(self, m: int, n_values: list[int], trials: int, dimensions: int, batch: int): 
        results = {}
        for n in n_values:
            gaps = [0] * trials
            max_load = [0] * trials
            for trial in range(trials):
                loads = [0] * m
                batch_loads = [0]*m
                for ball in range(n):
                    if(ball%batch == 0):
                        ## act batch loads
                        for j in range(m):
                            loads[j] = loads[j] + batch_loads[j] 
                            batch_loads[j] = 0
     
                    act = random.randint(0, m-1)
                    minimum = loads[act]
                    idx = [act]

                    for i in range(dimensions-1):
                        act = random.randint(0, m-1)
                        if(loads[act] < minimum):
                            minimum = loads[act]
                            idx = [act]
                        elif(loads[act] == minimum):
                            idx = idx + [act]
                    
                    bin_idx = random.choice(idx)
                    batch_loads[bin_idx] += 1
                    
                #last act
                for j in range(m):
                    loads[j] = loads[j] + batch_loads[j]      
                max_load[trial] = max(loads)
                gaps[trial] = max_load[trial] - n/m
            results[n] = {
                'avg_gap' : np.mean(gaps),
                'std_gap' : np.std(gaps),
                'gap_values' : gaps,
                'max_loads_values' : max_load,
                'avg_max_load' : np.mean(max_load),
                'std_max_load' : np.std(max_load)
            } 
        return results