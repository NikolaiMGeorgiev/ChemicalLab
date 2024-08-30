
import unittest
from unittest.mock import MagicMock, patch
from models import Chats, Messages, DiaryLog
from database import DB

class TestDB(unittest.TestCase):
    @patch("sqlalchemy.orm.sessionmaker")
    @patch("sqlalchemy.create_engine")
    def setUp(self, mock_engine, mock_sessionmaker):
        engine = MagicMock()
        connection = MagicMock()
        self.session = MagicMock()
        self.query = MagicMock()

        mock_engine.return_value = engine
        engine.connect.return_value = connection
        mock_sessionmaker.return_value = MagicMock(return_value=self.session)

        self.db = DB()
        self.db.get_dict_result = MagicMock()
        self.db.session = self.session

        self.db.session.query.return_value = self.query
        self.db.session.query.filter.return_value = self.query

    def test_get_chat(self):
        mock_chat = MagicMock()
        chat_data = {"id": 100, "user_id": 1, "vendor_id": 2}
        self.db.session.query.return_value.filter.return_value.first.return_value = mock_chat
        self.db.get_dict_result.return_value = chat_data

        result = self.db.get_chat(1)

        self.db.session.query.assert_called_once_with(Chats)
        self.db.session.query.return_value.filter.return_value.first.assert_called_once()
        self.assertEqual(result, chat_data)

    def test_get_chat_no_chat(self):
        self.db.session.query.return_value.filter.return_value.first.return_value = None

        result = self.db.get_chat(101)

        self.db.session.query.assert_called_once_with(Chats)
        self.db.session.query.return_value.filter.return_value.first.assert_called_once()
        self.assertIsNone(result)
    
    def test_get_chat_by_users(self):
        mock_chat = MagicMock()
        chat_data = {"id": 1, "user_id": 1, "vendor_id": 2}
        self.db.session.query.filter.return_value.first.return_value = mock_chat
        self.db.get_dict_result.return_value = chat_data

        result = self.db.get_chat_by_users(1, 2)

        self.db.session.query.assert_called_once_with(Chats)
        self.db.session.query.return_value.filter.return_value.first.assert_called_once()
        self.assertEqual(result, chat_data)

    def test_get_chat_by_users_no_chat(self):
        self.db.session.query.return_value.filter.return_value.first.return_value = None

        result = self.db.get_chat_by_users(1, 2)

        self.db.session.query.assert_called_once_with(Chats)
        self.db.session.query.return_value.filter.return_value.first.assert_called_once()
        self.assertIsNone(result)

    def test_get_pending_chat(self):
        mock_chat = MagicMock()
        chat_data = {"id": 1, "user_id": None, "vendor_id": 2}
        self.db.session.query.filter.return_value.order_by.return_value = mock_chat
        self.db.get_dict_result.return_value = chat_data

        result = self.db.get_pending_chat(2)

        self.db.session.query.assert_called_once_with(Chats)
        self.db.session.query.return_value.filter.return_value.order_by.assert_called_once()
        self.assertEqual(result, chat_data)

    def test_get_unreceived_message(self):
        mock_message = MagicMock()
        message_data = {
            "id": 1, 
            "chat_id": 1, 
            "content": "Message content", 
            "sent_time": "30-08-2024 12:12:12",
            "sender": "user",
            "read": 0

        }
        self.db.session.query.filter.return_value.first.return_value = mock_message
        self.db.get_dict_result.return_value = message_data

        result = self.db.get_unreceived_message(1, "user")

        self.db.session.query.assert_called_once_with(Messages)
        self.db.session.query.return_value.filter.return_value.first.assert_called_once()
        self.assertEqual(result, message_data)

    def test_get_unreceived_message_no_messages(self):
        self.db.session.query.return_value.filter.return_value.first.return_value = None

        result = self.db.get_unreceived_message(1, "user")

        self.db.session.query.assert_called_once_with(Messages)
        self.db.session.query.return_value.filter.return_value.first.assert_called_once()
        self.assertIsNone(result)

    def test_join_pending_chat(self):
        mock_chat = MagicMock()
        mock_chat.__dict__["id"] = 1
        mock_chat.__dict__["user_id"] = None
        self.db.session.query.filter.return_value.order_by.return_value.first.return_value = mock_chat
        self.db.get_dict_result.return_value = {"id": 1, "user_id": None}

        result = self.db.join_pending_chat(1)

        self.db.session.query.assert_called_once_with(Chats)
        self.db.session.query.return_value.filter.return_value.order_by.return_value.first.assert_called_once()
        self.db.session.commit.assert_called_once()
        self.assertEqual(result, {"id": 1, "user_id": None})
    
    def test_join_pending_chat_no_chat(self):
        self.db.session.query.return_value.filter.return_value.order_by.return_value.first.return_value = None

        result = self.db.join_pending_chat(1)

        self.db.session.query.assert_called_once_with(Chats)
        self.db.session.query.return_value.filter.return_value.order_by.return_value.first.assert_called_once()
        self.db.session.commit.assert_not_called()
        self.assertIsNone(result)


if __name__ == "__main__":
    unittest.main()
