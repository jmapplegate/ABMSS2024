#### household_functions.py

import numpy as np

def tribute_hours(p, S_N, omega, m):
    #negative m increases tribute hours
    return np.maximum((p * S_N - m) / omega, 0)

def optional_hours(beta, alpha, H_max, omega, m, p, S_N):
    #only excess m to p*S_N counts in optional hours
    return max(0, beta * H_max - alpha / omega * max(0, (m - p * S_N)))

def plan_consumption(S_N, omega, p, hours, m):
    income = hours * omega
    demand = np.maximum((income + m) / p, S_N)
    return demand, income

def calculate_utility(H_max, H_W, S_C, S_N, alpha, beta):
    return (H_max - H_W) ** alpha * (S_C - S_N) ** beta

def update_ledger(income, p, s, m):
    expenditure = p * s
    m += income - expenditure
    return m, expenditure