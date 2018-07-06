import os
import shutil

path = r"C:/Users/zhuhy/Desktop/test"

KEYWORDS = ["nano", "self-assembl", "self assembl", "atomic force microscop", "atomic-force-microscop",
            "scanning-tunneling-microscop", "scanning tunneling microscop", "atomistic simulation", "biomotor",
            "molecular device", "molecular electronics", "molecular modeling", "molecular motor", "molecular sensor",
            "molecular simulation", "quantum computing", "quantum dot", "quantum effect", "plasmonic", "meta-material",
            "metamaterial", "spintronic", "molecular system", "supramolecul", "fullerene", "dendrimer", "graphen",
            "two-dimensional material", "atom thick layer", "2D AND material", "atom layer deposition",
            "2D AND material", "atom layer deposition", "artificial photosynthes", "cellulose fiber", "cellulose tube",
            "optoelectronic", "opto-electronic", "bio-photonics", "biophotonic", "opto-genetic", "optogenetic",
            "DNA computing", "DNA assembling", "proteomic", "synthetic biolog", "mesoscale structure",
            "mesoscale phenomena", "mesoscale science", "mesoscale engineering", "mesoscale model"]

for root, dirs, files in os.walk("D:/USPTO2017/"):
    for name in files:
        if name.split(".")[-1] == "json":
            file = os.path.join(root, name)
            f = open(file, encoding='utf8')
            s = f.read()
            f.close()
            for k in KEYWORDS:
                if k in s:
                    shutil.copy2(file, os.path.join("E:/Patent2017/", name))
                    break
    print(root)