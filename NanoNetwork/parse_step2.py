import xlrd
import pickle

CAS_replace = r"C:\Users\zhuhy\Desktop\Nano Network\CAS\Chinese Academy of Sciences.xlsx"
CHINA_cities = r"C:\Users\zhuhy\Desktop\Nano Network\china_cities.txt"
US_cities = r'C:\Users\zhuhy\Desktop\Nano Network\us_cities.txt'

cas_wb = xlrd.open_workbook(CAS_replace)
cas_ws = cas_wb.sheet_by_index(0)
cas_aliases = cas_ws.col_values(1, 0)

f = open(CHINA_cities, 'r', encoding='utf8')
CN_cities = f.readlines()
CN_cities = [x.upper().strip() for x in CN_cities]
CN_entites = ["KUANG CHI", "HUAZHONG", "BEIHANG", "FOXCONN", "FUDAN", "JIMEI", "SINOPEC", " PLA", "PLA ",
              "HARBIN", "NANKAI", "TONGJI", "XIAN", "CNOOC", "URUMQI", "KUNSHAN", "CN ACAD AGRICULTURAL MECH",
              "STATE GRID", "HUANGHUAI", "SANXING", "HUADONG", "HUANAN", "HUABEI", "BENGBU", "INNER MONGOLIA",
              "ZHANGJIAGANG", "QINGHUANGDAO", "SINO", "YINCHUAN", "ZHONGYUAN", "CATAS", "LUDONG", "YUYAO",
              "NATIONAL UNIV OF DEFENSE TECH", "QIINGHUA", "QILU", "PEOPLE"]
CN_cities += CN_entites
f.close()

abbr = {"UNIVERSITY": "UNIV", "INDUSTRY": "IND", "SCIENCE": "SCI", "TECHNOLOGY": "TECH",
        "INSTITUTE": "INST", "INSTITUTION": "INST", "INDUSTRIAL": "IND"}

cty_dict = {
    "KOREA": "KR", "SEOUL": "KR", "JAPAN": "JP", "NIPPON": "JP", "NIHHON": "JP", "NISSIN": "JP", "HITACHI": "JP",
    "TOHOKU": "JP", "NISSHIN": "JP", "SHINSHU": "JP", "OSAKA": "JP", "FRENCH": "FR", "FRANCE": "FR", "ONTARIO": "CA",
    "SINGAPORE": "SG", "KYOTO": "JP", "QUEBEC": "CA", "SONY": "JP", "TOKYO": "JP", "TOYOTA": "JP", "TOSHIBA": "JP",
    "NAGOYA": "JP", "SAMSUNG": "KR", "UNIV OF CAMBRIDGE": "UK", "UNIV OF OXFORD": "UK", "YONSEI": "KR", "DELI": "IN",
    "CHUNG ANG": "KR"
}

us_states = [
    'Alabama','Alaska','Arizona','Arkansas','California','Colorado',
    'Connecticut','Delaware','Florida','Georgia','Hawaii','Idaho', 'Hawai i',
    'Illinois','Indiana','Iowa','Kansas','Kentucky','Louisiana',
    'Maine','Maryland','Massachusetts','Michigan','Minnesota',
    'Mississippi', 'Missouri','Montana','Nebraska','Nevada',
    'New Hampshire','New Jersey','New Mexico','New York',
    'North Carolina','North Dakota','Ohio','Oklahoma','Oregon','Pennsylvania','Rhode Island',
    'South Carolina','South Dakota','Tennessee','Texas','Utah','Vermont','Virginia','Washington','West Virginia',
    'Wisconsin','Wyoming', 'United States', 'America', 'US ', 'USA']
us_states = [x.upper() for x in us_states]
f = open(US_cities, 'r', encoding='utf8')
for line in f:
    us_states.append(line.upper().strip())
f.close()
US_entities = ["BOSTON", "HARVARD", "HOUSTON", "STANFORD", "CINCINNATI", "NNCRYSTAL", "RUTGERS"]
us_states += US_entities
us_states = list(set(us_states))

f = open("Parse-Step1.pkl" ,'rb')
col_SIPO, col_USPTO, entity_dict = pickle.load(f)
f.close()

f = open("cn_unknown.csv", 'r')
for line in f:
    a = line.split(",")[0].strip()
    b = line.split(",")[1].strip()
    entity_dict[a] = b
f.close()
f = open("us_unknown.csv", 'r')
for line in f:
    a = line.split(",")[0].strip()
    b = line.split(",")[1].strip()
    entity_dict[a] = b
f.close()

for col in col_SIPO:
    for a in col:
        sa = a.strip()
        flag = False
        for d in entity_dict.keys():
            if sa in d:
                flag = True
                entity_dict[sa] = entity_dict[d]
                break
        if not flag:
            for cn in CN_cities:
                if cn in sa:
                    flag = True
                    entity_dict[sa] = 'CN'
                    break
            if not flag:
                for us in us_states:
                    if us in sa:
                        flag = True
                        entity_dict[sa] = 'US'
                        break
                if not flag:
                    for cty in cty_dict.keys():
                        if cty in sa:
                            flag = True
                            entity_dict[sa] = cty_dict[cty]
                            break

for col in col_USPTO:
    for a in col:
        sa = a.strip()
        flag = False
        for d in entity_dict.keys():
            if sa in d:
                flag = True
                entity_dict[sa] = entity_dict[d]
                break
        if not flag:
            for cn in CN_cities:
                if cn in sa:
                    flag = True
                    entity_dict[sa] = 'CN'
                    break
            if not flag:
                for us in us_states:
                    if us in sa:
                        flag = True
                        entity_dict[sa] = 'US'
                        break
                if not flag:
                    for cty in cty_dict.keys():
                        if cty in sa:
                            flag = True
                            entity_dict[sa] = cty_dict[cty]
                            break

entity_domain_dict = {}

for d in entity_dict.keys():
    flag = False
    for a in ["UNIV", "INST", "ACADEM", "ECOL", "NATIONAL", "COLLEGE"]:
        if a in d:
            entity_domain_dict[d] = 'ACA'
            flag = True
    if not flag:
        entity_domain_dict[d] = 'IND'

f = open("entity_dict.pkl", "wb")
pickle.dump((entity_dict, entity_domain_dict), f)
f.close()