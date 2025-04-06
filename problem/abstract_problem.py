

from abc import ABC, abstractmethod
from pymoo.core.problem import ElementwiseProblem
from poly_sbst.common.abstract_executor import AbstractExecutor
import numpy as np

class AbstractProblem(ElementwiseProblem, ABC):
    """
    This is the base class for performing solution evaluation.

    Attributes:
        executor (AbstractExecutor): The executor used for evaluating solutions.
        n_var (int): The number of decision variables.
        n_obj (int): The number of objectives.
        n_ieq_constr (int): The number of inequality constraints.
        xl (Optional): The lower bounds of the decision variables.
        xu (Optional): The upper bounds of the decision variables.
        execution_data (dict): A dictionary to store execution data.
        n_evals (int): The number of evaluations performed.

    Methods:
        _evaluate: Abstract method for evaluating a solution.
        name: Property method to get the name of the problem.
    """

    def __init__(self, executor: AbstractExecutor, n_var: int=1, n_obj=1, n_ieq_constr=1, xl=None, xu=None):
        self.executor = executor
        self._name = "AbstractProblem"

        super().__init__(n_var=n_var, n_obj=n_obj, n_ieq_constr=n_ieq_constr, xl=xl, xu=xu)

        self.execution_data = {}
        self.n_evals = 0

    @abstractmethod
    def _evaluate(self, x, out, *args, **kwargs):
        """
        Abstract method for evaluating a solution.

        Args:
            x: The solution to be evaluated.
            out: The output array to store the evaluated objectives and constraints.
            *args: Additional positional arguments.
            **kwargs: Additional keyword arguments.
        """
        pass

    @property
    def name(self) -> int:
        """
        Get the name of the problem.

        Returns:
            str: The name of the problem.
        """
        return self._name
