"""
Unit tests for Problem 4: MeetingRoom

Instructions:
Complete the unit test methods below using Python's unittest framework.
Your test methods must assert MULTIPLE ATTRIBUTES on the MeetingRoom object
(e.g., bookings list, total_hours_booked, free slots, utilization rate)
to verify room state and conflict management.

Running tests:
    python -m unittest test_problem4.py -v
"""
import unittest
from problem4 import MeetingRoom


class TestMeetingRoom(unittest.TestCase):

    def setUp(self):
        """Set up test fixtures before each test method."""
        self.room = MeetingRoom("Conference-A", capacity=10)

    def test_initial_state_multi_attributes(self):
        """
        Verify initial state of an empty meeting room.
        """
        self.assertEqual(self.room.room_id, "Conference-A")
        self.assertEqual(self.room.capacity, 10)
        self.assertEqual(self.room.bookings, [])
        self.assertEqual(self.room.total_hours_booked, 0)
        self.assertFalse(self.room.is_maintenance)
        self.assertEqual(self.room.get_free_slots(), [(8, 18)])
        self.assertEqual(self.room.get_utilization_rate(), 0.0)

    def test_single_booking_multi_attributes(self):
        """
        Test making a single valid booking.
        Verify bookings list, total_hours_booked, utilization rate, and free slots.
        """
        # TODO: Book meeting 'B01' from 10 to 12 with 5 attendees
        self.room.book("B01", "Team Meeting", 10, 12, 5)

        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B01")
        self.assertEqual(self.room.bookings[0]["title"], "Team Meeting")
        self.assertEqual(self.room.bookings[0]["attendees"], 5)
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(self.room.get_utilization_rate(), 0.2)
        self.assertEqual(
            self.room.get_free_slots(),
            [(8, 10), (12, 18)]
        )

    def test_back_to_back_meetings_allowed(self):
        """
        Test that valid consecutive / back-to-back meetings (e.g. 9-10 and 10-12)
        are permitted without raising conflict errors.
        Verify multi-attribute state after both bookings succeed.
        """
        # TODO: Book 'B01' from 9 to 10
        
        self.room.book("B01", "Morning Meeting", 9, 10, 5)
        self.room.book("B02", "Team Meeting", 10, 12, 6)

        self.assertEqual(len(self.room.bookings), 2)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B01")
        self.assertEqual(self.room.bookings[1]["booking_id"], "B02")
        self.assertEqual(self.room.total_hours_booked, 3)
        self.assertEqual(self.room.get_utilization_rate(), 0.3)
        self.assertEqual(
            self.room.get_free_slots(),
            [(8, 9), (12, 18)]
        )


    def test_overlapping_booking_rejected(self):
        """
        Test that overlapping bookings (e.g. 9-11 and 10-12, or completely inside 9-12 and 10-11)
        raise ValueError and leave room state unchanged.
        """
        # TODO: Implement test with self.assertRaises(ValueError)
        
        self.room.book("B01", "First Meeting", 9, 12, 5)

        bookings_before = self.room.bookings.copy()
        hours_before = self.room.total_hours_booked

        with self.assertRaises(ValueError):
            self.room.book("B02", "Overlapping Meeting", 10, 11, 4)

        self.assertEqual(self.room.bookings, bookings_before)
        self.assertEqual(self.room.total_hours_booked, hours_before)
        self.assertEqual(len(self.room.bookings), 1)


    def test_cancel_booking_updates_all_attributes(self):
        """
        Test that cancelling a booking correctly removes it from bookings,
        decrements total_hours_booked, and restores free slots.
        """
        # TODO: Book two meetings, cancel one, verify all attributes
        
        self.room.book("B01", "Morning Meeting", 9, 11, 5)
        self.room.book("B02", "Afternoon Meeting", 13, 15, 6)

        self.assertEqual(len(self.room.bookings), 2)
        self.assertEqual(self.room.total_hours_booked, 4)

        self.room.cancel("B01")

        self.assertEqual(len(self.room.bookings), 1)
        self.assertEqual(self.room.bookings[0]["booking_id"], "B02")
        self.assertEqual(self.room.total_hours_booked, 2)
        self.assertEqual(
            self.room.get_free_slots(),
            [(8, 13), (15, 18)]
        )
        self.assertEqual(self.room.get_utilization_rate(), 0.2)


    def test_capacity_and_validation_exceptions(self):
        """
        Test edge cases and exceptions:
        - Attendees exceeding capacity (ValueError)
        - Start time >= End time (ValueError)
        - Duplicate booking ID (ValueError)
        - Booking when room is under maintenance (RuntimeError)
        - Cancelling non-existent booking (KeyError)
        """
        # TODO: Implement exception tests using self.assertRaises()
        pass


if __name__ == "__main__":
    unittest.main()
