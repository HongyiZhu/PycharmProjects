__author__ = 'Hongyi'

import USPTO_tool
import sys


def main():
    # Two sets of queries
    new_f = open('new_uspto_query.txt', "r")
    old_f = open('old_uspto_query.txt', 'r')
    new_query = []
    for line in new_f:
        new_query.append(line.strip().replace(" ", "+"))
    old_query = []
    for line in old_f:
        old_query.append(line.strip().replace(" ", "+"))
    new_f.close()
    old_f.close()

    # URL base
    base = "http://patft.uspto.gov/netacgi/nph-Parser?Sect1=PTO2&Sect2=HITOFF" \
           "&u=%2Fnetahtml%2FPTO%2Fsearch-adv.htm&r=0&p=1&f=S&l=50&Query="

    country = sys.argv[1]
    year = sys.argv[2]

    pat_list = []   # patent list for each year
    if int(year) > 2010:
        # Query with new keywords
        for key in new_query:
            # generate query link
            print("Querying %s %s %s" % (country, year, key))
            query = "isd/%s+AND+acn/%s+AND+(ttl/%s+OR+abst/%s+OR+aclm/%s)" % (year, country, key, key, key)
            query = query.replace("/", "%2F").replace("(", "%28").replace(")", "%29")\
                .replace(" ", "+").replace("\"", "%22").replace("$", "%24")
            url = base + query + "&d=PTXT"

            # parse the query result
            key_result = USPTO_tool.analyze_url(url)
            print("incoming patents: %s" % str(len(key_result)))

            # remove duplicate entry
            for result in key_result:
                if result in pat_list:
                    pass
                else:
                    pat_list.append(result)
            print("unique patents: %s" % str(len(pat_list)))
    else:
        # Query with old keywords
        for key in old_query:
            # generate query link
            print("Querying %s %s %s" % (country, year, key))
            query = "isd/%s+AND+acn/%s+AND+(ttl/%s+OR+abst/%s+OR+aclm/%s)" % (year, country, key, key, key)
            query = query.replace("/", "%2F").replace("(", "%28").replace(")", "%29")\
                .replace(" ", "+").replace("\"", "%22").replace("$", "%24")
            url = base + query + "&d=PTXT"

            # Parse query result
            key_result = USPTO_tool.analyze_url(url)
            print("incoming patents: %s" % str(len(key_result)))

            # remove duplicate entry
            for result in key_result:
                if result in pat_list:
                    pass
                else:
                    pat_list.append(result)
            print("unique patents: %s" % str(len(pat_list)))

    # log module
    log = open("%s-%s.log" % (country, year), "w")
    for pat in pat_list:
        log.write(pat)
        log.write("\n")
    log.close()
    log = open("general.log", "a")
    log.write("%s\t%s\t%s\n" % (country, year, len(pat_list)))
    log.close()

if __name__ == "__main__":
    main()
