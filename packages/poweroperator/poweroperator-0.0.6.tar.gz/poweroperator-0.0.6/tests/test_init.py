import unittest


class TestImport(unittest.TestCase):
    def test_import_poweroperator(self):
        """Test that poweroperator module can be imported"""
        try:
            import poweroperator
            self.assertTrue(True)
        except ImportError:
            self.fail("Failed to import poweroperator module")
    
    def test_import_api(self):
        """Test that poweroperator_api module can be imported"""
        try:
            from poweroperator import poweroperator_api
            self.assertTrue(True)
        except ImportError:
            self.fail("Failed to import poweroperator_api module")


if __name__ == "__main__":
    unittest.main()