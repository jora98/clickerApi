import unittest
from app import app, db
from model.geoarea import GeoArea
from model.pollution import Pollution
from config.database import TestConfig

class TestAPIEndpoints(unittest.TestCase):
    def setUp(self):
        # Use the test configuration
        app.config.from_object(TestConfig)
        print(app.config['SQLALCHEMY_DATABASE_URI'])
        self.app = app.test_client()
        self.app_context = app.app_context()
        self.app_context.push()
        
        # Create the tables using the application context
        with self.app_context:
            db.create_all()

        print(app.config['SQLALCHEMY_DATABASE_URI'])

    def tearDown(self):
        # Drop the tables using the application context
        with self.app_context:
            db.session.remove()
            db.drop_all()
        
        self.app_context.pop()

    def test_get_geoareas(self):
        # Insert test data into the database
        geoarea1 = GeoArea(
        id=1,
        name='Area 1',
        datecreated='2023-01-01 00:00:00',
        language='German',
        last_update='2023-08-25 00:00:00',
        mandant='Mandant A',
        admincomment='Comment 1',
        automaticsearch=True,
        polygon='polygon_data_1'
        )

        geoarea2 = GeoArea(
            id=2,
            name='Area 2',
            datecreated='2023-02-01 00:00:00',
            language='English',
            last_update='2023-08-26 00:00:00',
            mandant='Mandant B',
            admincomment='Comment 2',
            automaticsearch=False,
            polygon='polygon_data_2'
        )

        db.session.add_all([geoarea1, geoarea2])
        db.session.commit()

        # Send a GET request to the /geoarea endpoint
        with app.test_client() as client:
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
            self.assertEqual(response_data[0]['polygon'], 'polygon_data_1')

            # Assert the expected data for the second geoarea
            self.assertEqual(response_data[1]['id'], 2)
            self.assertEqual(response_data[1]['name'], 'Area 2')
            self.assertEqual(response_data[1]['datecreated'], '2023-02-01T00:00:00')
            self.assertEqual(response_data[1]['language'], 'English')
            self.assertEqual(response_data[1]['last_update'], '2023-08-26T00:00:00')
            self.assertEqual(response_data[1]['mandant'], 'Mandant B')
            self.assertEqual(response_data[1]['admincomment'], 'Comment 2')
            self.assertEqual(response_data[1]['automaticsearch'], False)
            self.assertEqual(response_data[1]['polygon'], 'polygon_data_2')
    
    def test_get_pollutions(self):
        # Insert test data into the database
        geoarea = GeoArea(
            id=1,
            name='Area 1',
            datecreated='2023-01-01 00:00:00',
            language='German',
            last_update='2023-08-25 00:00:00',
            mandant='Mandant A',
            admincomment='Comment 1',
            automaticsearch=True,
            polygon='polygon_data_1'
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
        db.session.add_all([geoarea, pollution1, pollution2])
        db.session.commit()

        # Send a GET request to the /pollution/byGeoarea_fk/<geoarea_fk> endpoint
        with app.test_client() as client:
            response = client.get('/pollution/byGeoarea_fk/1')

            # Assert response status code
            self.assertEqual(response.status_code, 200)

            # Parse JSON response data
            response_data = response.get_json()

            # Assert the expected number of pollutions in the response
            self.assertEqual(len(response_data), 2)

            # Assert the expected data for the first pollution
            self.assertEqual(response_data[0]['name'], 'Pollution 1')
            self.assertEqual(response_data[0]['count'], 10)
            self.assertEqual(response_data[0]['description'], 'Description 1')
            self.assertEqual(response_data[1]['name'], 'Pollution 2')
            self.assertEqual(response_data[1]['count'], 5)
            self.assertEqual(response_data[1]['description'], 'Description 2')

    def test_update_pollution_description(self):
        # Insert test data into the database
        geoarea = GeoArea(
            id=1,
            name='Area 1',
            datecreated='2023-01-01 00:00:00',
            language='German',
            last_update='2023-08-25 00:00:00',
            mandant='Mandant A',
            admincomment='Comment 1',
            automaticsearch=True,
            polygon='polygon_data_1'
            )

        pollution = Pollution(
            name='Pollution',
            count=10,
            description='Description',
            geoarea_fk=1
        )
        db.session.add_all([pollution, geoarea])
        db.session.commit()

        # Send a PUT request to the /pollution/pollutionDescription/<pollution_id> endpoint
        with app.test_client() as client:
            response = client.put('/pollution/pollutionDescription/' + pollution.id, json={'description': 'Updated Description'})

            # Assert response status code
            self.assertEqual(response.status_code, 200)

            # Check the updated description in the database
            updated_pollution = Pollution.query.get(pollution.id)
            self.assertEqual(updated_pollution.description, 'Updated Description')

if __name__ == '__main__':
    unittest.main()
