import mysql.connector
from config import Config

conn = mysql.connector.connect(

    host=Config.MYSQL_HOST,

    user=Config.MYSQL_USER,

    password=Config.MYSQL_PASSWORD,

    database=Config.MYSQL_DATABASE

)

cursor = conn.cursor()

print("MySQL Connected Successfully")