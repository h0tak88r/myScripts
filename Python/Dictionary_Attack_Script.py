import numpy as np
from itertools import permutations, product, chain
import math
import time


def casing_count(word):
    """
    Counts the number of possible casings for a given word.
    """
    if word.isdigit():
        # If the word is a digit, it can only be represented in one casing.
        count = 1
    else:
        # Otherwise, the number of possible casings is 2 to the power of the word length.
        count = pow(2, len(word))
    return count


def all_casings(input_string):
    """
    Generates all possible casings for a given string.
    """
    if not input_string:
        yield ""
    else:
        first = input_string[:1]
        if first.lower() == first.upper():
            # If the character is not a letter, keep it as is.
            for sub_casing in all_casings(input_string[1:]):
                yield first + sub_casing
        else:
            # If the character is a letter, generate two casings: one lowercase and one uppercase.
            for sub_casing in all_casings(input_string[1:]):
                yield first.lower() + sub_casing
                yield first.upper() + sub_casing


def perm_count(string_list):
    """
    Counts the total number of permutations for a given list of strings.
    """
    casing_counts = [casing_count(word) for word in string_list]
    total_permutations = np.product(casing_counts) * math.factorial(len(string_list))
    return total_permutations

print("""

  _    __  _        _   ___  ___     
 | |_ /  \| |_ __ _| |_( _ )( _ )_ _ 
 | ' \ () |  _/ _` | / / _ \/ _ \ '_|
 |_||_\__/ \__\__,_|_\_\___/\___/_|  
                                     
""")
time.sleep(3)
print("\033[1;32m[+] OK,First let's start with keywords about the victim 👀 \033[0m")
# Ask the user for a list of phrases separated by commas.
phrases = input("\033[1;32m[+] Enter keywords separated by commas:\033[0m \n").split(',')
phrases = [x.strip() for x in phrases]

print("\033[1;32m🚀 CALCULATING COMBINATIONS....\033[0m")
time.sleep(3)

# Print the number of permutations for each combination of phrases.
for i in range(1, len(phrases) + 1):
    phrases_subset = phrases[:i]
    word_counts = [casing_count(word) for word in phrases_subset]
    dictionary = dict(zip(phrases_subset, word_counts))
    total_permutations = perm_count(phrases_subset)
    print(f"{dictionary} = {total_permutations} permutations")

# Generate all possible casings for each word in the list.
all_casings_list = [set(all_casings(word)) for word in phrases]

# Generate all possible permutations of the list of phrases with all possible casings.
permutations_set = set()
for i in range(1, len(phrases)+1):
    for element in product(*all_casings_list[:i]):
        for permutation in permutations(element):
            permutations_set.add(chain(permutation))

# Convert the set of permutations to a list.
permutations_list = [list(gen) for gen in permutations_set]

print("\033[1;32m✅ Saving our work in [passwords.txt] WORDLIST..... \033[0m")
time.sleep(5)
# Write the list of permutations to a file.
count = 0
with open('passwords.txt', 'w') as file:
    for password in permutations_list:
        file.write("".join(password) + "\n")
        count += 1
# print number of passwords generated
print("\033[1;32m[+] Number of possible passwords:\033[0m", count)
print("\033[1;32m                                     🙌 THAT'S IT !,YOU'RE DONE                \033[0m")
