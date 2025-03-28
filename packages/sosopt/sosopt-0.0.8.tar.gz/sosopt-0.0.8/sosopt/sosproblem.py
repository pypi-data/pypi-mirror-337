from __future__ import annotations

from dataclasses import dataclass, replace

from sosopt.coneconstraints.coneconstraint import ConeConstraint
import statemonad

from polymat.typing import ScalarPolynomialExpression, VectorExpression, State

from sosopt.conicproblem import ConicProblem
from sosopt.polynomialconstraints.polynomialconstraint import PolynomialConstraint
from sosopt.polymat.decisionvariablesymbol import DecisionVariableSymbol
from sosopt.solvers.solvermixin import SolverMixin


@dataclass(frozen=True)
class SOSProblem:
    """
    Generic sum of squares problem.
    This problem contains expression objects.
    """

    lin_cost: ScalarPolynomialExpression
    quad_cost: VectorExpression | None
    constraints: tuple[PolynomialConstraint | ConeConstraint, ...]
    solver: SolverMixin
    # conic_problem: ConicProblem
    settings: dict

    def copy(self, /, **others):
        return replace(self, **others)

    def eval(self, substitutions: dict[DecisionVariableSymbol, tuple[float, ...]]):
        def gen_evaluated_constraints():
            for constraint in self.constraints:
                evaluated_constraint = constraint.eval(substitutions)

                if evaluated_constraint:
                    yield evaluated_constraint

        evaluated_constraints = tuple(gen_evaluated_constraints())
        return init_sos_problem(
            lin_cost=self.lin_cost.eval(substitutions),
            quad_cost=self.quad_cost.eval(substitutions) if self.quad_cost is not None else None,
            solver=self.solver,
            constraints=evaluated_constraints,
        )

    def to_conic_problem(self):
        def _to_conic_problem(state: State):
            cone_constraints = []

            # def gen_cone_constraints():
            for constraint in self.constraints:
                match constraint:
                    case PolynomialConstraint():
                        for primitive in constraint.primitives:
                            state, cone_constraint = primitive.to_cone_constraint(
                                settings=self.settings
                            ).apply(state)
                            cone_constraints.append(cone_constraint)

                    case ConeConstraint():
                        cone_constraints.append(constraint)

            # cone_constraints = tuple(gen_cone_constraints())

            problem = ConicProblem(
                lin_cost=self.lin_cost,
                quad_cost=self.quad_cost,
                solver=self.solver,
                constraints=tuple(cone_constraints),
            )

            # return statemonad.from_[State](problem)
            return state, problem

        return statemonad.get_map_put(_to_conic_problem)

    def solve(self):
        return self.to_conic_problem().flat_map(lambda p: p.solve())


def init_sos_problem(
    lin_cost: ScalarPolynomialExpression,
    constraints: tuple[PolynomialConstraint | ConeConstraint, ...],
    solver: SolverMixin,
    quad_cost: VectorExpression | None = None,
    settings: dict | None = None,
    sparse_gram: bool | None = None,
):

    if sparse_gram is None:
        sparse_gram = True

    if settings is None:
        settings = {
            'sparse_gram': sparse_gram,
        }

    return SOSProblem(
        lin_cost=lin_cost,
        quad_cost=quad_cost,
        constraints=constraints,
        solver=solver,
        settings=settings,
    )
