---
id: erdos-straus-ap
claim: |-
  Every positive solution of 4/n = 1/x+1/y+1/z with x<y<z in arithmetic progression arises uniquely
  as (x,y,z)=g(a-d,a,a+d) with a>d>0, gcd(a,d)=1, t>=1, D=3a^2-d^2, and g=tD with n=4ta(a^2-d^2)
  for opposite parity or g=tD/2 with n=2ta(a^2-d^2) when both are odd. No primitive denominator
  triple exists.
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
  claim_id: "egyptian_fractions:erdos_straus_ap"
  assertion_kind: classification
  display: "Complete if-and-only-if classification of Erdos-Straus solutions with AP denominators; no primitive triple exists."
  scope:
    domain: diophantine_number_theory
    label: "Erdos-Straus solutions whose three denominators form an arithmetic progression"
  definitions:
    ap_denominators: "x<y<z with y-x = z-y; STRICTLY increasing, so d>0 and constant triples are out of scope"
    primitive: "gcd(x,y,z)=1"
  tags: [erdos_straus, egyptian_fraction, diophantine, classification, arithmetic_progression]
claims:
  - id: parameterization_iff
    inference: deductive
    truth_mode: certified
    status: closed
  - id: no_primitive_triple
    inference: deductive
    truth_mode: certified
    status: closed
  - id: parity_gcd_lemma
    inference: deductive
    truth_mode: certified
    status: closed
---

# Erdos-Straus solutions with arithmetic-progression denominators

## THEOREM

Every positive solution of `4/n = 1/x + 1/y + 1/z` whose ordered denominators `x < y < z` form an
arithmetic progression arises **uniquely** as

    (x, y, z) = g * (a - d, a, a + d),   a > d > 0,  gcd(a, d) = 1,  t >= 1,  D = 3a^2 - d^2

| parity of a, d | g | n |
|---|---|---|
| opposite | `t*D` | `4*t*a*(a^2 - d^2)` |
| both odd | `t*D / 2` | `2*t*a*(a^2 - d^2)` |

Consequences: the parameterization is **if and only if**; the parameters are uniquely recoverable;
the displayed scale is minimal in each branch; and **no primitive denominator triple exists** —
`gcd(x,y,z) = 1` is impossible, because `gcd(x,y,z) = tD/h >= 11`.

The two branches are exhaustive: `gcd(a,d) = 1` makes the both-even case unreachable.

## ⛔ THE HALF THAT COULD BE FALSE IS THE HALF THE VENDOR NEVER TESTS

An if-and-only-if has two directions:

- **Soundness** — every constructed triple really is a solution. The vendor checks this, over
  `a <= 500`, `t <= 6`.
- **Completeness** — every solution really is constructed. **Nothing shipped tests this.** The
  in-package `verify` checks minimality only for `a < 15`, and the shipped standalone verifier's
  line `primitive_triples_found=0` is a **hardcoded print literal** — that file never searches for
  a primitive triple at all.

Completeness is the direction that could actually fail. It was run here.

## Independence — completeness proven, twice

Brute force over **every** AP-denominator solution in a bounded range, using no parameterization:

| range | solutions found | reproduced by the formula | missed | spurious | primitive |
|---|---|---|---|---|---|
| `z <= 1200` | 97 | **97** | **0** | **0** | **0** |
| `z <= 4000` | 366 | **366** | **0** | **0** | **0** |

Also verified: the closed forms for `n` on every constructed solution (0 disagreements); the parity
gcd lemma `gcd(3a^2-d^2, 4a(a^2-d^2))` equals 1 for opposite parity and 2 for both-odd, tested on
every coprime pair with `a <= 1200` (0 counterexamples); uniqueness of `(a,d,t)` (0 collisions).

Standalone verifier: `oracle/library/patents/artifacts/verify_erdos_straus_ap.py`, carrying
negative controls it must reject.

## Scope

Strictly increasing denominators only — `d > 0` is a hard precondition in the source, so degenerate
constant "progressions" such as `4/4 = 1/3 + 1/3 + 1/3` are **out of scope**, not counterexamples.

## ⛔ THE OPERATION THAT "PROVES" THIS IS A FAKE. THE THEOREM IS NOT.

`erdos_straus_ap_parameterization_theorem` (`frontier8/egyptian_ap.py:120` → `theorem()` at `:86`)
**takes no `data`**. It returns `proved` for `{'center': 0, 'difference': 0, 'n': -1}`. Quarantined
in `oracle/reality/frontier_arsenal/mathfire_blade.py`. The theorem stands on the re-derivations
above, not on that operation.

## Falsifier

An AP-denominator solution of `4/n = 1/x+1/y+1/z` not produced by the parameterization, or any such
solution with `gcd(x,y,z) = 1`.
