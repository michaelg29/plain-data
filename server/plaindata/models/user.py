"""
    user model class
"""

from ..data.sql import sql

import string

"""
    validates user against sql database (login)
"""
def validateUser(username, password):
    results = sql.sql_executeReadQuery(f"select ID, LastName, FirstName, Email from dbo.Users where Username = '{username}' and Password = '{password}'")

    if results:
        return results[0]
    else:
        return None

"""
    ensures new data has valid values
"""
def validateNewData(user):
    ret = validateData(user)

    # validate username
    check = sql.sql_executeReadQuery(f"select Username from dbo.Users where Username = '{user['Username']}'")

    if check:
        ret['result'] = False
        ret['reasons'].append('username:exists')

    # validate email
    check = sql.sql_executeReadQuery(f"select Email from dbo.Users where Email = '{user['Email']}'")

    if check:
        ret['result'] = False
        ret['reasons'].append('email:exists')

    return ret

"""
    ensures data is valid
"""
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
            ret['reasons'].append('pwd:invalid_char')

    if len(user['Password']) < 8:
        ret['result'] = False
        ret['reasons'].append('pwd:short')

    if upper_count < 1:
        ret['result'] = False
        ret['reasons'].append('pwd:upper')

    if lower_count < 1:
        ret['result'] = False
        ret['reasons'].append('pwd:lower')

    if digit_count < 1:
        ret['result'] = False
        ret['reasons'].append('pwd:digit')

    if symbol_count < 1:
        ret['result'] = False
        ret['reasons'].append('pwd:symbol')

    return ret

"""
    creates user with data
"""
def createUser(user):
    ret = validateData(user)

    # add user to table
    if ret['result']:
        try:
            sql.sql_executeWriteQuery(f"insert into dbo.Users values ('{user['LastName']}','{user['FirstName']}','{user['Username']}','{user['Password']}','{user['Email']}', '')")

            # get created id
            ret['id'] = sql.sql_executeReadQuery(f"select ID from dbo.Users where Username = '{user['Username']}'")[0][0]
        except Exception as e:
            print(e)
            ret['result'] = False
            ret['reasons'].append('cnxn')

    return ret

"""
    saves data for existing user
"""
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

"""
    adds flag to user
"""
def setFlag(id, email, flag):
    ret = {
        "result": True,
        "reasons": []
    }

    try:
        results = sql.sql_executeReadQuery(f"select Flags from dbo.Users where ID = {id} and Email = '{email}'")
        if results:
            flag += ',' + results[0][0]
            sql.sql_executeWriteQuery(f"update dbo.Users set Flags = '{flag}'")
        else:
            ret['result'] = False
            ret['reasons'].append('user:noexist')

    except Exception as e:
        print(e)
        ret['result'] = False
        ret['reasons'].append('cnxn')

    return ret