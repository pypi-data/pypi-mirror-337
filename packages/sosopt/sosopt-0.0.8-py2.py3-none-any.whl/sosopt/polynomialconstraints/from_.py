from __future__ import annotations

from donotation import do

import polymat
from polymat.typing import (
    MatrixExpression,
    SymmetricMatrixExpression,
)

from sosopt.polynomialconstraints.putinarpsatzconstraint import init_putinar_psatz_constraint
from sosopt.polynomialconstraints.sumofsqauresconstraint import init_sum_of_squares_constraint
from sosopt.polynomialconstraints.zeropolynomialconstraint import init_zero_polynomial_constraint
from sosopt.semialgebraicset import SemialgebraicSet


def zero_polynomial_constraint(
    name: str,
    equal_to_zero: MatrixExpression,
):
    return init_zero_polynomial_constraint(
        name=name,
        zero_matrix=equal_to_zero,
    )


def sos_constraint(
    name: str,
    greater_than_zero: MatrixExpression | None = None,
    smaller_than_zero: MatrixExpression | None = None,
):    
    if greater_than_zero is not None:
        positive_matrix = greater_than_zero
    elif smaller_than_zero is not None:
        positive_matrix = -smaller_than_zero
    else:
        raise Exception("SOS constraint requires condition.")

    return init_sum_of_squares_constraint(
        name=name,
        positive_matrix=positive_matrix,
    )


@do()
def sos_matrix_constraint(
    name: str,
    greater_than_zero: SymmetricMatrixExpression | None = None,
    smaller_than_zero: SymmetricMatrixExpression | None = None,
):
    if greater_than_zero is not None:
        condition = greater_than_zero
    elif smaller_than_zero is not None:
        condition = -smaller_than_zero
    else:
        raise Exception("SOS constraint requires condition.")

    shape = yield from polymat.to_shape(condition)

    x = polymat.define_variable(f"{name}_x", size=shape[0])

    return sos_constraint(
        name=name,
        greater_than_zero=x.T @ condition @ x,
    )


def psatz_putinar_constraint(
    name: str,
    domain: SemialgebraicSet | None = None,
    greater_than_zero: MatrixExpression | None = None,
    smaller_than_zero: MatrixExpression | None = None,
):
    
    if greater_than_zero is not None:
        positive_matrix = greater_than_zero
    elif smaller_than_zero is not None:
        positive_matrix = -smaller_than_zero
    else:
        raise Exception("SOS constraint requires condition.")

    return init_putinar_psatz_constraint(
        name,
        expression=positive_matrix,
        domain=domain,
    )