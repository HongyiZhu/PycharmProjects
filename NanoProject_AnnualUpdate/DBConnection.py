import pyodbc


class DBConnection:
    dbConn = None

    def __init__(self):
        self.dbConn = pyodbc.connect(r'Driver={SQL Server Native Client 11.0};'
                                r'Server=AIL-NANO;'
                                r'Database=NanoUSPTO;'
                                r'Trusted_Connection=yes')

    def getCursor(self):
        return self.dbConn.cursor()

    def close(self):
        self.dbConn.close()


# conn = DBConnection()
# cur = conn.getCursor()
# cur.execute("""SELECT TOP 10 *
#   FROM [patent2016].[dbo].[usp_assignee]""")
# result = cur.fetchall()
# for row in result:
#     print(row)
# cur.close()
# conn.close()