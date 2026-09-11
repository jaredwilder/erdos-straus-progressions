---
id: erdos-straus-gp
claim: |-
  Every positive solution of 4/n = 1/x+1/y+1/z whose ordered denominators x<y<z form a GEOMETRIC
  progression arises uniquely as (x,y,z) = tD(a^2, ab, b^2) with 0<a<b, gcd(a,b)=1,
  D = a^2+ab+b^2, t>=1, and n = 4t a^2 b^2. The parameterisation is if-and-only-if, the
  parameters are uniquely recoverable, and no primitive denominator triple exists.
status: closed
tier: gold
reality_score: 0.95
domain: math
origin: external_drop
artifact_kind: classification
truth_mode: certified
scope_grade: bounded_family
inference: deductive
independence: independently_reverified
reproducibility: artifact_verified
novelty: cleared
claim_ir:
  claim_id: "egyptian_fractions:erdos_straus_gp"
  assertion_kind: classification
  display: "Complete if-and-only-if classification of Erdos-Straus solutions with geometric-progression denominators."
  scope:
    domain: diophantine_number_theory
    label: "Erdos-Straus solutions whose three denominators form a geometric progression"
  definitions:
    geometric_denominators: "x<y<z with y^2 = xz; detected structurally, so RATIONAL common ratios are included, not only integer ratios"
    primitive: "gcd(x,y,z)=1"
  tags: [erdos_straus, egyptian_fraction, diophantine, classification, geometric_progression]
claims:
  - id: parameterisation_iff
    inference: deductive
    truth_mode: certified
    status: closed
  - id: no_primitive_triple
    inference: deductive
    truth_mode: certified
    status: closed
  - id: gcd_divisibility_lemma
    inference: deductive
    truth_mode: certified
    status: closed
---

# Erdos-Straus solutions with geometric-progression denominators

## THEOREM

Let `x < y < z` be positive integers in geometric progression with `4/n = 1/x + 1/y + 1/z`.

Every integer geometric triple is uniquely `(x,y,z) = g(a², ab, b²)` with `0 < a < b`,
`gcd(a,b) = 1`. Put `D = a² + ab + b²`. Then all solutions, and only the solutions, are

    g = tD,    n = 4t a² b²,    (x,y,z) = tD(a², ab, b²),    t >= 1.

The parameterisation is unique, and **no primitive denominator triple exists**.

## The proof is four lines, and its load-bearing step is tested here

The reciprocal sum is `(a²+ab+b²)/(g a² b²) = D/(g a² b²)`, so `nD = 4g a² b²`. For coprime
`a, b` one has `gcd(D, ab) = 1` and `D` odd, hence **`gcd(D, 4a²b²) = 1`**, so `D | g`. Writing
`g = tD` gives the classification; substitution proves sufficiency.

That gcd lemma is the entire argument. It was **tested over every coprime pair below 300 — zero
counterexamples** — rather than assumed.

## Independence — completeness is the half that could fail, and it is the half checked here

| direction | who checks it | result |
|---|---|---|
| **soundness** — every constructed triple is a solution | vendor, at scale | 73,064 coprime pairs, 292,256 constructed solutions |
| **completeness** — every solution is constructed | **this estate** | brute force with NO parameterisation |

Brute force over every geometric triple with `z <= 4000`, detecting the progression structurally
as `y² = xz` so rational ratios are included:

| solutions found | reproduced by the formula | missed | spurious | primitive |
|---|---|---|---|---|
| 236 | **236** | **0** | **0** | **0** |

Also verified: the closed form for `n` on every constructed solution (0 disagreements), and
uniqueness of `(a,b)` (0 collisions).

Standalone verifier: `oracle/library/patents/artifacts/verify_erdos_straus_gp.py`, carrying four
negative controls it must reject.

## Relationship to the AP theorem — different theorem, different D

This estate already banked the **arithmetic**-progression classification (`erdos-straus-ap`),
where `D = 3a² − d²` and the parity of `a, d` splits the result into two branches. The geometric
case has `D = a² + ab + b²`, no parity split, and a different divisibility argument. They are
companions, not restatements — and both conclude that no primitive triple exists, which is the
genuinely interesting shared consequence.

## Scope

Strictly increasing denominators only. The progression is detected as `y² = xz`, which admits
rational common ratios; restricting to integer ratios would shrink the search space and make
completeness trivially easier to satisfy.

## Falsifier

A geometric-progression solution not produced by the parameterisation; or any such solution with
`gcd(x,y,z) = 1`; or a coprime pair `a < b` with `gcd(a²+ab+b², 4a²b²) != 1`.
