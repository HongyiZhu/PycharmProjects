import pymysql

class databaseWrapper:
    def __init__(self):
        self.conn = None

    def connect(self):
        self.conn = pymysql.connect(host='localhost',
                                    port=3306,
                                    user='zhuhy',
                                    passwd='Edwardsj211211',
                                    db='misq',
                                    use_unicode=True,
                                    charset="utf8",
                                    autocommit=True)

    def get_cursor(self):
        self.connect()
        return self.conn.cursor()

    def disconnect(self):
        self.conn.close()