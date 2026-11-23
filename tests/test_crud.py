import unittest
from datetime import date
from unittest.mock import MagicMock, patch

from app.crud import (
    get_birthday_for_year,
    create_contact,
    update_contact,
    delete_contact,
)


class TestGetBirthdayForYear(unittest.TestCase):
    def test_regular_birthday(self):
        birthday = date(1995, 5, 15)

        result = get_birthday_for_year(birthday, 2026)

        self.assertEqual(result, date(2026, 5, 15))

    def test_birthday_on_leap_year(self):
        birthday = date(2000, 2, 29)

        result = get_birthday_for_year(birthday, 2024)

        self.assertEqual(result, date(2024, 2, 29))

    def test_birthday_on_non_leap_year(self):
        birthday = date(2000, 2, 29)

        result = get_birthday_for_year(birthday, 2025)

        self.assertEqual(result, date(2025, 2, 28))


class TestContactCRUD(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()

    @patch("app.crud.models.Contact")
    def test_create_contact(self, mock_contact):
        contact_data = MagicMock()
        contact_data.model_dump.return_value = {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john@example.com",
            "phone": "123456789",
            "birthday": date(1995, 5, 15),
        }

        user_id = 1

        result = create_contact(self.db, contact_data, user_id)

        mock_contact.assert_called_once_with(
            first_name="John",
            last_name="Doe",
            email="john@example.com",
            phone="123456789",
            birthday=date(1995, 5, 15),
            user_id=user_id,
        )

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        self.assertEqual(result, mock_contact.return_value)

    def test_update_contact(self):
        db_contact = MagicMock()

        contact_data = MagicMock()
        contact_data.model_dump.return_value = {
            "first_name": "Jane",
            "last_name": "Doe",
        }

        result = update_contact(self.db, db_contact, contact_data)

        self.assertEqual(db_contact.first_name, "Jane")
        self.assertEqual(db_contact.last_name, "Doe")

        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(db_contact)

        self.assertEqual(result, db_contact)

    def test_delete_contact(self):
        db_contact = MagicMock()

        delete_contact(self.db, db_contact)

        self.db.delete.assert_called_once_with(db_contact)
        self.db.commit.assert_called_once()


if __name__ == "__main__":
    unittest.main()
