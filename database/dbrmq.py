import mysql.connector
import json
from cradb import init_db
from rmqrpc import listen

db_host = 'localhost'
db_user = 'craapp'
db_password = 'password'

cradb = mysql.connector.connect(
    host=db_host, user=db_user, password=db_password)

init_db(cradb)

def execute(db, sql, *args):
    answer = "DONE"
    if sql.lstrip()[:6].upper() == 'SELECT':
        answer = []
        with db.cursor() as cursor:
            cursor.execute(sql, args)
            column_names=[column[0] for column in cursor.description]
            result = cursor.fetchall()
            for row in result:
                answer.append(dict(zip(column_names, row)))
    else:
        with db.cursor() as cursor:
            cursor.execute(sql, args)
            db.commit()
    return answer

def get_user(r):
    sql = '''SELECT username, email, password_hash FROM users WHERE username = %s'''
    return execute(cradb, sql, r['username'])

def get_users(r):
    sql = '''SELECT username, email FROM users'''
    return execute(cradb, sql)

def register_user(r):
    sql = '''INSERT INTO users (username, email, password_hash) VALUES (%s, %s, %s)'''
    return execute(cradb, sql, r['username'], r['email'], r['password_hash'])

def get_alerts(r):
    sql = '''SELECT users.email, alerts.username, numerator, denominator, threshold, last
        FROM alerts
        INNER JOIN users ON alerts.username = users.username
        WHERE alerts.username = %s'''
    return execute(cradb, sql, r['username'])

def set_alert(r):
    sql = '''REPLACE INTO alerts (username, numerator, denominator, threshold)
        VALUES (%s, %s, %s, CONVERT(%s, DECIMAL(12,6)))'''
    return execute(cradb, sql, r['username'], r['numerator'], r['denominator'], r['threshold'])

def update_alert(r):
    sql = '''UPDATE alerts SET last = CONVERT(%s, DECIMAL(12,6))
        WHERE username = %s AND numerator = %s AND denominator = %s AND threshold = CONVERT(%s, DECIMAL(12,6))'''
    return execute(cradb, sql, r['last'], r['username'], r['numerator'], r['denominator'], r['threshold'])

def delete_alert(r):
    sql = '''DELETE FROM alerts
        WHERE username = %s AND numerator = %s AND denominator = %s AND
        threshold = CONVERT(%s, DECIMAL(12,6))'''
    return execute(cradb, sql, r['username'], r['numerator'], r['denominator'], r['threshold'])

listen(get_user, get_users, register_user,
       get_alerts, set_alert, update_alert, delete_alert)