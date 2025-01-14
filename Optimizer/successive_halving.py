import numpy as np
from typing import Dict, List
import time
import json
import Optimizer.algorithm_parameters as alg_params

import sys
import os

import Optimizer.evaluate_params
from Optimizer import util

sys.path.insert(0, os.path.abspath(".."))  # Add parent directory to path for imports to work


def select_and_average_errors(errors_dict: Dict[str, float], selected_metrics: List[str]) -> float:
    """
    Select and average specified errors.

    Parameters
    ----------
    errors_dict : dict
        Dictionary of computed error measures.
    selected_metrics : list
        List of selected metrics to average.

    Returns
    -------
    float
        The average of the selected error measures.
    """

    selected_errors = [errors_dict[metric] for metric in selected_metrics]
    return np.mean(selected_errors)

# 50 normally, 15 for iim and m-rnn (or even less)
def successive_halving(ground_truth_matrix: np.ndarray, obfuscated_matrix: np.ndarray,
                       selected_metrics: List[str], algorithm: str,
                       num_configs: int = 50, num_iterations: int = 2,
                       reduction_factor: int = 2) -> tuple:
    """
    Conduct the successive halving hyperparameter optimization.

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
    num_configs: int
        Number of configurations to try.
    num_iterations: int
        Number of iterations to run the optimization.
    reduction_factor: int
        Reduction factor for the number of configurations kept after each iteration.

    Returns
    -------
    tuple
        The configuration with the lowest average selected error measures.
    """

    # Define the parameter names for each algorithm
    param_names = alg_params.PARAM_NAMES

    data_length = len(ground_truth_matrix)
    chunk_size = data_length // num_iterations

    # prepare configurations for each algorithm separately
    if algorithm == 'cdrec':
        max_rank = obfuscated_matrix.shape[1] - 1
        temp_rank_range = [i for i in alg_params.CDREC_RANK_RANGE if i < max_rank]

        if not temp_rank_range:
            raise ValueError("No suitable rank found within CDREC_RANK_RANGE for the given matrix shape!")

        configs = [(np.random.choice(temp_rank_range),
                    np.random.choice(alg_params.CDREC_EPS_RANGE),
                    np.random.choice(alg_params.CDREC_ITERS_RANGE)) for _ in range(num_configs)]
    elif algorithm == 'iim':
        configs = [(np.random.choice(alg_params.IIM_LEARNING_NEIGHBOR_RANGE))
                   for _ in range(num_configs)]
    elif algorithm == 'mrnn':
        configs = [(np.random.choice(alg_params.MRNN_HIDDEN_DIM_RANGE),
                    np.random.choice(alg_params.MRNN_LEARNING_RATE_CHANGE),
                    np.random.choice(alg_params.MRNN_NUM_ITER_RANGE),
                    np.random.choice(alg_params.MRNN_KEEP_PROB_RANGE),
                    # np.random.choice(alg_params.MRNN_SEQ_LEN_RANGE)
                    ) for _ in range(num_configs)]
    elif algorithm == 'stmvl':
        configs = [(np.random.choice(alg_params.STMVL_WINDOW_SIZE_RANGE),
                    np.random.choice(alg_params.STMVL_GAMMA_RANGE),
                    np.random.choice(alg_params.STMVL_ALPHA_RANGE)) for _ in range(num_configs)]
    else:
        raise ValueError(f"Invalid algorithm: {algorithm}")

    for i in range(num_iterations):
        # Calculate how much data to use in this iteration
        end_idx = (i + 1) * chunk_size
        partial_ground_truth = ground_truth_matrix[:end_idx]
        partial_obfuscated = obfuscated_matrix[:end_idx]

        scores = [select_and_average_errors(
            Optimizer.evaluate_params.evaluate_params(partial_ground_truth, partial_obfuscated, algorithm, config, selected_metrics),
            selected_metrics) for config in configs]

        top_configs_idx = np.argsort(scores)[:max(1, len(configs) // reduction_factor)]
        configs = [configs[i] for i in top_configs_idx]
        if len(configs) <= 1:
            break  # Exit the loop if only 1 configuration remains

    if not configs:
        raise ValueError("No configurations left after successive halving.")

    if (algorithm == 'iim'):
        best_config = min(configs, key=lambda single_config: select_and_average_errors(
            Optimizer.evaluate_params.evaluate_params(ground_truth_matrix, obfuscated_matrix, algorithm, [single_config],
                                                      selected_metrics), selected_metrics))
    else:
        best_config = min(configs, key=lambda config: select_and_average_errors(
            Optimizer.evaluate_params.evaluate_params(ground_truth_matrix, obfuscated_matrix, algorithm,
                                                      config, selected_metrics), selected_metrics))

    best_score = select_and_average_errors(
        Optimizer.evaluate_params.evaluate_params(ground_truth_matrix, obfuscated_matrix, algorithm, best_config,
                                                  selected_metrics), selected_metrics)

    # Convert the configuration tuple to a dictionary
    best_config_dict = {name: value for name, value in zip(param_names[algorithm], best_config)}

    return best_config_dict, best_score


if __name__ == '__main__':
    algos = ['cdrec']
    datasets = [
        'bafu', 'chlorine', 'climate',
        'drift',
        'meteo'
    ]
    dataset_files = [
        'BAFU', 'cl2fullLarge', 'climate',
        'batch10',
        'meteo_total'
    ]
    metrics = ['mi', 'corr']

    results = {}
    for algo in algos:
        for dataset, data_file in zip(datasets, dataset_files):
            raw_file_path = f"../Datasets/{dataset}/raw_matrices/{data_file}_eighth.txt"
            obf_file_path = f"../Datasets/{dataset}/obfuscated/{data_file}_eighth_obfuscated_10.txt"

            if dataset == 'drift':
                raw_file_path = f"../Datasets/{dataset}/drift10/raw_matrices/{data_file}_eighth.txt"
                obf_file_path = f"../Datasets/{dataset}/obfuscated/{data_file}_eighth_obfuscated_10.txt"
            raw_matrix = np.loadtxt(raw_file_path, delimiter=" ", )
            obf_matrix = np.loadtxt(obf_file_path, delimiter=" ", )

            start_time = time.time()
            optimization_result = successive_halving(
                raw_matrix,
                obf_matrix,
                metrics,
                algo
            )
            elapsed_time = time.time() - start_time

            # Convert optimization result to be JSON serializable
            optimization_result = util.json_serializable(optimization_result)

            results[dataset] = {
                'best_params': optimization_result[0],
                'best_score': optimization_result[1],
                'dataset': dataset,
                'time': elapsed_time
            }
            print(dataset)

        # Save results in a JSON file
        with open(f'optimization_results_{algo}_succesive_halving_{metrics[0]}_{metrics[1]}.json',
                  'w') as outfile:
            json.dump(results, outfile)

    print(results)
