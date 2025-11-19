import subprocess

def execute_sql_command(command, db_name=None, root_user="root", root_password=None):
    """
    Execute MySQL commands through the Linux command line (like your teammates).
    Uses: sudo mysql -u root [-p***] [-D db] -e "<SQL>"
    """
    mysql_cmd = ['sudo', 'mysql', '-u', root_user]

    if root_password:
        mysql_cmd.extend(['-p' + root_password])

    if db_name:
        mysql_cmd.extend(['-D', db_name])

    mysql_cmd.extend(['-e', command])

    try:
        result = subprocess.run(
            mysql_cmd,
            capture_output=True,
            text=True,
            check=True
        )
        return True, result.stdout, None
    except subprocess.CalledProcessError as e:
        return False, None, e.stderr


def create_database(db_name, db_user, db_password, root_user="root", root_password=None):
    """
    Create database and user with privileges. Same flow as your teammates.
    """
    sql_commands = f"""
    CREATE DATABASE IF NOT EXISTS {db_name};
    CREATE USER IF NOT EXISTS '{db_user}'@'%' IDENTIFIED BY '{db_password}';
    GRANT ALL PRIVILEGES ON {db_name}.* TO '{db_user}'@'%';
    FLUSH PRIVILEGES;
    SHOW DATABASES LIKE '{db_name}';
    SELECT user, host FROM mysql.user WHERE user = '{db_user}';
    """

    success, output, error = execute_sql_command(
        sql_commands,
        None, root_user, root_password
    )

    if success:
        print(f"Database '{db_name}' and user '{db_user}' created successfully!")
        if output:
            print(output)
        return True
    else:
        print(f"Error creating database and user: {error}")
        return False


def create_table(db_name, table_name, table_sql, root_user="root", root_password=None):
    """
    Drop + create table from provided SQL. Same pattern as teammates.
    """
    drop_success, _, drop_error = execute_sql_command(
        f"DROP TABLE IF EXISTS {table_name};",
        db_name, root_user, root_password
    )

    if not drop_success:
        print(f"Could not drop table {table_name}: {drop_error}")

    success, _, error = execute_sql_command(table_sql, db_name, root_user, root_password)

    if success:
        print(f"Table '{table_name}' created successfully!")
        return True
    else:
        print(f"Error creating table '{table_name}': {error}")
        return False


def update_table_with_test_data(db_name, table_name, test_data_sql, root_user="root", root_password=None):
    """
    Insert test data into a table and print a row count (same vibe as their example).
    """
    success, _, error = execute_sql_command(test_data_sql, db_name, root_user, root_password)

    if success:
        count_success, count_output, count_error = execute_sql_command(
            f"SELECT COUNT(*) as record_count FROM {table_name};",
            db_name, root_user, root_password
        )

        if count_success:
            print(f"Test data inserted successfully into '{table_name}'!")
            print(f"Records in {table_name}: {count_output.strip()}")
        else:
            print(f"Test data inserted, but could not count records: {count_error}")

        return True
    else:
        print(f"Error inserting test data into '{table_name}': {error}")
        return False


def cleanup_table(db_name, table_name, root_user="root", root_password=None):
    """
    Truncate a table.
    """
    success, _, error = execute_sql_command(
        f"TRUNCATE TABLE {table_name};",
        db_name, root_user, root_password
    )

    if success:
        print(f"Table '{table_name}' cleaned up successfully!")
        return True
    else:
        print(f"Error cleaning up table '{table_name}': {error}")
        return False
