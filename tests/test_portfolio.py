import numpy as np, pandas as pd, datetime as dt
from src.curve import build_zero_curve, shift_curve
from src.cashflows import cashflows_plain_vanilla, to_date
from src.pricing import price_from_curve
from src.portfolio import report_portfolio

def test_portfolio_dv01_additivity():
    mats = np.array([1,5], float); y = np.array([0.03,0.03], float)
    r = build_zero_curve(mats, y)
    VAL = dt.date(2025,1,1)

    pf = pd.DataFrame({
        "id":["A","B"],
        "face":[100,100],
        "coupon":[0.03,0.05],
        "freq":[1,1],
        "maturity":["2030-01-01","2030-01-01"]
    })
    rep = report_portfolio(pf, r, VAL)

    # ΔP portefeuille = somme ΔP lignes (parallèle)
    r_up = shift_curve(r, 100)
    def price_portfolio(rr):
        P=0.0
        for _,row in pf.iterrows():
            flows = cashflows_plain_vanilla(float(row["face"]), float(row["coupon"]), int(row["freq"]), VAL, to_date(row["maturity"]))
            P += price_from_curve(rr, flows)
        return P
    assert abs((price_portfolio(r_up)-price_portfolio(r)) - rep["dP_+100bps"].sum()) < 1e-6
