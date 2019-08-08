"""
    local sql database connection
"""

import pyodbc

# connection
driver = '{SQL SERVER}'
server = 'localhost\SQLEXPRESS' 
database = 'plain-data' 
username = 'plain-data-server' 
password = 'admin-pd-123'

class sql:
    cnxn = None
    cursor = None

    """
        initializes sql connection
    """
    def sql_init():
        try:
            sql.cnxn = pyodbc.connect(f"DRIVER={driver};Server={server};Database={database};User Id={username};Password={password}")
            print('sql connection established')

            sql.cursor = sql.cnxn.cursor()
        except Exception as e:
            print(e)

    """
        executes read query
        returns results
    """
    def sql_executeReadQuery(query):
        try:
            sql.cursor.execute(query)
            
            return sql.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    """
        executes write query
        returns True if successful
    """
    def sql_executeWriteQuery(query):
        try:
            sql.cursor.execute(query)

            # commit changes
            sql.cnxn.commit()

            return True
        except Exception as e:
            print("SQl40:",e)
            # rollback with error
            sql.cnxn.rollback()
            return False

    def sql_cleanup():
        sql.cnxn.close()