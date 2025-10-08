from __future__ import annotations
from typing import Dict, List
import datetime as dt
import pandas as pd

from .cashflows import to_date, cashflows_plain_vanilla
from .pricing import price_from_curve
from .risk import price_sensitivities
from .curve import shift_curve

def price_line(row: pd.Series, r_of_t, settle: dt.date) -> Dict[str, float]:
    face = float(row["face"])
    coupon = float(row["coupon"])
    freq = int(row["freq"])
    maturity = to_date(row["maturity"])
    flows = cashflows_plain_vanilla(face, coupon, freq, settle, maturity)
    met = price_sensitivities(r_of_t, flows, bp_step=1.0)
    return {"price": met["price"], "dv01": met["dv01"], "dmod": met["dmod"], "conv": met["conv"]}

def stress_line(row: pd.Series, r_of_t, settle: dt.date, bump_bps: float) -> float:
    face = float(row["face"])
    coupon = float(row["coupon"])
    freq = int(row["freq"])
    maturity = to_date(row["maturity"])
    flows = cashflows_plain_vanilla(face, coupon, freq, settle, maturity)
    P0 = price_from_curve(r_of_t, flows)
    P1 = price_from_curve(shift_curve(r_of_t, bump_bps), flows)
    return P1 - P0  

def report_portfolio(pf: pd.DataFrame, r_of_t, settle: dt.date) -> pd.DataFrame:
    rows = []
    for _, row in pf.iterrows():
        metrics = price_line(row, r_of_t, settle)
        dp_25  = stress_line(row, r_of_t, settle, +25)
        dp_100 = stress_line(row, r_of_t, settle, +100)
        rows.append({
            "id": row["id"],
            **metrics,
            "dP_+25bps": dp_25,
            "dP_+100bps": dp_100,
        })
    out = pd.DataFrame(rows)
    out["dv01_contrib_%"] = 100 * out["dv01"] / out["dv01"].sum() if out["dv01"].sum() else 0.0
    out["price_weight_%"] = 100 * out["price"] / out["price"].sum() if out["price"].sum() else 0.0
    return out
