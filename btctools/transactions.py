from __future__ import unicode_literals


from hextools import (
    little_endian_varint, little_endian_uint32, little_endian_str,
    little_endian_hex, little_endian_uint64
)
from scripts.base import PayToPubkeyScript


class Input:
    def __init__(self, tx_hash, output_id):
        self.tx_hash = tx_hash
        self.output_id = output_id

        self.sequence_no = 0xffffffff
        self.script = 'toto'

    @property
    def script_length(self):
        return len(self.script)

    def to_hex(self):
        return ''.join([
            little_endian_hex(self.tx_hash),
            little_endian_uint32(self.output_id),
            little_endian_varint(self.script_length),
            little_endian_str(self.script),
            little_endian_uint32(self.sequence_no),
        ])


class Output:
    def __init__(self, address, amount):
        self.address = address
        self.amount = amount

        self.script = PayToPubkeyScript(self.address)

    @property
    def script_length(self):
        return len(self.script)

    def to_hex(self):
        return ''.join([
            little_endian_uint64(self.amount),
            little_endian_varint(self.script_length),
            self.script.to_hex()
        ])


class Transaction:
    """A Bitcoin transaction.

    More info on a transaction data format:

        https://en.bitcoin.it/wiki/Transactions
        https://en.bitcoin.it/w/images/en/e/e1/TxBinaryMap.png

    """
    def __init__(self, inputs=[], outputs=[]):
        """Creates a transaction object.

        Inputs are a list of (<transaction hash>, <output id>) tuples.
        Outputs are a list of (<address>, <amount>) tuples.

        """
        self.inputs = [Input(*i) for i in inputs]
        self.outputs = [Output(*o) for o in outputs]

        self.lock_time = 0
        self.version = 1

    @property
    def in_counter(self):
        return len(self.inputs)

    @property
    def out_counter(self):
        return len(self.outputs)

    def to_hex(self):
        """Return the raw transaction as an hexadecimal string.

        See here for the detail of the structure:
            https://en.bitcoin.it/wiki/Protocol_specification#tx

        """
        input_hex = ''.join(i.to_hex() for i in self.inputs)
        output_hex = ''.join(o.to_hex() for o in self.outputs)

        return ''.join([
            little_endian_uint32(self.version),
            little_endian_varint(self.in_counter),
            input_hex,
            little_endian_varint(self.out_counter),
            output_hex,
            little_endian_uint32(self.lock_time)
        ])
