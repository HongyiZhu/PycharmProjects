__author__ = 'Hongyi'

import sqlite3
import arff
import csv
import os


def init():
    path = "D:/sensors/"
    filelist = os.listdir(path)

    # set up an embedded database
    h.execute("""CREATE TABLE heartbeat
                (sensor_id text, event_id int, accer_x int, accer_y int, accer_z int,
                event_timestamp real, event_date text, log_time text, battery_capacity int, tag text default null)""")
    o.execute("""CREATE TABLE object
                (sensor_id text, event_id int, accer_x int, accer_y int, accer_z int,
                event_timestamp real, event_date text, log_time text, battery_capacity int, tag text default null)""")
    m.execute("""CREATE TABLE motion
                (sensor_id text, event_id int, accer_x int, accer_y int, accer_z int,
                event_timestamp real, event_date text, log_time text, battery_capacity int, tag text default null)""")

    # Read data from csv files
    motion = open("D:/sensors/EB99.csv")
    motion_data = csv.DictReader(motion)
    for line in motion_data:
        # print(line)
        if line['event_id'] != 1:
            sql = """INSERT INTO motion (sensor_id, event_id, accer_x, accer_y, accer_z, event_timestamp, event_date,
                        log_time, battery_capacity) VALUES ('%s', %d, %d, %d, %d, %f, '%s', '%s', %d)""" % \
                  (line['sensor_id'], int(line['event_id']), int(line['accer_x']), int(line['accer_y']), int(line['accer_z']),
                   float(line['event_timestamp']), line['event_date'], line['log_time'], int(line['battery_capacity']))
            m.execute(sql)
        else:
            sql = """INSERT INTO heartbeat (sensor_id, event_id, accer_x, accer_y, accer_z, event_timestamp, event_date,
                        log_time, battery_capacity) VALUES ('%s', %d, %d, %d, %d, %f, '%s', '%s', %d)""" % \
                  (line['sensor_id'], int(line['event_id']), int(line['accer_x']), int(line['accer_y']), int(line['accer_z']),
                   float(line['event_timestamp']), line['event_date'], line['log_time'], int(line['battery_capacity']))
            h.execute(sql)
    # print(m.execute("select count(*) from motion").fetchone())
    motion.close()

    filelist.remove('EB99.csv')
    for filename in filelist:
        object = open(path + filename)
        signal = csv.DictReader(object)
        for line in signal:
            if line['event_id'] != 1:
                sql = """INSERT INTO object (sensor_id, event_id, accer_x, accer_y, accer_z, event_timestamp, event_date,
                            log_time, battery_capacity) VALUES ('%s', %d, %d, %d, %d, %f, '%s', '%s', %d)""" % \
                      (line['sensor_id'], int(line['event_id']), int(line['accer_x']), int(line['accer_y']), int(line['accer_z']),
                       float(line['event_timestamp']), line['event_date'], line['log_time'], int(line['battery_capacity']))
                o.execute(sql)
            else:
                sql = """INSERT INTO heartbeat (sensor_id, event_id, accer_x, accer_y, accer_z, event_timestamp, event_date,
                            log_time, battery_capacity) VALUES ('%s', %d, %d, %d, %d, %f, '%s', '%s', %d)""" % \
                      (line['sensor_id'], int(line['event_id']), int(line['accer_x']), int(line['accer_y']), int(line['accer_z']),
                       float(line['event_timestamp']), line['event_date'], line['log_time'], int(line['battery_capacity']))
                h.execute(sql)
        object.close()


def generate(arff_file):
    ou = open(arff_file, "w")
    dataset = {
        'description': 'Motion sensor dataset',
        'relation': 'whatever',
        'attributes': [
            ('chair_prev', 'REAL'),
            ('bath_prev', 'REAL'),
            ('down_prev', 'REAL'),
            ('up_prev', 'REAL'),
            ('chair_post', 'REAL'),
            ('bath_post', 'REAL'),
            ('down_post', 'REAL'),
            ('up_post', 'REAL'),
            ('a_prev', 'REAL'),
            ('a_post', 'REAL'),
            ('tag', ['walk', 'chair', 'bath', 'down', 'up'])
        ]
    }

    sql = """select * from motion order by event_timestamp asc;"""
    m.execute(sql)
    data = []
    counter = 0
    for record in m:
        # print(record)
        row = []
        ts = float(record[5])
        prev = get_prev_obj(ts)
        post = get_post_obj(ts)
        for item in prev:
            row.append(item)
        for item in post:
            row.append(item)
        a = get_a(ts)
        for item in a:
            row.append(item)
        if record[-1] is None:
            row.append('?')
        else:
            row.append(record[-1])
        data.append(row)
        counter += 1
        print(counter)
    dataset['data'] = data
    ou.write(arff.dumps(dataset))
    ou.close()


def get_a(ts):
    sql = """select * from motion where event_timestamp > %f and event_timestamp < %f""" % (ts - 5, ts)
    m2.execute(sql)
    sum1 = [0, 0, 0]
    count1 = 0
    list1 = m2.fetchall()
    for record in list1:
        sum1 = [old + new for old, new in zip(sum1, list(record)[2:5])]
        count1 += 1
    if count1 != 0:
        ave1 = [x/float(count1) for x in sum1]
        pre_a_sum = 0
        for record in list1:
            tri_ax = [r-a for r, a in zip(list(record)[2:5], ave1)]
            pre_a_sum += (tri_ax[0] ** 2 + tri_ax[1] ** 2 + tri_ax[2] ** 2) ** 0.5
        pre_a_ave = pre_a_sum / float(count1)
    else:
        pre_a_ave = -1

    sql = """select * from motion where event_timestamp > %f and event_timestamp < %f""" % (ts, ts + 5)
    m2.execute(sql)
    sum2 = [0, 0, 0]
    count2 = 0
    list2 = m2.fetchall()
    for record in list2:
        sum2 = [old + new for old, new in zip(sum2, list(record)[2:5])]
        count2 += 1
    if count2 != 0:
        ave2 = [x/float(count2) for x in sum2]
        post_a_sum = 0
        for record in list2:
            tri_ax = [r-a for r, a in zip(list(record)[2:5], ave2)]
            post_a_sum += (tri_ax[0] ** 2 + tri_ax[1] ** 2 + tri_ax[2] ** 2) ** 0.5
        post_a_ave = post_a_sum / float(count2)
    else:
        post_a_ave = -1

    return [pre_a_ave, post_a_ave]


def get_prev_obj(ts):
    result = []
    for obj in obj_id:
        sql = """select * from object where event_timestamp < %f and sensor_id = '%s' order by event_timestamp desc""" \
              % (ts, obj)
        rts = o.execute(sql).fetchone()
        if rts is None:
            result.append(999999)
        else:
            result.append(float(ts - rts[5]))
    # print(result)
    return result


def get_post_obj(ts):
    result = []
    for obj in obj_id:
        sql = """select * from object where event_timestamp > %f and sensor_id = '%s' order by event_timestamp asc""" \
              % (ts, obj)
        rts = o.execute(sql).fetchone()
        if rts is None:
            result.append(999999)
        else:
            result.append(float(rts[5] - ts))
    # print(result)
    return result

obj_id = ['84EB1878E555', '84EB1878E755', '84EB1878E74C', '84EB1878E93D']
conn = sqlite3.connect(":memory:")
h = conn.cursor()
o = conn.cursor()
m = conn.cursor()
m2 = conn.cursor()
init()
generate("D:/motion.arff")

