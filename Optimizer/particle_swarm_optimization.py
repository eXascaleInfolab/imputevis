import pyswarms as ps
from typing import Dict, List, Tuple
import numpy as np
from skopt.space import Integer
from Optimizer.algorithm_parameters import SEARCH_SPACES_PSO

# Import the 'evaluate_params' function from the 'successive_halving' module
from successive_halving import evaluate_params


def pso_optimization(ground_truth_matrix: np.ndarray, obfuscated_matrix: np.ndarray,
                     selected_metrics: List[str], algorithm: str,
                     pso_params: Dict[str, float]) -> Tuple[str, float]:
    """
    Conduct the Particle Swarm Optimization (PSO) hyperparameter optimization.

    Parameters
    ----------
    ground_truth_matrix : np.ndarray
        The original unobfuscated matrix.
    obfuscated_matrix : np.ndarray
        The obfuscated matrix.
    selected_metrics : list
        List of selected metrics to consider for optimization.
    algorithm : str
        The algorithm to use.
        Valid values: 'cdrec', 'mrnn', 'stmvl', 'iim'
    pso_params : dict
        PSO parameters including 'c1', 'c2', 'w', and 'n_particles'.

    Returns
    -------
    tuple
        The best parameters and their corresponding scores.
    """

    # Define the search space
    search_space = SEARCH_SPACES_PSO

    # Select the correct search space based on the algorithm
    bounds = search_space[algorithm]

    # Convert search space to PSO-friendly format (two lists: one for min and one for max values for each parameter)
    lower_bounds, upper_bounds = zip(*bounds)
    bounds = (np.array(lower_bounds), np.array(upper_bounds))

    # Define the objective function (to minimize)
    def objective(params):
        n_particles = params.shape[0]  # Get the number of particles
        # Initialize array to hold the errors for each particle
        errors_for_all_particles = np.zeros(n_particles)

        for i in range(n_particles):  # Iterate over each particle
            particle_params = params[i]  # Get the parameters for this particle

            # Convert parameters to appropriate types (int or float)
            if algorithm == 'cdrec':
                particle_params = [int(particle_params[0]), particle_params[1], int(particle_params[2])]
            if algorithm == 'iim':
                particle_params = map(int, particle_params)
            elif algorithm == 'mrnn':
                particle_params = [int(particle_params[0]), particle_params[1], int(particle_params[2]),
                                   particle_params[3], int(particle_params[4])]
            elif algorithm == 'stmvl':
                particle_params = [int(particle_params[0]), particle_params[1], int(particle_params[2])]

            errors = evaluate_params(ground_truth_matrix, obfuscated_matrix, algorithm, tuple(particle_params),
                                     selected_metrics)

            # Assume that lower is better for all metrics, calculate the mean error for this particle
            errors_for_all_particles[i] = np.mean([errors[metric] for metric in selected_metrics])

        return errors_for_all_particles

    # Call instance of PSO
    n_particles = pso_params.get('n_particles', 50)
    options = {'c1': pso_params.get('c1', 0.5), 'c2': pso_params.get('c2', 0.3), 'w': pso_params.get('w', 0.9)}
    optimizer = ps.single.GlobalBestPSO(n_particles=n_particles, dimensions=len(bounds[0]), options=options,
                                        bounds=bounds)

    # Perform optimization
    iterations = pso_params.get('iterations', 10)
    cost, pos = optimizer.optimize(objective, iters=iterations)

    # Optimal parameters
    if algorithm in ['cdrec', 'iim']:
        optimal_params = list(map(int, pos))
    elif algorithm == 'mrnn':
        optimal_params = [int(pos[0]), pos[1], int(pos[2]), pos[3], int(pos[4])]
    elif algorithm == 'stmvl':
        optimal_params = [int(pos[0]), pos[1], int(pos[2])]
    optimal_params_dict = {f"param_{i + 1}": value for i, value in enumerate(optimal_params)}

    return optimal_params_dict, cost


if __name__ == '__main__':
    algo = "iim"  # choose an algorithm to optimize
    raw_matrix = np.loadtxt("../Datasets/bafu/raw_matrices/BAFU_tiny.txt", delimiter=" ", )
    obf_matrix = np.loadtxt("../Datasets/bafu/obfuscated/BAFU_tiny_obfuscated_10.txt", delimiter=" ", )

    # Define your PSO parameters
    pso_parameters = {
        'c1': 0.5,  # cognitive parameter
        'c2': 0.3,  # social parameter
        'w': 0.9,  # inertia weight
        'n_particles': 20,  # number of particles
        'iterations': 10  # number of iterations
    }

    best_params, best_score = pso_optimization(
        raw_matrix,
        obf_matrix,
        ['rmse'],  # choose one or more metrics to optimize
        algo,
        pso_parameters  # pass your PSO parameters
    )

    print(f"Best parameters for {algo}: {best_params}")
    print(f"Best score: {best_score}")