# Lara Foqaha 1220071 
# Maysa Khanfar 1221623
# Q1 - many time pad attack
# assuming plaintext charecters are lower/upper case letters + space

# converting from hex to binary
def to_binary(hex_val):
    return format(hex_val, '08b')

# XOR result classification 
def classify_xor(xor_res):
    prefix = (xor_res >> 5) & 0b111  # shifting xor result right by 5 bits to get only most 3 bits
    # based on the upper 3 bits we can know the type of XORed msgs
    if prefix == 0b000:
        return "same case (upper-upper or lower-lower)"
    elif prefix == 0b001:
        return "upper - lower"
    elif prefix == 0b010:
        return "lower - space"
    elif prefix == 0b011:
        return "upper - space"
    else:
        return "impossible for (upper, lower, space)"


# creating a list of all candidate plaintext types for that xor result
def plaintext_candidates(xor_res):
    prefix = (xor_res >> 5) & 0b111  # getting the top 3 bits
    result = []

    # if prefix = 000 then both messages are upper or both lower
    if prefix == 0b000:
        result.append(("uppercase", "uppercase"))
        result.append(("lowercase", "lowercase"))

    # if prefix = 001 then one is upper and the other is lower
    elif prefix == 0b001:
        result.append(("uppercase", "lowercase"))
        result.append(("lowercase", "uppercase"))
    
    # if prefix = 010 then one is lower and the other is sapce
    elif prefix == 0b010:
        result.append(("lowercase", "space"))
        result.append(("space", "lowercase"))
    
    # if prefix = 011 then one is upper and the other is space
    elif prefix == 0b011:
        result.append(("uppercase", "space"))
        result.append(("space", "uppercase"))

    return result


# checking if a plaintext is allowed in our assumption (space, a-z, A-Z)
def is_allowed(ch):
    space = 0x20    # space ASCII in hex = 0x20
    upper_A, upper_Z = 0x41, 0x5A    # A-Z in hex = 0x41 - 0x5A
    lower_a, lower_z = 0x61, 0x7A     # a-z in hex = 0x61 - 0x7A
    return (ch == space or upper_A <= ch <= upper_Z or lower_a <= ch <= lower_z)


# analyzing one set of three ciphertexts
def analyze(ciphertexts, label):

    print("\n=======================================")
    print(f"       Analyzing Set: {label}")
    print("=======================================\n")

    C1, C2, C3 = ciphertexts

    # XOR results computation 
    x1_2 = C1 ^ C2  # xor between first and second ciphertexts
    x1_3 = C1 ^ C3  # xor between first and third ciphertexts
    x2_3 = C2 ^ C3  # xor between second and third ciphertexts

    print("Ciphertexts (binary):")
    print("C1 =", to_binary(C1))
    print("C2 =", to_binary(C2))
    print("C3 =", to_binary(C3))

    print("\nXOR Results (binary):")
    print("C1 XOR C2 =", to_binary(x1_2))
    print("C1 XOR C3 =", to_binary(x1_3))
    print("C2 XOR C3 =", to_binary(x2_3))

    print("\nCandidate plaintext type deductions:\n")

    xor_list = [("C1 xor C2", x1_2), ("C1 xor C3", x1_3), ("C2 xor C3", x2_3) ]

    # printing all possible type pairs for each XOR result
    for res_name, xor_res in xor_list:
        print(f"--- {res_name} ---")
        print(f" XOR result = {to_binary(xor_res)}  --> {classify_xor(xor_res)}")

        # showing all possible combinations of plaintext types for this xor byte
        possible_pairs = plaintext_candidates(xor_res)
        for a, b in possible_pairs:
            print(f"    possible: {a} / {b}")
        print()

    # --- space deduction (identifying forced spaces) ---
    # counting for each message index how many xor relations say it's related to space
    space_counts = {1: 0, 2: 0, 3: 0}

    # checking each xor result if it suggests space in m
    # check C1 xor C2
    if classify_xor(x1_2) in ["lower - space", "upper - space"]:
        space_counts[1] += 1   # m1 might be space
        space_counts[2] += 1   # m2 might be space

    # check C1 xor C3
    if classify_xor(x1_3) in ["lower - space", "upper - space"]:
        space_counts[1] += 1
        space_counts[3] += 1

    # check C2 xor C3
    if classify_xor(x2_3) in ["lower - space", "upper - space"]:
        space_counts[2] += 1
        space_counts[3] += 1

    # now checking which message index has 2 or more space indicators
    forced_spaces = []  # will store plaintext positions that must be space
    for index, count in space_counts.items():   
        if count >= 2:   # if this message appeared in 2+ space relations
            forced_spaces.append(index)   # then this message must be space

    # if only one position is always linked to space, we can deduce it is space
    if len(forced_spaces) == 1:
        idx = forced_spaces[0]
        print("XOR deduction:")
        print(f"m{idx} must be a space character based on XOR results.\n")


    # --- recover actual plaintexts (only if unique solution) ---
    # brute forcing keys from 0 to 255
    solutions = []
    for K in range(256):
        m1 = C1 ^ K
        m2 = C2 ^ K
        m3 = C3 ^ K
        # keep only valid plaintexts
        if is_allowed(m1) and is_allowed(m2) and is_allowed(m3):
            solutions.append((m1, m2, m3))

    # checking if solution is unique
    if len(solutions) == 1:
        m1, m2, m3 = solutions[0]
        print("Recovered plaintexts:")
        print("m1 =", repr(chr(m1)), " binary:", to_binary(m1))
        print("m2 =", repr(chr(m2)), " binary:", to_binary(m2))
        print("m3 =", repr(chr(m3)), " binary:", to_binary(m3))
        print()
    else:
        print("Plaintext cannot be uniquely recovered (candidates above are the result).\n")


# --- testing different sets ---
set1 = [0xEF, 0xA4, 0xD3] # expected plaintexts are small k, capital W and space
set2 = [0x10, 0x30, 0x50] # one plaintext is space the others are out of range
set3 = [0xB4, 0xF9, 0x40] # xor result out of range
set4 = [0x14, 0x36, 0x0F] # doesnt have unique solution (plaintexts are lower/upper)
set5 = [0x66, 0x32, 0x23] # same case as set 1 but different output

analyze(set1, "Set 1")
analyze(set2, "Set 2")
analyze(set3, "Set 3")
analyze(set4, "Set 4")
analyze(set5, "Set 5")