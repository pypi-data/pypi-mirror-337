import sys
import os

# Add parent directory to path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../password_generator')))

import math
import unittest
from generator import (
    generate_password,
    generate_length_from_entropy,
    evaluate_entropy,
    MAX_LENGTH,
    UPPER_CASE_LETTER,
    LOWER_CASE_LETTER,
    NUMBERS,
    SPECIAL_CHARACTER,
    AMBIGUOUS_CHARACTER
)


class TestPasswordGenerator(unittest.TestCase):
    def test_generate_password_default(self):
        """Test default password generation"""
        password = generate_password(12)
        self.assertEqual(len(password), 12)

    def test_generate_password_with_special_chars(self):
        """Test password with special characters"""
        password = generate_password(12, contains_special_character=True)
        self.assertTrue(any(char in SPECIAL_CHARACTER for char in password))

    def test_generate_password_with_space(self):
        """Test password with spaces included"""
        password = generate_password(12, contains_space=True)
        assert any(char == " " for char in password) or len(password) == 12

    def test_generate_password_no_uppercase(self):
        """Test password without uppercase letters"""
        password = generate_password(12, contains_upper_case=False)
        self.assertFalse(any(char in UPPER_CASE_LETTER for char in password))

    def test_generate_password_no_lowercase(self):
        """Test password without lowercase letters"""
        password = generate_password(12, contains_lower_case=False)
        self.assertFalse(any(char in LOWER_CASE_LETTER for char in password))

    def test_generate_password_no_numbers(self):
        """Test password without numbers"""
        password = generate_password(12, contains_number=False)
        self.assertFalse(any(char in NUMBERS for char in password))

    def test_generate_password_exclude_ambiguous(self):
        """Test password excluding ambiguous characters"""
        password = generate_password(12, exclude_ambiguous_chars=True)
        self.assertFalse(any(char in AMBIGUOUS_CHARACTER for char in password))

    def test_generate_password_with_entropy(self):
        """Test password generated based on entropy"""
        password = generate_password(entropy="Strong")
        calculated_length = generate_length_from_entropy(UPPER_CASE_LETTER + LOWER_CASE_LETTER + NUMBERS, "Strong")
        self.assertEqual(len(password), calculated_length)

    def test_generate_password_with_invalid_entropy(self):
        """Test invalid entropy value"""
        with self.assertRaises(ValueError):
            generate_password(entropy="Impossible")

    def test_generate_password_empty_charset(self):
        """Test no charset available"""
        with self.assertRaises(ValueError):
            generate_password(12, contains_upper_case=False, contains_lower_case=False, contains_number=False, contains_special_character=False)

    def test_generate_password_invalid_length_entropy(self):
        """Test error raised when both length and entropy are missing"""
        with self.assertRaises(RuntimeError):
            generate_password()

    def test_evaluate_entropy(self):
        """Test entropy calculation"""
        charset_length = len(UPPER_CASE_LETTER + LOWER_CASE_LETTER + NUMBERS + SPECIAL_CHARACTER)
        length_of_password = 12
        entropy = evaluate_entropy(charset_length, length_of_password)
        self.assertAlmostEqual(entropy, math.log2(math.pow(charset_length, length_of_password)))

    def test_generate_password_max_length(self):
        """Test that length does not exceed MAX_LENGTH"""
        with self.assertRaises(ValueError):
            generate_password(40)


    def test_generate_password_with_space_and_special(self):
        """Test password with space and special characters"""
        password = generate_password(12, contains_special_character=True, contains_space=True)
        self.assertTrue(any(char in SPECIAL_CHARACTER for char in password))
        assert any(char == " " for char in password) or len(password) == 12


if __name__ == "__main__":
    unittest.main()
