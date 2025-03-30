import random
import string

def generate_password(length=12):
    """Generate a random password with letters, digits, and symbols."""
    characters = string.ascii_letters + string.digits + string.punctuation
    return "".join(random.choice(characters) for _ in range(length))
