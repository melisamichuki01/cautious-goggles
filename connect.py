import psycopg2
import mysql.connector
import pymysql

# PostgreSQL connection (site2)
def connect_to_postgresql():
    try:
        conn = psycopg2.connect(
            user="root",
            password="root",
            host="192.168.16.128",  # PostgreSQL host
            port=5432,
            database="site2"
        )
        print("Connected to PostgreSQL (site2) successfully!")
        return conn
    except Exception as e:
        print(f"PostgreSQL connection failed: {e}")
        return None

# MySQL connection (site1)
def connect_to_mysql():
    try:
        conn = mysql.connector.connect(
            user="root",
            password="root",
            host="192.168.16.130",  # MySQL host
            port=3306,
            database="site1"
        )
        print("Connected to MySQL (site1) successfully!")
        return conn
    except Exception as e:
        print(f"MySQL connection failed: {e}")
        return None

# MariaDB connection (site3)
def connect_to_mariadb():
    try:
        conn = pymysql.connect(
            user="root",
            password="root",
            host="192.168.100.27",
            database="site3"
        )
        print("Connected to MariaDB (site3) successfully!")
        return conn
    except Exception as e:
        print(f"MariaDB connection failed: {e}")
        return None

# Test all connections
postgres_conn = connect_to_postgresql()
if postgres_conn:
    postgres_conn.close()

mysql_conn = connect_to_mysql()
if mysql_conn:
    mysql_conn.close()

mariadb_conn = connect_to_mariadb()
if mariadb_conn:
    mariadb_conn.close()
