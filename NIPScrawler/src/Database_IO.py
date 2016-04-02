import pymysql


def db_connect_new():
    return pymysql.connect(host="localhost",
                           port=3306,
                           user="zhuhy",
                           passwd="Elpsycongroo!",
                           db="nips",
                           charset='utf8',
                           autocommit=True).cursor()


class DatabaseConnection:

    def __init__(self):
        self.cursor = db_connect_new()

    def insert(self, query):
        self.cursor.execute(query)