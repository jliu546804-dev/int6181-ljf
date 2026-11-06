"""Unit tests for Problem 4: MeetingRoom."""
import unittest
from problem4 import MeetingRoom


class TestMeetingRoom(unittest.TestCase):
    def setUp(self):
        self.room = MeetingRoom("Conference-A", capacity=10)

    def test_initial_state_multi_attributes(self):
        self.assertEqual(self.room.room_id, "Conference-A")
        self.assertEqual(self.room.capacity, 10)
        self.assertEqual(self.room.bookings, [])
        self.assertEqual(self.room.total_hours_booked, 0)
        self.assertFalse(self.room.is_maintenance)
        self.assertEqual(self.room.get_free_slots(8, 18), [(8, 18)])
        self.assertEqual(self.room.get_utilization_rate(10), 0.0)

    def test_single_booking_multi_attributes(self):
        self.assertTrue(self.room.book("B01", "Team meeting", 10, 12, 5))
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B01")
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(self.room.get_utilization_rate(10), 0.2)
        self.assertEqual(self.room.get_free_slots(8, 18), [(8, 10), (12, 18)])

    def test_back_to_back_meetings_allowed(self):
        self.room.book("B01", "Morning meeting", 9, 10, 5)
        self.room.book("B02", "Next meeting", 10, 12, 4)
        self.assertEqual([b["booking_id"] for b in self.room.bookings], ["B01", "B02"])
        self.assertEqual(self.room.total_hours_booked, 3)
        self.assertEqual(self.room.get_free_slots(8, 18), [(8, 9), (12, 18)])
        self.assertEqual(self.room.get_utilization_rate(10), 0.3)

    def test_overlapping_booking_rejected(self):
        self.room.book("B01", "First", 9, 12, 5)
        before_bookings = list(self.room.bookings)
        before_hours = self.room.total_hours_booked
        with self.assertRaises(ValueError):
            self.room.book("B02", "Overlap", 10, 11, 3)
        self.assertEqual(self.room.bookings, before_bookings)
        self.assertEqual(self.room.total_hours_booked, before_hours)

    def test_cancel_booking_updates_all_attributes(self):
        self.room.book("B01", "First", 9, 10, 5)
        self.room.book("B02", "Second", 11, 13, 4)
        self.assertTrue(self.room.cancel("B01"))
        self.assertEqual([b["booking_id"] for b in self.room.bookings], ["B02"])
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(self.room.get_free_slots(8, 18), [(8, 11), (13, 18)])
        self.assertEqual(self.room.get_utilization_rate(10), 0.2)

    def test_capacity_and_validation_exceptions(self):
        with self.assertRaises(ValueError):
            self.room.book("B01", "Too many", 9, 10, 11)
        with self.assertRaises(ValueError):
            self.room.book("B02", "Bad time", 10, 10, 2)
        self.room.book("B03", "Valid", 9, 10, 2)
        with self.assertRaises(ValueError):
            self.room.book("B03", "Duplicate", 11, 12, 2)
        self.room.is_maintenance = True
        with self.assertRaises(RuntimeError):
            self.room.book("B04", "Maintenance", 11, 12, 2)
        with self.assertRaises(KeyError):
            self.room.cancel("NOT-FOUND")
        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.total_hours_booked, 1)


if __name__ == "__main__":
    unittest.main()
