from typing import Callable, Sequence, Tuple
from .curve import discount_factor

Cashflow = Tuple[float, float]

def price_from_curve(r_of_t: Callable[[float], float], cashflows: Sequence[Cashflow]) -> float:
    """actualiser une liste de flux à partir d'une courbe de taux zero-coupon

    Args:
        r_of_t (Callable[[float], float]): une fonction de coure zero qui donne le taux continue au temps t
        cashflows (Sequence[Cashflow]): liste de tuples (t, cf)

    Returns:
        float: somme des flux actualisés
    """
    total = 0.0
    for t, cf in cashflows:
        if t<= 0:
            raise ValueError("chaque échéance t doit être > 0")
        total += cf * discount_factor(r_of_t, t)
    return float(total)


