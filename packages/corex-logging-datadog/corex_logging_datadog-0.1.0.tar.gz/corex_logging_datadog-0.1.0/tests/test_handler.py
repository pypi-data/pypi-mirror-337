import unittest
from corex_logging_datadog.handler import DatadogHandler

class TestDatadogHandler(unittest.TestCase):
    def test_example_method(self):
        handler = DatadogHandler()
        # This is a placeholder test; adjust the assertion as needed.
        self.assertIsNone(handler.example_method())

if __name__ == "__main__":
    unittest.main()
