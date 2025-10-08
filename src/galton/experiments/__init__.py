from src.galton.experiments.galton_triangle_matrix import GaltonTriangleMatrix
from src.galton.experiments.galton_binomial import GaltonBinomial
from src.galton.experiments.binomial_normal import BinomialNormal

EXPERIMENT_REGISTRY = {
    "galton_triangle_matrix": GaltonTriangleMatrix,
    "galton_binomial": GaltonBinomial,
    "binomial_normal": BinomialNormal,
}
