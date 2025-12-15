from new_create_db_table import *
from const import *
import sys

def main():
    try:
        # 1) DB + user
        # if not create_database(ASL_DB_NAME, ASL_DB_USER, ASL_DB_PASSWORD, ROOT_USER, ROOT_PASSWORD):
        #     sys.exit(1)

        # 2) Table (drop + create)
        if not create_table(ASL_DB_NAME, VIDEO_GLOSS_REQUESTS_TABLE, VIDEO_GLOSS_REQUESTS_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        # 3) Optional seed rows
        # if not update_table_with_test_data(ASL_DB_NAME, VIDEO_GLOSS_REQUESTS_TABLE, VIDEO_GLOSS_TEST_DATA, ROOT_USER, ROOT_PASSWORD):
        #     sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
