# erdos-straus-progressions

**Two complete classifications of Erdős–Straus solutions whose denominators form a progression. Both are if-and-only-if. Both ship a verifier that exits 0.**

Author: Jared Wilder. First public timestamp: 2026-09-11.

For the equation `4/n = 1/x + 1/y + 1/z`, this repository settles the exact structure of all positive solutions whose ordered denominators lie in **arithmetic progression** or **geometric progression**.

---

## 1. Arithmetic progression denominators

Every positive solution of `4/n = 1/x + 1/y + 1/z` whose ordered denominators `x < y < z` form an arithmetic progression arises **uniquely** as

```
(x, y, z) = g * (a - d, a, a + d),   a > d > 0,  gcd(a, d) = 1,  t >= 1,  D = 3a^2 - d^2
```

| parity of `a, d` | `g` | `n` |
|---|---|---|
| opposite | `t*D` | `4*t*a*(a^2 - d^2)` |
| both odd | `t*D / 2` | `2*t*a*(a^2 - d^2)` |

The parameterisation is **if and only if**, the parameters `(a, d, t)` are uniquely recoverable, and **no primitive denominator triple exists**.

## 2. Geometric progression denominators

Every integer geometric triple is uniquely `(x, y, z) = g(a^2, ab, b^2)` with `0 < a < b`, `gcd(a, b) = 1`. With `D = a^2 + ab + b^2`, all solutions and only the solutions are

```
g = t*D,    n = 4*t*a^2*b^2,    (x, y, z) = t*D*(a^2, ab, b^2),    t >= 1
```

Again the parameterisation is unique, and again **no primitive denominator triple exists**.

---

## What "no primitive triple exists" means

A primitive triple would be a solution not of the form `t` times a smaller one. There are none in either family. The verifiers check every solution they enumerate rather than assuming this from the parametrisation.

## Run the verifiers

```
python verifiers/verify_erdos_straus_ap.py
python verifiers/verify_erdos_straus_gp.py
```

Both exit 0. Re-run on 2026-09-11 from committed source:

| check | AP | GP |
|---|---|---|
| brute-force solutions found | **97** | **236** |
| reproduced by the formula | 97 | 236 |
| **missed** | **0** | **0** |
| **spurious** | **0** | **0** |
| primitive triples found | 0 | 0 |
| gcd lemma counterexamples | 0 (every coprime pair `a <= 300`) | 0 (every coprime `a < b < 300`) |
| parameter collisions | 0 | 0 |

The published finding files record a wider sweep than the shipped verifier runs by default: the AP family was checked to `z <= 4000` with **366 found and 366 reproduced**, and the GP family to `z <= 4000` with **236 found and 236 reproduced**.

## Negative controls

Each verifier carries cases it must reject before any positive result counts:

- `(1,2,3)` is not a solution, and is rejected;
- a non-AP triple is never produced by the AP parameterisation;
- a non-geometric AP triple is never produced by the GP parameterisation;
- every triple the GP side produces really is geometric;
- brute force must actually recover positive examples — 97 and 236 solutions respectively.

A search returning nothing everywhere could make a bad completeness check look good; these controls demonstrate that the verifier can recover the intended objects.

## Scope

The two iff theorems classify exactly the arithmetic-progression and geometric-progression denominator families. They are exact integer derivations with independent finite rechecks, rather than proof-assistant formalizations.

## License

Apache-2.0.