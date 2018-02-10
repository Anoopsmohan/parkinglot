__author__ = 'anoop.sm'

import unittest
from argument_validator import ValidateArgument


class MyTestCase(unittest.TestCase):

    # File path tester1
    def test_file_path_validator(self):
        validate_argument = ValidateArgument("xyz")
        self.assertEqual(validate_argument.validate_file_path(), False)

    # File path tester2
    def test_file_path_validator1(self):
        validate_argument = ValidateArgument("/Users/anoop.sm/repos/python_pblm_solving/parkinglot/input_file.txt")
        self.assertEqual(validate_argument.validate_file_path(), True)

    # File extension tester1
    def test_file_extension_validator1(self):
        validate_argument = ValidateArgument("/Users/anoop.sm/repos/python_pblm_solving/parkinglot/input_file.abc")
        self.assertEqual(validate_argument.validate_extension(), False)

    # File extension tester2
    def test_file_extension_validator2(self):
        validate_argument = ValidateArgument("/Users/anoop.sm/repos/python_pblm_solving/parkinglot/input_file.txt")
        self.assertEqual(validate_argument.validate_extension(), True)


if __name__ == '__main__':
    unittest.main()
