import pickle

f = open("Parse-Step1.pkl" ,'rb')
col_SIPO, col_USPTO, _ = pickle.load(f)
f.close()
f = open("entity_dict.pkl" ,'rb')
entity_country_dict, entity_domain_dict = pickle.load(f)
f.close()


def build_nodelist(cols):
    nodelist = []
    for col in cols:
        for c in col:
            for a in c:
                if a not in nodelist:
                    nodelist.append(a)
    return nodelist


def build(col, nodelist, dict_country, dict_domain):
    """
    Edge Type:
    0 - black - UKN of any party
    1 - purple - domestic A-A
    2 - red - domestic A-I
    3 - yellow - domestic I-I
    4 - blue - international A-A
    5 - cyan - international A-I
    6 - green - international I-I

    2 standards for domestic and international:
    I. domestic: same country
    II. domestic: same as 'CN' or same as 'US'

    :param nodelist: list of all nodes
    :param dict_country: country attribute of the node
    :param dict_domain:  domain attribute of the node
    :return: the network
    """
    rows = []
    for c in col:
        for i in range(len(c) - 1):
            for j in range(i + 1, len(c)):
                node1 = c[i]
                node2 = c[j]
                ind1 = nodelist.index(node1)
                ind2 = nodelist.index(node2)
                if entity_country_dict[node1] == 'UKN' or entity_country_dict[node2] == 'UKN':
                    t = 0
                else:
                    # if entity_country_dict[node1] == entity_country_dict[node2]:
                    if entity_country_dict[node1] == 'US' and entity_country_dict[node2] == 'US':
                        if not entity_domain_dict[node1] == entity_domain_dict[node2]:
                            t = 2
                        elif entity_domain_dict[node1] == "ACA":
                            t = 1
                        else:
                            t = 3
                    else:
                        if not entity_domain_dict[node1] == entity_domain_dict[node2]:
                            t = 5
                        elif entity_domain_dict[node1] == "ACA":
                            t = 4
                        else:
                            t = 6
                temp = ["s"+str(ind1), "s"+str(ind2), "1", str(t)]
                rows.append(temp)
    return rows


def write_to_gdf(nodelist, net):
    f = open("USPTO_C2.gdf", "w", encoding="utf8")
    f.write("nodedef>name VARCHAR,label VARCHAR\n")
    for i, n in enumerate(nodelist):
        f.write("s" + str(i) + "," + n + "\n")
    f.write("edgedef>node1 VARCHAR,node2 VARCHAR, weight DOUBLE, type VARCHAR\n")
    for row in net:
        s = ",".join(row)
        f.write(s)
        f.write("\n")
    f.close()

nl = build_nodelist((col_SIPO, col_USPTO))
net = build(col_USPTO, nl, entity_country_dict, entity_domain_dict)
write_to_gdf(nl, net)



