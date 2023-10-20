import string
import secrets


def createRequestID():
    characters = string.ascii_letters + string.digits  # You can customize this as needed

    # Use secrets.token_urlsafe() to generate a URL-safe random string
    random_string = ''.join(secrets.choice(characters) for _ in range(16))

    return random_string