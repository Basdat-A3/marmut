import psycopg2
from psycopg2 import Error
from django.conf import settings

try:
    # Connect ke db
    connection = psycopg2.connect(
        dbname='postgres',
        user='postgres.yuwisqswkwkvtnjpwavj',
        password='dbmarmut123',
        host='aws-0-ap-southeast-1.pooler.supabase.com',
        port='5432'
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