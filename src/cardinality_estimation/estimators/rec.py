"""
Inspired by: 
https://github.com/zacharyvoase/python-recordinality/blob/master/recordinality.py
(la poca documentació que hi ha d'aixó es un document del conrado i aquest git)
"""
import argparse
import math
import os
import struct
import sys

from csiphash import siphash24
from cskipdict import SkipDict

from .base import CardinalityEstimator


class Element(object):
    __slots__ = ('value', 'count')

    def __init__(self, value):
        self.value = value
        self.count = 1

class RecordinalityEstimator(CardinalityEstimator):
    def __init__(self, size, hash_key=None, store_values=True):
        if hash_key is None:
            hash_key = os.urandom(16)
        self.hash = lambda val: struct.unpack('q', siphash24(hash_key, val))[0]
        self.k_records = SkipDict()
        self.size = size
        self.modifications = 0
        self.store_values = store_values

    def add(self, value):
        hash = self.hash(value)
        if hash in self.k_records:
            element = self.k_records[hash]
            if self.store_values and element.value == value:
                element.count += 1
        elif len(self.k_records) < self.size:
            self.k_records[hash] = Element(value if self.store_values else None)
            self.modifications += 1
        else:
            min_key, min_val = self.k_records.minimum()
            if min_key < hash:
                del self.k_records[min_key]
                self.k_records[hash] = Element(value if self.store_values else None)
                self.modifications += 1

    def cardinality(self):
        if self.modifications <= self.size:
            return self.modifications
        pow = self.modifications - self.size + 1
        estimate = (self.size * math.pow(1 + (1.0 / self.size), pow)) - 1
        return int(estimate)