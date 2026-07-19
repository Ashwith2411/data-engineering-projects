import psycopg2

# Try with admin123
try:
    conn = psycopg2.connect(
        host="localhost",
        port=5432,  # Default port
        database="postgres",  # Default database
        user="postgres",
        password="root"
    )
    print("✅ Password 'admin123' works!")
    conn.close()
except Exception as e:
    print(f"❌ Password 'admin123' failed: {e}")
    
    # Try with 'postgres'
    try:
        conn = psycopg2.connect(
            host="localhost",
            port=5432,
            database="postgres",
            user="postgres",
            password="postgres"
        )
        print("✅ Password 'postgres' works!")
        conn.close()
    except Exception as e2:
        print(f"❌ Password 'postgres' failed: {e2}")
        
        # Try with 'admin'
        try:
            conn = psycopg2.connect(
                host="localhost",
                port=5432,
                database="postgres",
                user="postgres",
                password="admin123"
            )
            print("✅ Password 'admin' works!")
            conn.close()
        except Exception as e3:
            print(f"❌ All attempts failed!")
            print("Please check your password in pgAdmin")