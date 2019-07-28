import pyodbc

# connection
server = 'localhost' 
database = 'MundusInvicte' 
username = 'plain-data-server' 
password = 'admin-pd-123'

cnxn = None
cursor = None

def sql_init():
    try:
        cnxn = pyodbc.connect('DRIVER={SQL Server};Server='+server+';Database='+database+';User Id='+username+';Password='+ password)
        print('sql connection established')

        # cursor object
        cursor = cnxn.cursor()
    except Exception as e:
        print(e)

def sql_executeReadQuery(query):
    try:
        cursor.execute(query)
        
        return cursor.fetchall()
    except:
        return None

def sql_executeWriteQuery(query):
    try:
        cursor.execute(query)

        # commit changes
        cnxn.commit()
    except:
        # rollback with error
        cnxn.rollback()

def sql_cleanup():
    cnxn.close()