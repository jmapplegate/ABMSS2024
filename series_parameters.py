#### series_parameters.py

def series_params():
    series_name = 'ABMSS2024_1'
    directory = './results/'

    #### series variables
    seed = None
    t_max = 500 #number of simulation steps
    reps = 100 #repetitions of each parameter set

    #### simulation variables
    n_list = [100] #number of households
    omega_0_list = [10] #inital wage
    p_0_list = [1] #intial price
    H_max = 480 #max household hours per month

    #### firm parameters
    A_list = [3] #firm production function coefficient
    gamma_list = [1.2] #firm production function exponent
    mu_list = [3] #memory for firm expectation updates

    #### base consumption requirement
    S_N_list = [1200] #[1200] #minimum household consumption

    #### simulated annealing control parameters
    delta_0_list = [.1] #coefficient of decay function
    theta_list = [.1]  #exponent of decay function
    min_pct_list = [0]  #
 
    param_sets = [[n, omega_0, p_0, A, gamma, mu, S_N, delta_0, theta, min_pct] for n in n_list 
                    for omega_0 in omega_0_list for p_0 in p_0_list for A in A_list for 
                    gamma in gamma_list for mu in mu_list for S_N in S_N_list 
                    for delta_0 in delta_0_list for theta in theta_list for min_pct in min_pct_list]

    #### determine number of distinct parameter sets
    n_sets = len(param_sets)
    
    #### add fixed parameters
    #### resulting list is: s, t_max, n, H_max, omega_0, p_0, A, gamma, mu, S_N, delta_0, theta, min_pct
    for s in range(n_sets):
        (param_sets[s]).insert(0, t_max)
        (param_sets[s]).insert(2, H_max)
        (param_sets[s]).insert(0, s)

    #### include run number as 1st parameter for multithreading
    expanded_sets = [item.copy() for item in param_sets for i in range(reps)]
    run_list = list(range(reps)) * n_sets
    for i in range(n_sets * reps):
        (expanded_sets[i]).insert(0, run_list[i])

    return directory, series_name, seed, reps, n_sets, expanded_sets