import random
import numpy as np

class ChoiceRunner:
    def ball_simulator(self, m: int, n_values: list[int], trials: int, 
                       dimensions: int, batch: int): 
        results = {}
        
        for n in n_values:
            gaps = [0] * trials
            max_loads = [0] * trials
            
            for trial in range(trials):
                loads = [0] * m
                batch_loads = [0] * m
                
                for ball in range(n):
                    # Dimensions, now with choice functions
                    sampled_bins = np.random.choice(m, size=dimensions, replace=True)
                    min_load = loads[sampled_bins[0]]
                    candidates = [sampled_bins[0]]
                    
                    for bin_idx in sampled_bins[1:]:
                        if loads[bin_idx] < min_load:
                            min_load = loads[bin_idx]
                            candidates = [bin_idx]
                        elif loads[bin_idx] == min_load:
                            candidates.append(bin_idx)
                    
                    chosen_bin = random.choice(candidates)
                    batch_loads[chosen_bin] += 1
                    
                    # Batching
                    if (ball + 1) % batch == 0:
                        loads += batch_loads
                        batch_loads = [0] * m
                
                # Last act
                loads += batch_loads
                
                max_loads[trial] = np.max(loads)
                gaps[trial] = max_loads[trial] - n / m
            
            results[n] = {
                'avg_gap': np.mean(gaps),
                'std_gap': np.std(gaps),
                'gap_values': gaps.tolist(),
                'max_loads_values': max_loads.tolist(),
                'avg_max_load': np.mean(max_loads),
                'std_max_load': np.std(max_loads)
            }
        
        return results