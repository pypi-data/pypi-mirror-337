import unittest
from is_prime import is_prime, get_primes


class TestPrimeChecker(unittest.TestCase):
    def test_prime_numbers(self):
        prime_numbers = [2, 3, 5, 7, 11, 13, 17, 19]
        for num in prime_numbers:
            self.assertTrue(is_prime(num), f"{num} should be prime")

    def test_non_prime_numbers(self):
        non_prime_numbers = [0, 1, 4, 6, 8, 9, 10, 12]
        for num in non_prime_numbers:
            self.assertFalse(is_prime(num), f"{num} should not be prime")

    def test_get_primes(self):
        self.assertEqual(get_primes(10, 20), [11, 13, 17, 19])

    def test_invalid_input(self):
        with self.assertRaises(ValueError):
            is_prime(3.14)
        with self.assertRaises(ValueError):
            is_prime("not a number")


if __name__ == "__main__":
    unittest.main()
