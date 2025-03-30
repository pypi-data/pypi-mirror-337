import numpy as np
from .penalty import constrained_objective_function

def BMR_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Best-Mean-Random (BMR) algorithm by R.V. Rao.
    
    BMR is a simple, metaphor-free optimization algorithm that uses the best solution,
    mean solution, and a random solution to guide the search process.
    
    Reference: Ravipudi Venkata Rao and Ravikumar Shah (2024), "BMR and BWR: Two simple metaphor-free 
    optimization algorithms for solving real-life non-convex constrained and unconstrained problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))

    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')

    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)

        # Get best solution and score for this iteration
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx].copy()
        mean_solution = np.mean(population, axis=0)
        best_score = fitness[best_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)

        # Update population
        for i in range(population_size):
            r1, r2, r3, r4 = np.random.rand(4)
            T = np.random.choice([1, 2])
            random_solution = population[np.random.randint(population_size)]

            if r4 > 0.5:
                population[i] += r1 * (best_solution - T * mean_solution) + r2 * (best_solution - random_solution)
            else:
                population[i] = bounds[:, 1] - (bounds[:, 1] - bounds[:, 0]) * r3

        # Clip to bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)

    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def BWR_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Best-Worst-Random (BWR) algorithm by R.V. Rao.
    
    BWR is a simple, metaphor-free optimization algorithm that uses the best solution,
    worst solution, and a random solution to guide the search process.
    
    Reference: Ravipudi Venkata Rao and Ravikumar Shah (2024), "BMR and BWR: Two simple metaphor-free 
    optimization algorithms for solving real-life non-convex constrained and unconstrained problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))

    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'worst_scores': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')

    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)

        # Get best and worst solutions for this iteration
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx].copy()
        worst_solution = population[worst_idx].copy()
        best_score = fitness[best_idx]
        worst_score = fitness[worst_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['worst_scores'].append(worst_score)
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)

        # Update population
        for i in range(population_size):
            r1, r2, r3, r4 = np.random.rand(4)
            T = np.random.choice([1, 2])
            random_solution = population[np.random.randint(population_size)]

            if r4 > 0.5:
                population[i] += r1 * (best_solution - T * random_solution) - r2 * (worst_solution - random_solution)
            else:
                population[i] = bounds[:, 1] - (bounds[:, 1] - bounds[:, 0]) * r3

        # Clip to bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)

    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def Jaya_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Jaya algorithm by R.V. Rao.
    
    Jaya is a simple, parameter-free optimization algorithm that always tries to move toward the best solution
    and away from the worst solution.
    
    Reference: R.V. Rao, "Jaya: A simple and new optimization algorithm for solving constrained and unconstrained 
    optimization problems", International Journal of Industrial Engineering Computations, 7(1), 2016, 19-34.
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'worst_scores': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')

    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best and worst solutions for this iteration
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx].copy()
        worst_solution = population[worst_idx].copy()
        best_score = fitness[best_idx]
        worst_score = fitness[worst_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['worst_scores'].append(worst_score)
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
        
        # Update population
        new_population = np.zeros_like(population)
        for i in range(population_size):
            r1 = np.random.rand(num_variables)
            r2 = np.random.rand(num_variables)
            
            # Move toward best and away from worst
            new_solution = population[i] + r1 * (best_solution - np.abs(population[i])) - r2 * (worst_solution - np.abs(population[i]))
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Keep the better solution
            if new_fitness < fitness[i]:
                population[i] = new_solution
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)

    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def Rao1_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Rao-1 algorithm by R.V. Rao.
    
    Rao-1 is a simple, metaphor-free optimization algorithm that uses the best solution to guide the search.
    
    Reference: R.V. Rao, "Rao algorithms: Three metaphor-less simple algorithms for solving optimization problems",
    International Journal of Industrial Engineering Computations, 11(2), 2020, 193-212.
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best solution and score for this iteration
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx].copy()
        best_score = fitness[best_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
        
        # Update population
        for i in range(population_size):
            r = np.random.rand()
            
            # Rao-1 update rule
            if r < 0.5:
                population[i] = population[i] + r * (best_solution - np.abs(population[i]))
            else:
                population[i] = population[i] + r * (best_solution - np.mean(population, axis=0))
        
        # Clip to bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def Rao2_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Rao-2 algorithm by R.V. Rao.
    
    Rao-2 is a simple, metaphor-free optimization algorithm that uses the best and worst solutions to guide the search.
    
    Reference: R.V. Rao, "Rao algorithms: Three metaphor-less simple algorithms for solving optimization problems",
    International Journal of Industrial Engineering Computations, 11(2), 2020, 193-212.
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'worst_scores': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best and worst solutions for this iteration
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx].copy()
        worst_solution = population[worst_idx].copy()
        best_score = fitness[best_idx]
        worst_score = fitness[worst_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['worst_scores'].append(worst_score)
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
        
        # Update population
        for i in range(population_size):
            r = np.random.rand()
            
            # Rao-2 update rule
            if r < 0.5:
                population[i] = population[i] + r * (best_solution - np.abs(population[i])) - r * (worst_solution - np.abs(population[i]))
            else:
                population[i] = population[i] + r * (best_solution - np.mean(population, axis=0)) - r * (worst_solution - np.abs(population[i]))
        
        # Clip to bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def Rao3_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Rao-3 algorithm by R.V. Rao.
    
    Rao-3 is a simple, metaphor-free optimization algorithm that uses the best solution and a phase factor
    to guide the search.
    
    Reference: R.V. Rao, "Rao algorithms: Three metaphor-less simple algorithms for solving optimization problems",
    International Journal of Industrial Engineering Computations, 11(2), 2020, 193-212.
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': [],
            'phase_values': []  # Track the phase values
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best solution and score for this iteration
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx].copy()
        best_score = fitness[best_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Calculate phase value (varies with iteration)
        phase = 1 - iteration / num_iterations
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['mean_scores'].append(np.mean(fitness))
            convergence_history['phase_values'].append(phase)
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
        
        # Update population
        for i in range(population_size):
            r = np.random.rand()
            
            # Rao-3 update rule with phase factor
            population[i] = population[i] + r * phase * (best_solution - np.abs(population[i]))
        
        # Clip to bounds
        population = np.clip(population, bounds[:, 0], bounds[:, 1])
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def TLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Teaching-Learning-Based Optimization (TLBO) algorithm by R.V. Rao.
    
    TLBO is a parameter-free algorithm inspired by the teaching-learning process in a classroom.
    It consists of two phases: Teacher Phase and Learner Phase.
    
    Reference: R.V. Rao, V.J. Savsani, D.P. Vakharia, "Teaching-Learning-Based Optimization: An optimization method 
    for continuous non-linear large scale problems", Information Sciences, 183(1), 2012, 1-15.
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': [],
            'teacher_phase_improvements': [],
            'learner_phase_improvements': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best solution (teacher) and score for this iteration
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx]
        best_score = fitness[best_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
            
            # Initialize improvement counters for this iteration
            teacher_improvements = 0
            learner_improvements = 0
        
        # Teacher Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution based on teacher
            new_solution = population[i] + np.random.rand(num_variables) * (best_solution - TF * mean_solution)
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    teacher_improvements += 1
            else:
                new_population[i] = population[i]
        
        # Update population after Teacher Phase
        population = new_population.copy()
        
        # Learner Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Select another learner randomly, different from i
            j = i
            while j == i:
                j = np.random.randint(0, population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    learner_improvements += 1
            else:
                new_population[i] = population[i]
        
        # Update population after Learner Phase
        population = new_population.copy()
        
        # Track phase improvements
        if track_history:
            convergence_history['teacher_phase_improvements'].append(teacher_improvements)
            convergence_history['learner_phase_improvements'].append(learner_improvements)
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def QOJAYA_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Quasi-Oppositional Jaya (QOJAYA) algorithm by R.V. Rao.
    
    QOJAYA enhances the standard Jaya algorithm by incorporating quasi-oppositional learning
    to improve convergence speed and solution quality.
    
    Reference: Rao, R.V. (2019). "Jaya: An Advanced Optimization Algorithm and its Engineering Applications."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'worst_scores': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': [],
            'opposition_improvements': []  # Track improvements from opposition
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    # Function to generate quasi-opposite point
    def quasi_opposite_point(x, a, b):
        return a + b - np.random.rand() * x
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
            opposition_improvements = 0
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best and worst solutions for this iteration
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx].copy()
        worst_solution = population[worst_idx].copy()
        best_score = fitness[best_idx]
        worst_score = fitness[worst_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['worst_scores'].append(worst_score)
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
        
        # Update population
        new_population = np.zeros_like(population)
        for i in range(population_size):
            r1 = np.random.rand(num_variables)
            r2 = np.random.rand(num_variables)
            
            # Jaya update rule
            new_solution = population[i] + r1 * (best_solution - np.abs(population[i])) - r2 * (worst_solution - np.abs(population[i]))
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Generate quasi-opposite solution
            qo_solution = np.array([quasi_opposite_point(new_solution[j], bounds[j, 0], bounds[j, 1]) for j in range(num_variables)])
            qo_solution = np.clip(qo_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate both solutions
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
                qo_fitness = constrained_objective_function(qo_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
                qo_fitness = objective_func(qo_solution)
            
            # Select the better solution
            if qo_fitness < new_fitness and qo_fitness < fitness[i]:
                new_population[i] = qo_solution
                fitness[i] = qo_fitness
                if track_history:
                    opposition_improvements += 1
            elif new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
            else:
                new_population[i] = population[i]
        
        # Update population
        population = new_population.copy()
        
        # Track opposition improvements
        if track_history:
            convergence_history['opposition_improvements'].append(opposition_improvements)
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def TLBO_with_Elitism_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Teaching-Learning-Based Optimization (TLBO) with Elitism by R.V. Rao.
    
    This version of TLBO incorporates elitism to preserve the best solutions across generations,
    improving convergence and solution quality.
    
    Reference: Rao, R.V., Patel, V. (2013). "Improved teaching-learning-based optimization algorithm 
    for solving unconstrained optimization problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': [],
            'elite_scores': [],  # Track elite population scores
            'teacher_phase_improvements': [],  # Track improvements in teacher phase
            'learner_phase_improvements': []  # Track improvements in learner phase
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    # Elite size (typically a small percentage of the population)
    elite_size = max(1, int(0.1 * population_size))
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
            teacher_phase_improvements = 0
            learner_phase_improvements = 0
        
        # Evaluate fitness of the population
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Store elite solutions
        elite_indices = np.argsort(fitness)[:elite_size]
        elite_solutions = population[elite_indices].copy()
        elite_fitness = np.array(fitness)[elite_indices].copy()
        
        # Find the best solution (teacher)
        best_idx = np.argmin(fitness)
        best_solution = population[best_idx]
        
        # Record the best score
        best_score = fitness[best_idx]
        best_scores.append(best_score)
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Track history
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['mean_scores'].append(np.mean(fitness))
            convergence_history['elite_scores'].append(np.mean(elite_fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
            
            # End timing for this iteration
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
        
        # Teacher Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution based on teacher
            r = np.random.rand(num_variables)
            new_solution = population[i] + r * (best_solution - TF * mean_solution)
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    teacher_phase_improvements += 1
            else:
                new_population[i] = population[i]
        
        # Update population after Teacher Phase
        population = new_population.copy()
        
        # Learner Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Select another learner randomly, different from i
            j = i
            while j == i:
                j = np.random.randint(0, population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    learner_phase_improvements += 1
            else:
                new_population[i] = population[i]
        
        # Update population after Learner Phase
        population = new_population.copy()
        
        # Apply elitism: replace worst solutions with elite solutions
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
            
        worst_indices = np.argsort(fitness)[-int(0.1*population_size):]
        for i, idx in enumerate(worst_indices):
            population[idx] = elite_solutions[i]
        
        # Track phase improvements
        if track_history:
            convergence_history['teacher_phase_improvements'].append(teacher_phase_improvements)
            convergence_history['learner_phase_improvements'].append(learner_phase_improvements)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def JCRO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Jaya-based Chemical Reaction Optimization (JCRO) algorithm by R.V. Rao.
    
    JCRO is a hybrid algorithm combining Jaya with Chemical Reaction Optimization principles
    for enhanced exploration and exploitation balance.
    
    Reference: Rao, R.V., Rai, D.P. (2017). "Optimization of welding processes using 
    quasi-oppositional-based Jaya algorithm."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population (molecules)
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'worst_scores': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': [],
            'synthesis_improvements': [],
            'decomposition_improvements': [],
            'intermolecular_improvements': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    # CRO parameters
    ke_loss_rate = 0.2
    molecular_collision_rate = 0.2
    
    # Initialize kinetic energy for each molecule
    kinetic_energy = np.ones(population_size) * 1000
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
            synthesis_improvements = 0
            decomposition_improvements = 0
            intermolecular_improvements = 0
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best and worst solutions for this iteration
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx].copy()
        worst_solution = population[worst_idx].copy()
        best_score = fitness[best_idx]
        worst_score = fitness[worst_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['worst_scores'].append(worst_score)
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
        
        # Update population using CRO operators
        for i in range(population_size):
            # Decide which operator to use
            if np.random.rand() < molecular_collision_rate:
                # Intermolecular collision (synthesis or decomposition)
                if np.random.rand() < 0.5:
                    # Synthesis: combine two molecules
                    j = np.random.randint(population_size)
                    while j == i:
                        j = np.random.randint(population_size)
                    
                    # Create new solution using synthesis
                    r = np.random.rand(num_variables)
                    new_solution = r * population[i] + (1 - r) * population[j]
                    
                    # Apply Jaya-inspired modification
                    new_solution += np.random.rand(num_variables) * (best_solution - np.abs(new_solution)) - np.random.rand(num_variables) * (worst_solution - np.abs(new_solution))
                    
                    # Ensure bounds are respected
                    new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
                    
                    # Evaluate new solution
                    if constraints:
                        new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
                    else:
                        new_fitness = objective_func(new_solution)
                    
                    # Accept if better
                    if new_fitness < fitness[i]:
                        population[i] = new_solution
                        fitness[i] = new_fitness
                        kinetic_energy[i] = kinetic_energy[i] * (1 - ke_loss_rate)
                        if track_history:
                            synthesis_improvements += 1
                else:
                    # Decomposition: split one molecule into two
                    # Create two new solutions
                    r1 = np.random.rand(num_variables)
                    r2 = np.random.rand(num_variables)
                    
                    new_solution1 = population[i] + r1 * (best_solution - np.abs(population[i]))
                    new_solution2 = population[i] - r2 * (worst_solution - np.abs(population[i]))
                    
                    # Ensure bounds are respected
                    new_solution1 = np.clip(new_solution1, bounds[:, 0], bounds[:, 1])
                    new_solution2 = np.clip(new_solution2, bounds[:, 0], bounds[:, 1])
                    
                    # Evaluate new solutions
                    if constraints:
                        new_fitness1 = constrained_objective_function(new_solution1, objective_func, constraints)
                        new_fitness2 = constrained_objective_function(new_solution2, objective_func, constraints)
                    else:
                        new_fitness1 = objective_func(new_solution1)
                        new_fitness2 = objective_func(new_solution2)
                    
                    # Replace current solution with the better of the two new solutions
                    if new_fitness1 < new_fitness2 and new_fitness1 < fitness[i]:
                        population[i] = new_solution1
                        fitness[i] = new_fitness1
                        kinetic_energy[i] = kinetic_energy[i] * (1 - ke_loss_rate)
                        if track_history:
                            decomposition_improvements += 1
                    elif new_fitness2 < fitness[i]:
                        population[i] = new_solution2
                        fitness[i] = new_fitness2
                        kinetic_energy[i] = kinetic_energy[i] * (1 - ke_loss_rate)
                        if track_history:
                            decomposition_improvements += 1
            else:
                # Intramolecular collision (Jaya update)
                r1 = np.random.rand(num_variables)
                r2 = np.random.rand(num_variables)
                
                # Standard Jaya update
                new_solution = population[i] + r1 * (best_solution - np.abs(population[i])) - r2 * (worst_solution - np.abs(population[i]))
                
                # Ensure bounds are respected
                new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
                
                # Evaluate new solution
                if constraints:
                    new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
                else:
                    new_fitness = objective_func(new_solution)
                
                # Accept if better
                if new_fitness < fitness[i]:
                    population[i] = new_solution
                    fitness[i] = new_fitness
                    kinetic_energy[i] = kinetic_energy[i] * (1 - ke_loss_rate)
                    if track_history:
                        intermolecular_improvements += 1
        
        # Track CRO improvements
        if track_history:
            convergence_history['synthesis_improvements'].append(synthesis_improvements)
            convergence_history['decomposition_improvements'].append(decomposition_improvements)
            convergence_history['intermolecular_improvements'].append(intermolecular_improvements)
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def GOTLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Generalized Oppositional Teaching-Learning-Based Optimization (GOTLBO) algorithm.
    
    GOTLBO enhances the standard TLBO algorithm by incorporating oppositional learning
    and generalized learning phases for improved exploration and exploitation.
    
    Reference: Rao, R.V., Patel, V. (2013). "An improved teaching-learning-based optimization algorithm
    for solving unconstrained optimization problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'worst_scores': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': [],
            'teacher_phase_improvements': [],
            'learner_phase_improvements': [],
            'opposition_phase_improvements': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    # Function to generate opposite solution
    def opposite_solution(solution, bounds):
        return bounds[:, 0] + bounds[:, 1] - solution
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
            teacher_phase_improvements = 0
            learner_phase_improvements = 0
            opposition_phase_improvements = 0
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best and worst solutions for this iteration
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx].copy()
        worst_solution = population[worst_idx].copy()
        best_score = fitness[best_idx]
        worst_score = fitness[worst_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['worst_scores'].append(worst_score)
            convergence_history['mean_scores'].append(np.mean(fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Teacher Phase
        for i in range(population_size):
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution based on teacher
            r = np.random.rand(num_variables)
            new_solution = population[i] + r * (best_solution - TF * mean_solution)
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    teacher_phase_improvements += 1
        
        # Learner Phase
        for i in range(population_size):
            # Select another learner randomly
            j = np.random.randint(population_size)
            while j == i:
                j = np.random.randint(population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    learner_phase_improvements += 1
        
        # Oppositional Learning Phase (for the worst half of the population)
        sorted_indices = np.argsort(fitness)
        for i in range(population_size // 2, population_size):
            idx = sorted_indices[i]
            
            # Generate opposite solution
            opp_solution = opposite_solution(population[idx], bounds)
            
            # Evaluate opposite solution
            if constraints:
                opp_fitness = constrained_objective_function(opp_solution, objective_func, constraints)
            else:
                opp_fitness = objective_func(opp_solution)
            
            # Accept if better
            if opp_fitness < fitness[idx]:
                population[idx] = opp_solution
                fitness[idx] = opp_fitness
                if track_history:
                    opposition_phase_improvements += 1
        
        # Track phase improvements
        if track_history:
            convergence_history['teacher_phase_improvements'].append(teacher_phase_improvements)
            convergence_history['learner_phase_improvements'].append(learner_phase_improvements)
            convergence_history['opposition_phase_improvements'].append(opposition_phase_improvements)
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def ITLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_func, constraints=None, track_history=True):
    """
    Implementation of the Improved Teaching-Learning-Based Optimization (ITLBO) algorithm.
    
    ITLBO enhances the standard TLBO algorithm by incorporating elitism and adaptive teaching factor
    to improve convergence speed and solution quality.
    
    Reference: Rao, R.V., Patel, V. (2013). "An improved teaching-learning-based optimization algorithm
    for solving unconstrained optimization problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_func : function
        Objective function to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    best_solution : numpy.ndarray
        Best solution found
    best_scores : list
        Best score in each iteration (returned if track_history is False)
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    best_scores = []
    if track_history:
        convergence_history = {
            'best_scores': [],
            'best_solutions': [],
            'worst_scores': [],
            'mean_scores': [],
            'population_diversity': [],
            'iteration_times': [],
            'teacher_phase_improvements': [],
            'learner_phase_improvements': [],
            'elite_scores': []
        }
    
    # Track the global best solution across all iterations
    global_best_solution = None
    global_best_score = float('inf')
    
    # Elite size (typically a small percentage of the population)
    elite_size = max(1, int(0.1 * population_size))
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
            teacher_phase_improvements = 0
            learner_phase_improvements = 0
        
        # Evaluate fitness
        if constraints:
            fitness = [constrained_objective_function(ind, objective_func, constraints) for ind in population]
        else:
            fitness = np.apply_along_axis(objective_func, 1, population)
        
        # Get best and worst solutions for this iteration
        best_idx = np.argmin(fitness)
        worst_idx = np.argmax(fitness)
        best_solution = population[best_idx].copy()
        worst_solution = population[worst_idx].copy()
        best_score = fitness[best_idx]
        worst_score = fitness[worst_idx]
        
        # Update global best if better
        if best_score < global_best_score:
            global_best_solution = best_solution.copy()
            global_best_score = best_score
        
        # Store elite solutions
        elite_indices = np.argsort(fitness)[:elite_size]
        elite_solutions = population[elite_indices].copy()
        elite_fitness = [fitness[i] for i in elite_indices]
        
        # Track history
        best_scores.append(best_score)
        if track_history:
            convergence_history['best_scores'].append(best_score)
            convergence_history['best_solutions'].append(best_solution.copy())
            convergence_history['worst_scores'].append(worst_score)
            convergence_history['mean_scores'].append(np.mean(fitness))
            convergence_history['elite_scores'].append(np.mean(elite_fitness))
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Teacher Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Adaptive teaching factor based on fitness
            # Better solutions get smaller TF (more precise adjustments)
            # Worse solutions get larger TF (more exploration)
            normalized_rank = np.argsort(np.argsort(fitness))[i] / (population_size - 1)
            TF = 1 + normalized_rank  # TF will be between 1 and 2
            
            # Generate new solution based on teacher
            r = np.random.rand(num_variables)
            new_solution = population[i] + r * (best_solution - TF * mean_solution)
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    teacher_phase_improvements += 1
            else:
                new_population[i] = population[i]
        
        # Update population after Teacher Phase
        population = new_population.copy()
        
        # Learner Phase
        new_population = np.zeros_like(population)
        for i in range(population_size):
            # Select another learner randomly, different from i
            j = i
            while j == i:
                j = np.random.randint(0, population_size)
            
            # Generate new solution based on interaction with another learner
            if fitness[i] < fitness[j]:  # If current solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
            else:  # If other solution is better
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints:
                new_fitness = constrained_objective_function(new_solution, objective_func, constraints)
            else:
                new_fitness = objective_func(new_solution)
            
            # Accept if better
            if new_fitness < fitness[i]:
                new_population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    learner_phase_improvements += 1
            else:
                new_population[i] = population[i]
        
        # Update population after Learner Phase
        population = new_population.copy()
        
        # Apply elitism: replace worst solutions with elite solutions
        worst_indices = np.argsort(fitness)[-int(0.1*population_size):]
        for i, idx in enumerate(worst_indices):
            population[idx] = elite_solutions[i]
        
        # Track phase improvements
        if track_history:
            convergence_history['teacher_phase_improvements'].append(teacher_phase_improvements)
            convergence_history['learner_phase_improvements'].append(learner_phase_improvements)
        
        # End timing for this iteration
        if track_history:
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return global_best_solution, best_scores, convergence_history
    else:
        return global_best_solution, best_scores


def MultiObjective_TLBO_algorithm(bounds, num_iterations, population_size, num_variables, objective_funcs, constraints=None, track_history=True):
    """
    Implementation of the Multi-Objective Teaching-Learning-Based Optimization (MO-TLBO) algorithm.
    
    MO-TLBO extends the TLBO algorithm to handle multiple objective functions simultaneously,
    finding a set of Pareto-optimal solutions.
    
    Reference: Rao, R.V., Patel, V. (2014). "An improved teaching-learning-based optimization algorithm 
    for solving multi-objective optimization problems."
    
    Parameters:
    -----------
    bounds : numpy.ndarray
        Bounds for each variable, shape (num_variables, 2)
    num_iterations : int
        Number of iterations to run the algorithm
    population_size : int
        Size of the population
    num_variables : int
        Number of variables in the optimization problem
    objective_funcs : list
        List of objective functions to minimize
    constraints : list, optional
        List of constraint functions
    track_history : bool, optional
        Whether to track detailed convergence history (default: True)
        
    Returns:
    --------
    pareto_front : numpy.ndarray
        Set of non-dominated solutions (Pareto front)
    pareto_fitness : numpy.ndarray
        Fitness values of the Pareto front solutions
    convergence_history : dict
        Detailed convergence history (returned if track_history is True)
    """
    # Number of objective functions
    num_objectives = len(objective_funcs)
    
    # Initialize population
    population = np.random.uniform(low=bounds[:, 0], high=bounds[:, 1], size=(population_size, num_variables))
    
    # Initialize history tracking
    if track_history:
        convergence_history = {
            'pareto_front_size': [],
            'pareto_fronts': [],
            'pareto_fitness': [],
            'population_diversity': [],
            'iteration_times': [],
            'teacher_phase_improvements': [],
            'learner_phase_improvements': [],
            'hypervolume': []
        }
    
    # Function to evaluate all objectives
    def evaluate_objectives(solution):
        return np.array([func(solution) for func in objective_funcs])
    
    # Function to check if solution1 dominates solution2
    def dominates(fitness1, fitness2):
        # For minimization problems
        return np.all(fitness1 <= fitness2) and np.any(fitness1 < fitness2)
    
    # Function to find non-dominated solutions (Pareto front)
    def find_pareto_front(population, fitness):
        pareto_indices = []
        for i in range(len(population)):
            dominated = False
            for j in range(len(population)):
                if i != j and dominates(fitness[j], fitness[i]):
                    dominated = True
                    break
            if not dominated:
                pareto_indices.append(i)
        return population[pareto_indices], fitness[pareto_indices]
    
    # Function to calculate hypervolume (approximate)
    def calculate_hypervolume(pareto_fitness, reference_point):
        if len(pareto_fitness) == 0:
            return 0
        
        # Sort by first objective
        sorted_indices = np.argsort(pareto_fitness[:, 0])
        sorted_fitness = pareto_fitness[sorted_indices]
        
        # Calculate hypervolume
        hv = 0
        for i in range(len(sorted_fitness)):
            if i == 0:
                width = reference_point[0] - sorted_fitness[i, 0]
            else:
                width = sorted_fitness[i-1, 0] - sorted_fitness[i, 0]
            
            height = reference_point[1] - sorted_fitness[i, 1]
            hv += width * height
        
        return hv
    
    # Evaluate initial population
    fitness = np.array([evaluate_objectives(ind) for ind in population])
    
    # Find initial Pareto front
    pareto_front, pareto_fitness = find_pareto_front(population, fitness)
    
    # Reference point for hypervolume calculation (worst value in each objective + some margin)
    reference_point = np.max(fitness, axis=0) * 1.1
    
    for iteration in range(num_iterations):
        # Start timing this iteration if tracking history
        if track_history:
            import time
            start_time = time.time()
            teacher_phase_improvements = 0
            learner_phase_improvements = 0
        
        # Calculate mean of the population
        mean_solution = np.mean(population, axis=0)
        
        # Teacher Phase
        for i in range(population_size):
            # Select a random solution from the Pareto front as teacher
            if len(pareto_front) > 0:
                teacher_idx = np.random.randint(len(pareto_front))
                teacher = pareto_front[teacher_idx]
            else:
                # If no Pareto front yet, use the best solution for the first objective
                best_idx = np.argmin(fitness[:, 0])
                teacher = population[best_idx]
            
            # Teaching factor (either 1 or 2)
            TF = np.random.randint(1, 3)
            
            # Generate new solution
            r = np.random.rand(num_variables)
            
            # Improved teacher phase formula
            diff_mean = teacher - TF * mean_solution
            new_solution = population[i] + r * diff_mean
            
            # Add influence from elite solutions
            if i not in np.argsort(fitness[:, 0])[:int(0.1*population_size)]:  # Don't modify elite solutions
                elite_idx = np.random.choice(np.argsort(fitness[:, 0])[:int(0.1*population_size)])
                new_solution += np.random.rand(num_variables) * 0.1 * (population[elite_idx] - population[i])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints and any(constraint(new_solution) > 0 for constraint in constraints):
                # Skip if constraints are violated
                continue
            
            new_fitness = evaluate_objectives(new_solution)
            
            # Accept if new solution dominates current solution or is non-dominated
            if dominates(new_fitness, fitness[i]) or not dominates(fitness[i], new_fitness):
                population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    teacher_phase_improvements += 1
        
        # Learner Phase
        for i in range(population_size):
            # Select another learner randomly
            j = np.random.randint(population_size)
            while j == i:
                j = np.random.randint(population_size)
            
            # Determine which solution is better (using non-domination)
            if dominates(fitness[i], fitness[j]):
                # i dominates j
                new_solution = population[i] + np.random.rand(num_variables) * (population[i] - population[j])
                
                # Add influence from a third solution
                if dominates(fitness[i], fitness[j]):  # If current solution is better than j
                    new_solution += np.random.rand(num_variables) * 0.5 * (population[i] - population[j])
                else:  # If j is better than current solution
                    new_solution += np.random.rand(num_variables) * 0.5 * (population[j] - population[i])
            else:  # If other solution is better
                # Move toward j and away from i
                new_solution = population[i] + np.random.rand(num_variables) * (population[j] - population[i])
                
                # Add influence from a third solution
                if dominates(fitness[j], fitness[i]):  # If j is better than i
                    new_solution += np.random.rand(num_variables) * 0.5 * (population[j] - population[i])
                else:  # If i is better than j
                    new_solution += np.random.rand(num_variables) * 0.5 * (population[i] - population[j])
            
            # Ensure bounds are respected
            new_solution = np.clip(new_solution, bounds[:, 0], bounds[:, 1])
            
            # Evaluate new solution
            if constraints and any(constraint(new_solution) > 0 for constraint in constraints):
                # Skip if constraints are violated
                continue
            
            new_fitness = evaluate_objectives(new_solution)
            
            # Accept if new solution dominates current solution or is non-dominated
            if dominates(new_fitness, fitness[i]) or not dominates(fitness[i], new_fitness):
                population[i] = new_solution
                fitness[i] = new_fitness
                if track_history:
                    learner_phase_improvements += 1
        
        # Update Pareto front
        pareto_front, pareto_fitness = find_pareto_front(population, fitness)
        
        # Track history
        if track_history:
            convergence_history['pareto_front_size'].append(len(pareto_front))
            convergence_history['pareto_fronts'].append(pareto_front.copy())
            convergence_history['pareto_fitness'].append(pareto_fitness.copy())
            
            # Calculate population diversity (mean pairwise Euclidean distance)
            diversity = 0
            if population_size > 1:
                for i in range(population_size):
                    for j in range(i+1, population_size):
                        diversity += np.linalg.norm(population[i] - population[j])
                diversity /= (population_size * (population_size - 1) / 2)
            convergence_history['population_diversity'].append(diversity)
            
            # Track phase improvements
            convergence_history['teacher_phase_improvements'].append(teacher_phase_improvements)
            convergence_history['learner_phase_improvements'].append(learner_phase_improvements)
            
            # Calculate hypervolume if we have 2 objectives
            if num_objectives == 2:
                hv = calculate_hypervolume(pareto_fitness, reference_point)
                convergence_history['hypervolume'].append(hv)
            else:
                convergence_history['hypervolume'].append(None)
            
            # End timing for this iteration
            end_time = time.time()
            convergence_history['iteration_times'].append(end_time - start_time)
    
    # Return appropriate results based on track_history flag
    if track_history:
        return pareto_front, pareto_fitness, convergence_history
    else:
        return pareto_front, pareto_fitness
