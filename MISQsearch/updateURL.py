from MISQsearch.dbconnection import databaseWrapper
import pickle

db = databaseWrapper()
cur = db.get_cursor()

f = open("MISQ_paper_list.pkl", "rb")
paperURL = pickle.load(f)
paperURL = [x for x in paperURL if ".pdf" not in x]

for i in range(len(paperURL)):
    paper = paperURL[i]

    sql = "UPDATE `paper` SET URL = %s WHERE ID = '%s'" % (db.conn.escape(paper), str(i + 1))
    cur.execute(sql)