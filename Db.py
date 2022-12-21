import sqlite3
import getpass
import string
import random
from sqlite3 import Error


def init_passwd():
    generated_password = ""
    alphabet_string_lowercase = string.ascii_lowercase
    alphabet_string_uppercase = string.ascii_uppercase
    special_characters = list(set(string.punctuation))
    numbers = string.digits

    while len(generated_password) <= 12:
        generated_password += alphabet_string_lowercase[random.randint(0, len(alphabet_string_lowercase) - 1)]
        generated_password += alphabet_string_uppercase[random.randint(0, len(alphabet_string_uppercase) - 1)]
        generated_password += special_characters[random.randint(0, len(special_characters) - 1)]
        generated_password += numbers[random.randint(0, len(numbers) - 1)]

    # print("".join((random.sample(list(generated_password), len(generated_password) - 1))))
    generated_password = list(generated_password)
    random.shuffle(generated_password)
    generated_password = "".join(generated_password)
    print(generated_password)


def create_data(conn, task):
    """
    Create a new task
    :param conn:
    :param task:
    :return:
    """

    sql = ''' INSERT INTO user_data(name,password,date,site)
              VALUES(?,?,?,?) '''
    cur = conn.cursor()
    cur.execute(sql, task)
    conn.commit()
    return cur.lastrowid


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


def create_table(conn, create_table_sql):
    """ create a table from the create_table_sql statement
    :param conn: Connection object
    :param create_table_sql: a CREATE TABLE statement
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(create_table_sql)
    except Error as e:
        print(e)


def main():
    database = "C:\\Users\\" + getpass.getuser() + "\\Desktop\\Dbfolder\\pswDb.db"

    sql_create_projects_table = """ CREATE TABLE IF NOT EXISTS user_data (
                                        id integer PRIMARY KEY,
                                        name text NOT NULL,
                                        password text NOT NULL,
                                        date text,
                                        site text
                                    ); """

    # sql_create_tasks_table = """CREATE TABLE IF NOT EXISTS tasks (
    #                                 id integer PRIMARY KEY,
    #                                 name text NOT NULL,
    #                                 priority integer,
    #                                 status_id integer NOT NULL,
    #                                 project_id integer NOT NULL,
    #                                 begin_date text NOT NULL,
    #                                 end_date text NOT NULL,
    #                                 FOREIGN KEY (project_id) REFERENCES projects (id)
    #                             );"""

    # create a database connection
    conn = create_connection(database)

    # create tables
    if conn is not None:
        # create projects table
        create_table(conn, sql_create_projects_table)

        # create tasks table
        #create_table(conn, sql_create_tasks_table)
    else:
        print("Error! cannot create the database connection.")

    create_data(conn,("charles","hello", "6/26/1985","google.com"))
