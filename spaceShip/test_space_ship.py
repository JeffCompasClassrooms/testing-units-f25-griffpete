import math
import unittest
from space_ship import *

class test_space_ship(unittest.TestCase):
    # Inital
    def test_initial_positition(self):
        ship = SpaceshipNavigation()
        self.assertEqual(ship.get_position(), (0, 0, 0))

    def test_initial_velocity(self):
        ship = SpaceshipNavigation()
        self.assertEqual(ship.get_velocity(), (0, 0, 0))

    # Position
    def test_set_position_locked(self):
        ship = SpaceshipNavigation()
        ship.lock_navigation(True)
        result = ship.set_position(1, 2, 3)
        self.assertFalse(result)

    def test_set_position_unlocked(self):
        ship = SpaceshipNavigation()
        result = ship.set_position(1, 2, 3)
        self.assertTrue(result)

    def test_set_position_changed_locked(self):
        ship = SpaceshipNavigation()
        ship.lock_navigation(True)
        ship.set_position(1, 2, 3)
        self.assertEqual(ship.get_position(), (0, 0, 0))

    def test_set_position_changed_unlocked(self):
        ship = SpaceshipNavigation()
        result = ship.set_position(1, 2, 3)
        self.assertTrue(result)  # Should return True when successful
        self.assertEqual(ship.get_position(), (1.0, 2.0, 3.0))

    # Velocity
    def test_velocity_locked(self):
        ship = SpaceshipNavigation()
        ship.lock_navigation(True)
        result = ship.set_velocity(1, 2, 3)
        self.assertFalse(result)

    def test_velocity_unlocked(self):
        ship = SpaceshipNavigation()
        result = ship.set_velocity(1, 2, 3)
        self.assertTrue(result)

    def test_velocity_out_of_speed_limit(self):
        ship = SpaceshipNavigation()
        result = ship.set_velocity(999, 999, 999)
        self.assertFalse(result)

    def test_velocity_changed_locked(self):
        ship = SpaceshipNavigation()
        ship.lock_navigation(True)
        ship.set_velocity(1, 2, 3)
        self.assertEqual(ship.get_velocity(), (0, 0, 0))

    def test_velocity_changed_unlocked(self):
        ship = SpaceshipNavigation()
        ship.set_velocity(1, 2, 3)
        self.assertEqual(ship.get_velocity(), (1, 2, 3))

    # Move
    def test_move_locked(self):
        ship = SpaceshipNavigation()
        ship.lock_navigation(True)
        result = ship.move(1, 2, 3)
        self.assertFalse(result)

    def test_move_unlocked(self):
        ship = SpaceshipNavigation()
        result = ship.move(1, 2, 3)
        self.assertTrue(result)

    def test_move_zero_unlocked(self):
        ship = SpaceshipNavigation()
        result = ship.move(0, 0, 0)
        self.assertTrue(result)

    def test_move_changed_locked(self):
        ship = SpaceshipNavigation()
        ship.lock_navigation(True)
        ship.move(1, 2, 3)
        self.assertEqual(ship.get_position(), (0, 0, 0))

    def test_move_changed_unlocked(self):
        ship = SpaceshipNavigation()
        ship.move(1, 2, 3)
        self.assertEqual(ship.get_position(), (1.0, 2.0, 3.0))

    def test_move_changed_preset_unlocked(self):
        ship = SpaceshipNavigation()
        ship.set_position(1, 2, 3)
        ship.move(1, 2, 3)
        self.assertEqual(ship.get_position(), (2.0, 4.0, 6.0))

    def test_move_greater(self):
        ship = SpaceshipNavigation()
        ship.set_position(1, 2, 3)
        position1 = ship.get_position()
        ship.move(1, 2, 3)
        position2 = ship.get_position()
        self.assertGreater(position2, position1)

    def test_move_less(self):
        ship = SpaceshipNavigation()
        ship.set_position(1, 2, 3)
        position1 = ship.get_position()
        ship.move(-10, -20, -30)
        position2 = ship.get_position()
        self.assertLess(position2, position1)

    def test_move_no_fuel(self):
        ship = SpaceshipNavigation()
        move = ship.move(1000, 2000, 3000)
        self.assertFalse(move)

    # Accelerate
    def test_accelerate_locked(self):
        ship = SpaceshipNavigation()
        ship.lock_navigation(True)
        result = ship.accelerate(1, 2, 3, 10)
        self.assertFalse(result)

    def test_accelerate_unlocked(self):
        ship = SpaceshipNavigation()
        result = ship.accelerate(1, 2, 3, 10)
        self.assertTrue(result)

    def test_accelerate_zero_time(self):
        ship = SpaceshipNavigation()
        result = ship.accelerate(1, 2, 3, 0)
        self.assertFalse(result)

    def test_accelerate_changed_locked(self):
        ship = SpaceshipNavigation()
        ship.lock_navigation(True)
        ship.accelerate(1, 2, 3, 10)
        self.assertEqual(ship.get_velocity(), (0, 0, 0))

    def test_accelerate_changed_unlocked(self):
        ship = SpaceshipNavigation()
        ship.accelerate(1, 2, 3, 10)
        self.assertEqual(ship.get_velocity(), (10, 20, 30))

    def test_accelerate_changed_preset_unlocked(self):
        ship = SpaceshipNavigation()
        ship.set_velocity(1, 1, 1)
        ship.accelerate(1, 2, 3, 10)
        self.assertEqual(ship.get_velocity(), (11, 21, 31))

    def test_accelerate_out_of_speed_limit(self):
        ship = SpaceshipNavigation()
        result = ship.accelerate(999, 999, 999, 10)
        self.assertFalse(result)

    def test_accelerate_no_fuel(self):
        ship = SpaceshipNavigation()
        accelerate = ship.accelerate(10, 10, 10, 9999)
        self.assertFalse(accelerate)

    # Distance
    def test_calculate_distance(self):
        ship = SpaceshipNavigation()
        calculate_distance = ship.calculate_distance_to(10, 10, 10)
        self.assertEqual(calculate_distance, math.sqrt(300))

    def test_calculate_distance_preset(self):
        ship = SpaceshipNavigation()
        ship.set_position(5, 5, 5)
        calculate_distance = ship.calculate_distance_to(10, 10, 10)
        self.assertEqual(calculate_distance, math.sqrt(75))

if __name__ == "__main__":
    unittest.main()
