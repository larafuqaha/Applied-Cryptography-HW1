# Lara Foqaha 1220071 
# Maysa Khanfar 1221623
# Q4 - perfect secrecy

# message space and key space sizes
m_size = 3   # message space: {0, 1, 2}
k_size = 2   # key space: {0, 1, 2}

# defined encryption function
def Enc(k, m):
    # for example encryption function: (m + k) mod m_size
    return (m + k) % m_size

# defined decryption function
def Dec(k, c):
    return (c - k) % m_size


# building probability distributions for each message over ciphertexts
cipher_dist = {}

# for every message m we check how often each ciphertext c appears when trying all keys
for m in range(m_size):
    cipher_count = [0] * m_size   # counts number of ciphertexts for each message initially all 0

    # trying every key in the key space
    for k in range(k_size):
        c = Enc(k, m)
        cipher_count[c] += 1  # counting how many times ciphertext c appears

    # converting counts to probability
    total = k_size
    prob = []
    for x in cipher_count:
        prob.append(x / total)

    cipher_dist[m] = prob  # storing probability distribution for message m


# checking perfect secrecy
# all Pr[C=c | M=m] must be equal for all m
perfect = True
first = cipher_dist[0] # all must match first

for m in range(1, m_size):
    if cipher_dist[m] != first:
        perfect = False
        break

# Output
print("Ciphertext distributions given each message:\n")
for m in range(m_size):
    print(f"M = {m}: {cipher_dist[m]}")

if perfect:
    print("\nThe scheme is perfectly secret.")
else:
    print("\nThe scheme is not perfectly secret.")
