import os
os.environ['APP_ENVIRONMENT'] = 'test'
import datetime

import location_tool
from location_tool import models
from location_tool.database import db_session, truncate_database
import unittest
import config.test as test_config
import json

class LocationToolTestCase(unittest.TestCase):

    def setUp(self):
        os.environ['APP_ENVIRONMENT'] = 'test'
        location_tool.app.config['TESTING'] = True
        location_tool.app.config.from_object(test_config)
        self.app = location_tool.app.test_client()

    def tearDown(self):
        pass

    def test_db(self):
        self.assertEqual(location_tool.database.engine.url.database,
                         test_config.DB_NAME)
        self.assertEqual(location_tool.app.config['DATABASE'], test_config.DATABASE)

    def test_home_page(self):
        rv = self.app.get('/')
        self.assertEqual("200 OK", rv.status)

    def test_create_bounding_box_returns_201(self):
        truncate_database(db_session)
        post_data = json.dumps({
            'name': 'Test Bounding Box',
            'coordinates': {
                'northEast': { 'lat': 3.0, 'lng': -2.0 },
                'southWest': { 'lat': 1.0, 'lng': -4.0 }
            }
        })
        rv = self.app.post('/bounding-boxes',
                           data=post_data,
                           headers={'content-type':'application/json'})
        self.assertEqual("201 CREATED", rv.status)

    def test_create_bounding_box_adds_to_db(self):
        truncate_database(db_session)
        post_data = json.dumps({
            'name': 'Test Bounding Box',
            'coordinates': {
                'northEast': { 'lat': 3.0, 'lng': -2.0 },
                'southWest': { 'lat': 1.0, 'lng': -4.0 }
            }
        })
        rv = self.app.post('/bounding-boxes',
                           data=post_data,
                           headers={'content-type':'application/json'})
        count = models.BoundingBox.query.filter(
            models.BoundingBox.name == 'Test Bounding Box'
        ).count()
        self.assertEqual(count, 1)

    def test_create_bounding_box_transforms_coordinates(self):
        truncate_database(db_session)
        post_data = json.dumps({
            'name': 'Test Bounding Box',
            'coordinates': {
                'northEast': { 'lat': 3.0, 'lng': -2.0 },
                'southWest': { 'lat': 1.0, 'lng': -4.0 }
            }
        })
        rv = self.app.post('/bounding-boxes',
                           data=post_data,
                           headers={'content-type':'application/json'})
        bounding_box = models.BoundingBox.query.filter(
            models.BoundingBox.name == 'Test Bounding Box'
        ).first()
        transformed = {
            'northeast': { 'lat': 3.0, 'lng': -2.0 },
            'northwest': { 'lat': 3.0, 'lng': -4.0 },
            'southwest': { 'lat': 1.0, 'lng': -4.0 },
            'southeast': { 'lat': 1.0, 'lng': -2.0 },
            'center': { 'lat': 2.0, 'lng': -3.0 }
        }
        self.assertEqual(bounding_box.coordinates, transformed)

    def test_create_bounding_box_returns_new_record(self):
        truncate_database(db_session)
        post_data = json.dumps({
            'name': 'Test Bounding Box',
            'coordinates': {
                'northEast': { 'lat': 1.0, 'lng': -2.0 },
                'southWest': { 'lat': 3.0, 'lng': -4.0 }
            }
        })
        rv = self.app.post('/bounding-boxes',
                           data=post_data,
                           headers={'content-type':'application/json'})
        body = json.loads(rv.data)
        self.assertEqual(body, {
            'name': 'Test Bounding Box',
            'created_at': datetime.date.today().strftime('%Y-%m-%d'),
            'state': 'processing'
        })

if __name__ == '__main__':
    unittest.main()
