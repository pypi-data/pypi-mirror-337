import unittest
import numpy as np
from rao_algorithms.algorithms import (
    QOJAYA_algorithm,
    GOTLBO_algorithm,
    ITLBO_algorithm,
    MultiObjective_TLBO_algorithm
)

# Test functions
def sphere_function(x):
    """Sphere function: f(x) = sum(x_i^2)"""
    return np.sum(x**2)

def rastrigin_function(x):
    """Rastrigin function: f(x) = 10*n + sum(x_i^2 - 10*cos(2*pi*x_i))"""
    n = len(x)
    return 10 * n + np.sum(x**2 - 10 * np.cos(2 * np.pi * x))

def ackley_function(x):
    """Ackley function"""
    a, b, c = 20, 0.2, 2 * np.pi
    n = len(x)
    sum1 = np.sum(x**2)
    sum2 = np.sum(np.cos(c * x))
    term1 = -a * np.exp(-b * np.sqrt(sum1 / n))
    term2 = -np.exp(sum2 / n)
    return term1 + term2 + a + np.exp(1)

# Multi-objective test functions
def schaffer_n1_f1(x):
    """First objective of Schaffer N1 problem"""
    return x[0]**2

def schaffer_n1_f2(x):
    """Second objective of Schaffer N1 problem"""
    return (x[0] - 2)**2

# Constraint function
def constraint_example(x):
    """Example constraint: g(x) <= 0 where g(x) = x[0] + x[1] - 1"""
    return x[0] + x[1] - 1

def constraint_1(x):
    return x[0] - 5

def constraint_2(x):
    return x[1] - 5

def objective_function(x):
    return np.sum(x**2)


class TestNewAlgorithms(unittest.TestCase):
    
    def setUp(self):
        # Common parameters for all tests
        self.population_size = 30
        self.num_iterations = 200
        self.num_variables = 5
        self.bounds = np.array([[-5, 5] for _ in range(self.num_variables)])
        
        # Set a relaxed threshold for stochastic algorithms
        self.threshold = 500.0  # Relaxed threshold for stochastic algorithms
        
    def test_QOJAYA_unconstrained(self):
        """Test QOJAYA algorithm on unconstrained optimization problems"""
        # Test on sphere function
        best_solution, best_scores, _ = QOJAYA_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            lambda x: np.sum(x**2)
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(np.sum(best_solution**2), 10.0)
        
        # Test on Rastrigin function
        best_solution, best_scores, _ = QOJAYA_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            rastrigin_function
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(rastrigin_function(best_solution), 100.0)
        
        # Test on Ackley function
        best_solution, best_scores, _ = QOJAYA_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            ackley_function
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(ackley_function(best_solution), 15.0)

    def test_QOJAYA_constrained(self):
        """Test QOJAYA algorithm on constrained optimization problems"""
        constraints = [constraint_1, constraint_2]
        
        best_solution, best_scores, _ = QOJAYA_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            objective_function,
            constraints
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(objective_function(best_solution), 50.0)

    def test_GOTLBO_unconstrained(self):
        """Test GOTLBO algorithm on unconstrained optimization problems"""
        # Test on sphere function
        best_solution, best_scores, _ = GOTLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            lambda x: np.sum(x**2)
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(np.sum(best_solution**2), 10.0)
        
        # Test on Rastrigin function
        best_solution, best_scores, _ = GOTLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            rastrigin_function
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(rastrigin_function(best_solution), 100.0)
        
        # Test on Ackley function
        best_solution, best_scores, _ = GOTLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            ackley_function
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(ackley_function(best_solution), 15.0)

    def test_GOTLBO_constrained(self):
        """Test GOTLBO algorithm on constrained optimization problems"""
        constraints = [constraint_1, constraint_2]
        
        best_solution, best_scores, _ = GOTLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            objective_function,
            constraints
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(objective_function(best_solution), 50.0)

    def test_ITLBO_unconstrained(self):
        """Test ITLBO algorithm on unconstrained optimization problems"""
        # Test on sphere function
        best_solution, best_scores, _ = ITLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            lambda x: np.sum(x**2)
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(np.sum(best_solution**2), 10.0)
        
        # Test on Rastrigin function
        best_solution, best_scores, _ = ITLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            rastrigin_function
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(rastrigin_function(best_solution), 100.0)
        
        # Test on Ackley function
        best_solution, best_scores, _ = ITLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            ackley_function
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(ackley_function(best_solution), 15.0)

    def test_ITLBO_constrained(self):
        """Test ITLBO algorithm on constrained optimization problems"""
        constraints = [constraint_1, constraint_2]
        
        best_solution, best_scores, _ = ITLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            objective_function,
            constraints
        )
        self.assertEqual(len(best_solution), self.num_variables)
        self.assertLess(objective_function(best_solution), 50.0)

    def test_MultiObjective_TLBO(self):
        """Test Multi-objective TLBO algorithm"""
        # Use a smaller problem for multi-objective optimization
        num_vars = 1
        bounds = np.array([[-10, 10] for _ in range(num_vars)])
        
        # Test on Schaffer N1 problem (a common multi-objective test problem)
        pareto_front, pareto_fitness, best_scores_history = MultiObjective_TLBO_algorithm(
            bounds, 
            self.num_iterations, 
            self.population_size, 
            num_vars, 
            [schaffer_n1_f1, schaffer_n1_f2]
        )
        
        # Check if we have a non-empty Pareto front
        self.assertGreater(len(pareto_front), 0)
        
        # Check if all solutions in the Pareto front are within bounds
        for solution in pareto_front:
            for i in range(num_vars):
                self.assertTrue(solution[i] >= bounds[i, 0])
                self.assertTrue(solution[i] <= bounds[i, 1])
        
        # Check if the algorithm makes progress over iterations for at least one objective
        # Due to the stochastic nature of the algorithm and the trade-offs in multi-objective optimization,
        # we can't guarantee improvement in all objectives simultaneously
        improvement_found = False
        for obj_scores in best_scores_history:
            if obj_scores[-1] < obj_scores[0]:
                improvement_found = True
                break
        self.assertTrue(improvement_found, "No improvement found in any objective")
        
        # Test with constraints
        pareto_front, pareto_fitness, best_scores_history = MultiObjective_TLBO_algorithm(
            bounds, 
            self.num_iterations, 
            self.population_size, 
            num_vars, 
            [schaffer_n1_f1, schaffer_n1_f2],
            constraints=[lambda x: x[0] - 5]  # x[0] <= 5
        )
        
        # Check if we have a non-empty Pareto front
        self.assertGreater(len(pareto_front), 0)
        
        # Check if all solutions satisfy the constraint
        for solution in pareto_front:
            self.assertLessEqual(solution[0], 5.1)  # Allow small violation due to numerical issues


if __name__ == '__main__':
    unittest.main()
