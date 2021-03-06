from __future__ import unicode_literals

import hashlib
import binascii


def hash160(data):
    ripemd160 = hashlib.new('ripemd160')
    ripemd160.update(data)

    return ripemd160.digest()


def sha256(data):
    """hashes a bytes array and return binary value."""
    digest = hashlib.sha256(data).digest()
    return digest


def double_sha256(data):
    """Double hash a bytes array and return a binary value."""
    hash = sha256(sha256(data))
    return hash


def sha256_hex(data):
    """Hashes a string and return a hex string."""
    data = sha256(data)
    hex = binascii.hexlify(data)
    return hex.decode('utf-8')


def double_sha256_hex(data):
    """Double hashes a string and return a hex string."""
    data = double_sha256(data)
    hex = binascii.hexlify(data)
    return hex.decode('utf-8')
