"""Transparent finite-size and asymptotic cost models for exTNFS experiments.

The finite-size equations follow Barbulescu--Duquesne (2019), while norm
selection remains an explicit input.  The asymptotic model uses their
``L_Q[c]`` convention and never hides the finite-size prefactor.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from functools import lru_cache
from math import ceil, log, log2

import mpmath as mp


def _log2_sum(left: float, right: float) -> float:
    maximum = max(left, right)
    return maximum + log2(2.0 ** (left - maximum) + 2.0 ** (right - maximum))


@lru_cache(maxsize=8)
def _dickman_intervals(
    maximum_integer: int,
    polynomial_degree: int,
) -> tuple[tuple[mp.mpf, ...], ...]:
    """Build stable Chebyshev representations of Dickman's rho by interval.

    On ``n <= u <= n + 1`` the delay equation is
    ``rho'(u) = -rho(u - 1) / u``.  Representing each unit interval separately
    avoids the catastrophic cancellation of a low-order cumulative quadrature
    once rho falls to about 1e-12 in the BLS12 worked example.
    """
    if maximum_integer < 1:
        raise ValueError("maximum_integer must be positive")
    if polynomial_degree < 12:
        raise ValueError("polynomial_degree must be at least 12")

    with mp.workdps(80):
        intervals: list[tuple[mp.mpf, ...]] = [(mp.mpf(1),)]
        for integer_part in range(1, maximum_integer + 1):
            previous = intervals[-1]

            def derivative(local_u: mp.mpf) -> mp.mpf:
                return -_evaluate_polynomial(previous, local_u) / (
                    integer_part + local_u
                )

            # mpmath returns ordinary-power coefficients in descending order.
            descending = mp.chebyfit(
                derivative,
                [mp.mpf(0), mp.mpf(1)],
                polynomial_degree,
            )
            derivative_ascending = tuple(reversed(descending))
            current = (
                _evaluate_polynomial(previous, mp.mpf(1)),
                *(
                    derivative_ascending[index] / (index + 1)
                    for index in range(len(derivative_ascending))
                ),
            )
            intervals.append(current)
    return tuple(intervals)


def _evaluate_polynomial(coefficients: tuple[mp.mpf, ...], value: mp.mpf) -> mp.mpf:
    """Evaluate ascending power-basis coefficients using Horner's rule."""
    result = mp.mpf(0)
    for coefficient in reversed(coefficients):
        result = result * value + coefficient
    return result


def dickman_rho(u: float, *, polynomial_degree: int = 30) -> float:
    """Approximate Dickman's rho with interval Chebyshev integration."""
    if u < 0:
        raise ValueError("u must be non-negative")
    if u <= 1:
        return 1.0
    if u > 16:
        raise ValueError("the Dickman evaluator is validated only for u <= 16")
    intervals = _dickman_intervals(ceil(u), polynomial_degree)
    integer_part = int(u)
    with mp.workdps(80):
        if u == integer_part:
            return float(
                _evaluate_polynomial(intervals[integer_part - 1], mp.mpf(1))
            )
        return float(
            _evaluate_polynomial(
                intervals[integer_part],
                mp.mpf(str(u - integer_part)),
            )
        )


def log2_dickman_rho(u: float, *, polynomial_degree: int = 30) -> float:
    """Return log2(rho(u)) with a clear failure on numerical underflow."""
    probability = dickman_rho(u, polynomial_degree=polynomial_degree)
    if probability <= 0:
        raise ArithmeticError("Dickman approximation became non-positive")
    return log2(probability)


