import pymysql
import math
import random
import numpy as np
import pickle
# import cPickle

labels = {"push": 1, "pull": 2, "up": 3, "down": 4}


def get_walking(lst):
    results = lst[:10]
    start = random.randint(0, len(lst) - 250) + 10
    results += lst[start: start + 230]

    return get_human_results(results)


def get_null_human(lst):
    results = list(lst)
    random.shuffle(results)
    results = tuple(results)

    return get_human_results(results)


def get_human(table, index):
    sql = "Select x, y, z from %s where `group`=%d and id='D202B31CD2C3' order by ts asc" % (table, index)
    cursor.execute(sql)
    results = cursor.fetchall()

    return get_human_results(results)


def get_human_results(results):
    x = 0
    y = 0
    z = 0

    for i in range(10):
        x += results[i][0]
        y += results[i][1]
        z += results[i][2]

    average_x, average_y, average_z = int(x / 10), int(y / 10), int(z / 10)
    l_avg = average_x ** 2 + average_y ** 2 + average_z ** 2

    if len(results) > 240:
        front = int((len(results) - 240)/2)
        results = results[front:front+240]
    elif len(results) < 240:
        lack = int((240-len(results))/2)
        results = standing[0:lack] + results + standing[-(240 - lack - len(results) + 1):-1]

    new_results = []
    for (x, y, z) in results:
        x1 = x - average_x
        y1 = y - average_y
        z1 = z - average_z
        l_temp = x ** 2 + y ** 2 + z ** 2
        dot_multi = x * average_x + y * average_y + z * average_z

        w_p = int((l_temp - (math.fabs(dot_multi) / (l_avg ** 0.5)) ** 2))
        w = 0 if w_p == 0 else int(w_p ** 0.5)

        new_results.append((x1, y1, z1, w))

    return new_results


def get_null_object(lst):
    results = list(lst)
    random.shuffle(results)
    results = tuple(results)

    return get_object_results(results)


def get_object(table, index):
    sql = "Select x, y, z from %s where `group`=%d and id='EB0BE26E8C52' order by ts asc" % (table, index)
    cursor.execute(sql)
    results = cursor.fetchall()

    return get_object_results(results)


def get_object_results(results):
    x = 0
    y = 0
    z = 0

    for i in range(10):
        x += results[i][0]
        y += results[i][1]
        z += results[i][2]

    average_x, average_y, average_z = int(x / 10), int(y / 10), int(z / 10)
    l_avg = average_x ** 2 + average_y ** 2 + average_z ** 2

    if len(results) > 240:
        front = int((len(results) - 240)/2)
        results = results[front:front+240]
    elif len(results) < 240:
        lack = int((240-len(results))/2)
        results = (results[0],) * lack + results + (results[-1],) * (240 - lack - len(results) + 1)

    new_results = []
    for (x, y, z) in results:
        x1 = x - average_x
        y1 = y - average_y
        z1 = z - average_z
        l_temp = x ** 2 + y ** 2 + z ** 2
        dot_multi = x * average_x + y * average_y + z * average_z

        w_p = int((l_temp - (math.fabs(dot_multi) / (l_avg ** 0.5)) ** 2))
        w = 0 if w_p == 0 else int(w_p ** 0.5)

        new_results.append((x1, y1, z1, w))

    return new_results


def get_tuple_list(human_t, object_t):
    humans = []
    objects = []

    temp1 = [(x, y, z, w) for (x, y, z, w) in human_t]
    temp2 = [(x, y, z, w) for (x, y, z, w) in object_t]
    humans.append(temp1)
    objects.append(temp2)

    temp1 = [(x, z, y, w) for (x, y, z, w) in human_t]
    temp2 = [(x, z, y, w) for (x, y, z, w) in object_t]
    humans.append(temp1)
    objects.append(temp2)

    temp1 = [(y, z, x, w) for (x, y, z, w) in human_t]
    temp2 = [(y, z, x, w) for (x, y, z, w) in object_t]
    humans.append(temp1)
    objects.append(temp2)

    temp1 = [(y, x, z, w) for (x, y, z, w) in human_t]
    temp2 = [(y, x, z, w) for (x, y, z, w) in object_t]
    humans.append(temp1)
    objects.append(temp2)

    temp1 = [(z, x, y, w) for (x, y, z, w) in human_t]
    temp2 = [(z, x, y, w) for (x, y, z, w) in object_t]
    humans.append(temp1)
    objects.append(temp2)

    temp1 = [(z, y, x, w) for (x, y, z, w) in human_t]
    temp2 = [(z, y, x, w) for (x, y, z, w) in object_t]
    humans.append(temp1)
    objects.append(temp2)

    return humans, objects


