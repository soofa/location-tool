import location_tool
import unittest

class LocationToolTestCase(unittest.TestCase):

    def setUp(self):
        location_tool.app.config['TESTING'] = True
        self.app = location_tool.app.test_client()

    def tearDown(self):
        pass

    def test_root_url(self):
        rv = self.app.get('/')
        assert "200 OK" == rv.status

if __name__ == '__main__':
    unittest.main()
