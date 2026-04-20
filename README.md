# Applied Cryptography — HW 1

Four Python programs implementing and analyzing foundational cryptographic concepts: OTP reuse attacks, Vigenère cryptanalysis, PRF/PRP distinguishers, and Shannon perfect secrecy testing.

**Course:** Applied Cryptography — ENCS4320  
Department of Electrical and Computer Engineering  
**Team:** Lara Fuqaha · Maysa Khanfar

---

## Questions

### Q1 — Many-Time Pad Attack (`Q1.py`)

Analyzes multiple 8-bit ciphertexts encrypted with the same OTP key, demonstrating how key reuse compromises security.

**Approach:**
- Computes pairwise XORs (C1⊕C2, C1⊕C3, C2⊕C3) for each ciphertext set
- Classifies each XOR result by its upper 3 bits to deduce plaintext character types (uppercase/lowercase/space)
- Deduces forced space positions: if a plaintext index appears in 2+ "letter–space" XOR relations, it must be a space
- Brute-forces all 256 possible keys and keeps only solutions consistent with the allowed alphabet {A–Z, a–z, space}

**Test cases (5 sets):**

| Set | Ciphertexts | Result |
|-----|-------------|--------|
| 1 | `[EF, A4, D3]` | Unique recovery: m1='k', m2=' ', m3='W' |
| 2 | `[10, 30, 50]` | m3 deduced as space; no unique solution (out-of-range characters) |
| 3 | `[B4, F9, 40]` | XOR result impossible under assumed alphabet |
| 4 | `[14, 36, 0F]` | Multiple valid solutions; not uniquely recoverable |
| 5 | `[66, 32, 23]` | Unique recovery |

---

### Q2 — Vigenère Known-Plaintext Recovery (`Q2.py`)

Simulates Trudy's cryptanalysis of a Vigenère cipher given a known plaintext–ciphertext pair.

**Given:** plaintext `HAPPPY`, ciphertext `MOGZDD`, key length ≤ 6

**Method:** Computes the shift at each position as `ki = (ci - mi) mod 26`, then tests all key lengths from 1 to the upper bound. A key length L is valid only if no two positions that map to the same key index require different shifts.

**Result:** Two keys are consistent with the data — `FORKO` (length 5) and `FORKOF` (length 6) — so the key is **not uniquely recoverable**.

---

### Q3 — PRF/PRP Distinguishers (`Q3.py`)

Implements a weak linear PRF and a Feistel-based PRP, then designs distinguishing experiments against truly random functions and permutations.

**PRF:** `F(x) = (a·x + b) mod 2¹⁶` with a random 16-bit key (a, b)

**PRP:** 3-round Feistel network over 16-bit inputs (split into two 8-bit halves), using the above PRF as the round function

**PRF distinguisher:** Exploits the fixed difference property — `F(x+1) - F(x) = a` always. If all sampled differences are equal, the oracle is the weak PRF. Achieves **100% accuracy**.

**PRP distinguisher:** Measures `Enc(x) XOR Enc(x+1)` across many inputs. The linear round function causes XOR differences to repeat frequently in the Feistel PRP but not in a random permutation. Achieves **~98.4% accuracy**.

---

### Q4 — Shannon Perfect Secrecy Tester (`Q4.py`)

Tests whether a given encryption scheme satisfies Shannon's perfect secrecy condition:  
`Pr[C=c | M=m]` must be identical for all messages m.

**Method:** For each message m, encrypts it under every key in the key space and builds the ciphertext probability distribution. Checks whether all distributions match.

**Test cases:**

| Parameters | Enc rule | Result |
|------------|----------|--------|
| m_size=3, k_size=3 | `(m+k) mod 3` | Perfectly secret — uniform distribution [1/3, 1/3, 1/3] for all messages |
| m_size=3, k_size=2 | `(m+k) mod 3` | Not perfectly secret — distributions differ across messages |

---

## Running the Programs

Each question is a standalone script. Run individually:

```bash
python Q1.py
python Q2.py
python Q3.py
python Q4.py
```

---

## Files

| File | Description |
|------|-------------|
| `Q1.py` | Many-time pad attack |
| `Q2.py` | Vigenère known-plaintext recovery |
| `Q3.py` | PRF/PRP distinguishers |
| `Q4.py` | Perfect secrecy tester |
| `HW1.pdf` | Submitted report |

