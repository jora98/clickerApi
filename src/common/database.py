import psycopg2

def initialize():
    dbname = "clicker"
    user = "postgres"
    password = "!C0mplex"
    host = "localhost"
    port = "5432"

    try:
        # Connect to the existing database
        connection = psycopg2.connect(
            dbname=dbname,
            user=user,
            password=password,
            host=host,
            port=port
        )

        print("Connected to the PostgreSQL database successfully.")

        # You can perform database operations here, for example:
        # cursor = connection.cursor()
        # cursor.execute("SELECT * FROM your_table_name;")
        # rows = cursor.fetchall()
        # print(rows)

    except psycopg2.Error as e:
        print(f"Error connecting to the database: {e}")

    finally:
        # Close the connection
        if connection:
            connection.close()
