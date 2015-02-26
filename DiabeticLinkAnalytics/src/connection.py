__author__ = 'hzhu'

import psycopg2

conn = psycopg2.connect("postgres://u49ft5tr72079n:p1ib5ko81m3et8dqh353declbmb@ec2-54-225-229-40.compute-1.amazonaws.com:5682/dtcidhu2mcmoo")
cur = conn.cursor()
cur.execute("""
    select *
    from tracking_weight_logs;""")
rows = cur.fetchall()
for row in rows:
    print row

