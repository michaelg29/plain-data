from ..data.sql import sql

import string

def validateUser(username, password):
    results = sql.sql_executeReadQuery(f"select ID, LastName, FirstName, Email from dbo.Users where Username = '{username}' and Password = '{password}'")

    if results:
        return results[0]
    else:
        return None

def validateNewData(user):
    ret = validateData(user)

    # validate username
    check = sql.sql_executeReadQuery(f"select Username from dbo.Users where Username = '{user['Username']}'")

    if check:
        ret['result'] = False
        ret['reasons'].append('username.exists')

    # validate email
    check = sql.sql_executeReadQuery(f"select Email from dbo.Users where Email = '{user['Email']}'")

    if check:
        ret['result'] = False
        ret['reasons'].append('email.exists')

    return ret

def validateData(user):
    ret = {
        "result": True,
        "reasons": []
    }

    # validate password
    upper_count = 0
    lower_count = 0
    digit_count = 0
    symbol_count = 0

    for c in user['Password']:
        if c in string.ascii_uppercase: 
            upper_count += 1
        elif c in string.ascii_lowercase:
            lower_count += 1
        elif c in string.digits:
            digit_count += 1
        elif c in string.punctuation:
            symbol_count += 1
        else:
            ret['result'] = False
            ret['reasons'].append('pwd.invalid_char')

    if len(user['Password']) < 8:
        ret['result'] = False
        ret['reasons'].append('pwd.short')

    if upper_count < 1:
        ret['result'] = False
        ret['reasons'].append('pwd.upper')

    if lower_count < 1:
        ret['result'] = False
        ret['reasons'].append('pwd.lower')

    if digit_count < 1:
        ret['result'] = False
        ret['reasons'].append('pwd.digit')

    if symbol_count < 1:
        ret['result'] = False
        ret['reasons'].append('pwd.symbol')

    return ret

def createUser(user):
    ret = validateData(user)

    # add user to table
    if ret['result']:
        try:
            sql.sql_executeWriteQuery(f"insert into dbo.Users values ('{user['LastName']}','{user['FirstName']}','{user['Username']}','{user['Password']}','{user['Email']}')")

            # get created id
            ret['id'] = sql.sql_executeReadQuery(f"select ID from dbo.Users where Username = '{user['Username']}'")[0][0]
        except Exception as e:
            print(e)
            ret['result'] = False
            ret['reasons'].append('cnxn')

    return ret

def saveUser(user):
    ret = validateData(user)

    if ret['result']:
        try:
            sql.sql_executeWriteQuery(f"update dbo.Users set LastName = '{user['LastName']}', FirstName = '{user['FirstName']}', Username = '{user['Username']}', Password = '{user['Password']}', Email = '{user['Email']}' where ID = {user['ID']}")
        except Exception as e:
            print(e)
            ret['result'] = False
            ret['reasons'].append('cnxn')

    return ret