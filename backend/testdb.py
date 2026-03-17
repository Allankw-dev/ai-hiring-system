from app.core.database import engine

try:
    connection = engine.connect()
    print("Database connection successful!")
    connection.close()
except Exception as e:
    print("Connection failed:")
    print(e)