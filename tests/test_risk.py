import numpy as np
from src.curve import build_zero_curve
from src.pricing import price_from_curve
from src.risk import dv01, duration_modified, convexity

def test_zc_5y_duration_convexity():
    # Courbe plate 3% (continu)
    mats = np.array([1.0, 5.0], float)
    y    = np.array([0.03, 0.03], float)
    r = build_zero_curve(mats, y)

    # Zéro-coupon 5 ans
    flows = [(5.0, 100.0)]
    P = price_from_curve(r, flows)

    dmod = duration_modified(r, flows)    
    conv = convexity(r, flows)            
    dv   = dv01(r, flows)                 

    # tolérances numériques (centrée ±1 bp → petit écart ~5e-4)
    assert abs(dmod - 5.0)  < 1e-3
    assert abs(conv - 25.0) < 1e-2
    assert abs(dv - (P * 5.0 * 1e-4)) < 1e-6


