from pymoo.core.crossover import Crossover
import numpy as np
import abc



class AbstractCrossover(Crossover, abc.ABC):
    """
    Abstract base class for crossover operations.

    Parameters:
    - cross_rate (float): The probability of performing crossover.

    Methods:
    - _do(problem, X, **kwargs): Performs crossover operation on the input population.
    - _do_crossover(problem, a, b): Performs crossover between two parents and returns the offspring.
    """
    def __init__(self, cross_rate: float = 0.9):
        super().__init__(2, 2)
        self.cross_rate = cross_rate

    def _do(self, problem, X, **kwargs):
        """
        Performs crossover operation on the input population.

        Parameters:
        - problem: The optimization problem.
        - X: The input population.
        - **kwargs: Additional arguments.

        Returns:
        - Y: The output population after crossover.
        """
        _, n_matings, n_var = X.shape
        Y = np.full_like(X, None, dtype=object)

        for k in range(n_matings):
            r = np.random.random()
            a, b = X[0, k, 0], X[1, k, 0]
            if r < self.cross_rate:
                off_a, off_b = self._do_crossover(problem, a, b)
                Y[0, k, 0], Y[1, k, 0] = off_a, off_b
            else:
                Y[0, k, 0], Y[1, k, 0] = a, b

        return Y
    
    @abc.abstractmethod
    def _do_crossover(self, problem, a, b) -> tuple: 
        """
        Performs crossover between two parents and returns the offspring.

        Parameters:
        - problem: The optimization problem.
        - a: The first parent.
        - b: The second parent.

        Returns:
        - tuple: The offspring generated from crossover.
        """
        pass