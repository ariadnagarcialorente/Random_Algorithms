

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


def bin_distro_where_n_equal_m(bin_distros: list[list[int]]) -> list[int]:
    """
    Find the bin distribution when the number of balls equals the number of bins.

    :param bin_distros: list of bin states over time; each entry is a list[int] for that time step
    :return: the distribution at the step where total balls = number of bins
    """
    for distro in bin_distros:
        if sum(distro) >= len(distro):
            return distro
    raise ValueError("No distribution found where number of balls equals number of bins")