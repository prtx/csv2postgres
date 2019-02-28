import os
import csv
import psycopg2
import argparse
import settings


def create_connection(database="postgres"):
    connection = psycopg2.connect(
        user=settings.DB_USER,
        password=settings.DB_PASSWORD,
        host=settings.DB_HOST,
        port=settings.DB_PORT,
        database=database,
    )
    connection.autocommit = True
    return connection


def create_db_if_not_exists(database):
    connection = create_connection()
    cursor = connection.cursor()
    cursor.execute(
        "SELECT COUNT(*) = 0 FROM pg_catalog.pg_database WHERE datname = '{}'".format(
            database
        )
    )
    not_exists_row = cursor.fetchone()
    not_exists = not_exists_row[0]
    if not_exists:
        cursor.execute("CREATE DATABASE {}".format(database))


TYPE_DICT = {"str": "varchar", "int": "bigint", "float": "float"}


def csv_to_table(file_path, delimiter, skip_line=0, insert_till=-1):
    with open(file_path) as csv_file:
        # skip line till header
        for _ in range(skip_line):
            next(csv_file)

        # read file and header
        reader = csv.reader(csv_file, delimiter=delimiter)
        headers = [x.split("|") for x in next(reader)]

        # create table
        columns = ["{} {}".format(x[0], TYPE_DICT[x[1]]) for x in headers]
        table_name = os.path.splitext(file_path)[0].split("/")[-1]
        cursor.execute(
            "CREATE TABLE {} (id serial PRIMARY KEY, {});".format(
                table_name, ", ".join(columns)
            )
        )

        # insert data rows
        for i, row in enumerate(reader):
            if i == insert_till:
                break
            cursor.execute(
                """INSERT INTO {} ({}) VALUES ('{}')""".format(
                    table_name,
                    ", ".join([x[0] for x in headers]),
                    "', '".join([x.replace("'", "''") for x in row]),
                )
            )


def parse_args(args=None):
    """
    Function to parse command line arguments
    
    :param args: parser arguments
    :type args: list
    :return: command line argument information
    :rtype: argparse.Namespace
    """
    parser = argparse.ArgumentParser(description="CSV to postgres table.")
    parser.add_argument("csv", type=str, help="CSV file path")
    parser.add_argument("-d", "--delimiter", type=str, help="Delimiter")
    parser.add_argument("-sl", "--skip-line", type=int, help="Skip line till header")
    parser.add_argument("-it", "--insert-till", type=int, help="Insert till line number")

    # if arguments passed as parameters then parse them else not
    if args:
        return parser.parse_args(args)
    return parser.parse_args()


if __name__ == "__main__":
    create_db_if_not_exists(settings.DB_NAME)

    connection = create_connection(settings.DB_NAME)
    cursor = connection.cursor()

    args = parse_args()
    kwargs = {k: v for k, v in vars(args).items() if v}
    csv_file = kwargs.pop("csv")
    delimiter = kwargs.pop("delimiter")

    csv_to_table(csv_file, delimiter, **kwargs)
