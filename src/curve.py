import numpy as np
from typing import Callable, Sequence

def build_zero_curve(mats_years: Sequence[float], yields_cc: Sequence[float]) -> Callable[[float], float]:
    """construire r(t) (taux continu) par interpolation log-linéaire sur ln(DF) 

    Args:
        mats_years (Sequence[float]): maturités croissantes en années
        yields_cc (Sequence[float]): taux continus correspondants

    Returns:
        r_of_t(t): fonction renvoyant le taux continu pour n'importe quel t > 0
    """
    mats = np.asarray(mats_years, dtype=float)
    r = np.asarray(yields_cc, dtype=float)

    if mats.ndim != 1 or r.ndim != 1 or len(mats) != len(r):
        raise ValueError("mats_years et yields_cc doivent être 1D de même longueur")
    if not np.all(np.diff(mats) > 0):
        raise ValueError("mats_years doivent être croissantes")
    
    # formule taux continu : DF(T) = exp(-rT) ==> lnDF(T) = -rT
    lnDF = -r * mats
    def r_of_t(t: float) -> float:
        # cette fonction va construire une courbe de taux ZC même pour des maturités intermédiaires au-delà de la dernière observée
        t = float(t)
        if t <= 0:
            raise ValueError("t doit être > 0 en années") 
        # extrapolation courte / petite maturité : le taux est approché linéairement depuis l'origine
        if t <= mats[0]:
            lnDF_t = lnDF[0] * (t / mats[0])
        # extrapolation longue : on prolonge la courbe à plat
        elif t >= mats[-1]:
            lnDF_t = lnDF[-1] * (t / mats[-1])
        else:
            i = np.searchsorted(mats, t) - 1 
            w = (t - mats[i] / (mats[i+1] - mats[i]))
            lnDF_t = (1 - w) * lnDF[i] + w * lnDF[i+1]

        return -lnDF_t / t
    return r_of_t

def discount_factor(r_of_t: Callable[[float], float], t: float) -> float:
    return float(np.exp(-r_of_t(float(t)) * float(t)))
def shift_curve(r_of_t: Callable[[float], float], shift_bps: float) -> Callable[[float], float]:
    dy = shift_bps / 1e4
    return lambda tt: r_of_t(tt) + dy

