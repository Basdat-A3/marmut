import psycopg2
from psycopg2 import Error
from django.conf import settings


def get_database_cursor():
    try:
        # Connect to the database
        connection = psycopg2.connect(
            user=settings.DATABASES['default']['USER'],
            password=settings.DATABASES['default']['PASSWORD'],
            host=settings.DATABASES['default']['HOST'],
            port=settings.DATABASES['default']['PORT'],
            database=settings.DATABASES['default']['NAME']
        )

        # Create a cursor for database operations
        cursor = connection.cursor()

        # Print detail postgre 
        print("PostgreSQL server information")
        print(connection.get_dsn_parameters(), "\n")

        # Set the search path to the desired schema (e.g., 'marmut')
        cursor.execute("SET search_path TO marmut")

        return connection, cursor

    except (Exception, Error) as error:
        print("Error while connecting to PostgreSQL:", error)

try:
    # Connect ke db
    connection = psycopg2.connect(
        user = settings.DATABASES['default']['USER'],
        password = settings.DATABASES['default']['PASSWORD'],
        host = settings.DATABASES['default']['HOST'],
        port = settings.DATABASES['default']['PORT'],
        database = settings.DATABASES['default']['NAME'],
        # connection pooling
        # https://docs.djangoproject.com/en/3.0/ref/databases/#persistent-connections
        # https://docs.djangoproject.com/en/3.0/ref/databases/#connection-pooling
        # https://docs.djangoproject.com/en/3.0/ref/settings/#conn-max-age
    )

    # Buat cursor buat operasiin db
    cursor = connection.cursor()

    # Print detail postgre 
    print("PostgreSQL server information")
    print(connection.get_dsn_parameters(), "\n")

    # Coba query
    cursor.execute("SELECT version();")

    # Fetch result
    record = cursor.fetchall()
    print("You are connected to - ", record, "\n")

    # Masuk ke schema marmut
    cursor.execute("SET search_path TO marmut")
  
except (Exception, Error) as error:
    print("Error while connecting to PostgreSQL", error)