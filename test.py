import unittest
from api import app


class MyAppTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        app.config["TESTING"] = True
        cls.client = app.test_client()

    def test_index_page(self):
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data.decode(), "<p>Hello, World!</p>")

    def test_get_actors(self):
        response = self.client.get("/mydb")
        self.assertEqual(response.status_code, 200)
        self.assertIn("1000.00", response.data.decode())

    def test_get_mydb_by_id(self):
        response = self.client.get("/mydb/15")
        self.assertEqual(response.status_code, 200)
        self.assertIn("8000.00", response.data.decode())


if __name__ == "__main__":
    unittest.main()
