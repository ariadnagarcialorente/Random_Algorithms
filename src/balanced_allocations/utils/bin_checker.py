

def max_gap(bins: list[int]) -> float:
    """
    Compute the gap G_n = max_i (X_i - n/m)

    :param bins: list of counts of balls in each bin
    :return: the gap as a float
    """
    n = sum(bins)  # total number of balls
    m = len(bins)  # total number of bins
    avg = n / m  # expected load per bin
    return max(x - avg for x in bins)


def bin_distro_where_n_equal_m(results: list[list[int]], batch_size: int = 1) -> list[int]:
    """
    Extract the bin distribution at the step where n == m.
    :param results: list of bin distributions over time
    :param batch_size: number of balls added per step
    :return: bin distribution when n == m
    """
    m = len(results[0])  # number of bins
    step_index = m // batch_size  # index where n == m
    if step_index < len(results):
        return results[step_index]
    else:
        return results[-1]  # fallback to last step if index out of bounds