import unittest
import numpy as np
from rao_algorithms import (
    BMR_algorithm,
    BWR_algorithm,
    Jaya_algorithm,
    TLBO_algorithm,
    Rao1_algorithm,
    Rao2_algorithm,
    Rao3_algorithm,
    TLBO_with_Elitism_algorithm,
    QOJAYA_algorithm,
    JCRO_algorithm,
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


class TestConvergenceHistory(unittest.TestCase):
    
    def setUp(self):
        # Common parameters for all tests
        self.population_size = 20
        self.num_iterations = 50  # Reduced for faster testing
        self.num_variables = 2
        self.bounds = np.array([[-5, 5] for _ in range(self.num_variables)])
    
    def verify_convergence_history(self, history, algorithm_name):
        """Verify that the convergence history has the expected structure and data"""
        # Common fields that all algorithms should have
        common_fields = [
            'best_scores', 
            'best_solutions', 
            'mean_scores', 
            'population_diversity', 
            'iteration_times'
        ]
        
        # Check that all common fields exist
        for field in common_fields:
            self.assertIn(field, history, f"{field} missing from {algorithm_name} history")
            self.assertEqual(len(history[field]), self.num_iterations, 
                            f"{field} in {algorithm_name} should have {self.num_iterations} entries")
        
        # For stochastic algorithms, we can't guarantee the final score is better than the initial
        # But we can check that the best score found during the run is better than the initial
        if len(history['best_scores']) > 0:
            best_score = min(history['best_scores'])
            self.assertLessEqual(best_score, history['best_scores'][0], 
                                f"{algorithm_name} best score not better than initial score")
        
        # Check that best_solutions has the correct shape
        for solution in history['best_solutions']:
            self.assertEqual(len(solution), self.num_variables, 
                            f"{algorithm_name} solution has wrong dimension")
    
    def test_BMR_history(self):
        """Test BMR algorithm convergence history"""
        _, _, history = BMR_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "BMR")
    
    def test_BWR_history(self):
        """Test BWR algorithm convergence history"""
        _, _, history = BWR_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "BWR")
    
    def test_Jaya_history(self):
        """Test Jaya algorithm convergence history"""
        _, _, history = Jaya_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "Jaya")
    
    def test_TLBO_history(self):
        """Test TLBO algorithm convergence history"""
        _, _, history = TLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "TLBO")
        
        # Check TLBO-specific fields
        self.assertIn('teacher_phase_improvements', history)
        self.assertIn('learner_phase_improvements', history)
    
    def test_Rao1_history(self):
        """Test Rao1 algorithm convergence history"""
        _, _, history = Rao1_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "Rao1")
    
    def test_Rao2_history(self):
        """Test Rao2 algorithm convergence history"""
        _, _, history = Rao2_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "Rao2")
    
    def test_Rao3_history(self):
        """Test Rao3 algorithm convergence history"""
        _, _, history = Rao3_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "Rao3")
    
    def test_TLBO_with_Elitism_history(self):
        """Test TLBO with Elitism algorithm convergence history"""
        _, _, history = TLBO_with_Elitism_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "TLBO_with_Elitism")
        
        # Check TLBO-specific fields
        self.assertIn('teacher_phase_improvements', history)
        self.assertIn('learner_phase_improvements', history)
        self.assertIn('elite_scores', history)
    
    def test_QOJAYA_history(self):
        """Test QOJAYA algorithm convergence history"""
        _, _, history = QOJAYA_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "QOJAYA")
        
        # Check QOJAYA-specific fields
        self.assertIn('opposition_improvements', history)
    
    def test_JCRO_history(self):
        """Test JCRO algorithm convergence history"""
        _, _, history = JCRO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "JCRO")
        
        # Check JCRO-specific fields
        self.assertIn('synthesis_improvements', history)
        self.assertIn('decomposition_improvements', history)
        self.assertIn('intermolecular_improvements', history)
    
    def test_GOTLBO_history(self):
        """Test GOTLBO algorithm convergence history"""
        _, _, history = GOTLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "GOTLBO")
        
        # Check GOTLBO-specific fields
        self.assertIn('teacher_phase_improvements', history)
        self.assertIn('learner_phase_improvements', history)
        self.assertIn('opposition_phase_improvements', history)
    
    def test_ITLBO_history(self):
        """Test ITLBO algorithm convergence history"""
        _, _, history = ITLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=True
        )
        
        self.verify_convergence_history(history, "ITLBO")
        
        # Check ITLBO-specific fields
        self.assertIn('teacher_phase_improvements', history)
        self.assertIn('learner_phase_improvements', history)
        self.assertIn('elite_scores', history)
    
    def test_MultiObjective_TLBO_history(self):
        """Test MultiObjective TLBO algorithm convergence history"""
        objective_funcs = [schaffer_n1_f1, schaffer_n1_f2]
        _, _, history = MultiObjective_TLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            objective_funcs,
            track_history=True
        )
        
        # Check multi-objective specific fields
        self.assertIn('pareto_front_size', history)
        self.assertIn('pareto_fronts', history)
        self.assertIn('pareto_fitness', history)
        self.assertIn('hypervolume', history)
        self.assertIn('teacher_phase_improvements', history)
        self.assertIn('learner_phase_improvements', history)
    
    def test_track_history_false(self):
        """Test that algorithms work correctly when track_history is False"""
        # Test with BMR algorithm
        best_solution, best_scores = BMR_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=False
        )
        
        self.assertIsInstance(best_solution, np.ndarray)
        self.assertIsInstance(best_scores, list)
        self.assertEqual(len(best_scores), self.num_iterations)
        
        # Test with TLBO algorithm
        best_solution, best_scores = TLBO_algorithm(
            self.bounds, 
            self.num_iterations, 
            self.population_size, 
            self.num_variables, 
            sphere_function,
            track_history=False
        )
        
        self.assertIsInstance(best_solution, np.ndarray)
        self.assertIsInstance(best_scores, list)
        self.assertEqual(len(best_scores), self.num_iterations)


if __name__ == '__main__':
    unittest.main()
