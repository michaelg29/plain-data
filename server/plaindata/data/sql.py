import pyodbc

# connection
server = 'localhost' 
database = 'plain-data' 
username = 'plain-data-server' 
password = 'admin-pd-123'

class sql:
    cnxn = None
    cursor = None

    def sql_init():
        try:
            sql.cnxn = pyodbc.connect('DRIVER={SQL Server};Server='+server+';Database='+database+';User Id='+username+';Password='+ password)
            print('sql connection established')

            sql.cursor = sql.cnxn.cursor()
        except Exception as e:
            print(e)

    def sql_executeReadQuery(query):
        try:
            sql.cursor.execute(query)
            
            return sql.cursor.fetchall()
        except Exception as e:
            print(e)
            return None

    def sql_executeWriteQuery(query):
        try:
            sql.cursor.execute(query)

            # commit changes
            sql.cnxn.commit()
        except:
            # rollback with error
            sql.cnxn.rollback()

    def sql_cleanup():
        sql.cnxn.close()