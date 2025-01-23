import random

def generate_verification_code() -> int:
    return random.randint(1000, 9999)
