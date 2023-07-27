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
    def find(connection, table_name, query):
        try:
            cursor = connection.cursor()
            sql_query = f"SELECT * FROM {table_name} WHERE {query};"
            cursor.execute(sql_query)
            return cursor.fetchall()

        except psycopg2.Error as e:
            print(f"Error executing query: {e}")

        finally:
            if cursor:
                cursor.close()


    def find_by_email(connection, table_name, email):
        try:
            cursor = connection.cursor()
            sql_query = f"SELECT * FROM {table_name} WHERE email LIKE %s;"
            cursor.execute(sql_query, (f"%{email}%",))
            return cursor.fetchall()

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
            placeholders = ', '.join(['%s' for _ in data.values()])
            query = f"INSERT INTO {table_name} ({columns}) VALUES ({placeholders});"

            # Extract the values as a tuple to prevent SQL injection
            values = tuple(data.values())

            # Execute the query with the values as parameters
            cursor.execute(query, values)

            # Commit the changes
            connection.commit()

            print("Data inserted successfully.")

        except psycopg2.Error as e:
            print(f"Error inserting data: {e}")

        finally:
            if cursor:
                cursor.close()

