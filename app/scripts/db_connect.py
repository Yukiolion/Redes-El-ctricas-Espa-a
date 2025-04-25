from dotenv import load_dotenv
import mysql.connector
import os

load_dotenv()

db_host = os.getenv("DATABASE_HOST")
db_user = os.getenv("DATABASE_USER")
db_psw = os.getenv("DATABASE_PASSWORD")
db_name = os.getenv("DATABASE_NAME")

def db_connect():
    # Conexión MySQL
    conn = mysql.connector.connect(
        host=db_host,
        user=db_user,
        password=db_psw,
        database=db_name
    )

    return conn