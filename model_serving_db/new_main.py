# create_db_table.py — Cloud SQL version

import mysql.connector
from mysql.connector import Error as MySQLError
from typing import Optional
from const import CLOUD_SQL_HOST, CLOUD_SQL_PORT, ROOT_USER, ROOT_PASSWORD


def execute_sql_command(
    command: str,
    db_name: Optional[str] = None,
    root_user: str = ROOT_USER,
    root_password: Optional[str] = ROOT_PASSWORD,
):
    """
    Execute one or more SQL statements against Cloud SQL (MySQL)
    using mysql-connector-python.

    This replaces the old 'sudo mysql -e "<SQL>"' approach.
    """
    conn = None
    try:
        conn = mysql.connector.connect(
            host=CLOUD_SQL_HOST,
            port=CLOUD_SQL_PORT,
            user=root_user,
            password=root_password,
            database=db_name if db_name else None,
        )

        cursor = conn.cursor()
        # Allow multi-statement commands (e.g., CREATE DB; CREATE USER; GRANT ...)
        for result in cursor.execute(command, multi=True):
            # You *can* inspect result if needed, but we just iterate to execute all parts
            pass

        conn.commit()
        cursor.close()
        return True, "OK", None
    except MySQLError as e:
        return False, None, str(e)
    finally:
        if conn is not None and conn.is_connected():
            conn.close()


def create_database(
    db_name: str,
    db_user: str,
    db_password: str,
    root_user: str = ROOT_USER,
    root_password: Optional[str] = ROOT_PASSWORD,
):
    """
    Create database and user with privileges (Cloud SQL).
    Root user must exist on Cloud SQL with given password.
    """

    sql_commands = f"""
    CREATE DATABASE IF NOT EXISTS {db_name};
    CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_password}';
    GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'%';
    FLUSH PRIVILEGES;
    """

    success, output, error = execute_sql_command(
        sql_commands,
        None,
        root_user,
        root_password,
    )

    if success:
        print(f"Database '{db_name}' and user '{db_user}' created successfully!")
        return True
    else:
        print(f"Error creating database and user: {error}")
        return False


def create_table(
    db_name: str,
    table_name: str,
    table_sql: str,
    root_user: str = ROOT_USER,
    root_password: Optional[str] = ROOT_PASSWORD,
):
    """
    Drop + create table from provided SQL, now on Cloud SQL.
    """
    # DROP TABLE IF EXISTS
    drop_success, _, drop_error = execute_sql_command(
        f"DROP TABLE IF EXISTS {table_name};",
        db_name,
        root_user,
        root_password,
    )

    if not drop_success:
        print(f"Could not drop table {table_name}: {drop_error}")

    # CREATE TABLE ...
    success, _, error = execute_sql_command(
        table_sql,
        db_name,
        root_user,
        root_password,
    )

    if success:
        print(f"Table '{table_name}' created successfully!")
        return True
    else:
        print(f"Error creating table '{table_name}': {error}")
        return False


def update_table_with_test_data(
    db_name: str,
    table_name: str,
    test_data_sql: str,
    root_user: str = ROOT_USER,
    root_password: Optional[str] = ROOT_PASSWORD,
):
    """
    Insert test data into a table and print row count (on Cloud SQL).
    """
    success, _, error = execute_sql_command(
        test_data_sql,
        db_name,
        root_user,
        root_password,
    )

    if success:
        count_sql = f"SELECT COUNT(*) AS record_count FROM {table_name};"
        count_success, count_output, count_error = execute_sql_command(
            count_sql,
            db_name,
            root_user,
            root_password,
        )

        if count_success:
            print(f"Test data inserted successfully into '{table_name}'!")
            print(f"Records in {table_name}: {count_output}")
        else:
            print(f"Test data inserted, but could not count records: {count_error}")

        return True
    else:
        print(f"Error inserting test data into '{table_name}': {error}")
        return False


def cleanup_table(
    db_name: str,
    table_name: str,
    root_user: str = ROOT_USER,
    root_password: Optional[str] = ROOT_PASSWORD,
):
    """
    TRUNCATE a table (Cloud SQL).
    """
    success, _, error = execute_sql_command(
        f"TRUNCATE TABLE {table_name};",
        db_name,
        root_user,
        root_password,
    )

    if success:
        print(f"Table '{table_name}' cleaned up successfully!")
        return True
    else:
        print(f"Error cleaning up table '{table_name}': {error}")
        return False
