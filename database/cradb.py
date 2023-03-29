import mysql.connector

def init_db(connection):
    db_name = 'cra'

    tables = {}
    tables['users'] = '''
        CREATE TABLE `users` (
            `username` VARCHAR(255) NOT NULL,
            `email` VARCHAR(255) NOT NULL,
            `password_hash` VARCHAR(255) NOT NULL,
            PRIMARY KEY (`username`)
        )
    '''
    tables['alerts'] = '''
        CREATE TABLE `alerts` (
            `username` VARCHAR(255) NOT NULL,
            `numerator` VARCHAR(8) NOT NULL,
            `denominator` VARCHAR(8) NOT NULL,
            `threshold` DECIMAL(12,6) NOT NULL,
            `last` DECIMAL(12,6),
            PRIMARY KEY (`username`, `numerator`, `denominator`, `threshold`)
        )
    '''

    def create_database(cursor):
        try:
            cursor.execute(
                "CREATE DATABASE {} DEFAULT CHARACTER SET 'utf8'".format(db_name))
        except mysql.connector.Error as err:
            print("Failed creating database: {}".format(err))
            exit(1)

    cursor = connection.cursor()

    try:
        cursor.execute("USE {}".format(db_name))
    except mysql.connector.Error as err:
        print("Database {} does not exists.".format(db_name))
        if err.errno == mysql.connector.errorcode.ER_BAD_DB_ERROR:
            create_database(cursor)
            print("Database {} created successfully.".format(db_name))
            connection.database = db_name
        else:
            print(err)
            exit(1)

    for table_name in tables:
        table_description = tables[table_name]
        try:
            print("Creating table {}: ".format(table_name), end='')
            cursor.execute(table_description)
        except mysql.connector.Error as err:
            if err.errno == mysql.connector.errorcode.ER_TABLE_EXISTS_ERROR:
                print("already exists.")
            else:
                print(err.msg)
        else:
            print("OK")

    cursor.close()