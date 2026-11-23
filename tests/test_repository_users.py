import unittest
from unittest.mock import MagicMock, patch

from app.repository_users import (
    get_user_by_email,
    create_user,
    update_token,
    confirm_user_email,
    update_avatar,
)


class TestRepositoryUsers(unittest.TestCase):
    def setUp(self):
        self.db = MagicMock()
        self.user = MagicMock()

    def test_get_user_by_email(self):
        email = "test@example.com"
        self.db.query.return_value.filter.return_value.first.return_value = (
            self.user
        )

        result = get_user_by_email(email, self.db)

        self.db.query.assert_called_once()
        self.assertEqual(result, self.user)

    @patch("app.repository_users.auth_service.get_password_hash")
    @patch("app.repository_users.User")
    def test_create_user(self, mock_user, mock_hash):
        body = MagicMock()
        body.username = "TestUser"
        body.email = "test@example.com"
        body.password = "password123"

        mock_hash.return_value = "hashed_password"

        result = create_user(body, self.db)

        mock_hash.assert_called_once_with("password123")

        mock_user.assert_called_once_with(
            username="TestUser",
            email="test@example.com",
            password="hashed_password",
        )

        self.db.add.assert_called_once()
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once()

        self.assertEqual(result, mock_user.return_value)

    def test_update_token(self):
        refresh_token = "new_refresh_token"

        update_token(self.user, refresh_token, self.db)

        self.assertEqual(self.user.refresh_token, refresh_token)
        self.db.commit.assert_called_once()

    def test_confirm_user_email(self):
        confirm_user_email(self.user, self.db)

        self.assertTrue(self.user.confirmed)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(self.user)

    def test_update_avatar(self):
        avatar_url = "https://example.com/avatar.jpg"

        result = update_avatar(self.user, avatar_url, self.db)

        self.assertEqual(self.user.avatar, avatar_url)
        self.db.commit.assert_called_once()
        self.db.refresh.assert_called_once_with(self.user)

        self.assertEqual(result, self.user)


if __name__ == "__main__":
    unittest.main()
