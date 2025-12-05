"""
Setup Snowflake database, schemas, and tables
"""
import snowflake.connector
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.connection_config import get_snowflake_config, validate_config


def execute_sql_file(cursor, filepath):
    """Execute SQL from a file"""
    with open(filepath, 'r') as f:
        sql_content = f.read()
    
    # Split by semicolon and execute each statement
    statements = [stmt.strip() for stmt in sql_content.split(';') if stmt.strip()]
    
    for stmt in statements:
        try:
            print(f"Executing: {stmt[:100]}...")
            cursor.execute(stmt)
            print("✅ Success")
        except Exception as e:
            print(f"❌ Error: {str(e)}")
            raise


def setup_snowflake():
    """Setup Snowflake environment"""
    try:
        validate_config()
        config = get_snowflake_config()
        
        print("Connecting to Snowflake...")
        conn = snowflake.connector.connect(
            account=config['account'],
            user=config['user'],
            password=config['password'],
            role=config['role']
        )
        
        cursor = conn.cursor()
        
        # Get base directory
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        sql_dir = os.path.join(base_dir, 'sql', 'ddl')
        
        # Execute DDL scripts
        print("\n📁 Creating schemas...")
        execute_sql_file(cursor, os.path.join(sql_dir, 'create_schemas.sql'))
        
        print("\n📊 Creating raw tables...")
        execute_sql_file(cursor, os.path.join(sql_dir, 'create_raw_tables.sql'))
        
        print("\n📈 Creating analytics tables...")
        execute_sql_file(cursor, os.path.join(sql_dir, 'create_analytics_tables.sql'))
        
        print("\n✅ Snowflake setup completed successfully!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Setup failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = setup_snowflake()
    sys.exit(0 if success else 1)
