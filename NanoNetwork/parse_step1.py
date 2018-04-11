import xlrd
import re

SIPO_file = r"C:\Users\zhuhy\Desktop\Nano Network\nanotech data\SIPO-59970\SIPO 1-59970.xlsx"
USPTO_file = r"C:\Users\zhuhy\Desktop\Nano Network\nanotech data\USPTO-37508\USPTO 1-37508.xlsx"
SIPO_text = r"C:\Users\zhuhy\Desktop\Nano Network\SIPO.txt"
USPTO_text = r"C:\Users\zhuhy\Desktop\Nano Network\USPTO.txt"

entity_country_dict = {}

SIPO_wb = xlrd.open_workbook(SIPO_file)
SIPO_ws = SIPO_wb.sheet_by_index(0)
SIPO_PAH = SIPO_ws.col_values(19, 1)

USPTO_wb = xlrd.open_workbook(USPTO_file)
USPTO_ws = USPTO_wb.sheet_by_index(0)
USPTO_PAH = USPTO_ws.col_values(17, 1)


def parsePAH(pah):
    for record in pah:
        for line in record.split("\n"):
            regex = re.compile(r'(.+)\(\[(\w+)\]\)')
            z = re.match(regex, line)
            if z:
                entity = z.group(1).strip().upper().split(";")[0]
                country = z.group(2).upper()
                if entity not in entity_country_dict.keys():
                    entity_country_dict[entity] = country

parsePAH(USPTO_PAH)
parsePAH(SIPO_PAH)

f = open(SIPO_text, 'r', encoding='utf8')
g = open(USPTO_text, 'r', encoding='utf8')

f.readline()
f.readline()
g.readline()
g.readline()

SIPO_line = f.readline()
USPTO_line = g.readline()

collaborated_SIPO = []
collaborated_USPTO = []
temp_list = []
while SIPO_line[:2] != 'EF':
    if SIPO_line[:3] == "AU ":
        temp_list.append(SIPO_line[3:].strip().upper())
        SIPO_line = f.readline()
        while SIPO_line[:3] == "   ":
            temp_list.append(SIPO_line[3:].strip().upper())
            SIPO_line = f.readline()
        if len(temp_list) > 1:
            collaborated_SIPO.append(temp_list)
        else:
            SIPO_line = f.readline()
    else:
        SIPO_line = f.readline()
    temp_list = []

while USPTO_line[:2] != 'EF':
    if USPTO_line[:3] == "AU ":
        temp_list.append(USPTO_line[3:].strip().upper())
        USPTO_line = g.readline()
        while USPTO_line[:3] == "   ":
            temp_list.append(USPTO_line[3:].strip().upper())
            USPTO_line = g.readline()
        if len(temp_list) > 1:
            collaborated_USPTO.append(temp_list)
        else:
            USPTO_line = g.readline()
    else:
        USPTO_line = g.readline()
    temp_list = []

f.close()
g.close()
