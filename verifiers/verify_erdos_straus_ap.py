#!/usr/bin/env python3
"""verify_erdos_straus_ap - STANDALONE verifier: Erdos-Straus solutions with AP denominators.

A stranger runs this with nothing but CPython. No repo, no package, no network, no arguments.

    python verify_erdos_straus_ap.py

THE THEOREM (produced by MathFire 8.0.0, an external drop; INDEPENDENTLY VERIFIED here):

    Every positive solution of  4/n = 1/x + 1/y + 1/z  whose ordered denominators x < y < z
    form an arithmetic progression arises UNIQUELY as

        (x, y, z) = g * (a - d, a, a + d),      a > d > 0,  gcd(a, d) = 1,  t >= 1

    with  D = 3a^2 - d^2  and

        a, d opposite parity:   g = t*D,      n = 4*t*a*(a^2 - d^2)
        a, d both odd:          g = t*D / 2,  n = 2*t*a*(a^2 - d^2)

    In particular NO PRIMITIVE denominator triple exists: gcd(x, y, z) = 1 is impossible.

⛔ THE DIRECTION THAT MATTERS IS THE ONE THE VENDOR NEVER TESTS.

There are two halves to an "if and only if":
    SOUNDNESS   -- every triple the formula builds really is a solution.
    COMPLETENESS -- every solution really is built by the formula.

The vendor's shipped standalone verifier checks SOUNDNESS only, over a >= 500 and t <= 6, and
its in-package `verify` checks minimality just for a < 15. Its printed line
`primitive_triples_found=0` is a HARDCODED PRINT LITERAL -- nothing in that file ever searches
for a primitive triple.

COMPLETENESS is the half that could actually be false, and it is the half nobody ran. This
script runs it: it brute-forces every AP-denominator solution in a bounded range WITHOUT using
the parameterisation at all, then checks the parameterisation reproduces every one of them.

THE HYPOTHESES ARE HARD PRECONDITIONS, not advice (they are enforced in the vendor source):
    a > d > 0        -- so x < y < z strictly; constant "APs" like 4/4 = 1/3+1/3+1/3 are OUT OF SCOPE
    gcd(a, d) = 1    -- reduced parameters
    t >= 1

WHY THE PARITY SPLIT IS EXACTLY TWO CASES: gcd(3a^2 - d^2, 4a(a^2 - d^2)) is 1 when a and d
have opposite parity and 2 when both are odd. Under gcd(a,d) = 1 the both-even case cannot
occur, so the two branches are exhaustive. This script tests that gcd lemma directly rather
than trusting it.

EXIT 0 iff every check passes.
"""
from __future__ import annotations

import sys
from fractions import Fraction
from math import gcd

LIMIT = 1200          # brute-force every AP solution with z <= LIMIT
A_MAX = 300           # parameter sweep bound


def brute_force(limit: int = LIMIT) -> set[tuple[int, int, int]]:
    """Every (x,y,z) in AP with 4/n = 1/x+1/y+1/z for some positive integer n.

    Uses NO parameterisation. Exact rational arithmetic, no floats.
    """
    out = set()
    for x in range(1, limit + 1):
        for y in range(x + 1, limit + 1):
            z = 2 * y - x                      # arithmetic progression
            if z > limit or z <= y:
                continue
            s = Fraction(1, x) + Fraction(1, y) + Fraction(1, z)
            q = Fraction(4, 1) / s             # n such that 4/n = s
            if q.denominator == 1 and q.numerator > 0:
                out.add((x, y, z))
    return out


def from_parameters(limit: int = LIMIT, a_max: int = A_MAX):
    """Every triple the theorem's formula produces, with z <= limit. Also returns n."""
    triples = {}
    for a in range(2, a_max + 1):
        for d in range(1, a):
            if gcd(a, d) != 1:
                continue
            D = 3 * a * a - d * d
            both_odd = (a % 2 == 1) and (d % 2 == 1)
            h = 2 if both_odd else 1
            if D % h:
                continue
            q = D // h
            t = 1
            while True:
                g = t * q
                x, y, z = g * (a - d), g * a, g * (a + d)
                if z > limit:
                    break
                n = (2 if both_odd else 4) * t * a * (a * a - d * d)
                triples[(x, y, z)] = n
                t += 1
    return triples


def main() -> int:
    failures = []

    def check(label, ok, detail=""):
        print(f"  [{'OK ' if ok else 'FAIL'}] {label}{('  ' + detail) if detail else ''}")
        if not ok:
            failures.append(label)

    print(f"Brute-forcing every AP-denominator solution with z <= {LIMIT}, no parameterisation.\n")
    brute = brute_force()
    param = from_parameters()
    print(f"  brute force found: {len(brute)}    parameterisation produced: {len(param)}\n")

    missed = brute - set(param)
    check("COMPLETENESS - parameterisation misses NOTHING", not missed,
          f"{len(missed)} missed" + (f", e.g. {sorted(missed)[:3]}" if missed else ""))

    spurious = [t for t in param if t not in brute and t[2] <= LIMIT]
    check("SOUNDNESS - every constructed triple is a real solution", not spurious,
          f"{len(spurious)} spurious")

    # the n values must agree with the closed forms
    bad_n = []
    for (x, y, z), n in param.items():
        if Fraction(4, n) != Fraction(1, x) + Fraction(1, y) + Fraction(1, z):
            bad_n.append((x, y, z, n))
    check("the closed forms for n are correct on every constructed solution", not bad_n,
          f"{len(bad_n)} disagreements")

    prim = [t for t in brute if gcd(gcd(t[0], t[1]), t[2]) == 1]
    check("NO PRIMITIVE TRIPLE EXISTS - searched, not asserted", not prim,
          f"{len(prim)} found among {len(brute)} solutions")

    # the parity gcd lemma, tested rather than trusted
    bad_lemma = []
    for a in range(2, A_MAX + 1):
        for d in range(1, a):
            if gcd(a, d) != 1:
                continue
            want = 2 if (a % 2 and d % 2) else 1
            got = gcd(3 * a * a - d * d, 4 * a * (a * a - d * d))
            if got != want:
                bad_lemma.append((a, d, got, want))
    check(f"parity gcd lemma holds for every coprime pair a <= {A_MAX}", not bad_lemma,
          f"{len(bad_lemma)} counterexamples")

    # uniqueness: no two distinct parameter triples give the same denominators
    seen, collisions = {}, 0
    for a in range(2, 80):
        for d in range(1, a):
            if gcd(a, d) != 1:
                continue
            D = 3 * a * a - d * d
            h = 2 if (a % 2 and d % 2) else 1
            if D % h:
                continue
            g = D // h
            key = (g * (a - d), g * a, g * (a + d))
            if key in seen and seen[key] != (a, d):
                collisions += 1
            seen[key] = (a, d)
    check("parameters are uniquely recoverable - no two (a,d) give the same triple",
          collisions == 0, f"{collisions} collisions")

    # NEGATIVE CONTROLS: a checker that never rejects is not a checker
    check("negative control - (1,2,3) is NOT a solution", (1, 2, 3) not in brute)
    check("negative control - a non-AP triple is never produced",
          all(y - x == z - y for (x, y, z) in param))
    check("negative control - brute force actually found something", len(brute) > 0,
          f"{len(brute)} solutions")

    print(f"\n{'ALL CHECKS PASSED' if not failures else 'FAILED: ' + ', '.join(failures)}")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
