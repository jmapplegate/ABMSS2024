#### firm_functions.py

import numpy as np

def profit(omega, p, S_M, H_M):
    return p * S_M - omega * H_M

def determine_hours(S_D, A, gamma, S_N, n, I):
    if S_D >= n * S_N:
        planned = S_D
    else:
        planned = n * S_N
    # use inventory, could make hours demanded = 0
    if 0 < I < planned:
        planned -= I
    elif I >= planned:
        planned = 0
    H = (planned / A) ** ( 1 / gamma)
    return H

def produce_supply(A, N, gamma):
    return A * N ** gamma

def adjust_inventory(S_P, S_M, I):
    I += S_P - S_M
    return I

#### exponential decay
def decay(t, delta_0, theta, min_pct):
    return max(delta_0*np.exp(-1*theta*t), min_pct)

### WAGE AND PRICE UPDATE ALGORITHMS
### percentage change algorithms
### with pct set by decay function, simulated annealing
### with constant percent, fixed change
def update_wage_price(omega, p, H_S, H_D, S_S, S_D, pct):
    omega_new = omega
    if S_S > S_D:
        if H_S > H_D:
            p = p * (1 - pct)
        else:
            omega_new = omega_new * (1 - pct)
    elif S_S < S_D:
        if H_S > H_D:
            omega_new = omega_new * (1 + pct)
        else:
            p = p * (1 + pct)
    #### sticky wage
    #omega_new = omega
    return omega_new, p

def update_expectation(value, memory, mu):
    memory = np.append(memory[1:], value)
    weights = np.arange(1, mu + 1)
    hat = np.average(memory, weights = weights)
    # only use last observed value
    #hat = value
    return hat, memory