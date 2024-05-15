import psycopg2
from psycopg2 import Error
from django.conf import settings

try:
    # Connect ke db
    connection = psycopg2.connect(
        user = settings.DATABASES['default']['USER'],
        password = settings.DATABASES['default']['PASSWORD'],
        host = settings.DATABASES['default']['HOST'],
        port = settings.DATABASES['default']['PORT'],
        database = settings.DATABASES['default']['NAME'],
        # make sure to set the statement_timeout to the same value as CONN_MAX_AGE
        # options=f"-c statement_timeout={settings.CONN_MAX_AGE}"
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