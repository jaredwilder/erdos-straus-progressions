# Erdős–Straus solutions with progression denominators

**Two complete if-and-only-if classifications** for solutions of

```text
4/n = 1/x + 1/y + 1/z
```

when the ordered denominators form either an **arithmetic progression** or a **geometric progression**.

Author: Jared Wilder. First public timestamp: 2026-09-11.

## 1. Arithmetic-progression denominators

Every positive solution with `x<y<z` in arithmetic progression arises uniquely as

```text
(x,y,z) = g(a-d,a,a+d),
a>d>0,
gcd(a,d)=1,
t>=1,
D=3a^2-d^2.
```

| parity of `a,d` | `g` | `n` |
|---|---|---|
| opposite | `tD` | `4ta(a^2-d^2)` |
| both odd | `tD/2` | `2ta(a^2-d^2)` |

The parametrization is iff, the parameters `(a,d,t)` are uniquely recoverable, and **no primitive denominator triple occurs in this family**.

## 2. Geometric-progression denominators

Every integer geometric triple has a unique representation

```text
(x,y,z) = g(a^2,ab,b^2),
0<a<b,
gcd(a,b)=1.
```

Writing

```text
D = a^2+ab+b^2,
```

all solutions and only the solutions are

```text
g = tD,
n = 4ta^2b^2,
(x,y,z) = tD(a^2,ab,b^2),
t>=1.
```

Again the parametrization is unique, and **no primitive denominator triple occurs**.

## Primitive triples

A primitive denominator triple would not be an integer multiple of a smaller solution triple. The classifications above show that neither progression family contains one.

## Independent computational checks

The repository includes direct finite checks of the formulas:

```bash
python verifiers/verify_erdos_straus_ap.py
python verifiers/verify_erdos_straus_gp.py
```

On the committed default ranges:

| check | AP | GP |
|---|---:|---:|
| brute-force solutions found | **97** | **236** |
| reproduced by the formula | 97 | 236 |
| missed | **0** | **0** |
| spurious | **0** | **0** |
| primitive triples found | 0 | 0 |
| gcd-lemma counterexamples | 0 for coprime `a<=300` | 0 for coprime `a<b<300` |
| parameter collisions | 0 | 0 |

The archived research files record a wider AP check through `z<=4000`, with **366 solutions found and 366 reproduced**; the GP check through the same bound finds and reproduces 236.

The checking programs also include deliberately invalid examples and malformed progression cases to confirm that the implementation rejects objects outside the theorem's hypotheses while successfully finding genuine solutions.

## Mathematical scope

These two theorems completely classify the **arithmetic-progression** and **geometric-progression** denominator subfamilies. The proofs are exact integer derivations; the finite programs provide independent checks of the closed forms.

## License

Apache-2.0.