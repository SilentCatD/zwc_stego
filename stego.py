invisible = {
    "\u200B",
    "\u200E",
    "\u202C",
    "\u202A",
    "\u202B",
    "\u202C",
    "\u202D",
}

bits_to_zwc = {
    "0001": "\u200B\u202A",
    "0010": "\u202A\u200B",
    "0011": "\u202C\u202A",
    "0100": "\u202A\u202C",
    "0101": "\u202C\u202D",
    "0110": "\u200B\u202C",
    "0111": "\u202C\u200B",
    "1000": "\u202A\u202B",
    "1001": "\u202B\u202A",
    "1010": "\u200E\u202D",
    "1011": "\u202D\u200E",
    "1100": "\u200E\u202C",
    "1101": "\u202C\u200E",
    "1110": "\u202D\u202C",
    "1111": "\u202D\u200B",
    "0000": "\u200B\u202D"
}

zwc_to_bits = {bits_to_zwc[x]: x for x in bits_to_zwc.keys()}


def to_bits(s: str) -> str:
    result: str = ""
    for c in s:
        bits = bin(ord(c))[2:]
        bits = bits.zfill(8)
        result += bits
    return result


def invert(s: str) -> str:
    result = ""
    for c in s:
        if c == "0":
            result += "1"
        else:
            result += "0"
    return result


def from_bits(bits: str) -> str:
    chars: str = ""
    for b in range(len(bits) // 8):
        byte = bits[b * 8:(b + 1) * 8]
        chars += chr(int(''.join([bit for bit in byte]), 2))
    return chars


def separate(bits: str) -> list[str]:
    result: list[str] = []
    for b in range(len(bits) // 4):
        result.append(bits[b * 4: (b + 1) * 4])
    return result


def xor_pair(first: str, second: str) -> str:
    assert len(first) == len(second)
    return bin(int(first, 2) ^ int(second, 2))[2:].zfill(4)


def xor_separated_bits(separated_bits: list[str]) -> list[str]:
    result: list[str] = []
    for b in range(0, len(separated_bits), 2):
        result.append(xor_pair(separated_bits[b], separated_bits[b + 1]))
    return result


def merged_xor(separated_bits: list[str], xor_ed_bits: list[str]) -> list[str]:
    result: list[str] = []
    for b in range(0, len(separated_bits), 2):
        result.append(separated_bits[b] + xor_ed_bits[b // 2])
    return result


def map_bits_to_zwc(bits: str, mapped: dict[str, str]) -> str:
    assert len(bits) == 4
    return mapped[bits]


def encode_to_zwc(merged_xor_ed: list[str]) -> str:
    result = ""
    for bits in merged_xor_ed:
        result += map_bits_to_zwc(bits[:4], bits_to_zwc)
        result += map_bits_to_zwc(bits[4:], bits_to_zwc)
    return result


def extract_bits_from_stego(stego_text: str, mapped: dict[str, str]) -> str:
    hidden_char = ""
    for c in stego_text:
        if c in invisible:
            hidden_char += c
    bits = ""
    for c_index in range(0, len(hidden_char), 2):
        bits += mapped[hidden_char[c_index] + hidden_char[c_index + 1]]
    return bits


def embed(msg_file: str, cover_file: str, stego_file: str = None):
    assert msg_file.endswith('.txt') and cover_file.endswith('.txt')
    if stego_file:
        assert stego_file.endswith('txt')
    with open(msg_file, 'r', encoding='utf-8') as f:
        msg = f.read()

    with open(cover_file, 'r', encoding='utf-8') as f:
        cover = f.read()

    msg_bits = to_bits(msg)

    # if use_key:
    #     key = key_gen(msg_bits, 'key')
    #     msg_bits = encrypt(msg_bits, key)

    inverted = invert(msg_bits)
    separated = separate(inverted)
    xor_ed = xor_separated_bits(separated)
    merged_xor_ed = merged_xor(separated, xor_ed)
    encoded = encode_to_zwc(merged_xor_ed)
    stego_text = encoded + cover

    out_file = stego_file
    if not out_file:
        file = cover_file.split('.')[0]
        out_file = file + '_embedded.txt'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(stego_text)


def extract(embedded_file: str, output_msg_file: str = None):
    with open(embedded_file, 'r', encoding='utf-8') as f:
        stego_text = f.read()
    bits = extract_bits_from_stego(stego_text, zwc_to_bits)
    bits_separated = separate(bits)
    xor_ed = xor_separated_bits(bits_separated)
    merged_xor_ed = merged_xor(bits_separated, xor_ed)
    bits_inverted = invert("".join(merged_xor_ed))

    decoded = from_bits(bits_inverted)

    out_file = output_msg_file
    if not out_file:
        file = embedded_file.split('.')[0]
        out_file = file + '_extracted.txt'
    with open(out_file, 'w', encoding='utf-8') as f:
        f.write(decoded)
