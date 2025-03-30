import unittest
from neoagent.module import create


class TestNeoAgent(unittest.TestCase):
    def test_create(self):
        self.assertEqual(create(), "create agent success")


if __name__ == "__main__":
    unittest.main()
