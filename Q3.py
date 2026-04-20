# Maysa Khanfar 1221623
# Lara Fuqaha 1220071
# Q3 - PRF/PRP distinguishers

import random

# Global
BITS = 16
MODULO = 2 ** BITS   # this is 2^16
ONLY16 = MODULO - 1   # mask = 0xFFFF

HALF_BITS = 8   # feistel uses 8 bit left + 8 bit right
HALF_MASK = (1 << HALF_BITS) - 1   # 0xFF


def get_random_key():
    # just choose random a and b for the PRF
    a = random.randrange(MODULO)
    b = random.randrange(MODULO)
    return a, b


# PRF: f(x) = a*x + b  (mod 2^16)
def weak_prf(x, a, b):
    x &= ONLY16      # make sure x is only 16 bits
    return (a * x + b) & ONLY16  # also keep result 16-bit

# this is the feistel PRP built from the weak PRF
def our_feistel(x, a, b, rounds=3):
    x &= ONLY16
    L = (x >> HALF_BITS) & HALF_MASK    # take upper 8 bits
    R = x & HALF_MASK      # take lower 8 bits

    # run the rounds
    for _ in range(rounds):
        # run the PRF on the right half, but we only keep 8 bits of it
        f_val = weak_prf(R, a, b) & HALF_MASK
        # feistel swap + xor
        L, R = R, (L ^ f_val) & HALF_MASK

    # put L and R back into 16 bits
    return ((L << HALF_BITS) | R) & ONLY16


# making a fully random function from 16-bit -> 16-bit
def random_func16():
    store = {}

    def f(x):
        x &= ONLY16
        if x not in store:
            store[x] = random.randrange(MODULO)
        return store[x]

    return f

# making a fully random permutation of 16-bit numbers
def random_perm16():
    arr = list(range(MODULO))
    random.shuffle(arr)

    def enc(x):
        x &= ONLY16
        return arr[x]

    return enc

# PRF DISTINGUISHER
# for our PRF f(x)=a*x+b, the diff f(x+1)-f(x) is always 'a'
def prf_detector(oracle, tries=20):

    diffs = []
    for _ in range(tries):
        x = random.randrange(MODULO - 1)
        y1 = oracle(x)
        y2 = oracle((x + 1) & ONLY16)
        # check the difference
        diffs.append((y2 - y1) & ONLY16)

    first = diffs[0]
    same = all(d == first for d in diffs[1:])

    # if all the differences match, it is our PRF
    return same


def run_prf_test(rounds=1000):
    # run many trials where each trial: PRF or random function, then we run prf distinguisher and check if the distinguisher guessed correctly

    right = 0
    for _ in range(rounds):
        real_prf = random.choice([True, False])

        if real_prf:
            aa, bb = get_random_key()
            oracle = lambda x, aa=aa, bb=bb: weak_prf(x, aa, bb)
        else:
            oracle = random_func16()

        guess = prf_detector(oracle)

        # if we used PRF and guess_is_prf=True -> correct
        # if we used random and guess_is_prf=False -> correct
        if (real_prf and guess) or (not real_prf and not guess):
            right += 1

    print(f"our PRF distinguisher success: {right / rounds:.4f}")

# PRP DISTINGUISHER
# our PRP is weak, so xor diffs repeat a lot
def prp_detector(enc, tries=300, diff_val=1):

    results = []
    for _ in range(tries):
        x = random.randrange(MODULO - 1)
        c1 = enc(x)
        c2 = enc((x + diff_val) & ONLY16)
        results.append(c1 ^ c2)

    # count frequencies of each diff
    freq = {}
    for d in results:
        freq[d] = freq.get(d, 0) + 1

    max_repeat = max(freq.values())

    # if there is a Δc that appears many times, we suspect PRP.
    # if one diff repeats many times -> looks like our PRP
    return max_repeat >= 3


def run_prp_test(rounds=500):
    # run many trials where each trial: use Feistel PRP or random permutation then we run PRP distinguisher and check if the distinguisher guessed correctly

    right = 0
    for _ in range(rounds):
        real_prp = random.choice([True, False])

        if real_prp:
            # use our Feistel PRP with random (a,b)
            aa, bb = get_random_key()
            enc = lambda x, aa=aa, bb=bb: our_feistel(x, aa, bb)
        else:
            # use a truly random permutation
            enc = random_perm16()

        guess = prp_detector(enc)

        if (real_prp and guess) or (not real_prp and not guess):
            right += 1

    print(f"our PRP distinguisher success: {right / rounds:.4f}")


# main
if __name__ == "__main__":
    print("=== Running PRF test (our version) ===")
    run_prf_test(rounds=500)

    print("\n=== Running PRP test (our version) ===")
    run_prp_test(rounds=500)
