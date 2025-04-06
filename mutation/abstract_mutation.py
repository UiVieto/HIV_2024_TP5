from pymoo.core.mutation import Mutation
import numpy as np
import abc

class AbstractMutation(Mutation, abc.ABC):
    """
    Abstract base class for mutation operators.

    Args:
        mut_rate (float): The mutation rate, representing the probability of mutation for each individual.
        generator: The random number generator to use for generating random numbers.

    Attributes:
        mut_rate (float): The mutation rate.
        generator: The random number generator.

    Methods:
        _do: Perform mutation on the given population.
        _do_mutation: Perform mutation on an individual.

    """

    def __init__(self, mut_rate: float = 0.4, generator=None):
        super().__init__()
        self.mut_rate = mut_rate
        self.generator = generator

    def _do(self, problem, X, **kwargs):
        """
        Perform mutation on the given population.

        Args:
            problem: The optimization problem.
            X: The population to mutate.
            **kwargs: Additional keyword arguments.

        Returns:
            The mutated population.

        """
        self.problem = problem

        # for each individual
        for i in range(len(X)):
            r = np.random.random()

            # with a probability of mut_rate - change the order of characters
            if r < self.mut_rate:
                X[i, 0] = self._do_mutation(X[i, 0])

        return X

    @abc.abstractmethod
    def _do_mutation(self, x) -> np.ndarray:
        """
        Perform mutation on an individual.

        Args:
            x: The individual to mutate.

        Returns:
            The mutated individual.

        """
        pass