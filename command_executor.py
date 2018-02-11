__author__ = 'anoop.sm'

from car import Car
import commands


class ParkingLot(object):

    def __init__(self):
        self.slot_count = 0
        self.free_slots = []
        self.busy_slots = {}
        self.reg_slot_map = {}
        self.commands = commands.Commands()

    def check_slot_created(self):
        if self.slot_count == 0:
            print("Parking lot not created!")
            return False
        else:
            return True

    def create_parking_lot(self, count):
        '''
        :param count: slot count
        :return: message
        '''

        count = int(count)
        if self.slot_count > 0:
            return "Slot count already set."

        if count <= 0:
            return "Invalid slot count"

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

        if not self.check_slot_created(): return

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

        slot = int(slot)
        # Check slot created or not
        if not self.check_slot_created(): return

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
        if not self.check_slot_created(): return

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
        if not self.check_slot_created(): return

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
        if not self.check_slot_created(): return

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
        if not self.check_slot_created(): return

        # Validate vehicle number
        if not self.validate_vehicle_number(reg_no):
            return "Invalid vehicle number"

        slot = self.reg_slot_map.get(reg_no.upper())
        if not slot:
            return "Not Found"

        return slot

    def execute_command(self, user_input):
        '''
        Execute entered command
        :param user_input: Command needs to be executed
        :return: Print execution output
        '''
        inputs = user_input.strip().split(" ")
        command = inputs[0]
        params = inputs[1:]
        command = self.commands.command_map.get(command)
        msg = "Invalid command!"
        if command:
            try:
                msg = command(self, *params)
            except Exception as ex:
                print(ex.message)
                msg = "Invalid arguments"
        return msg

    def init_interactive_mode(self):
        print("Please enter the commands. Enter 'exit' to quit")

        while True:
            user_input = raw_input()

            if user_input.upper() == 'EXIT':
                print("Good Bye!")
                break

            if user_input:
                output = self.execute_command(user_input)
                if output: print(output)

    def init_file_mode(self, file_path):
        for command in open(file_path, "r"):
            if command.strip():
                output = self.execute_command(command)
                if output: print(output)