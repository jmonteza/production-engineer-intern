import secrets
import string


def generate_ship_code():
    return ''.join(secrets.choice(string.digits) for i in range(16))


def generate_tracking_number():
    return secrets.token_hex(10).upper()


print(generate_tracking_number())

print(generate_ship_code())
