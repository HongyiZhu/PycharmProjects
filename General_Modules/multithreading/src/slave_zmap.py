__author__ = 'zhuhy'

import sys
import pymysql
import subprocess
from subprocess import PIPE
import time

db = pymysql.connect(host="128.196.27.147",  # your host, usually localhost
                     user="ShodanTeam",  # your username
                     passwd="Sh0d@n7e",  # your password
                     db="shodan",
                     charset='utf8',
                     autocommit=True)  # name of the data base

cur_ip = db.cursor()
cur_port = db.cursor()
cur_ou = db.cursor()
ip_list = []
port_list = []


def main():
    """
    Executable body, call other functions from here
    :return: Exit code
    """
    arg1 = sys.argv[1]
    arg2 = sys.argv[2]
    f = open(arg1 + "_" + arg2 + "_out.log", "a")
    g = open(arg1 + "_" + arg2 + ".log", "a")

    try:
        cur_ip.execute("""
                    SELECT `ip`, `searchid`
                    FROM `shodan`.`scadashodan`
                    WHERE `portnum` = 80
                    LIMIT %s, %s;
                    """ % (sys.argv[1], str(int(sys.argv[2]) - int(sys.argv[1]) + 1)))
    except Exception as err:
        g.write("SQL ERROR: {0}\n".format(err))
        g.flush()
        exit(0)

    try:
        cur_port.execute("""
                    SELECT `port`
                    FROM `shodan`.`sy_scada_port_list`
                    ORDER BY port;
                    """)
    except Exception as err:
        g.write("SQL ERROR: {0}\n".format(err))
        g.flush()
        exit(0)

    ip_result = cur_ip.fetchall()
    #ip_result = [("128.196.27.147",1), ("128.196.27.170",2),("10.128.50.165",3), ("74.125.224.81",4)]
    port_result = cur_port.fetchall()
    #port_result = [(80,),(3306,),(102,)]
    for (result) in port_result:
        port_list.append(result[0])

    for (result) in ip_result:
        ip = result[0]
        id = result[1]

        proc_list = []

        # intitalize two lists
        port_check_list = [1 for i in range(len(port_list))]
        proc_list = [None for i in range(len(port_list))]
        port_string_list = []

        g.write("Scan IP: " + ip + "\n")
        g.flush()
        for i in range(len(port_check_list)):
            proc_list[i] = subprocess.Popen(["zmap", "-p", str(port_list[i]), "{0} -o -".format(ip)],
                                            stdout=PIPE,
                                            stderr=PIPE)  # create a scanning thread for the port

        # waiting for the scan
        while True:
            bigflag = True
            for i in range(len(port_list)):
                if port_check_list[i] == 1: # check this port
                    proc = proc_list[i]
                    flag = proc.poll()
                    if flag is None:
                        bigflag = False
                    else:
                        stdou, stderr = proc.communicate()
                        if stderr.decode("utf8").strip().find("hits: 100.00%") != -1:
                            port_string_list.append(str(port_list[i]))
                            port_check_list[i] = 0
                        elif stderr.decode("utf8").strip().find("0.00%") == -1:
                            proc_list[i] = subprocess.Popen(["zmap", "-p", str(port_list[i]), "{0} -o -".format(ip)],
                                                            stdout=PIPE,
                                                            stderr=PIPE)
                        else:
                            port_check_list[i] = 0
            if bigflag:
                break

        port_string = ";".join(port_string_list)
        port_string = port_string.strip()
        g.write("Open Ports: " + port_string + "\n")
        g.flush()

        if port_string != "":
            sql = """
                  INSERT INTO `shodan`.`zmap_verified_devices` (
                  `ip`, `timestamp`, `portlist`, `id`
                  ) VALUES (
                  '%s', '%s', '%s', '%s'
                  );
                  """ % (ip, time.time(), port_string, id)
            f.write(sql + "\n")
            f.flush()














if __name__ == "__main__":
    main()
