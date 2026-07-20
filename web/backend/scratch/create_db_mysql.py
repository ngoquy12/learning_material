import pymysql

try:
    connection = pymysql.connect(
        host='localhost',
        user='root',
        password='22121944',
        port=3306
    )
    with connection.cursor() as cursor:
        cursor.execute("CREATE DATABASE IF NOT EXISTS elearning_agent_db")
    connection.commit()
    connection.close()
    print("Database elearning_agent_db created successfully")
except Exception as e:
    print(f"Failed to create database: {e}")
