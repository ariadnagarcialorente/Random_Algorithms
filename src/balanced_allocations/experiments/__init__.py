from .galton_triangle_matrix import GaltonTriangleMatrix
from .galton_binomial import GaltonBinomial
from .binomial_normal import BinomialNormal

EXPERIMENT_REGISTRY = {
    "galton_triangle_matrix": GaltonTriangleMatrix,
    "galton_binomial": GaltonBinomial,
    "binomial_normal": BinomialNormal,
}