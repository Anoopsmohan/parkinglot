__author__ = 'anoop.sm'

from car import Car


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
        '''
        :param count: slot count
        :return: message
        '''

        if self.slot_count > 0:
            return "Slot count already set."

        self.slot_count = count
        self.free_slots = list(range(1, count+1))
        return "Created a parking lot with {} slots".format(count)

    @staticmethod
    def validate_vehicle_number(reg_no):
        return len(reg_no.split("-")) == 4

    @staticmethod
    def validate_color(color):
        return color.strip().isalpha()

    def park(self, reg_no, color):
        '''
        Allocate slot for vehicle
        :param reg_no: Vehicle registration number
        :param color: Vehicle color
        :return: Message
        '''

        if not self.check_slot_created():
            return "Parking lot not created!"

        if len(self.free_slots) == 0:
            return "Sorry, parking lot is full"

        # Check vehicle number is already allocated or not
        slot = self.reg_slot_map.get(reg_no)
        if slot:
            return "Vehicle {} already there in slot {}".format(reg_no, slot)

        # Validate vehicle number
        if not self.validate_vehicle_number(reg_no):
            return "Invalid vehicle number"

        # Validate vehicle color
        if not self.validate_color(color):
            return "Invalid color"

        free_slot = sorted(self.free_slots)[0]
        self.free_slots.remove(free_slot)
        self.busy_slots[free_slot] = Car(reg_no.upper(), color)
        self.reg_slot_map[reg_no] = free_slot

        return "Allocated slot number: {}".format(free_slot)

    def leave(self, slot):
        '''
        Release slot
        :param slot: Slot number needs to be released
        :return: Message
        '''

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
        reg_no = self.busy_slots[slot].reg_no
        del self.reg_slot_map[reg_no]

        # Delete from busy slot
        del self.busy_slots[slot]

        # Add slot into free slots
        self.free_slots.append(slot)

        return "Slot number {} is free".format(slot)

    def status(self):
        '''
        Print current status of parking slot
        :return:
        '''

        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"

        # Check slots are allocated or not
        if not self.busy_slots:
            return "All slots are free!"

        # Print slot details in table format
        print("Slot No \t Registration No \t Color")
        for k, v in self.busy_slots.items():
            print("{} \t\t {} \t\t {}".format(k, v.reg_no, v.color))

    def registration_numbers_for_cars_with_colour(self, color):
        '''
        :param color: Vehicle color
        :return: Print list of vehicle numbers (reg no)
        '''

        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"

        # Validate vehicle color
        if not self.validate_color(color):
            return "Invalid color"

        vehicles = [k.reg_no for k in self.busy_slots.values() if k.color.lower() == color.lower()]
        if not vehicles:
            return "{} color vehicle does not exist!".format(color.capitalize())

        return ", ".join(vehicles)

    def slot_numbers_for_cars_with_colour(self, color):
        '''
        :param color: Vehicle color
        :return: List of vehicle numbers (reg no)
        '''

        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"

        # Validate vehicle color
        if not self.validate_color(color):
            return "Invalid color"

        # Get list of vehicle numbers from busy slots
        reg_numbers = [k.reg_no for k in self.busy_slots.values() if k.color.lower() == color.lower()]
        if not reg_numbers:
            return "{} color vehicle does not exist!".format(color.capitalize())

        # Join slot numbers
        return ", ".join([str(self.reg_slot_map[k]) for k in reg_numbers])

    def slot_number_for_registration_number(self, reg_no):
        '''
        :param reg_no: Vehicle number(reg no)
        :return: slot number of the corresponding vehicle number
        '''

        # Check slot created or not
        if not self.check_slot_created():
            return "Parking lot not created!"

        # Validate vehicle number
        if not self.validate_vehicle_number(reg_no):
            return "Invalid vehicle number"

        slot = self.reg_slot_map.get(reg_no.upper())
        if not slot:
            return "Not Found"

        return slot

    def is_valid_command(self, command):
        '''
        Validate entered command
        :param command: Command needs to be executed
        :return: True/False
        '''

        return command in self.VALID_COMMANDS

    def execute_command(self, command):
        '''
        Execute entered command
        :param command: Command needs to be executed
        :return: Print execution output
        '''

        inputs = command.strip().split(" ")
        command = inputs[0]
        input_length = len(inputs)
        msg = None
        if command == "create_parking_lot" and input_length == 2:
            msg = self.create_parking_lot(int(inputs[1]))
        elif command == "park" and input_length == 3:
            msg = self.park(inputs[1], inputs[2])
        elif command == "leave" and input_length == 2:
            msg = self.leave(int(inputs[1]))
        elif command == "status" and input_length == 1:
            self.status()
        elif command == "registration_numbers_for_cars_with_colour" and input_length == 2:
            msg = self.registration_numbers_for_cars_with_colour(inputs[1])
        elif command == "slot_numbers_for_cars_with_colour" and input_length == 2:
            msg = self.slot_numbers_for_cars_with_colour(inputs[1])
        elif command == "slot_number_for_registration_number" and input_length == 2:
            msg = self.slot_number_for_registration_number(inputs[1])
        else:
            msg = "Invalid arguments. Please correct it"
        return msg

    def init_interactive_mode(self):
        print("Please enter the commands. Enter 'exit' to quit")

        while True:
            command = raw_input()

            if self.is_valid_command(command.split(" ")[0].lower()):
                output = self.execute_command(command)
                if output: print(output)
            elif command:
                print("Invalid command. Please check again.")
            if command.upper() == 'EXIT': break

    def init_file_mode(self, file_path):
        for command in open(file_path, "r"):
            if command.strip() and self.is_valid_command(command.strip().split(" ")[0].lower()):
                output = self.execute_command(command)
                if output: print(output)
            elif command.strip():
                print("Invalid command ({}). Please check again.".format(command))