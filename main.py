from create_db_table import *
from const import *
import sys

def main():    
    try:
        if not create_database(SENTIMENT_DB_NAME, SENTIMENT_DB_USER, SENTIMENT_DB_PASSWORD, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)
        
        if not create_table(SENTIMENT_DB_NAME, REQUESTS_TABLE_NAME, REQUESTS_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)
        
        if not create_table(SENTIMENT_DB_NAME, SENTIMENTS_TABLE_NAME, SENTIMENTS_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)
        
        
        if not update_table_with_test_data(SENTIMENT_DB_NAME, REQUESTS_TABLE_NAME, REQUESTS_TEST_DATA, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)
        
        if not update_table_with_test_data(SENTIMENT_DB_NAME, SENTIMENTS_TABLE_NAME, SENTIMENTS_TEST_DATA, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)
        
    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()