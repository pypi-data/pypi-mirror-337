import random
import math
import string

MAX_LENGTH = 32
UPPER_CASE_LETTER = string.ascii_uppercase
LOWER_CASE_LETTER = string.ascii_lowercase
NUMBERS = "0123456789"
SPECIAL_CHARACTER = string.punctuation
AMBIGUOUS_CHARACTER = ["0","O","1","I","l","5","S"]

def generate_length_from_entropy(chars, entropy):
    """
    Generate length of the password given the entropy and chars.
    :param str chars: Char set of password
    :param str entropy: Level of entropy
    :return: length of password
    """
    entropy_bits = 0
    if entropy == "Weak":
        entropy_bits = 40
    elif entropy == "Moderate":
        entropy_bits = 60
    elif entropy == "Strong":
        entropy_bits = 80
    elif entropy == "Very Strong":
        entropy_bits = 100
    else:
        raise ValueError("Incorrect value given for entropy. Choose from 'Weak', 'Moderate', 'Strong', 'Very Strong'")

    char_set = len(chars)

    length = math.ceil(entropy_bits / (math.log2(char_set)))
    return length


def generate_password(length=None, contains_upper_case=True, contains_lower_case=True, contains_number=True, contains_special_character=False, contains_space=False, entropy=None, exclude_ambiguous_chars=False):
    """
    It will generate a password with the help of random module.

    :param int | None length: Length of the password. Not required in case entropy is provided
    :param boolean contains_upper_case: Should your password contain upper_case(default True)
    :param boolean contains_lower_case: Should your password contain lower_case(default True)
    :param boolean contains_number: Should your password contain number(default True)
    :param boolean contains_special_character: Should your password contain special_character(default False)
    :param boolean contains_space: Should the password contain space for better readability and added security(default False)
    :param str | None entropy: Desired entropy level. Possible values - "Weak", "Moderate", "Strong", "Very Strong". If specified, length will be adjusted automatically.
    :param exclude_ambiguous_chars: Should *exclude* ambiguous words link 0oI1l5S making it less prone to typos
    :return: A randomly generated password as string
    """

    if not length:
        if not entropy:
            raise RuntimeError("Either Length or Entropy is Required!")

    if length and length > 32:
        raise ValueError

    # Defining variable
    chars = ""
    password = ""

    # building charset
    if contains_upper_case:
        chars += UPPER_CASE_LETTER
    if contains_lower_case:
        chars += LOWER_CASE_LETTER
    if contains_number:
        chars += NUMBERS
    if contains_special_character:
        chars += SPECIAL_CHARACTER
    if contains_space:
        chars += " "
    if exclude_ambiguous_chars:
        for char in AMBIGUOUS_CHARACTER:
            chars = chars.replace(char, "")

    # To less character to have secure password.
    if len(chars) < 10:
        raise ValueError("⚠️ Not enough characters available to make a secure password!")

    if entropy:
        length = generate_length_from_entropy(chars, entropy)

    for _ in range(length):
        next_char = random.choice(chars)
        password += next_char

    return password

def evaluate_entropy(char_set_length, length_of_password):
    """
    Calculate entropy of password
    :param char_set_length: length of char set used to generate password
    :param length_of_password: length of the password
    :return: Float value of entropy
    """
    entropy = math.log2(math.pow(char_set_length, length_of_password))
    return entropy