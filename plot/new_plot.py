__author__ = 'Hongyi'

import csv
import matplotlib.pyplot as plt

f = open("D:/sensors/S2.csv")
S1 = csv.DictReader(f)
m_x = []
m_y = []
m_z = []
m_t = []
o_x = []
o_y = []
o_z = []
o_t = []
for line in S1:
    if 'EB99' in line['sensor_id']:
        m_x.append(int(line['accer_x']))
        m_y.append(int(line['accer_y']))
        m_z.append(int(line['accer_z']))
        m_t.append(float(line['event_timestamp']))
    else:
        o_x.append(int(line['accer_x']))
        o_y.append(int(line['accer_y']))
        o_z.append(int(line['accer_z']))
        o_t.append(float(line['event_timestamp']))
y = min(m_t)
m_t = [x - y for x in m_t]
o_t = [x - y for x in o_t]

ax = plt.subplot(111)
ax.set_xlabel('$Time (s)$')
ax.set_ylabel(r'$Acceleration\/Unit$')
line_x, = ax.plot(m_t, m_x, 'D--', color='0.65', label="$x-axis$")
line_y, = ax.plot(m_t, m_y, 'o--', color='0.8', label="$y-axis$")
line_z, = ax.plot(m_t, m_z, 's--', color='0.45', label="$z-axis$")
line_o, = ax.plot(o_t, o_x, '*-', ms=10, color='0', label="$object$")
# plt.legend(handles=[line_x, line_y, line_z, line_o])
box = ax.get_position()
ax.set_position([box.x0, box.y0, box.width * 0.85, box.height])
plt.legend(loc='center left', bbox_to_anchor=(1, 0.5), fancybox=True, shadow=True)
plt.show()
