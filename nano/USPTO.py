__author__ = 'Hongyi'

import USPTO_tool

# Country List
country_f = open('country_uspto.txt', 'r')
country_list = []
for line in country_f:
    country_list.append(line.strip())
country_f.close()

# Two sets of queries
new_f = open('new_uspto_query.txt', "r")
old_f = open('old_uspto_query.txt', 'r')
new_query = []
for line in new_f:
    new_query.append(line.strip().replace(" ", "+") + "%0D%0A")
old_query = []
for line in old_f:
    old_query.append(line.strip().replace(" ", "+") + "%0D%0A")
new_f.close()
old_f.close()

# Year range
starting = 2000
ending = 2014

# URL base
base = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF" \
       "&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query="
# iterate on countries
for country in country_list:
    # iterate on year
    for year in range(starting, ending + 1):
        pat_list = []   # patent list for each year
        if year > 2010:
            # Query with new keywords
            for key in new_query:
                # generate query link
                query = "isd/%s+AND+acn/%s+AND+(ttl/%s+OR+abst/%s+OR+aclm/%s)" % (str(year), country, key, key, key)
                query = query.replace("/", "%2F").replace("(", "%28").replace(")", "%29")\
                    .replace(" ", "+").replace("\"", "%22").replace("$", "%24")
                url = base + query + "&d=PTXT"

                # parse the query result
                key_result = USPTO_tool.analyze_url(url)

                # remove duplicate entry
                for result in key_result:
                    if result in pat_list:
                        pass
                    else:
                        pat_list.append(result)
        else:
            # Query with old keywords
            for key in old_query:
                # generate query link
                query = "isd/%s+AND+acn/%s+AND+(ttl/%s+OR+abst/%s+OR+aclm/%s)" % (str(year), country, key, key, key)
                query = query.replace("/", "%2F").replace("(", "%28").replace(")", "%29")\
                    .replace(" ", "+").replace("\"", "%22").replace("$", "%24")
                url = base + query + "&d=PTXT"

                # Parse query result
                key_result = USPTO_tool.analyze_url(url)

                # remove duplicate entry
                for result in key_result:
                    if result in pat_list:
                        pass
                    else:
                        pat_list.append(result)

        # patent number for each year
        pat_num = len(pat_list)