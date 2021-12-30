import mysql.connector


def connect():
  try:
    connection = mysql.connector.connect(
    host="localhost",
    user="cryptocoin",
    passwd="wkTeDI[mB[PmmH_-bRIcw<4ai}k6)yfrxel<",
    database="cryptocoin"
    )
    return connection
  except (Exception, mysql.connector.Error) as error:
    print(error)

def store_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'insert into login (user, passwd) values (%s, %s)'
    record_to_insert = (user, passwd)
    cursor.execute(query, record_to_insert)
    connection.commit()
  except (Exception, mysql.connector.Error) as error:
    print(error)
    print(f"There is already a user called {user}")
    return error

def find_user(user, passwd):
  try:
    connection = connect()
    cursor = connection.cursor()
    query = 'select * from login where user = %s and passwd = %s'
    record_to_insert = (user, passwd)
    cursor.execute(query, record_to_insert)
    response = cursor.fetchone()
    return response
  except (Exception, mysql.connector.Error) as error:
    print(error)

