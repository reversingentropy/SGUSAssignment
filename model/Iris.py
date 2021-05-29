from model.DatabasePool import DatabasePool

import datetime



class Iris:
    @classmethod
    def insertValues(cls,userid,sl,sw,pl,pw,prediction):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)

        sql="insert into irisprediction(userid,sepalLength,sepalWidth,petalLength,petalWidth,prediction) Values(%s,%s,%s,%s,%s,%s)"
        users = cursor.execute(sql,(userid,sl,sw,pl,pw,prediction))
        dbConn.commit()
        rows=cursor.rowcount
        #print(cursor.lastrowid)

        dbConn.close()

        return rows
    
    @classmethod
    def getValues(cls,userid):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql="SELECT predictionId, sepalLength,sepalWidth,petalLength,petalWidth,prediction, DATE_FORMAT(InsertionDate, '%d %M %Y %T')  from irisprediction where userid = %s ORDER BY predictionId DESC"
        cursor.execute(sql,(userid,))
        values = cursor.fetchall()
        dbConn.close()
        return values

    @classmethod
    def delete(cls,userid):
        dbConn=DatabasePool.getConnection()
        cursor = dbConn.cursor(dictionary=True)
        sql="delete from irisprediction where userid = %s order by predictionId desc limit 1"
        users = cursor.execute(sql,(userid,))
        dbConn.commit()
        rows=cursor.rowcount
        #print(cursor.lastrowid)
        dbConn.close()
        return rows
