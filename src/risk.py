from typing import Callable, Sequence, Tuple, Dict
from .pricing import price_from_curve
from .curve import shift_curve

Cashflow = Tuple[float, float]  

def dv01(r_of_t: Callable[[float], float], cashflows: Sequence[Cashflow], bp_step: float = 1.0) -> float:
    """
    DV01 = variation de prix pour un choc de 1 bp
    On bump la courbe de ±bp_step (en bps), DV01 ≈ |P_up - P_down| / (2 * bp_step)
    (Unités: devise par bp)
    """
    # dy = bp_step / 1e4
    # P = price_from_curve(r_of_t, cashflows)
    P_up   = price_from_curve(shift_curve(r_of_t, +bp_step), cashflows)
    P_down = price_from_curve(shift_curve(r_of_t, -bp_step), cashflows)
    # pente ~ (P_up - P_down) / (2*dy). DV01 = |pente| * 1bp
    return abs(P_up - P_down) / (2 * bp_step)

def duration_modified(r_of_t: Callable[[float], float], cashflows: Sequence[Cashflow], bp_step: float = 1.0) -> float:
    """
    D_mod (continu) = (1/P) * dP/dy
    Comme DV01 = P * D_mod * 1e-4, alors D_mod = DV01 / (P * 1e-4)
    """
    P = price_from_curve(r_of_t, cashflows)
    if P == 0.0:
        return 0.0
    dv = dv01(r_of_t, cashflows, bp_step=bp_step)
    return dv / (P * 1e-4)

def convexity(r_of_t: Callable[[float], float], cashflows: Sequence[Cashflow], bp_step: float = 1.0) -> float:
    """
    Convexité (par rapport au 'y' continu): Conv = (1/P) * d2P/dy2.
    Numériquement: d2P ≈ (P_up - 2P + P_down)/dy^2.
    """
    dy = bp_step / 1e4
    P = price_from_curve(r_of_t, cashflows)
    P_up   = price_from_curve(shift_curve(r_of_t, +bp_step), cashflows)
    P_down = price_from_curve(shift_curve(r_of_t, -bp_step), cashflows)
    if P == 0.0:
        return 0.0
    d2P = (P_up - 2 * P + P_down) / (dy * dy)
    return d2P / P

def price_sensitivities(r_of_t: Callable[[float], float], cashflows: Sequence[Cashflow], bp_step: float = 1.0) -> Dict[str, float]:
    """
    Petit utilitaire: renvoie {price, dv01, dmod, conv}.
    """
    P = price_from_curve(r_of_t, cashflows)
    dv = dv01(r_of_t, cashflows, bp_step=bp_step)
    dm = dv / P if P else 0.0
    cv = convexity(r_of_t, cashflows, bp_step=bp_step)
    return {"price": P, "dv01": dv, "dmod": dm, "conv": cv}
