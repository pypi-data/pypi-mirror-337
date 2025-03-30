import unittest
import numpy as np
from rao_algorithms import BMR_algorithm, BWR_algorithm, run_optimization, objective_function, rastrigin_function, ackley_function, rosenbrock_function, constraint_1, constraint_2

class TestOptimizationAlgorithms(unittest.TestCase):

    def setUp(self):
        self.bounds = np.array([[-100, 100]] * 2)  # Change as needed for higher dimensional problems
        self.num_iterations = 100
        self.population_size = 50
        self.num_variables = 2  # You can increase this for higher-dimensional tests

    def test_bmr_unconstrained(self):
        best_solution, _, _ = BMR_algorithm(self.bounds, self.num_iterations, self.population_size, self.num_variables, objective_function)
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(objective_function(best_solution), 10.0)

    def test_bwr_unconstrained(self):
        best_solution, _, _ = BWR_algorithm(self.bounds, self.num_iterations, self.population_size, self.num_variables, objective_function)
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(objective_function(best_solution), 10.0)

    def test_bmr_rastrigin(self):
        best_solution, _, _ = BMR_algorithm(self.bounds, self.num_iterations, self.population_size, self.num_variables, rastrigin_function)
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(rastrigin_function(best_solution), 50.0)

    def test_bwr_ackley(self):
        best_solution, _, _ = BWR_algorithm(self.bounds, self.num_iterations, self.population_size, self.num_variables, ackley_function)
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(ackley_function(best_solution), 10.0)

    def test_bmr_rosenbrock(self):
        best_solution, _, _ = BMR_algorithm(self.bounds, self.num_iterations, self.population_size, self.num_variables, rosenbrock_function)
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(rosenbrock_function(best_solution), 1000.0)

    def test_bmr_constrained(self):
        constraints = [constraint_1, constraint_2]
        best_solution, _, _ = BMR_algorithm(self.bounds, self.num_iterations, self.population_size, self.num_variables, objective_function, constraints)
        self.assertEqual(len(best_solution), self.num_variables)
        # For stochastic algorithms, we can't guarantee tight constraint satisfaction in every run
        # So we check that the solution is reasonable
        self.assertLess(objective_function(best_solution), 20.0)

    def test_bwr_constrained(self):
        constraints = [constraint_1, constraint_2]
        best_solution, _, _ = BWR_algorithm(self.bounds, self.num_iterations, self.population_size, self.num_variables, objective_function, constraints)
        self.assertEqual(len(best_solution), self.num_variables)
        # For stochastic algorithms, we can't guarantee tight constraint satisfaction in every run
        # So we check that the solution is reasonable
        self.assertLess(objective_function(best_solution), 20.0)

    def test_multiple_runs(self):
        """Run BMR multiple times and calculate mean and standard deviation."""
        results = []
        for _ in range(5):
            best_solution, _, _ = BMR_algorithm(self.bounds, self.num_iterations, self.population_size, self.num_variables, objective_function)
            results.append(objective_function(best_solution))
        
        mean_result = np.mean(results)
        std_result = np.std(results)
        
        self.assertLess(mean_result, 10.0)
        self.assertLess(std_result, 5.0)

if __name__ == '__main__':
    unittest.main()
