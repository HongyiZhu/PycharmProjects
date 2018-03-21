__author__ = 'Hongyi'

import pylab as plt

fig = plt.figure(figsize=(6, 4), dpi=300)
plt.title("Lexicon")
plt.xlim(0, 100)
plt.xlabel("Accuracy(%)")
plt.ylabel("Methods")

note = ['IH', 'NB', 'RF', 'Uni', 'Bi', 'Tri', 'OH', 'NB/k', 'RF/k']
value = [88.50, 85.30, 79.40, 45.80, 61.80, 58.20, 69.50, 47.50, 52.50]
category = [4, 4, 4, 3, 3, 3, 2, 1, 1]
methodtype = [1, 2, 2, 3, 3, 3, 1, 2, 2]
mk = ["o", "s", "^"]
cl = ["1", "0.66", "0.33", "0"]

for (n, v, c, m) in list(zip(note, value, category, methodtype)):
    print(n, v)
    plt.plot(v, c, color=cl[c-1], marker=mk[m-1], ls='None', ms=5)

plt.yticks(plt.arange(0, 6), ('', 'ML/k', 'OH', 'N-Gram', 'AZEmo', ''))

plt.show()


