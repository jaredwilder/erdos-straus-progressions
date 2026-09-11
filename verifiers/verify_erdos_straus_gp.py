#!/usr/bin/env python3
"""verify_erdos_straus_gp - STANDALONE verifier: Erdos-Straus with GEOMETRIC-progression denominators.

A stranger runs this with CPython alone. No repo, no package, no network, no arguments.

    python verify_erdos_straus_gp.py

THE THEOREM (produced by MathFire 10.0.0, an external drop; INDEPENDENTLY VERIFIED here):

    Let x < y < z be positive integers in GEOMETRIC progression with

        4/n = 1/x + 1/y + 1/z.

    Every integer geometric triple is uniquely (x,y,z) = g(a^2, ab, b^2) with 0 < a < b and
    gcd(a,b) = 1. Put D = a^2 + ab + b^2. Then all solutions, and only the solutions, are

        g = tD,   n = 4t a^2 b^2,   (x,y,z) = tD(a^2, ab, b^2),   t >= 1.

    The parameterisation is unique, and NO PRIMITIVE denominator triple exists.

THE PROOF IS SHORT AND THE VERIFIER CHECKS ITS LOAD-BEARING STEP. The reciprocal sum is
(a^2+ab+b^2)/(g a^2 b^2) = D/(g a^2 b^2), so nD = 4 g a^2 b^2. For coprime a,b one has
gcd(D, ab) = 1 and D odd, hence gcd(D, 4a^2b^2) = 1, so D | g. That gcd lemma is the whole
argument, and it is tested here over every coprime pair up to a bound rather than assumed.

⛔ THE HALF THAT COULD ACTUALLY BE FALSE IS COMPLETENESS, and it is the half checked hardest.
Soundness -- every constructed triple is a solution -- is easy and the vendor checks it.
COMPLETENESS -- every solution is constructed -- is the direction that could fail. This script
brute-forces every geometric-progression solution in a bounded range using NO parameterisation
at all, then verifies the formula reproduces every single one.

A geometric triple is detected structurally as y^2 = xz, which admits rational ratios; it is not
restricted to integer ratios. That matters: restricting to integer ratios would silently shrink
the search and make completeness trivially easier to satisfy.

EXIT 0 iff every check passes.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from math import gcd

LIMIT = 4000          # brute-force every GP solution with z <= LIMIT
PAR = 200             # parameter sweep bound for construction
LEMMA = 300           # bound for the gcd lemma sweep


def brute_force(limit: int = LIMIT) -> set[tuple[int, int, int]]:
    """Every (x,y,z) in geometric progression with 4/n = 1/x+1/y+1/z for a positive integer n.

    Detects the progression as y*y == x*z, so rational common ratios are included.
    """
    out = set()
    for x in range(1, limit + 1):
        for y in range(x + 1, limit + 1):
            if (y * y) % x:
                continue
            z = y * y // x                       # geometric: y^2 = xz
            if z <= y or z > limit:
                continue
            s = Fraction(1, x) + Fraction(1, y) + Fraction(1, z)
            q = Fraction(4, 1) / s
            if q.denominator == 1 and q.numerator > 0:
                out.add((x, y, z))
    return out


def from_parameters(limit: int = LIMIT, a_max: int = PAR) -> dict[tuple[int, int, int], int]:
    """Every triple the theorem's formula produces, with z <= limit, mapped to its n."""
    out: dict[tuple[int, int, int], int] = {}
    for a in range(1, a_max):
        for b in range(a + 1, a_max):
            if gcd(a, b) != 1:
                continue
            D = a * a + a * b + b * b
            t = 1
            while True:
                g = t * D
                x, y, z = g * a * a, g * a * b, g * b * b
                if z > limit:
                    break
                out[(x, y, z)] = 4 * t * a * a * b * b
                t += 1
    return out


def main() -> int:
    failures = []

    def check(label, ok, detail=""):
        print(f"  [{'OK ' if ok else 'FAIL'}] {label}{('  ' + detail) if detail else ''}")
        if not ok:
            failures.append(label)

    print(f"Brute-forcing every GP-denominator solution with z <= {LIMIT}, no parameterisation.\n")
    brute = brute_force()
    param = from_parameters()
    print(f"  brute force found: {len(brute)}    parameterisation produced: {len(param)}\n")

    missed = brute - set(param)
    check("COMPLETENESS - the parameterisation misses NOTHING", not missed,
          f"{len(missed)} missed" + (f", e.g. {sorted(missed)[:3]}" if missed else ""))

    spurious = [t for t in param if t not in brute]
    check("SOUNDNESS - every constructed triple is a real solution", not spurious,
          f"{len(spurious)} spurious")

    bad_n = [(k, n) for k, n in param.items()
             if Fraction(4, n) != Fraction(1, k[0]) + Fraction(1, k[1]) + Fraction(1, k[2])]
    check("the closed form n = 4t a^2 b^2 holds on every constructed solution", not bad_n,
          f"{len(bad_n)} disagreements")

    prim = [t for t in brute if gcd(gcd(t[0], t[1]), t[2]) == 1]
    check("NO PRIMITIVE TRIPLE EXISTS - searched, not asserted", not prim,
          f"{len(prim)} found among {len(brute)} solutions")

    # THE LOAD-BEARING LEMMA: gcd(D, 4a^2b^2) = 1 for coprime a, b
    viol = [(a, b) for a in range(1, LEMMA) for b in range(a + 1, LEMMA)
            if gcd(a, b) == 1 and gcd(a * a + a * b + b * b, 4 * a * a * b * b) != 1]
    check(f"gcd lemma gcd(D, 4a^2b^2) = 1 for every coprime pair a<b<{LEMMA}", not viol,
          f"{len(viol)} counterexamples")

    # uniqueness of the parameters
    seen, collisions = {}, 0
    for a in range(1, 90):
        for b in range(a + 1, 90):
            if gcd(a, b) != 1:
                continue
            D = a * a + a * b + b * b
            key = (D * a * a, D * a * b, D * b * b)
            if key in seen and seen[key] != (a, b):
                collisions += 1
            seen[key] = (a, b)
    check("parameters are uniquely recoverable - no two (a,b) give the same triple",
          collisions == 0, f"{collisions} collisions")

    # NEGATIVE CONTROLS: a checker that never rejects is not a checker
    check("negative control - (1,2,3) is not a GP solution", (1, 2, 3) not in brute)
    check("negative control - every produced triple really is geometric",
          all(y * y == x * z for (x, y, z) in param))
    check("negative control - brute force actually found something", len(brute) > 0,
          f"{len(brute)} solutions")
    check("negative control - a NON-geometric AP triple is never produced",
          (11, 22, 33) not in param)

    print(f"\n{'ALL CHECKS PASSED' if not failures else 'FAILED: ' + ', '.join(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
