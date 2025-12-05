"""
Test Snowflake connection
"""
import snowflake.connector
import sys
import os

# Add parent directory to path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.connection_config import get_snowflake_config, validate_config


def test_connection():
    """Test connection to Snowflake"""
    try:
        # Validate config
        validate_config()
        config = get_snowflake_config()
        
        print("Testing Snowflake connection...")
        print(f"Account: {config['account']}")
        print(f"User: {config['user']}")
        print(f"Database: {config['database']}")
        
        # Create connection
        conn = snowflake.connector.connect(
            account=config['account'],
            user=config['user'],
            password=config['password'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema=config['schema'],
            role=config['role']
        )
        
        # Test query
        cursor = conn.cursor()
        cursor.execute("SELECT CURRENT_VERSION()")
        version = cursor.fetchone()[0]
        
        print(f"\n✅ Connection successful!")
        print(f"Snowflake version: {version}")
        
        # Test warehouse
        cursor.execute("SELECT CURRENT_WAREHOUSE()")
        warehouse = cursor.fetchone()[0]
        print(f"Current warehouse: {warehouse}")
        
        # Test database
        cursor.execute("SELECT CURRENT_DATABASE()")
        database = cursor.fetchone()[0]
        print(f"Current database: {database}")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Connection failed: {str(e)}")
        return False


if __name__ == "__main__":
    success = test_connection()
    sys.exit(0 if success else 1)
