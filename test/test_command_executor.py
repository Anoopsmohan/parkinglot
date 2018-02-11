__author__ = 'anoop.sm'

import unittest

from command_executor import ParkingLot


class MyTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.parking_lot = ParkingLot()

    def test_execute_command(self):

        # create_parking_lot, park & leave
        self.assertEquals(self.parking_lot.execute_command("xxxx"), "Invalid arguments. Please correct it")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-HH-1234 White"), None)
        self.assertEquals(self.parking_lot.execute_command("create_parking_lot -3"), "Invalid slot count")
        self.assertEquals(self.parking_lot.execute_command("create_parking_lot 3"), "Created a parking lot with 3 slots")
        self.assertEquals(self.parking_lot.execute_command("create_parking_lot 6"), "Slot count already set.")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-HH-1234 White"), "Allocated slot number: 1")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-HH-9999 Red"), "Allocated slot number: 2")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-HH-9999 White"), "Vehicle KA-01-HH-9999 already there in slot 2")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-BB0001 Black"), "Invalid vehicle number")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-BB-0001 Black!"), "Invalid color")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-BB-0001 Black"), "Allocated slot number: 3")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-HH-7777 Red"), "Sorry, parking lot is full")
        self.assertEquals(self.parking_lot.execute_command("leave 4"), "Invalid slot number: 4")
        self.assertEquals(self.parking_lot.execute_command("leave 2"), "Slot number 2 is free")
        self.assertEquals(self.parking_lot.execute_command("park KA-01-P-333 White"), "Allocated slot number: 2")

        # registration_numbers_for_cars_with_colour
        self.assertEquals(self.parking_lot.execute_command("registration_numbers_for_cars_with_colour White1"), "Invalid color")
        self.assertEquals(self.parking_lot.execute_command("registration_numbers_for_cars_with_colour White"), "KA-01-HH-1234, KA-01-P-333")
        self.assertEquals(self.parking_lot.execute_command("registration_numbers_for_cars_with_colour black"), "KA-01-BB-0001")
        self.assertEquals(self.parking_lot.execute_command("registration_numbers_for_cars_with_colour blue"), "Blue color vehicle does not exist!")

        # slot_numbers_for_cars_with_colour
        self.assertEquals(self.parking_lot.execute_command("slot_numbers_for_cars_with_colour blue"), "Blue color vehicle does not exist!")
        self.assertEquals(self.parking_lot.execute_command("slot_numbers_for_cars_with_colour white1"), "Invalid color")
        self.assertEquals(self.parking_lot.execute_command("slot_numbers_for_cars_with_colour white"), "1, 2")

        # slot_number_for_registration_number
        self.assertEquals(self.parking_lot.execute_command("slot_number_for_registration_number xx-rr-ww"), "Invalid vehicle number")
        self.assertEquals(self.parking_lot.execute_command("slot_number_for_registration_number xx-yy-cc-dd"), "Not Found")
        self.assertEquals(self.parking_lot.execute_command("slot_number_for_registration_number KA-01-HH-1234"), 1)


if __name__ == '__main__':
    unittest.main()