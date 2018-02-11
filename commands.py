__author__ = 'anoop.sm'

import command_executor


class Commands(object):

    def __init__(self):
        self.command_map = {
            'create_parking_lot': command_executor.ParkingLot.create_parking_lot,
            'park': command_executor.ParkingLot.park,
            'leave': command_executor.ParkingLot.leave,
            'status': command_executor.ParkingLot.status,
            'registration_numbers_for_cars_with_colour': command_executor.ParkingLot.registration_numbers_for_cars_with_colour,
            'slot_numbers_for_cars_with_colour': command_executor.ParkingLot.slot_numbers_for_cars_with_colour,
            'slot_number_for_registration_number': command_executor.ParkingLot.slot_number_for_registration_number
        }