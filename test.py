import unittest

class Test(unittest.TestCase):
  def test_one(self):
    self.assertEquals(1, 2)

if __name__ == '__main__':
  unittest.main()
