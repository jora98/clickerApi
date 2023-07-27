import psycopg2

class Database(object):
    URI = "localhost"
    connection = None

    @staticmethod
    def initialize(dbname):
        user = "postgres"
        password = "!C0mplex"
        host = Database.URI
        port = "5432"

        try:
            Database.connection = psycopg2.connect(
                dbname=dbname,
                user=user,
                password=password,
                host=host,
                port=port
            )

            print("Connected to the PostgreSQL database successfully.")

        except psycopg2.Error as e:
            print(f"Error connecting to the database: {e}")
            return None

    @staticmethod
    def find_one(connection, table_name, query):
        try:
            cursor = connection.cursor()
            sql_query = f"SELECT * FROM {table_name} WHERE {query};"
            cursor.execute(sql_query)
            rows = cursor.fetchall()

            # Print or process the results
            for row in rows:
                print(row)

        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

        finally:
            if cursor:
                cursor.close()

    @staticmethod
    def insert(connection, table_name, data):
        try:
            cursor = connection.cursor()
            columns = ', '.join(data.keys())
            values = ', '.join([f"'{value}'" for value in data.values()])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({values});"
            cursor.execute(query)
            connection.commit()

            print("Data inserted successfully.")

        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")

        finally:
            if cursor:
                cursor.close()

