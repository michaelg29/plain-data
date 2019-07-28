from ..data.sql import sql

def validateUser(username, password):
    results = sql.sql_executeReadQuery("select * from dbo.Users where Username = '" + username + "' and Password = '" + password + "'")

    print("res:",results)

    if results:
        return results[0]
    else:
        return None