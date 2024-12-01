import binascii
from math import ceil

__all__ = ['Hash']

IV = [
    0x7380166F, 0x4914B2B9, 0x172442D7, 0xDA8A0600,
    0xA96F30BC, 0x163138AA, 0xE38DEE4D, 0xB0FB0E4E,
]

T_J = [
    0x79cc4519, 0x7a879d8a
]

def _rotl(x: int, n: int) -> int:
    """
    Rotate x left by n bits.
    """
    return ((x << n) & 0xFFFFFFFF) | ((x >> (32 - n)) & 0xFFFFFFFF)


def _sm3_ff_j(x: int, y: int, z: int, j: int) -> int:
    """
    SM3 function FFj.
    """
    if 0 <= j < 16:
        return x ^ y ^ z
    elif 16 <= j < 64:
        return (x & y) | (x & z) | (y & z)
    raise ValueError("j must be between 0 and 63")


def _sm3_gg_j(x: int, y: int, z: int, j: int) -> int:
    """
    SM3 function GGj.
    """
    if 0 <= j < 16:
        return x ^ y ^ z
    elif 16 <= j < 64:
        return (x & y) | (~x & z)
    raise ValueError("j must be between 0 and 63")


def _sm3_p_0(x: int) -> int:
    """
    SM3 function P0.
    """
    return x ^ _rotl(x, 9) ^ _rotl(x, 17)


def _sm3_p_1(x: int) -> int:
    """
    SM3 function P1.
    """
    return x ^ _rotl(x, 15) ^ _rotl(x, 23)


def _sm3_cf(v_i: list[int], b_i: list[int]) -> list[int]:
    """
    SM3 compression function.
    """

    w = []
    for i in range(0, 16):
        w.append(int.from_bytes(bytes(b_i[i*4:(i+1)*4]), byteorder='big'))

    for j in range(16, 68):
        w.append(_sm3_p_1(w[j - 16] ^ w[j - 9] ^ _rotl(w[j - 3], 15)) ^ _rotl(w[j - 13], 7) ^ w[j - 6])

    w_prime = [w[i] ^ w[i + 4] for i in range(64)]

    a, b, c, d, e, f, g, h = v_i

    for j in range(64):
        ss1 = _rotl((_rotl(a, 12) + e + _rotl(T_J[j // 16], j)) & 0xFFFFFFFF, 7)
        ss2 = ss1 ^ _rotl(a, 12)
        tt1 = (_sm3_ff_j(a, b, c, j) + d + ss2 + w_prime[j]) & 0xFFFFFFFF
        tt2 = (_sm3_gg_j(e, f, g, j) + h + ss1 + w[j]) & 0xFFFFFFFF
        d = c
        c = _rotl(b, 9)
        b = a
        a = tt1
        h = g
        g = _rotl(f, 19)
        f = e
        e = _sm3_p_0(tt2)

    v_j = [a, b, c, d, e, f, g, h]
    return [(v_j[i] ^ v_i[i]) & 0xFFFFFFFF for i in range(8)]


def _sm3_hash(msg: bytes) -> str:
    """
    SM3 hashing function.
    """
    msg_len = len(msg)
    msg_bits = msg_len * 8

    padded_msg = list(msg)
    padded_msg.append(0x80)
    pad_len = (64 - (msg_len + 1) % 64) % 64
    padded_msg.extend([0] * pad_len)
    padded_msg.extend((msg_bits).to_bytes(8, byteorder='big'))

    blocks = [padded_msg[i:i+64] for i in range(0, len(padded_msg), 64)]

    v = IV[:]
    for block in blocks:
        v = _sm3_cf(v, block)

    return ''.join(f"{x:08x}" for x in v)


def sm3_kdf(z: str, klen: int) -> str:
    """
    SM3 Key Derivation Function (KDF).
    """
    klen = int(klen)
    ct = 1
    rcnt = ceil(klen / 32)
    zin = list(binascii.a2b_hex(z))

    hash_output = ""
    for i in range(rcnt):
        msg = zin + list(ct.to_bytes(4, byteorder='big'))
        hash_output += _sm3_hash(bytes(msg))
        ct += 1
    return hash_output[:klen * 2]

class Hash:
    """
    A utility class for cryptographic operations.
    """

    @staticmethod
    def bytes_to_list(data: bytes) -> list[int]:
        """
        Converts a bytes object to a list of integers.
        """
        return list(data)

    @staticmethod
    def sm3_hash(msg: bytes) -> str:
        """
        Computes the SM3 hash of the input bytes.
        """
        return _sm3_hash(msg)

    @staticmethod
    def sm3_to_array(data: str | list) -> list[int]:
        """
        Converts an SM3 hash string to a list of integers.
        """
        if isinstance(data, str):b = data.encode("utf-8")
        else: b = bytes(data)

        h = Hash.sm3_hash(Hash.bytes_to_list(b))

        return [int(h[i: i + 2], 16) for i in range(0, len(h), 2)]