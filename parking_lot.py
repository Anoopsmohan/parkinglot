__author__ = 'anoop.sm'

import sys

from argument_validator import ValidateArgument
from command_executor import ParkingLot


def main():
    # Get argument count
    args_count = len(sys.argv)

    parking_lot = ParkingLot()

    # Initialize interactive mode if the argument count is 1
    # Initialize file mode if the argument count is 2
    # Return error if the argument count > 2

    try:
        if args_count == 1:
            parking_lot.init_interactive_mode()
        elif args_count == 2:
            validate_argument = ValidateArgument(sys.argv[1])

            if not validate_argument.validate_file_path(): print("Incorrect file path. Please check again.")
            elif not validate_argument.validate_extension(): print("Incorrect file extension. Please use .txt file")
            else: parking_lot.init_file_mode(sys.argv[1])

        else:
            print("Invalid arguments. Please use 'python parking_lot.py <input file path>'")
    except Exception as ex:
        print("Oops! Something went wrong. Error:{}".format(ex))


if __name__ == '__main__':
    main()