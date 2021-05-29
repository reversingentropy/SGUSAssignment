from model.DatabasePool import DatabasePool
from config.Settings import Settings
import jwt
import datetime
import bcrypt

class User:
    @classmethod
    def getUser(cls,username):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = 'select * from user where username=%s'
            cursor.execute(sql,(username,))
            user = cursor.fetchall()
            return user

        finally:
            dbConn.close()

    @classmethod
    def getUserId(cls,username):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = 'select userid from user where username=%s'
            cursor.execute(sql,(username,))
            userid = cursor.fetchall()
            return userid[0]['userid']

        finally:
            dbConn.close()

    
    @classmethod
    def getAllUsers(cls):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = "select * from user"
            cursor.execute(sql)
            users = cursor.fetchall()
            return users
        finally:
            dbConn.close()
    
    @classmethod
    def insertUser(cls,username,email,password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            password = password.encode()
            hashed = bcrypt.hashpw(password,bcrypt.gensalt())
            sql = "insert into user(username,email,password) values (%s,%s,%s)"
            users = cursor.execute(sql,(username,email,hashed))
            dbConn.commit()
            count = cursor.rowcount
            return count
        finally:
            dbConn.close()

    @classmethod
    def deleteUser(cls,userid):
        dbConn = DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql = "delete from user where userid = %s"
        users = cursor.execute(sql,(userid,))
        dbConn.commit()
        rows = cursor.rowcount
        dbConn.close()        
        return rows
    
    @classmethod
    def loginUser(cls,username,password):
        try:
            dbConn = DatabasePool.getConnection()
            cursor = dbConn.cursor(dictionary=True)
            sql = 'select * from user where username=%s'
            cursor.execute(sql,(username,))
            user = cursor.fetchone()
            if (user==None):
                    user = {"error":"User doesn't exist!"}
                    return user
            else:
                hashed = user['password'].encode(encoding='utf-8')
                if (bcrypt.checkpw(password,hashed)):
                    payload={'userid':user['userid'],"username":user['username'],'exp':datetime.datetime.utcnow()+datetime.timedelta(seconds=3600)}
                    token=jwt.encode(payload,Settings.secret,algorithm="HS256")                    
                    return {'jwt':token}            
                else:
                    user = {"error":"Invalid login credentials!"}
                    return user
        finally:
            dbConn.close()