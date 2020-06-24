import unittest

import flat_dict as fd

from constants import VERSION_KEY


class TestConfig(unittest.TestCase):

    def test_encode_empty(self):
        d = {}
        f = fd.encode(d)
        self.assertEqual(len(f), 1)

    def test_encode_check_version(self):
        d = {}
        f = fd.encode(d)
        self.assertIn('__fd_version__', f)

    def test_encode_one_element_dict(self):
        d = {'a': 1}
        f = fd.encode(d)
        self.assertEqual(len(f), 2)

    def test_decode_no_version_field(self):
        f = {'a': '1'}
        self.assertRaises(ValueError, lambda *a, **b: fd.decode(f))

    def test_decode_invalid_version(self):
        f = {VERSION_KEY: '', 'a': '1'}
        self.assertRaises(ValueError, lambda *a, **b: fd.decode(f))


if __name__ == '__main__':
    unittest.main()
