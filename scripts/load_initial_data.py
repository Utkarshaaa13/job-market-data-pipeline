"""
CSV to Snowflake Data Loader

This script extracts job listing data from a CSV file and loads it into 
Snowflake's RAW_DATA layer. It serves as the initial ingestion step in 
our ELT pipeline.

Key Technologies:
- Pandas: For reading and parsing CSV files
- Snowflake Connector: For database operations
- Python sys/os: For file path handling

Purpose:
- Read 1,000 job listings from CSV
- Validate and clean data
- Load into Snowflake RAW_DATA.JOB_LISTINGS_RAW table
- Support idempotent operations (can be run multiple times safely)

Author: Utkarsha Chandgadkar
Date: December 2025
"""

# Standard library imports for system operations
import sys  # For command-line arguments and exit codes
import os   # For file path operations

# Third-party imports for data handling and database connection
import snowflake.connector  # Snowflake's official Python connector
import pandas as pd  # For reading CSV and data manipulation

# Add parent directory to Python path so we can import our config module
# This allows us to import from config/ directory when running script from any location
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Import our custom configuration functions
# These handle Snowflake credentials and connection validation
from config.connection_config import get_snowflake_config, validate_config


def load_data_to_snowflake(csv_path):
    """
    Main function to load CSV data into Snowflake RAW layer
    
    This function performs the complete ETL extract and load process:
    1. Validates Snowflake configuration
    2. Reads CSV file using pandas
    3. Establishes connection to Snowflake
    4. Truncates existing table (for idempotency)
    5. Inserts data in batches
    6. Verifies successful load
    
    Args:
        csv_path (str): Full file path to the CSV file containing job listings
                       Expected format: tab-separated values with headers
    
    Returns:
        bool: True if data loaded successfully, False if any error occurred
    
    Design Decisions:
        - Using TRUNCATE instead of DELETE for faster table clearing
        - Batch size of 1000 balances memory usage and performance
        - Explicit NULL handling prevents Snowflake type errors
        - executemany() for efficient bulk inserts
    """
    try:
        # ================================================================
        # STEP 1: VALIDATE CONFIGURATION
        # ================================================================
        # Check that all required Snowflake credentials are present in .env file
        # This fails fast if configuration is incomplete, rather than during connection
        validate_config()
        
        # Load Snowflake credentials from environment variables
        # Returns a dictionary with account, user, password, warehouse, database, role
        config = get_snowflake_config()
        
        # Log the file path we're attempting to load
        # Helpful for debugging if file path is incorrect
        print(f"Loading data from: {csv_path}")
        
        # ================================================================
        # STEP 2: READ CSV FILE
        # ================================================================
        # Use pandas to read CSV file
        # sep='\t' because our data is tab-separated, not comma-separated
        # pandas automatically detects column names from first row
        df = pd.read_csv(csv_path, sep='\t')
        
        # Log row count for verification
        # This helps us validate we're reading the expected amount of data
        print(f"Loaded {len(df)} rows from CSV")
        
        # ================================================================
        # STEP 3: ESTABLISH SNOWFLAKE CONNECTION
        # ================================================================
        # Create connection object using credentials from config
        # We're specifically targeting the RAW_DATA schema for raw, untransformed data
        conn = snowflake.connector.connect(
            account=config['account'],      # Snowflake account identifier (e.g., xy12345.us-east-1)
            user=config['user'],            # Username for authentication
            password=config['password'],    # Password (stored securely in .env)
            warehouse=config['warehouse'],  # Virtual warehouse for compute resources
            database=config['database'],    # Database name (JOB_ANALYTICS)
            schema='RAW_DATA',             # Schema for raw, unprocessed data
            role=config['role']            # Role defines permissions and access level
        )
        
        # Create cursor object for executing SQL statements
        # Cursor allows us to run queries and fetch results
        cursor = conn.cursor()
        
        # ================================================================
        # STEP 4: TRUNCATE EXISTING TABLE
        # ================================================================
        # Clear all existing data from the target table
        # Using TRUNCATE instead of DELETE because:
        # 1. TRUNCATE is much faster (no row-by-row deletion)
        # 2. TRUNCATE doesn't generate undo logs
        # 3. Makes the pipeline idempotent (can run multiple times safely)
        print("Clearing existing data...")
        cursor.execute("TRUNCATE TABLE JOB_LISTINGS_RAW")
        
        # ================================================================
        # STEP 5: PREPARE DATA FOR INSERTION
        # ================================================================
        print("Inserting data...")
        
        # Initialize empty list to store tuples of row data
        # Each tuple represents one row to be inserted
        data_to_insert = []
        
        # Iterate through each row in the DataFrame
        # _ is used because we don't need the index, only the row data
        for _, row in df.iterrows():
            # Create a tuple for this row with proper NULL handling
            # We check pd.notna() for each field to handle missing values correctly
            # If value exists, cast to appropriate type; if missing, insert None (NULL in SQL)
            data_to_insert.append((
                # Job Title - cast to string, handle NaN
                # Using str() ensures consistent data type even if pandas infers differently
                str(row['job_title']) if pd.notna(row['job_title']) else None,
                
                # Company name - cast to string, handle NaN
                str(row['company']) if pd.notna(row['company']) else None,
                
                # Location string (e.g., "Austin, TX") - cast to string, handle NaN
                str(row['location']) if pd.notna(row['location']) else None,
                
                # Job type (e.g., "Full-time", "Remote") - cast to string, handle NaN
                str(row['job_type']) if pd.notna(row['job_type']) else None,
                
                # Category (e.g., "Engineering", "Data Science") - cast to string, handle NaN
                str(row['category']) if pd.notna(row['category']) else None,
                
                # Minimum salary - cast to float for numeric operations, handle NaN
                # Float allows decimal values and proper numeric sorting in Snowflake
                float(row['salary_min']) if pd.notna(row['salary_min']) else None,
                
                # Maximum salary - cast to float, handle NaN
                float(row['salary_max']) if pd.notna(row['salary_max']) else None,
                
                # Years of experience required - cast to float, handle NaN
                # Float because experience can be 2.5 years, etc.
                float(row['experience_required']) if pd.notna(row['experience_required']) else None,
                
                # Publication date string - cast to string, handle NaN
                # Could be converted to DATE type in transformation layer
                str(row['publication_date']) if pd.notna(row['publication_date']) else None,
                
                # Comma-separated skills string (e.g., "Python, SQL, AWS") - cast to string, handle NaN
                str(row['skills']) if pd.notna(row['skills']) else None,
                
                # Source file name for data lineage tracking
                # basename() extracts just filename, not full path
                # Useful for debugging and understanding where data came from
                os.path.basename(csv_path)
            ))
        
        # ================================================================
        # STEP 6: INSERT DATA IN BATCHES
        # ================================================================
        # Define batch size for bulk inserts
        # 1000 rows per batch balances:
        # - Memory usage (don't load all data at once)
        # - Network efficiency (fewer round trips to Snowflake)
        # - Transaction size (not too large to cause timeouts)
        batch_size = 1000
        
        # Loop through data in chunks of batch_size
        # range(start, stop, step) creates batch boundaries
        for i in range(0, len(data_to_insert), batch_size):
            # Slice the list to get current batch
            # Python list slicing: [start:end] where end is exclusive
            batch = data_to_insert[i:i+batch_size]
            
            # Execute INSERT statement for entire batch at once
            # executemany() is much faster than executing individual INSERTs
            # It sends all rows in one network call to Snowflake
            cursor.executemany(
                """
                INSERT INTO JOB_LISTINGS_RAW 
                (job_title, company, location, job_type, category, 
                 salary_min, salary_max, experience_required, 
                 publication_date, skills, source_file)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                batch  # List of tuples, each tuple is one row
            )
            
            # Print progress to monitor long-running loads
            # Shows which batch we're on and total batches
            # Example output: "Inserted batch 3/10"
            print(f"Inserted batch {i//batch_size + 1}/{(len(data_to_insert)-1)//batch_size + 1}")
        
        # ================================================================
        # STEP 7: VERIFY SUCCESSFUL LOAD
        # ================================================================
        # Query the table to count how many rows were actually inserted
        # This validates that our insert operations succeeded
        cursor.execute("SELECT COUNT(*) FROM JOB_LISTINGS_RAW")
        
        # fetchone() returns a tuple with one element (the count)
        # [0] extracts the actual count value from the tuple
        count = cursor.fetchone()[0]
        
        # Print success message with final row count
        # This gives us confidence the load completed successfully
        print(f"\n✅ Successfully loaded {count} rows into Snowflake!")
        
        # ================================================================
        # STEP 8: CLEANUP RESOURCES
        # ================================================================
        # Close cursor to free up resources
        cursor.close()
        
        # Close connection to Snowflake
        # Important to prevent connection leaks
        conn.close()
        
        # Return True to indicate successful execution
        return True
        
    except Exception as e:
        # ================================================================
        # ERROR HANDLING
        # ================================================================
        # If any error occurs during the process, catch it here
        # This prevents the script from crashing ungracefully
        
        # Print error message to console
        print(f"\n❌ Data load failed: {str(e)}")
        
        # Import traceback module for detailed error information
        import traceback
        
        # Print full stack trace to help debug the issue
        # Shows exactly which line caused the error
        traceback.print_exc()
        
        # Return False to indicate failure
        return False


# ====================================================================
# MAIN EXECUTION BLOCK
# ====================================================================
# This code only runs when script is executed directly (not imported)
# Allows this script to be used both as standalone and as importable module
if __name__ == "__main__":
    """
    Entry point when script is run from command line
    
    Usage:
        python load_initial_data.py                    # Uses default CSV path
        python load_initial_data.py /path/to/file.csv  # Uses custom CSV path
    
    Exit Codes:
        0 - Success (data loaded successfully)
        1 - Failure (error occurred during load)
    """
    
    # Check if user provided CSV path as command line argument
    # sys.argv is a list: [script_name, arg1, arg2, ...]
    # len > 1 means at least one argument was provided
    if len(sys.argv) > 1:
        # Use the first argument as CSV path
        # sys.argv[0] is script name, sys.argv[1] is first argument
        csv_path = sys.argv[1]
    else:
        # No argument provided, so construct default path
        
        # Get directory containing this script file
        # __file__ is the current script's path
        # abspath() converts to absolute path
        # dirname() twice goes up two levels: script_dir -> scripts_dir -> project_root
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        
        # Construct path to default CSV location
        # os.path.join() safely combines path components (handles OS-specific separators)
        # Expected structure: project_root/data/raw/job_listings.csv
        csv_path = os.path.join(base_dir, 'data', 'raw', 'job_listings.csv')
    
    # Execute the main load function
    # Returns True if successful, False if failed
    success = load_data_to_snowflake(csv_path)
    
    # Exit with appropriate status code
    # 0 = success (standard Unix convention)
    # 1 = failure (non-zero indicates error)
    # This allows other scripts/tools to check if load succeeded
    sys.exit(0 if success else 1)
