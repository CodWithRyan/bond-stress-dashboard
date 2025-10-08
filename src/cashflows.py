from __future__ import annotations
import datetime as dt 
from typing import List, Tuple

Cashflow = Tuple[float, float]

# _____________Dates utilitaires______________

def to_date(s: str) -> dt.date:
    """'YYYY-MM-DD' -> date"""
    return dt.date.fromisoformat(s)

def yearfrac_act365(start: dt.date, end: dt.date) -> float:
    """ACT/365 Fixed: (jours / 365)."""
    if end < start:
        raise ValueError("end < start")
    return (end - start).days / 365.0

def add_months(d: dt.date, months: int) -> dt.date:
    """Ajoute un nombre de mois à une date (sans dépendance externe)."""
    y = d.year + (d.month - 1 + months) // 12
    m = (d.month - 1 + months) % 12 + 1
    # clamp jour à la fin du mois si besoin
    last_day = _last_day_of_month(y, m)
    day = min(d.day, last_day)
    return dt.date(y, m, day)

def _last_day_of_month(y: int, m: int) -> int:
    if m == 12:
        return 31
    first_next = dt.date(y + (m // 12), (m % 12) + 1, 1)
    last_this = first_next - dt.timedelta(days=1)
    return last_this.day

# __________________Échéancier coupons plain vanilla________________

def build_coupon_schedule(settle: dt.date, maturity: dt.date, freq: int) -> List[dt.date]:
    """
    Renvoie les dates de paiement STRICTEMENT > settle, jusqu'à maturity incluse.
    On part de maturity et on recule de 12/freq mois pour trouver toutes les dates,
    puis on filtre celles > settle et on trie.
    """
    if freq <= 0 or 12 % freq != 0:
        raise ValueError("freq doit diviser 12 (1, 2, 4, 12).")
    step = 12 // freq

    # reculer depuis maturity
    pay_dates = []
    d = maturity
    # garde toutes les dates de coupon décroissantes
    while True:
        pay_dates.append(d)
        next_d = add_months(d, -step)
        if next_d <= settle:  # on s'arrête quand on franchit le settle
            break
        d = next_d

    # garder seulement celles strictement > settle et trier
    res = [d for d in pay_dates if d > settle]
    res.sort()
    return res

def cashflows_plain_vanilla(face: float, coupon: float, freq: int,
                            settle: dt.date, maturity: dt.date) -> List[Cashflow]:
    """
    Génère (t, CF) pour une obligation plain vanilla:
      - coupon rate 'coupon', payable 'freq' fois/an
      - nominal 'face' à l'échéance
      - Pas d'intérêt couru en V1
    """
    pay_dates = build_coupon_schedule(settle, maturity, freq)
    cpn = face * coupon / max(freq, 1)
    flows: List[Cashflow] = []
    for d in pay_dates:
        cf = cpn
        if d == pay_dates[-1]:  # dernier paiement: ajouter le nominal
            cf += face
        t = yearfrac_act365(settle, d)  # ACT/365F
        flows.append((t, cf))
    
    return flows