@dataclass(frozen=True, slots=True)
class FiniteTNFSParameters:
    """All choices needed by the Barbulescu--Duquesne finite-size equation."""

    coefficient_bound: float
    smoothness_bound_bits: float
    eta: int
    roots_of_unity_index: int = 1
    relation_automorphisms: int = 1
    linear_algebra_automorphisms: int = 1
    factor_base_numerator: float = 2.0
    matrix_numerator: float = 1.0
    sieve_space_sign_quotient: float = 2.0
    filtering_log2_bound_power: float = 1.0
    nonzero_entries_per_row: int = 128
    sieve_overhead_bits: float = 0.0
    linear_algebra_overhead_bits: float = 0.0
    dickman_polynomial_degree: int = 30

    def __post_init__(self) -> None:
        if self.coefficient_bound <= 0 or self.smoothness_bound_bits <= 0:
            raise ValueError("coefficient and smoothness bounds must be positive")
        integer_fields = (
            self.eta,
            self.roots_of_unity_index,
            self.relation_automorphisms,
            self.linear_algebra_automorphisms,
            self.nonzero_entries_per_row,
            self.dickman_polynomial_degree,
        )
        if any(value <= 0 for value in integer_fields):
            raise ValueError("dimension, automorphism, and matrix parameters must be positive")
        if self.dickman_polynomial_degree < 12:
            raise ValueError("Dickman polynomial degree must be at least 12")
        positive_real_fields = (
            self.factor_base_numerator,
            self.matrix_numerator,
            self.sieve_space_sign_quotient,
            self.filtering_log2_bound_power,
        )
        if any(value <= 0 for value in positive_real_fields):
            raise ValueError("factor-base, matrix, sign, and filtering parameters must be positive")


@dataclass(frozen=True, slots=True)
class FiniteTNFSResult:
    """A complete, inspectable decomposition of one finite-size estimate."""

    norm_f_bits: float
    norm_g_bits: float
    smoothness_f_log2: float
    smoothness_g_log2: float
    sieve_space_log2: float
    relation_yield_log2: float
    factor_base_log2: float
    reduced_factor_base_log2: float
    enough_relations: bool
    sieve_cost_log2: float
    linear_algebra_cost_log2: float
    total_cost_log2: float


def finite_tnfs_cost(
    norm_f_bits: float,
    norm_g_bits: float,
    parameters: FiniteTNFSParameters,
) -> FiniteTNFSResult:
    """Evaluate the finite-size SexTNFS model from explicit average norm sizes."""
    if norm_f_bits <= 0 or norm_g_bits <= 0:
        raise ValueError("norm bit sizes must be positive")
    bound_bits = parameters.smoothness_bound_bits
    log_probability_f = log2_dickman_rho(
        norm_f_bits / bound_bits,
        polynomial_degree=parameters.dickman_polynomial_degree,
    )
    log_probability_g = log2_dickman_rho(
        norm_g_bits / bound_bits,
        polynomial_degree=parameters.dickman_polynomial_degree,
    )

    natural_log_bound = bound_bits * log(2.0)
    log_factor_base = (
        log2(parameters.factor_base_numerator)
        + bound_bits
        - log2(natural_log_bound)
    )
    log_sieve_space = (
        2.0 * parameters.eta * log2(2.0 * parameters.coefficient_bound + 1.0)
        - log2(parameters.sieve_space_sign_quotient)
        - log2(parameters.roots_of_unity_index)
    )
    log_relation_yield = log_sieve_space + log_probability_f + log_probability_g

    log_relation_target = log_factor_base - log2(parameters.relation_automorphisms)
    log_sieve_cost = (
        log_relation_target
        - log_probability_f
        - log_probability_g
        + parameters.sieve_overhead_bits
    )
    log_matrix_dimension = (
        log2(parameters.matrix_numerator)
        + bound_bits
        - log2(natural_log_bound)
        - parameters.filtering_log2_bound_power * log2(bound_bits)
        - log2(parameters.linear_algebra_automorphisms)
    )
    log_linear_algebra = (
        log2(parameters.nonzero_entries_per_row)
        + 2.0 * log_matrix_dimension
        + parameters.linear_algebra_overhead_bits
    )
    return FiniteTNFSResult(
        norm_f_bits=norm_f_bits,
        norm_g_bits=norm_g_bits,
        smoothness_f_log2=log_probability_f,
        smoothness_g_log2=log_probability_g,
        sieve_space_log2=log_sieve_space,
        relation_yield_log2=log_relation_yield,
        factor_base_log2=log_factor_base,
        reduced_factor_base_log2=log_relation_target,
        enough_relations=log_relation_yield >= log_relation_target,
        sieve_cost_log2=log_sieve_cost,
        linear_algebra_cost_log2=log_linear_algebra,
        total_cost_log2=_log2_sum(log_sieve_cost, log_linear_algebra),
    )


