import hashlib
import random
import string

def generate_token(n=50):
    chars = string.ascii_letters + string.digits
    token = ''.join(random.SystemRandom().choice(chars) for _ in range(n))
    token = hashlib.sha1(token.encode()).hexdigest()

    return token
