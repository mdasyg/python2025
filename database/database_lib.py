import sqlite3
from sqlite3 import Error

def create_connection(db_file,verbose=False):
    """ create a database connection to the SQLite database
        specified by db_file
    :param db_file: database file
    :param verbose: whether to print connection status
    :return: Connection object or None
    """
    conn = None
    try:
        conn = sqlite3.connect(db_file)
        if verbose:
            print(f"Connected to database: {db_file}")
        return conn
    except Error as e:
        print(e)

    return conn



def execute_query(conn, query,verbose=False):
    """ Execute a single query
    :param conn: Connection object
    :param query: a SQL query
    :param verbose: whether to print execution status
    :return:
    """
    try:
        c = conn.cursor()
        c.execute(query)
        conn.commit()
        if verbose:
            print("Query executed successfully")
    except Error as e:
        print(e)
   
def execute_read_query(conn, query,verbose=False):
    """ Execute a read query and return the results
    :param conn: Connection object
    :param query: a SQL query
    :param verbose: whether to print execution status
    :return: list of tuples containing the query results
    """
    try:
        c = conn.cursor()
        c.execute(query)
        result = c.fetchall()
        columns = [description[0] for description in c.description]
        if verbose:
            print("Read query executed successfully. Rows fetched:", len(result))
        return columns,result
    except Error as e:
        print(e)
        return None, None