def get_feature(h, o):
    feature = []
    for i in range(240):
        feature.append(h[i][0] / 1000)
    for i in range(240):
        feature.append(o[i][0] / 1000)
    for i in range(240):
        feature.append(h[i][1] / 1000)
    for i in range(240):
        feature.append(o[i][1] / 1000)
    for i in range(240):
        feature.append(h[i][2] / 1000)
    for i in range(240):
        feature.append(o[i][2] / 1000)
    for i in range(240):
        feature.append(h[i][3] / 1000)
    for i in range(240):
        feature.append(o[i][3] / 1000)
    for i in range(240):
        feature.append(h[i][0] / 1000)
    for i in range(240):
        feature.append(o[i][1] / 1000)
    for i in range(240):
        feature.append(h[i][3] / 1000)
    for i in range(240):
        feature.append(o[i][0] / 1000)
    for i in range(240):
        feature.append(h[i][2] / 1000)
    for i in range(240):
        feature.append(o[i][3] / 1000)
    for i in range(240):
        feature.append(h[i][1] / 1000)
    for i in range(240):
        feature.append(o[i][2] / 1000)
    for i in range(240):
        feature.append(h[i][0] / 1000)

    return feature


def get_null_dataset():
    training = []
    validation = []
    test = []
    for k in sorted(labels.keys()):
        temp = []
        for ki in range(1, 3):
            s = k + str(ki)
            print(s)
            for j in range(1, 9):
                print(j)
                h, o = get_human(s, j), get_object(s, j)
                for idx in range(5):
                    nw = get_walking(walking)
                    nt = get_null_human(sitting)
                    nd = get_null_human(standing)
                    no = get_null_object(noobj)
                    feature = get_feature(h, no)
                    temp.append((feature, 0))
                    feature = get_feature(nw, o)
                    temp.append((feature, 0))
                    feature = get_feature(nt, o)
                    temp.append((feature, 0))
                    feature = get_feature(nd, o)
                    temp.append((feature, 0))
        random.shuffle(temp)
        training += temp[:720]
        validation += temp[720:840]
        test += temp[840:]

    return training, validation, test


def get_dataset():
    training = []
    validation = []
    test = []
    for k in sorted(labels.keys()):
        temp = []
        for ki in range(1, 3):
            s = k + str(ki)
            for j in range(1, 9):
                humans, objects = get_tuple_list(get_human(s, j), get_object(s, j))
                for i in range(6):
                    h = humans[i]
                    o = objects[i]
                    h = h[-25:] + h[:-25]
                    o = o[-25:] + h[:-25]
                    for idx in range(10):
                        feature = get_feature(h, o)
                        temp.append((feature, labels[k]))
                        h = h[5:] + h[0:5]
                        o = o[5:] + o[0:5]
        random.shuffle(temp)
        training += temp[:720]
        validation += temp[720:840]
        test += temp[840:]
    temp = []
    for k in sorted(labels.keys()):
        for ki in range(1, 3):
            s = k + str(ki)
            for j in range(1, 9):
                h = get_human(s, j)
                o = get_object(s, j)
                for idx in range(5):
                    nw = get_walking(walking)
                    nt = get_null_human(sitting)
                    nd = get_null_human(standing)
                    no = get_null_object(noobj)
                    feature = get_feature(h, no)
                    temp.append((feature, 0))
                    feature = get_feature(nw, o)
                    temp.append((feature, 0))
                    feature = get_feature(nt, o)
                    temp.append((feature, 0))
                    feature = get_feature(nd, o)
                    temp.append((feature, 0))
    random.shuffle(temp)
    training += temp[:720]
    validation += temp[720:840]
    test += temp[840:960]

    return training, validation, test


def to_np_set(tp):
    lb = []
    ft = []
    for tup in tp:
        ft.append(tup[0])
        lb.append(tup[1])
    return np.asarray(ft, dtype=np.float32), np.asarray(lb)

cursor = pymysql.connect(host="127.0.0.1",
                         database="activity",
                         user="root",
                         password="Edwardsj211211",
                         charset='utf8',
                         autocommit=True).cursor()


sql = "select x, y, z from standing order by ts asc"
cursor.execute(sql)
standing = cursor.fetchall()

sql = "select x, y, z from walking order by ts asc"
cursor.execute(sql)
walking = cursor.fetchall()

sql = "select x, y, z from sitting order by ts asc"
cursor.execute(sql)
sitting = cursor.fetchall()

sql = "select x, y, z from noobj order by ts asc"
cursor.execute(sql)
noobj = cursor.fetchall()

# for k in sorted(labels.keys()):
#     print(k, labels[k])

tr, va, te = get_dataset()
training = to_np_set(tr)
validation = to_np_set(va)
test = to_np_set(te)

data = (training, validation, test)

f = open("datadump.txt", 'wb')
# cPickle.dump(data, f)
pickle.dump(data, f)




