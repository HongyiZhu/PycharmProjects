import pymysql

f = open("ObjNoActivity.csv")

cursor = pymysql.connect(host="127.0.0.1",
                         database="activity",
                         user="root",
                         password="Edwardsj211211",
                         charset='utf8',
                         autocommit=True).cursor()

for row in f:
    element = row.split(",")
    ts = element[0].strip()
    group = element[2].strip()
    # if group == "0":
    #     continue
    id = element[3].strip()
    x = element[5].strip()
    y = element[6].strip()
    z = element[7].strip()
    sql = "INSERT INTO activity.noobj VALUES ('%s', '%s', '%s', '%s', '%s', '%s')" \
          % (ts, group, id, x, y, z)
    print(sql)
    try:
        cursor.execute(sql)
    except pymysql.err.IntegrityError:
        pass


