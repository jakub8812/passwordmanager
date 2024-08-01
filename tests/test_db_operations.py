import unittest
from db_operations import DbOperation

class TestDbOperation(unittest.TestCase):
    def setUp(self):
        self.db = DbOperation()
        self.db.create_table("test_password_info")
        self.db.delete_table("test_password_info") 
        self.db.create_table("test_password_info") 

    def tearDown(self):
        self.db.delete_table("test_password_info")

    def test_create_record(self):
        data = {'title': 'Test Title', 'username': 'TestUser', 'password': 'TestPass'}
        self.db.create_record(data, "test_password_info")
        records = list(self.db.show_records("test_password_info"))
        self.assertEqual(len(records), 1)
        self.assertEqual(records[0][3], 'Test Title')
        self.assertEqual(records[0][4], 'TestUser')
        self.assertEqual(records[0][5], 'TestPass')

    def test_update_record(self):
        data = {'title': 'Test Title', 'username': 'TestUser', 'password': 'TestPass'}
        self.db.create_record(data, "test_password_info")
        records = list(self.db.show_records("test_password_info"))
        record_id = records[0][0]
        update_data = {'ID': record_id, 'title': 'Updated Title', 'username': 'UpdatedUser', 'password': 'UpdatedPass'}
        self.db.update_record(update_data, "test_password_info")
        updated_records = list(self.db.show_records("test_password_info"))
        self.assertEqual(updated_records[0][3], 'Updated Title')
        self.assertEqual(updated_records[0][4], 'UpdatedUser')
        self.assertEqual(updated_records[0][5], 'UpdatedPass')

    def test_delete_record(self):
        data = {'title': 'Test Title', 'username': 'TestUser', 'password': 'TestPass'}
        self.db.create_record(data, "test_password_info")
        records = list(self.db.show_records("test_password_info"))
        record_id = records[0][0]
        self.db.delete_record(record_id, "test_password_info")
        records_after_deletion = list(self.db.show_records("test_password_info"))
        self.assertEqual(len(records_after_deletion), 0)

    def test_search_records(self):
        data = {'title': 'Test Title', 'username': 'TestUser', 'password': 'TestPass'}
        self.db.create_record(data, "test_password_info")
        search_results = list(self.db.search_records('Test Title', "test_password_info"))
        self.assertEqual(len(search_results), 1)
        self.assertEqual(search_results[0][3], 'Test Title')
        self.assertEqual(search_results[0][4], 'TestUser')
        self.assertEqual(search_results[0][5], 'TestPass')

if __name__ == '__main__':
    unittest.main()
