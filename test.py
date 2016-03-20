import unittest
from app import app

class Test(unittest.TestCase):
	def setUp(self):
		self.app = app.test_client()
		self.app.testing = True

  def test_one(self):
    self.assertEquals(2, 2)
    result = self.app.get('/')
    self.assertEquals(result.status_code, 200)
    self.assertEquals(result.data, "hello")


if __name__ == '__main__':
  unittest.main()
