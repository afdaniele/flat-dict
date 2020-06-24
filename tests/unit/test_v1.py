import unittest
from functools import partial
from parameterized import parameterized

import flat_dict as fd

from constants import VERSION_KEY

VERSION = '1.0'

fd_encode = partial(fd.encode, version=VERSION)
fd_decode = partial(fd.decode)


class TestConfig(unittest.TestCase):

    def test_encode_empty(self):
        d = {}
        f = fd_encode(d)
        self.assertEqual(f, {VERSION_KEY: VERSION})

    def test_decode_empty(self):
        f = {VERSION_KEY: VERSION}
        d = fd_decode(f)
        self.assertEqual(d, {})

    def test_encode_empty_loop(self):
        f = {}
        self.assertEqual(fd_decode(fd_encode(f)), f)

    def test_decode_empty_loop(self):
        f = {VERSION_KEY: VERSION}
        self.assertEqual(fd_encode(fd_decode(f)), f)

    def test_encode_1lvl(self):
        d = {'a': 1, 'b': 2}
        f = fd_encode(d)
        self.assertEqual(f, {VERSION_KEY: VERSION, '[s:a]': 'd:1', '[s:b]': 'd:2'})

    def test_decode_1lvl(self):
        f = {VERSION_KEY: VERSION, '[s:a]': 'd:1', '[s:b]': 'd:2'}
        d = fd_decode(f)
        self.assertEqual(d, {'a': 1, 'b': 2})

    @parameterized.expand([
        ["bracket1", "["],
        ["bracket2", "]"],
        ["dot", "."],
        ["bar", "|"],
        ["forward_slash", "/"],
        ["back_slash", "\\"],
    ])
    def test_loop_1lvl(self, _, separator):
        d = {'a': 1, 'b': 2}
        self.assertEqual(fd_decode(fd_encode(d, separator=separator), separator=separator), d)

    def test_encode_2lvl(self):
        d = {'a': 1, 'b': {'c': 2}}
        f = fd_encode(d)
        self.assertEqual(f, {VERSION_KEY: VERSION, '[s:a]': 'd:1', '[s:b][s:c]': 'd:2'})

    def test_decode_2lvl(self):
        f = {VERSION_KEY: VERSION, '[s:a]': 'd:1', '[s:b][s:c]': 'd:2'}
        d = fd_decode(f)
        self.assertEqual(d, {'a': 1, 'b': {'c': 2}})

    def test_loop_2lvl(self):
        d = {'a': 1, 'b': {'c': 2}}
        self.assertEqual(fd_decode(fd_encode(d)), d)

    def test_key_type_int(self):
        d = {'a': 1, 1: 'b'}
        f = fd_encode(d)
        self.assertEqual(f, {VERSION_KEY: VERSION, '[s:a]': 'd:1', '[d:1]': 's:b'})

    def test_key_type_float(self):
        d = {'a': 1, 1.12: 'c'}
        f = fd_encode(d)
        self.assertEqual(f, {VERSION_KEY: VERSION, '[s:a]': 'd:1', '[f:1.12]': 's:c'})

    def test_key_type_bool(self):
        d = {'a': 1, True: 'd'}
        f = fd_encode(d)
        self.assertEqual(f, {VERSION_KEY: VERSION, '[s:a]': 'd:1', '[b:1]': 's:d'})

    def test_loop_full1(self):
        d = {
            'a': 1,
            True: 2,
            'b': {
                'c': 3,
                'd': False
            }
        }
        self.assertEqual(fd_decode(fd_encode(d)), d)

    def test_list1(self):
        d = {
            'a': [
                {
                    'b': 1,
                    'c': 2
                },
                {
                    'b': 3,
                    'c': 4
                },
                {
                    'b': 5,
                    'c': 6
                }
            ]
        }
        self.assertEqual(fd_decode(fd_encode(d)), d)

    def test_list2(self):
        d = {
            'a': [
                [1, 2],
                [3, 4],
                [5, 6]
            ]
        }
        self.assertEqual(fd_decode(fd_encode(d)), d)


if __name__ == '__main__':
    unittest.main()
