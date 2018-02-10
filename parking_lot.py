__author__ = 'anoop.sm'

import sys
import os
import logging


class Car(object):
    def __init__(self, reg_no, color):
        self.reg_no = reg_no
        self.color = color


class ParkingLot(object):

    VALID_COMMANDS = ['create_parking_lot', 'park', 'leave', 'status', 'registration_numbers_for_cars_with_colour',
                      'slot_numbers_for_cars_with_colour', 'slot_number_for_registration_number']

    def __init__(self):
        self.slot_count = 0
        self.free_slots = []
        self.busy_slots = {}
        self.reg_slot_map = {}

    def check_slot_created(self):
        return self.slot_count > 0

    def create_parking_lot(self, count):
        try:
            self.slot_count = count
            self.free_slots = list(range(1, count+1))
            print "free_slots: {}".format(self.free_slots)
            return "Created a parking lot with {} slots".format(count)
        except Exception as e:
            return "Invalid slot count {}".format(e.message)

    def park(self, reg_no, color):
        if not self.check_slot_created():
            return "Parking lot not created!"

        if len(self.free_slots) == 0:
            return "Sorry, parking lot is full"

        # Check vehicle number is already allocated or not
        slot = self.reg_slot_map.get(reg_no)
        if slot:
            return "Vehicle {} already there in slot {}".format(reg_no, slot)

        free_slot = sorted(self.free_slots)[0]
        self.free_slots.remove(free_slot)
        self.busy_slots[free_slot] = {"color": color, "reg_no": reg_no}
        self.reg_slot_map[reg_no] = free_slot

        print "reg_slot_map : {}".format(self.reg_slot_map)
        return "Allocated slot number: {}".format(free_slot)

    def leave(self, slot):
        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"

        # Check slot is valid or not
        if slot not in list(range(1, self.slot_count+1)):
            return "Invalid slot number: {}".format(slot)

        # Check slot is allocated or not
        if not self.busy_slots.get(slot):
            return "Slot number {} is free".format(slot)

        # delete from reg_slot_map
        reg_no = self.busy_slots[slot]['reg_no']
        del self.reg_slot_map[reg_no]

        # Delete from busy slot
        del self.busy_slots[slot]

        # Add slot into free slots
        self.free_slots.append(slot)

        print "free slots: {}".format(self.free_slots)
        print "busy slots: {}".format(self.busy_slots)
        return "Slot number {} is free".format(slot)

    def status(self):
        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"

        # Check slots are allocated or not
        if not self.busy_slots:
            return "All slots are free!"

        # Print slot details in table format
        print "Slot No  Registration No \t Color"
        for k, v in self.busy_slots.items():
            print "{} \t\t {} \t\t {}".format(k, v['reg_no'], v['color'])

    def registration_numbers_for_cars_with_colour(self, color):
        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"
        vehicles = [k['reg_no']for k in self.busy_slots.values() if k['color'].lower() == color.lower()]
        if not vehicles:
            return "{} color vehicle not exisit!".format(color.capitalize())

        return ", ".join(vehicles)

    def slot_numbers_for_cars_with_colour(self, color):
        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"

        # Get list of vehicle numbers from busy slots
        reg_numbers = [k['reg_no']for k in self.busy_slots.values() if k['color'].lower() == color.lower()]
        if not reg_numbers:
            return "{} color vehicle does not exisit!".format(color.capitalize())

        # Join slot numbers
        return ", ".join([str(self.reg_slot_map[k]) for k in reg_numbers])

    def slot_number_for_registration_number(self, reg_no):
        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"

        slot = self.reg_slot_map[reg_no]
        if not slot:
            return "Not Found"

        return slot

    def is_valid_command(self, command):
        return command in self.VALID_COMMANDS

    def execute_command(self, command):
        inputs = command.split(" ")
        command = inputs[0]
        input_length = len(inputs)
        if command == "create_parking_lot" and input_length == 2:
            print self.create_parking_lot(int(inputs[1]))
        elif command == "park" and input_length == 3:
            print self.park(inputs[1], inputs[2])
        elif command == "leave" and input_length == 2:
            print self.leave(int(inputs[1]))
        elif command == "status" and input_length == 1:
            self.status()
        elif command == "registration_numbers_for_cars_with_colour" and input_length == 2:
            print self.registration_numbers_for_cars_with_colour(inputs[1])
        elif command == "slot_numbers_for_cars_with_colour" and input_length == 2:
            print self.slot_numbers_for_cars_with_colour(inputs[1])
        elif command == "slot_number_for_registration_number" and input_length == 2:
            print self.slot_number_for_registration_number(inputs[1])
        else:
            print "Invalid arguments. Please correct it"

    def init_interactive_mode(self):
        print "Please enter the commands. Enter 'exit' to quit"
        while True:
            command = raw_input()

            if self.is_valid_command(command.split(" ")[0].lower()):
                self.execute_command(command)
            elif command:
                print "Invalid command. Please check again."
            if command.upper() == 'EXIT': break


    def init_file_mode(self):
        pass


class ValidateArgument(object):
    VALID_EXTENTIONS = ['txt']

    def __init__(self, arg):
        self.arg = arg

    # Check file path is correct or not
    def validate_file_path(self):
        return os.path.isfile(self.arg)

    # Check file extension is correct or not
    def validate_extension(self):
        return self.arg.split('.')[-1].lower() in self.VALID_EXTENTIONS

if __name__ == '__main__':

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

            if not validate_argument.validate_file_path(): print "Incorrect file path. Please check again."
            elif not validate_argument.validate_extension(): print "Incorrect file extension. Please use .txt file"
            else: parking_lot.init_file_mode()

        else:
            print "Invalid arguments. Please use 'python parking_lot.py <input file path>'"
    except Exception as ex:
        logging.error("Oops! Something went wrong. Error:{}".format(ex.message))