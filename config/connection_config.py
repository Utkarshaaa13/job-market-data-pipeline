"""
Snowflake connection configuration
"""
import os
from dotenv import load_dotenv

load_dotenv()

SNOWFLAKE_CONFIG = {
    'account': os.getenv('SNOWFLAKE_ACCOUNT'),
    'user': os.getenv('SNOWFLAKE_USER'),
    'password': os.getenv('SNOWFLAKE_PASSWORD'),
    'warehouse': os.getenv('SNOWFLAKE_WAREHOUSE', 'COMPUTE_WH'),
    'database': os.getenv('SNOWFLAKE_DATABASE', 'JOB_ANALYTICS'),
    'schema': os.getenv('SNOWFLAKE_SCHEMA', 'RAW_DATA'),
    'role': os.getenv('SNOWFLAKE_ROLE', 'ACCOUNTADMIN')
}

def get_snowflake_config():
    """Return Snowflake configuration dictionary"""
    return SNOWFLAKE_CONFIG

def validate_config():
    """Validate that all required configuration is present"""
    required_fields = ['account', 'user', 'password']
    missing = [field for field in required_fields if not SNOWFLAKE_CONFIG.get(field)]
    
    if missing:
        raise ValueError(f"Missing required Snowflake configuration: {', '.join(missing)}")
    
    return True
