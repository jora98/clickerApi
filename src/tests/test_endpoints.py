import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from common.database import db
from model.geoarea import GeoArea
from model.pollution import Pollution
from config.database import TestConfig
from datetime import datetime, timedelta
import warnings

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        print("start setting up test environment...")

        warnings.filterwarnings("ignore")

        self.test_app = create_app(TestConfig, db)
        self.app = self.test_app.test_client()

        self.app_context = self.test_app.app_context()
        self.app_context.push()
        
        # Create the tables using the application context
        with self.test_app.app_context():
            db.create_all()
        
    def tearDown(self):
        # Drop the tables using the application context
        with self.test_app.app_context():
            print("tearDown")
            db.session.close_all()
            db.drop_all()

        
        self.app_context.pop()

    def test_get_geoareas(self):
        geoarea1 = GeoArea(
        id=1,
        name='Area 1',
        datecreated=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
        language='German',
        last_update=datetime.strptime('2023-08-25 00:00:00', '%Y-%m-%d %H:%M:%S'),
        mandant='Mandant A',
        admincomment='Comment 1',
        automaticsearch=True,
        polygon="POLYGON((1 2,2 3, 3 4, 5 6, 1 2))"
        )

        geoarea2 = GeoArea(
            id=2,
            name='Area 2',
            datecreated=datetime.strptime('2023-02-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
            language='English',
            last_update=datetime.strptime('2023-08-26 00:00:00', '%Y-%m-%d %H:%M:%S'),
            mandant='Mandant B',
            admincomment='Comment 2',
            automaticsearch=False,
            polygon="POLYGON((1 2,2 3, 3 4, 5 6, 1 2))"
        )

        db.session.add_all([geoarea1, geoarea2])
        db.session.commit()

        # Send a GET request to the /geoarea endpoint
        with self.test_app.test_client() as client:
            response = client.get('/geoarea')

            # Assert response status code
            self.assertEqual(response.status_code, 200)

            # Parse JSON response data
            response_data = response.get_json()

            # Assert the expected number of geoareas in the response
            self.assertEqual(len(response_data), 2)

            # Assert the expected data for the first geoarea
            self.assertEqual(response_data[0]['id'], 1)
            self.assertEqual(response_data[0]['name'], 'Area 1')
            self.assertEqual(response_data[0]['datecreated'], '2023-01-01T00:00:00')
            self.assertEqual(response_data[0]['language'], 'German')
            self.assertEqual(response_data[0]['last_update'], '2023-08-25T00:00:00')
            self.assertEqual(response_data[0]['mandant'], 'Mandant A')
            self.assertEqual(response_data[0]['admincomment'], 'Comment 1')
            self.assertEqual(response_data[0]['automaticsearch'], True)
            self.assertEqual(response_data[0]['polygon']['coordinates'], [[[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]])

            # Assert the expected data for the second geoarea
            self.assertEqual(response_data[1]['id'], 2)
            self.assertEqual(response_data[1]['name'], 'Area 2')
            self.assertEqual(response_data[1]['datecreated'], '2023-02-01T00:00:00')
            self.assertEqual(response_data[1]['language'], 'English')
            self.assertEqual(response_data[1]['last_update'], '2023-08-26T00:00:00')
            self.assertEqual(response_data[1]['mandant'], 'Mandant B')
            self.assertEqual(response_data[1]['admincomment'], 'Comment 2')
            self.assertEqual(response_data[1]['automaticsearch'], False)
            self.assertEqual(response_data[1]['polygon']['coordinates'], [[[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]])
    
    def test_get_pollutions(self):
        geoarea1 = GeoArea(
        id=1,
        name='Area 1',
        datecreated=datetime.strptime('2023-01-01 00:00:00', '%Y-%m-%d %H:%M:%S'),
        language='German',
        last_update=datetime.strptime('2023-08-25 00:00:00', '%Y-%m-%d %H:%M:%S'),
        mandant='Mandant A',
        admincomment='Comment 1',
        automaticsearch=True,
        polygon="POLYGON((1 2,2 3, 3 4, 5 6, 1 2))"
        )

        pollution1 = Pollution(
            name='Pollution 1',
            count=10,
            description='Description 1',
            geoarea_fk=1
        )

        pollution2 = Pollution(
            name='Pollution 2',
            count=5,
            description='Description 2',
            geoarea_fk=1
        )
        db.session.add_all([geoarea1, pollution1, pollution2])
        db.session.commit()

        with self.test_app.test_client() as client:
            response = client.get('/pollution/byGeoarea_fk/1')

            self.assertEqual(response.status_code, 200)

            response_data = response.get_json()

            self.assertEqual(len(response_data), 2)

            self.assertEqual(response_data[0]['name'], 'Pollution 1')
            self.assertEqual(response_data[0]['count'], 10)
            self.assertEqual(response_data[0]['description'], 'Description 1')
            self.assertEqual(response_data[1]['name'], 'Pollution 2')
            self.assertEqual(response_data[1]['count'], 5)
            self.assertEqual(response_data[1]['description'], 'Description 2')

    def test_update_pollution_description(self):
        geoarea = GeoArea(
            id=4,
            name='Area 4',
            datecreated='2023-01-01 00:00:00',
            language='German',
            last_update='2023-08-25 00:00:00',
            mandant='Mandant A',
            admincomment='Comment 1',
            automaticsearch=True,
            polygon="POLYGON((1 2,2 3, 3 4, 5 6, 1 2))"
            )

        pollution = Pollution(
            name='PollutionDescription',
            count=10,
            description='Description',
            geoarea_fk=4
        )
        db.session.add_all([pollution, geoarea])
        db.session.commit()

        expires = timedelta(days=7)
        access_token = create_access_token(identity=geoarea.id, expires_delta=expires)
        self.headers = {'Authorization': f'Bearer {access_token}'}

        # Send a PUT request to the /pollution/pollutionDescription/<pollution_id> endpoint
        with self.test_app.test_client() as client:
            response = client.put('/pollution/pollutionDescription/' + pollution.id, json={'description': 'Updated Description'}, headers=self.headers)

            # Assert response status code
            self.assertEqual(response.status_code, 200)

            # Check the updated description in the database
            updated_pollution = db.session.query(Pollution).get(pollution.id)
            self.assertEqual(updated_pollution.description, 'Updated Description')


    def test_update_pollution_count(self):
        geoarea = GeoArea(
            id=5,
            name='Area 5',
            datecreated='2023-01-01 00:00:00',
            language='German',
            last_update='2023-08-25 00:00:00',
            mandant='Mandant A',
            admincomment='Comment 1',
            automaticsearch=True,
            polygon="POLYGON((1 2,2 3, 3 4, 5 6, 1 2))"
            )

        pollution = Pollution(
            name='PollutionCount',
            count=10,
            description='Description',
            geoarea_fk=5
        )
        db.session.add_all([pollution, geoarea])
        db.session.commit()

        expires = timedelta(days=7)
        access_token = create_access_token(identity=geoarea.id, expires_delta=expires)
        self.headers = {'Authorization': f'Bearer {access_token}'}

        with self.test_app.test_client() as client:
            response = client.put('/pollution/pollutionCount/' + pollution.id, json={'count': 15}, headers=self.headers)

            self.assertEqual(response.status_code, 200)

            updated_pollution = db.session.query(Pollution).get(pollution.id)
            self.assertEqual(updated_pollution.count, 15)

if __name__ == '__main__':
    unittest.main()
