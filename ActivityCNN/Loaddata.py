import pickle

f = open('datadump.txt', 'rb')
tr, va, te = pickle.load(f)

print(tr)
print(va)
print(te)