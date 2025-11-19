from create_db_table import *
from const import *
import sys

def main():
    try:
        # 1) DB + user
        if not create_database(ASL_DB_NAME, ASL_DB_USER, ASL_DB_PASSWORD, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        # 2) Tables (drop + create)
        if not create_table(ASL_DB_NAME, USERS_TABLE_NAME, USERS_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        if not create_table(ASL_DB_NAME, MODELS_TABLE_NAME, MODELS_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        if not create_table(ASL_DB_NAME, SESSIONS_TABLE_NAME, SESSIONS_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        if not create_table(ASL_DB_NAME, GESTURES_TABLE_NAME, GESTURES_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        if not create_table(ASL_DB_NAME, PREDICTIONS_TABLE_NAME, PREDICTIONS_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        if not create_table(ASL_DB_NAME, CAPTIONS_TABLE_NAME, CAPTIONS_TABLE_SQL, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        # 3) Optional seed rows (like their sample inserts)
        if not update_table_with_test_data(ASL_DB_NAME, USERS_TABLE_NAME, USERS_TEST_DATA, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        if not update_table_with_test_data(ASL_DB_NAME, MODELS_TABLE_NAME, MODELS_TEST_DATA, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

        if not update_table_with_test_data(ASL_DB_NAME, GESTURES_TABLE_NAME, GESTURES_TEST_DATA, ROOT_USER, ROOT_PASSWORD):
            sys.exit(1)

    except Exception as e:
        print(f"Unexpected error: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