@dataclass(frozen=True, slots=True)
class AsymptoticTNFSModel:
    """An explicit o(1)-less ``2^kappa L_Q[c]`` model."""

    l_constant: float = 32.0
    log2_prefactor: float = -7.0
    l_exponent: float = 1.0 / 3.0
    notation_denominator: float = 9.0
    polynomial_selection: str = "SexTNFS special-form"
    calibration: str = "Barbulescu--Duquesne record prefactor"

    def __post_init__(self) -> None:
        if self.l_constant <= 0:
            raise ValueError("l_constant must be positive")
        if not 0 < self.l_exponent < 1:
            raise ValueError("l_exponent must lie strictly between zero and one")
        if self.notation_denominator <= 0:
            raise ValueError("notation_denominator must be positive")

    def security_bits_from_field_bits(self, field_bits: float) -> float:
        """Return log2 attack cost for a field containing about 2^field_bits elements."""
        if field_bits <= 1:
            raise ValueError("field_bits must exceed one")
        log_q = field_bits * log(2.0)
        log_l = (
            (self.l_constant / self.notation_denominator) ** self.l_exponent
            * log_q**self.l_exponent
            * log(log_q) ** (1.0 - self.l_exponent)
        )
        return self.log2_prefactor + log_l / log(2.0)

    def security_bits(self, p: int, embedding_degree: int) -> float:
        """Return log2 attack cost for F_(p^k)."""
        if p <= 1 or embedding_degree <= 0:
            raise ValueError("p and embedding_degree must be positive")
        return self.security_bits_from_field_bits(embedding_degree * log2(p))

    def calibrated_to(self, field_bits: float, security_bits: float, source: str) -> AsymptoticTNFSModel:
        """Return a copy whose named prefactor passes through one finite-size anchor."""
        unshifted = replace(self, log2_prefactor=0.0).security_bits_from_field_bits(field_bits)
        return replace(
            self,
            log2_prefactor=security_bits - unshifted,
            calibration=source,
        )


def tnfs_model_preset(name: str) -> AsymptoticTNFSModel:
    """Return one of the documented sensitivity scenarios."""
    normalized = name.lower()
    if normalized == "sextnfs-o1less":
        return AsymptoticTNFSModel()
    if normalized == "bn254-calibrated":
        return AsymptoticTNFSModel().calibrated_to(
            3072.0,
            99.69,
            "Barbulescu--Duquesne 2019 BN worked example",
        )
    if normalized == "extnfs-composite":
        return AsymptoticTNFSModel(
            l_constant=48.0,
            log2_prefactor=-7.0,
            polynomial_selection="exTNFS composite-degree",
            calibration="same record prefactor as the sensitivity baseline",
        )
    raise ValueError(
        "unknown model preset; expected sextnfs-o1less, bn254-calibrated, or extnfs-composite"
    )


def pollard_security_bits(order: int, *, overhead_bits: float = 0.0) -> float:
    """Return the conventional square-root generic-group cost in bits."""
    if order <= 1:
        raise ValueError("order must exceed one")
    return 0.5 * log2(order) + overhead_bits


def pollard_security_from_order_bits(order_bits: float, *, overhead_bits: float = 0.0) -> float:
    """Apply the same model when only a real-valued order bit size is known."""
    if order_bits <= 0:
        raise ValueError("order_bits must be positive")
    return 0.5 * order_bits + overhead_bits
