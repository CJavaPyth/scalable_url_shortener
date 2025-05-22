import string

BASE62 = string.ascii_letters + string.digits


def encode_base62(num):
    s = []
    while num > 0:
        s.append(BASE62[num % 62])
        num //= 62
    return ''.join(reversed(s))
