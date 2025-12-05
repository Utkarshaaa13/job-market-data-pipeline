"""
Load CSV data into Snowflake
"""
import snowflake.connector
import pandas as pd
import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from config.connection_config import get_snowflake_config, validate_config


def load_data_to_snowflake(csv_path):
    """Load CSV data into Snowflake"""
    try:
        validate_config()
        config = get_snowflake_config()
        
        print(f"Loading data from: {csv_path}")
        
        # Read CSV
        df = pd.read_csv(csv_path, sep='\t')
        print(f"Loaded {len(df)} rows from CSV")
        
        # Connect to Snowflake
        conn = snowflake.connector.connect(
            account=config['account'],
            user=config['user'],
            password=config['password'],
            warehouse=config['warehouse'],
            database=config['database'],
            schema='RAW_DATA',
            role=config['role']
        )
        
        cursor = conn.cursor()
        
        # Clear existing data
        print("Clearing existing data...")
        cursor.execute("TRUNCATE TABLE JOB_LISTINGS_RAW")
        
        # Prepare data for insertion
        print("Inserting data...")
        
        # Convert DataFrame to list of tuples
        data_to_insert = []
        for _, row in df.iterrows():
            data_to_insert.append((
                str(row['job_title']) if pd.notna(row['job_title']) else None,
                str(row['company']) if pd.notna(row['company']) else None,
                str(row['location']) if pd.notna(row['location']) else None,
                str(row['job_type']) if pd.notna(row['job_type']) else None,
                str(row['category']) if pd.notna(row['category']) else None,
                float(row['salary_min']) if pd.notna(row['salary_min']) else None,
                float(row['salary_max']) if pd.notna(row['salary_max']) else None,
                float(row['experience_required']) if pd.notna(row['experience_required']) else None,
                str(row['publication_date']) if pd.notna(row['publication_date']) else None,
                str(row['skills']) if pd.notna(row['skills']) else None,
                os.path.basename(csv_path)
            ))
        
        # Insert data in batches
        batch_size = 1000
        for i in range(0, len(data_to_insert), batch_size):
            batch = data_to_insert[i:i+batch_size]
            cursor.executemany(
                """
                INSERT INTO JOB_LISTINGS_RAW 
                (job_title, company, location, job_type, category, 
                 salary_min, salary_max, experience_required, 
                 publication_date, skills, source_file)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """,
                batch
            )
            print(f"Inserted batch {i//batch_size + 1}/{(len(data_to_insert)-1)//batch_size + 1}")
        
        # Verify insertion
        cursor.execute("SELECT COUNT(*) FROM JOB_LISTINGS_RAW")
        count = cursor.fetchone()[0]
        print(f"\n✅ Successfully loaded {count} rows into Snowflake!")
        
        cursor.close()
        conn.close()
        
        return True
        
    except Exception as e:
        print(f"\n❌ Data load failed: {str(e)}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == "__main__":
    # Get CSV path from command line or use default
    if len(sys.argv) > 1:
        csv_path = sys.argv[1]
    else:
        base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base_dir, 'data', 'raw', 'job_listings.csv')
    
    success = load_data_to_snowflake(csv_path)
    sys.exit(0 if success else 1)
