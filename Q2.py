# Lara Foqaha 1220071 
# Maysa Khanfar 1221623 
# Q2 - vigenere

plaintext = "HAPPPY"
ciphertext = "MOGZDD"
key_upper_bound = 6

# in case there were small letters
plaintext = plaintext.upper()
ciphertext = ciphertext.upper()

# converting from letter to number 0-25
def letter_to_num(l):
    return ord(l) - ord('A') 

# converting from number to letter 
def num_to_letter(n):
    return chr(n + ord('A'))

# computing key shifts for each position
shifts = []
for i in range(len(plaintext)):
    m = letter_to_num(plaintext[i])  # message
    c = letter_to_num(ciphertext[i])  # ciphertext
    k = (c - m) % 26  # key
    shifts.append(k)

# getting the 6 letter key by converting the numeric key to letters
full_key = ""
for k in shifts:
    full_key += num_to_letter(k)

# trying all key lengths up to 6 
# we check which key length works
def get_key_for_length(L):
    key = [None] * L  # creating a list of length L initialized to none
    for i in range(len(shifts)):
        pos = i % L  # key position (the key repeats every L letters)

        # if this position in the key is empty, we assign the shift to it
        if key[pos] is None:
            key[pos] = shifts[i]
        else:
            # else if it's already filled, it must match the current shift value
            if key[pos] != shifts[i]:
                return None   # conflict -> impossible key length
    return key

possible_keys = [] # storing all possible keys we find

# trying every possible key length from 1 up to 6 (upper bound)
for length in range(1, key_upper_bound + 1):
    k = get_key_for_length(length)

    # checking if the key is possible
    if k is not None:
        # converting numeric key to letters
        s = ""
        for x in k:
            s += num_to_letter(x)
        possible_keys.append((length, s)) # storing both the key and its length

# printing results
print("Plaintext:", plaintext)
print("Ciphertext:", ciphertext)
print("Computed 6 letter key:", full_key)
print("Possible keys with length <= 6:")

for length, k in possible_keys:
    print(" ", k, ": length = ", length)

# if more than one key works, not unique
if len(possible_keys) == 1:
    print("Key is uniquely determined.")
else:
    print("Key is not uniquely determined.")
