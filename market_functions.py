#### market_functions.py

import numpy as np

def aggregate_effort(H_S, H_D, H):
    if H_S > H_D:
        H_W = H_D / H_S * H
    else:
        H_W = H
    N = sum(H_W)
    return N, H_W

def sell_sugar(S_S, S_D, S):
    if S_S < S_D:
        S_C = S_S / S_D * S
    else:
        S_C = S
    return S_C