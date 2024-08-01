import unittest
from unittest.mock import MagicMock
from tkinter import Tk
from password_manager import root_window
from db_operations import DbOperation

class TestRootWindow(unittest.TestCase):
    def setUp(self):
        self.db = DbOperation()
        self.db.create_table("test_password_info")
        self.root = Tk()
        self.app = root_window(self.root, self.db)
        self.app.db.create_record = MagicMock()
        self.app.db.update_record = MagicMock()
        self.app.db.delete_record = MagicMock()
        self.app.db.search_records = MagicMock(return_value=[])

    def tearDown(self):
        self.root.destroy()
        self.db.delete_table("test_password_info")

    def test_save_record(self):
        self.app.entry_boxes[1].insert(0, "Test Title")
        self.app.entry_boxes[2].insert(0, "TestUser")
        self.app.entry_boxes[3].insert(0, "TestPass")
        self.app.save_record()
        self.app.db.create_record.assert_called_once_with(
            {'title': 'Test Title', 'username': 'TestUser', 'password': 'TestPass'}
        )

    def test_update_record(self):
        self.app.entry_boxes[0].insert(0, "1")
        self.app.entry_boxes[1].insert(0, "Updated Title")
        self.app.entry_boxes[2].insert(0, "UpdatedUser")
        self.app.entry_boxes[3].insert(0, "UpdatedPass")
        self.app.update_record()
        self.app.db.update_record.assert_called_once_with(
            {'ID': 1, 'title': 'Updated Title', 'username': 'UpdatedUser', 'password': 'UpdatedPass'}
        )

    def test_delete_record(self):
        self.app.entry_boxes[0].insert(0, "1")
        self.app.delete_record()
        self.app.db.delete_record.assert_called_once_with(1)


if __name__ == '__main__':
    unittest.main()
