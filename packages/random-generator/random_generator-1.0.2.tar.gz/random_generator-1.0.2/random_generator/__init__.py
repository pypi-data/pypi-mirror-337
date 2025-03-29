import random as random_libs
import secrets
import string as string_libs


def number(length):
    """
    Generate random numbers.
    :param length:
    :return:
    """
    characters = string_libs.digits
    random_string = ''.join(random_libs.choice(characters) for i in range(length))
    return random_string


def string(length):
    """
    Generate random string
    :param length:
    :return:
    """
    characters = string_libs.ascii_letters
    random_string = ''.join(random_libs.choice(characters) for i in range(length))
    return random_string


def unique_string(length):
    """
    Generate a random string of unique characters
    :param length:
    :return:
    """
    characters = string_libs.ascii_letters + string_libs.digits
    return ''.join(secrets.choice(characters) for _ in range(length))

def random_sha256(length):
    """
    Generate a random string of specified length using cryptographic random bytes.

    This static method utilizes the os.urandom function to generate cryptographic random bytes
    and hashes them using SHA-256 to create a random hexadecimal string.

    @param length: int
        The length of the random string to be generated.
    @return: str
        A random string of hexadecimal characters, derived from cryptographic random bytes.
    """
    random_bytes = os.urandom(length)
    random_hash = hashlib.sha256(random_bytes).hexdigest()
    return random_hash