from http import HTTPStatus
import warnings
import unittest
from flask_jwt_extended import create_access_token
from app import create_app
from common.database import db
from model.geoarea import GeoArea
from model.pollution import Pollution
from model.pollutionType import PollutionType
from config.database import TestConfig
from datetime import datetime, timedelta
from model.user import User
import logging

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
            self.assertEqual(response_data[0]['polygon']['coordinates'],
                             [[[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]])

            # Assert the expected data for the second geoarea
            self.assertEqual(response_data[1]['id'], 2)
            self.assertEqual(response_data[1]['name'], 'Area 2')
            self.assertEqual(response_data[1]['datecreated'], '2023-02-01T00:00:00')
            self.assertEqual(response_data[1]['language'], 'English')
            self.assertEqual(response_data[1]['last_update'], '2023-08-26T00:00:00')
            self.assertEqual(response_data[1]['mandant'], 'Mandant B')
            self.assertEqual(response_data[1]['admincomment'], 'Comment 2')
            self.assertEqual(response_data[1]['automaticsearch'], False)
            self.assertEqual(response_data[1]['polygon']['coordinates'],
                             [[[1.0, 2.0], [2.0, 3.0], [3.0, 4.0], [5.0, 6.0], [1.0, 2.0]]])

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

        pollutionType1 = PollutionType(
            name='Typ 1'
        )
        db.session.add(pollutionType1)
        db.session.commit()

        pollution1 = Pollution(
            count=10,
            description='Description 1',
            geoarea_fk=1,
            pollution_type_fk=db.session.query(PollutionType).first().id
        )

        pollution2 = Pollution(
            count=5,
            description='Description 2',
            geoarea_fk=1,
            pollution_type_fk=db.session.query(PollutionType).first().id
        )
        db.session.add_all([geoarea1, pollution1, pollution2])
        db.session.commit()

        with self.test_app.test_client() as client:
            response = client.get('/pollution/byGeoarea_fk/1')

            self.assertEqual(response.status_code, 200)

            response_data = response.get_json()

            self.assertEqual(len(response_data), 2)

            self.assertEqual(response_data[0]['pollution_type_fk'], db.session.query(PollutionType).first().id)
            self.assertEqual(response_data[0]['count'], 10)
            self.assertEqual(response_data[0]['description'], 'Description 1')
            self.assertEqual(response_data[1]['pollution_type_fk'], db.session.query(PollutionType).first().id)
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

        pollutionType1 = PollutionType(
            name='Typ 1'
        )
        db.session.add(pollutionType1)
        db.session.commit()

        pollution = Pollution(
            count=10,
            description='Description 1',
            geoarea_fk=4,
            pollution_type_fk=db.session.query(PollutionType).first().id
        )
        db.session.add_all([pollutionType1, pollution, geoarea])
        db.session.commit()

        expires = timedelta(days=7)
        access_token = create_access_token(identity=geoarea.id, expires_delta=expires)
        self.headers = {'Authorization': f'Bearer {access_token}'}

        # Send a PUT request to the /pollution/pollutionDescription/<pollution_id> endpoint
        with self.test_app.test_client() as client:
            response = client.put('/pollution/pollutionDescription/' + pollution.id,
                                  json={'description': 'Updated Description'}, headers=self.headers)

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

        pollutionType1 = PollutionType(
            name='Typ 1'
        )
        db.session.add(pollutionType1)
        db.session.commit()

        pollution = Pollution(
            count=10,
            description='Description 1',
            geoarea_fk=5,
            pollution_type_fk=db.session.query(PollutionType).first().id
        )
        db.session.add_all([pollutionType1, pollution, geoarea])
        db.session.commit()

        expires = timedelta(days=7)
        access_token = create_access_token(identity=geoarea.id, expires_delta=expires)
        self.headers = {'Authorization': f'Bearer {access_token}'}

        with self.test_app.test_client() as client:
            response = client.put('/pollution/pollutionCount/' + pollution.id,
                                  json={'count': 15}, headers=self.headers)

            self.assertEqual(response.status_code, 200)

            updated_pollution = db.session.query(Pollution).get(pollution.id)
            self.assertEqual(updated_pollution.count, 15)

    def test_create_new_pollution(self):
        geoarea = GeoArea(
            id=6,
            name='Area 6',
            datecreated='2023-01-01 00:00:00',
            language='German',
            last_update='2023-08-25 00:00:00',
            mandant='Mandant A',
            admincomment='Comment 1',
            automaticsearch=True,
            polygon="POLYGON((1 2,2 3, 3 4, 5 6, 1 2))"
        )

        pollutionType = PollutionType(
            name='Typ 1'
        )
        db.session.add_all([geoarea, pollutionType])
        db.session.commit()

        expires = timedelta(days=7)
        access_token = create_access_token(identity=geoarea.id, expires_delta=expires)
        self.headers = {'Authorization': f'Bearer {access_token}'}

        # Send a POST request to create a new pollution record
        with self.test_app.test_client() as client:
            response = client.post('/pollution/newPollution', json={
                'description': 'Test Description',
                'count': 42,
                'geoarea_fk': 6,
                'pollution_type_fk': db.session.query(PollutionType).first().id
            }, headers=self.headers)

            self.assertEqual(response.status_code, 201)

            # Check if the pollution record is created in the database
            created_pollution = db.session.query(Pollution).first()
            self.assertIsNotNone(created_pollution)
            self.assertEqual(created_pollution.pollution_type_fk, db.session.query(PollutionType).first().id)
            self.assertEqual(created_pollution.description, 'Test Description')
            self.assertEqual(created_pollution.count, 42)
            self.assertEqual(created_pollution.geoarea_fk, 6)

    def test_delete_Pollution(self):
        # Insert a test pollution and a test geoarea
        geoarea = GeoArea(
            id=7,
            name='Area 7',
            datecreated='2023-01-01 00:00:00',
            language='German',
            last_update='2023-08-25 00:00:00',
            mandant='Mandant A',
            admincomment='Comment 1',
            automaticsearch=True,
            polygon="POLYGON((1 2,2 3, 3 4, 5 6, 1 2))"
        )

        pollutionType1 = PollutionType(
            name='Typ 1'
        )
        db.session.add(pollutionType1)
        db.session.commit()

        pollution = Pollution(
            count=10,
            description='Description 1',
            geoarea_fk=7,
            pollution_type_fk=db.session.query(PollutionType).first().id
        )
        db.session.add_all([pollution, geoarea])
        db.session.commit()

        expires = timedelta(days=7)
        access_token = create_access_token(identity=geoarea.id, expires_delta=expires)
        self.headers = {'Authorization': f'Bearer {access_token}'}

        # Send a DELETE request to the /deletePollution endpoint
        with self.test_app.test_client() as client:
            response = client.delete('/pollution/deletePollution/' + pollution.id,
                                     headers=self.headers)

            # Assert response status code
            self.assertEqual(response.status_code, 200)

    def test_login(self):
        # Insert a test user into the database
        test_user = User(email='test@example.com', password='password')
        db.session.add(test_user)
        db.session.commit()

        # Send a POST request to the /login endpoint
        with self.test_app.test_client() as client:
            response = client.post('/login', json={
                'email': 'test@example.com',
                'password': 'password'
            })

            # Assert response status code
            self.assertEqual(response.status_code, HTTPStatus.OK)

            # Assert that the response contains a token
            response_data = response.get_json()
            self.assertIn('token', response_data)

    def test_register(self):
        # Send a POST request to the /register endpoint to create a new user
        with self.test_app.test_client() as client:
            response = client.post('/register', json={
                'email': 'newuser@example.com',
                'password': 'newpassword'
            })

            # Assert response status code
            self.assertEqual(response.status_code, HTTPStatus.CREATED)

            # Assert that the response contains a token
            response_data = response.get_json()
            self.assertIn('token', response_data)

            # Assert that the user is created in the database
            new_user = User.query.filter_by(email='newuser@example.com').first()
            self.assertIsNotNone(new_user)


if __name__ == '__main__':
    unittest.main()
