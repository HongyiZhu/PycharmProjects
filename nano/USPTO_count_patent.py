__author__ = 'Hongyi'

import USPTO_tool

# Country List
country_f = open('country_uspto.txt', 'r')
country_list = []
for line in country_f:
    country_list.append(line.strip())
country_f.close()

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
        print("Querying %s %s" % (country, str(year)))
        query = "isd/%s+AND+acn/%s" % (str(year), country)
        query = query.replace("/", "%2F").replace("(", "%28").replace(")", "%29")\
            .replace(" ", "+").replace("\"", "%22").replace("$", "%24")
        url = base + query + "&d=PTXT"
        amount = USPTO_tool.get_amount(url)

        # log module
        log = open("general.log", "a")
        log.write("%s\t%s\t%s\n" % (country, str(year), amount))
        log.close()
