__author__ = 'Hongyi'

# Two sets of queries
new_f = open('new_wos_query.txt', "r")
old_f = open('old_wos_query.txt', 'r')
new_query = new_f.readline().replace("\"", "\\\"")
old_query = old_f.readline().replace("\"", "\\\"")
new_f.close()
old_f.close()

# Country List
country_f = open('country_wos.txt', 'r')
country_line_list = []
for line in country_f:
    country_line_list.append(line.strip())
country_f.close()
# Parse CU= style
country_list_list = [x.split(";") for x in country_line_list]
country_string_list = []
for country in country_list_list:
    string = " or CU=".join(country)
    country_string_list.append("CU=" + string)

# Journal List
top_f = open("top_3_wos.txt", 'r')
top_query = top_f.readline().replace("\"", "\\\"")

# Year range
starting = 2015
ending = 2015

# Generate JS for all journals
f = open("wos_all_journal.txt", "w")
for country in country_string_list:
    for year in range(starting, ending+1):
        if year > 2010:
            jstr = "doc = document;textf = doc.getElementById(\"value(input1)\");" \
                   "textf.innerHTML = \"PY=%s and (%s) and (%s)\";s = doc.getElementById(\"searchButton\");" \
                   "b = s.firstElementChild;b.click();\n" % (str(year), old_query, country)
        else:
            jstr = "doc = document;textf = doc.getElementById(\"value(input1)\");" \
                   "textf.innerHTML = \"PY=%s and (%s) and (%s)\";s = doc.getElementById(\"searchButton\");" \
                   "b = s.firstElementChild;b.click();\n" % (str(year), old_query, country)
        f.write(jstr)
f.close()

# Generate JS for Top 3 Journals
f = open("wos_top_3_journal.txt", "w")
for country in country_string_list:
    for year in range(starting, ending+1):
        if year > 2010:
            jstr = "doc = document;textf = doc.getElementById(\"value(input1)\");" \
                   "textf.innerHTML = \"PY=%s and (%s) and (%s) and (%s)\";s = doc.getElementById(\"searchButton\");" \
                   "b = s.firstElementChild;b.click();\n" % (str(year), top_query, old_query, country)
        else:
            jstr = "doc = document;textf = doc.getElementById(\"value(input1)\");" \
                   "textf.innerHTML = \"PY=%s and (%s) and (%s) and (%s)\";s = doc.getElementById(\"searchButton\");" \
                   "b = s.firstElementChild;b.click();\n" % (str(year), top_query, old_query, country)
        f.write(jstr)
f.close()

# print(new_query)
