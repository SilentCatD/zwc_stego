import random


def to_bits(s: str) -> str:
    result: str = ""
    for c in s:
        bits = bin(ord(c))[2:]
        bits = bits.zfill(8)
        result += bits
    return result


def key_gen(msg: str, key_file: str) -> str:
    msg_len = len(to_bits(msg))
    key = random.getrandbits(msg_len)
    key = format(key, '0b')
    with open(key_file, 'w') as f:
        f.write(key)
    return key


def xor_str(str1: str, str2: str) -> str:
    assert len(str1) == len(str2)
    result = ""
    for i in range(len(str1)):
        assert str1[i] == '0' or str1[i] == '1'
        assert str2[i] == '0' or str2[i] == '1'
        xor_ed = int(str1[i]) ^ int(str2[i])
        result += xor_ed
    return result


def encrypt(message: str, key: str) -> str:
    assert len(message) == len(key)
    return xor_str(message, key)


def decrypt(encrypted: str, key: str) -> str:
    assert len(encrypted) == len(key)
    return xor_str(encrypted, key)
