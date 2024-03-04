#### simulation.py

import numpy as np

### import functions from model files
from initialisation_functions import *
from firm_functions import *
from household_functions import *
from market_functions import *

def simulation(r, s, t_max, n, H_max, omega_0, p_0, A, gamma, mu, S_N, delta_0, theta, min_pct, rng):
    sim_results = []
    t = 0
    pct_change = delta_0

    households = np.arange(0, n)

    #### intitialise firm and household
    I, pi, total_pi, omega, p, H_D, S_P, S_S = create_firm(omega_0, p_0)
    alphas, betas, H_N, H_O, H, H_W, income, m, S, S_C, U, expenditure = create_households(n, H_max, rng)
    N, S_D, H_M, S_M, H_S = 0, 0, 0, 0, 0

    #### initialise firm effort and demand expectations
    #idxs = rng.integers(0, n, size = mu)

    #### household sample S_hat
    S_hat, demand_memory = initialise_demand_expectation(n, alphas, betas, omega, p, H_max, S_N, mu)

    #### save initial results
    step_results = [s, r, t, t_max, n, H_max, A, gamma, mu, S_N, omega_0, p_0, delta_0, theta, min_pct, pct_change,
                    I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
                    np.sum(H_N), np.sum(H_O), np.sum(m), np.median(m), np.mean(m), np.max(m), 
                    np.min(m), np.mean(U), np.mean(alphas)]
    sim_results.append(step_results)

    #### the simulation steps can be run for a fixed number, t_max, 
    #### or with the stopping condition that S_S is within 1 unit of S_D.

    #### conditional steps
    # while ((abs(S_S - S_D) >= 1 or abs(pi) >= 1) and t < t_max) or t == 0:
    #     #print('supply demand delta is', abs(S_S - S_D), 'and pi is', abs(pi))
    #     t = t + 1

    #### t_max simulation steps
    for t in range(1, t_max + 1):
        #### firm determines hours
        H_D = determine_hours(S_hat, A, gamma, S_N, n, I)

        #### households determine effort and hours supplied
        H_N = tribute_hours(p, S_N, omega, m)
        for h in range(n):
            H_O[h] = optional_hours(betas[h], alphas[h], H_max, omega, m[h], p, S_N)
        H = np.minimum(H_N + H_O, H_max)

        #### market aggregates hours supplied, determines market hours and effective effort
        H_S = np.sum(H)
        H_M = min(H_D, H_S)
        N, H_W = aggregate_effort(H_S, H_D, H)

        #### firm produces sugar with effective labour
        S_P = produce_supply(A, N, gamma)
        S_S = S_P + I

        #### households plan sugar consumption
        S, income = plan_consumption(S_N, omega, p, H_W, m)

        #### market aggregates sugar demand and determines sugar sold
        S_D = np.sum(S)
        S_M = min(S_S, S_D)
        S_C = sell_sugar(S_S, S_D, S)

        #### calculate firm profit
        pi = profit(omega, p, S_M, H_M)
        total_pi += pi

        #### calculate household utility
        U = calculate_utility(H_max, H_W, S_C, S_N, alphas, betas)

        #### households adjust ledgers
        m, expenditure = update_ledger(income, p, S_C, m)

        #### firm adjusts inventory
        I = adjust_inventory(S_P, S_M, I)

        #### firm updates demand expectations
        S_hat, demand_memory = update_expectation(S_D, demand_memory, mu)

        #### firm raises or lowers wage and price
        #pct_change = delta_0
        ### for annealing
        pct_change = decay(t, delta_0, theta, min_pct)
        omega, p = update_wage_price(omega, p, H_S, H_D, S_S, S_D, pct_change)
        min_H_D = (n * S_N / A) ** (1 / gamma)

        #### write step state to frame
        step_results = [s, r, t, t_max, n, H_max, A, gamma, mu, S_N, omega_0, p_0, delta_0, theta, min_pct, pct_change,
                        I, pi, total_pi, omega, p, H_D, S_S, S_P, S_hat, N, H_S, H_M, S_D, S_M,
                        np.sum(H_N), np.sum(H_O), np.sum(m), np.median(m), np.mean(m), np.max(m), 
                        np.min(m), np.mean(U), np.mean(alphas)]
        sim_results.append(step_results)

    return sim_results