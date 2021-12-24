import sqlite3
from sqlite3 import Error


def create_connection(db_file):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        return conn
    except Error as e:
        print(e)

    return conn


def run_sql(conn, input_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(input_sql)
    except Error as e:
        print(e)




def main():
    database = r".\site.db"
    sql_drop_job = ''' DROP TABLE IF EXISTS Job;'''

    sql_create_job = """ CREATE TABLE IF NOT EXISTS Job (
                                        id integer PRIMARY KEY,
                                        func_name text NOT NULL,
                                        notes text,
                                        status text NOT NULL,
                                        date_requested numeric NOT NULL,
                                        input_path text, 
                                        date_completed numeric, 
                                        log text,
                                        output_path text,
                                        user_id integer NOT NULL,

                                        FOREIGN KEY (user_id) REFERENCES User(id)

                                    ); """

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        #delete job table
        run_sql(conn, sql_drop_job)
        # create job table
        run_sql(conn, sql_create_job)

        # #add sample data to job
        # run_sql(conn, sql_add_data_job)

        # create tasks table
        # create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")


if __name__ == '__main__':
    main()