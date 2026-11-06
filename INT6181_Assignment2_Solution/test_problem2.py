"""Unit tests for Problem 2: BankAccount."""
import unittest
from problem2 import BankAccount


class TestBankAccount(unittest.TestCase):
    def setUp(self):
        self.account_empty = BankAccount("ACC001", "Alice", initial_balance=0.0, overdraft_limit=100.0)
        self.account_funded = BankAccount("ACC002", "Bob", initial_balance=200.0, overdraft_limit=50.0)

    def test_initial_state_multi_attributes(self):
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.owner, "Alice")
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.overdraft_limit, 100.0)
        self.assertEqual(self.account_empty.transaction_history, [])
        self.assertEqual(self.account_empty.get_summary()["transaction_count"], 0)

        self.assertEqual(self.account_funded.balance, 200.0)
        self.assertEqual(self.account_funded.owner, "Bob")
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 1)
        self.assertEqual(self.account_funded.transaction_history[0]["type"], "INITIAL_DEPOSIT")
        self.assertEqual(self.account_funded.get_summary()["balance"], 200.0)

    def test_deposit_updates_multiple_attributes(self):
        self.assertTrue(self.account_empty.deposit(150.0))
        self.assertEqual(self.account_empty.balance, 150.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(len(self.account_empty.transaction_history), 1)
        self.assertEqual(self.account_empty.transaction_history[-1]["type"], "DEPOSIT")
        self.assertEqual(self.account_empty.transaction_history[-1]["balance_after"], 150.0)
        self.assertEqual(self.account_empty.get_summary()["transaction_count"], 1)

    def test_withdrawal_within_balance_multi_attributes(self):
        self.assertTrue(self.account_funded.withdraw(50.0, fee=2.50))
        self.assertEqual(self.account_funded.balance, 147.5)
        self.assertEqual(self.account_funded.status, "ACTIVE")
        self.assertEqual(len(self.account_funded.transaction_history), 2)
        transaction = self.account_funded.transaction_history[-1]
        self.assertEqual(transaction["type"], "WITHDRAWAL")
        self.assertEqual(transaction["amount"], 50.0)
        self.assertEqual(transaction["fee"], 2.5)
        self.assertEqual(self.account_funded.get_summary()["balance"], 147.5)

    def test_overdraft_withdrawal_and_status_transition(self):
        self.assertTrue(self.account_empty.withdraw(50.0))
        self.assertEqual(self.account_empty.balance, -50.0)
        self.assertEqual(self.account_empty.status, "OVERDRAWN")
        self.assertEqual(self.account_empty.transaction_history[-1]["balance_after"], -50.0)
        self.assertEqual(self.account_empty.get_summary()["status"], "OVERDRAWN")

    def test_deposit_recovering_from_overdrawn_status(self):
        self.account_empty.withdraw(50.0)
        self.assertEqual(self.account_empty.status, "OVERDRAWN")
        self.account_empty.deposit(50.0)
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_empty.status, "ACTIVE")
        self.assertEqual(self.account_empty.transaction_history[-1]["type"], "DEPOSIT")
        self.assertEqual(self.account_empty.get_summary()["status"], "ACTIVE")

    def test_transfer_between_accounts_multi_attributes(self):
        self.assertTrue(self.account_funded.transfer_to(self.account_empty, 50.0, transfer_fee=5.0))
        self.assertEqual(self.account_funded.balance, 145.0)
        self.assertEqual(self.account_empty.balance, 50.0)
        self.assertEqual(self.account_funded.transaction_history[-1]["fee"], 5.0)
        self.assertEqual(self.account_empty.transaction_history[-1]["type"], "DEPOSIT")
        self.assertEqual(self.account_funded.get_summary()["transaction_count"], 2)
        self.assertEqual(self.account_empty.get_summary()["balance"], 50.0)

    def test_frozen_account_restrictions(self):
        self.account_funded.freeze()
        with self.assertRaises(RuntimeError):
            self.account_funded.deposit(10.0)
        with self.assertRaises(RuntimeError):
            self.account_funded.withdraw(10.0)
        with self.assertRaises(RuntimeError):
            self.account_funded.transfer_to(self.account_empty, 10.0)
        self.assertEqual(self.account_funded.balance, 200.0)
        self.assertEqual(self.account_funded.status, "FROZEN")
        self.assertEqual(len(self.account_funded.transaction_history), 1)

    def test_invalid_operations_raise_exceptions(self):
        with self.assertRaises(ValueError):
            self.account_empty.deposit(0)
        with self.assertRaises(ValueError):
            self.account_funded.withdraw(0)
        with self.assertRaises(ValueError):
            self.account_funded.withdraw(10, fee=-1)
        with self.assertRaises(ValueError):
            self.account_empty.withdraw(101)
        with self.assertRaises(TypeError):
            self.account_funded.transfer_to("not an account", 10)
        with self.assertRaises(ValueError):
            BankAccount("BAD", "Test", initial_balance=-1)
        self.assertEqual(self.account_empty.balance, 0.0)
        self.assertEqual(self.account_funded.balance, 200.0)


if __name__ == "__main__":
    unittest.main()
