__author__ = 'Hongyi'

country = ["CU=USA", "(CU=Czech Republic or CU=England or CU=Austria or CU=Belgium or CU=Bulgaria or CU=Cyprus or CU=Denmark "
                     "or CU=Estonia or CU=Finland or CU=France or CU=Germany or CU=Greece or CU=Hungary or CU=Ireland "
                     "or CU=Italy or CU=Latvia or CU=Lithuania or CU=Luxembourg or CU=Malta or CU=Netherlands or CU=Poland "
                     "or CU=Portugal or CU=Romania or CU=Slovakia or CU=Slovenia or CU=Spain or CU=Sweden)",
           "CU=Japan", "CU=China"]

# for year in range(2000, 2015):
#     for i in range(4):
#         query = "PY={0} and (SO=NATURE or SO=\"PROCEEDINGS OF THE NATIONAL ACADEMY OF SCIENCES OF THE UNITED STATES OF AMERICA\" or SO=SCIENCE) " \
#                 "and (TS=\"atomic force microscope\" or TS=\"atomic force microscopic\" or TS=\"atomic force microscopy\" or TS=\"atomic-force-microscope\" " \
#                 "or TS=\"atomic-force-microscopy\" or TS=\"atomistic simulation\" or TS=\"biomotor\" or TS=\"molecular device\" or TS=\"molecular electronics\" " \
#                 "or TS=\"molecular modeling\" or TS=\"molecular motor\" or TS=\"molecular sensor\" or TS=\"molecular simulation\" or TS=\"nano*\" " \
#                 "or TS=\"quantum computing\" or TS=\"quantum dot*\" or TS=\"quantum effect*\" or TS=\"scanning tunneling microscope\" " \
#                 "or TS=\"scanning tunneling microscopic\" or TS=\"scanning tunneling microscopy\" or TS=\"scanning-tunneling-microscope\" " \
#                 "or TS=\"scanning-tunneling-microscopy\" or TS=\"self assembled\" or TS=\"self assembling\" or TS=\"self assembly\" or TS=\"selfassembl*\" " \
#                 "or TS=\"self-assembled\" or TS=\"self-assembling\" or TS=\"self-assembly\") and {1}".format(year, country[i])
#         print(query)

for year in range(2000, 2015):
    query = "PY={0} " \
            "and (TS=\"atomic force microscope\" or TS=\"atomic force microscopic\" or TS=\"atomic force microscopy\" or TS=\"atomic-force-microscope\" " \
            "or TS=\"atomic-force-microscopy\" or TS=\"atomistic simulation\" or TS=\"biomotor\" or TS=\"molecular device\" or TS=\"molecular electronics\" " \
            "or TS=\"molecular modeling\" or TS=\"molecular motor\" or TS=\"molecular sensor\" or TS=\"molecular simulation\" or TS=\"nano*\" " \
            "or TS=\"quantum computing\" or TS=\"quantum dot*\" or TS=\"quantum effect*\" or TS=\"scanning tunneling microscope\" " \
            "or TS=\"scanning tunneling microscopic\" or TS=\"scanning tunneling microscopy\" or TS=\"scanning-tunneling-microscope\" " \
            "or TS=\"scanning-tunneling-microscopy\" or TS=\"self assembled\" or TS=\"self assembling\" or TS=\"self assembly\" or TS=\"selfassembl*\" " \
            "or TS=\"self-assembled\" or TS=\"self-assembling\" or TS=\"self-assembly\")".format(year)
    print(query)