__author__ = 'Hongyi'

import pymysql


def str_replace(s):
    return str(s).replace("\\", "\\\\").replace("'", "\\'")


def db_connect():
    return pymysql.connect(host="192.168.0.83",
                                user='zhan',
                                passwd="9244",
                                db="twitter_db",
                                charset="utf8",
                                autocommit=True).cursor()

a = [["cancer"], ["diabetes"],["depression"],["hiv"],["acne"],["aids"],
 ["stroke"],["herpes"],["arthritis"],["breastcancer","breast cancer"], ["hepatitis"],
 ["autism"],["lupus"],["asthma"],["back pain"],["backpain"], ["headache"],
 ["hpv"],["obesity"],["diarrhoea"],["hypertension"],["eczema"],["constipation"],
 ["migraine"],["insomnia"],["meningitis"],["lymphoma"],["dementia"],["copd"],
 ["influenza"],["lung cancer","lungcancer"],["leukemia"],["chlamydia"],["osteoporosis"],
 ["prostatecancer"],["prostate cancer"],["fibromyalgia"],["multiple sclerosis","multiplesclerosis"],["heart disease", "heartdisease"],
 ["rheumatoid arthritis","rheumatoidarthritis"],["endometriosis"],["mentalillness","mental illness"],
 ["colon cancer","coloncancer"],["cystic fibrosis","cysticfibrosis"],["chickenpox","chicken pox"],
 ["lyme disease","lymedisease"],["bipolar disease","bipolardisease"],["gonorhoeaa"],["ovarian cancer", "ovariancancer"],
 ["cediac disease"],["whooping cough","whoopingcough"],["kidneydisease","kidney disease"]]

sql = """
        SELECT count(*)
        FROM tweet_weather
        WHERE keyword LIKE
        """

cur = db_connect()
distr = {}

for item in a:
    y = ["\"%{0}%\"".format(x) for x in item]
    temp_sql = sql + " OR keyword LIKE ".join(y)
    cur.execute(temp_sql)
    count = cur.fetchone()[0]
    distr[str(item)] = count

f = open("stat.csv", "w")
for item in a:
    f.write("\"" + item[0] + "\"," + str(distr[str(item)]) + "\n")