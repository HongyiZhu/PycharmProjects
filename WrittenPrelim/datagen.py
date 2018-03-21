import pickle
import numpy as np
np.random.seed(1024)

def gen_filter(t):
    push_t = np.random.randint(1, 2)
    pull_t = np.random.randint(1, 2)
    use_t = np.random.randint(2, 8)
    total = push_t + pull_t + use_t
    empty_t = np.random.randint(0, t - total, 1).tolist()[0]
    x = [0] * empty_t + [5] * push_t + [0] * use_t + [6] * pull_t + [0] * (t - total - empty_t)
    y = [0] * empty_t + [21] * (push_t + pull_t + use_t) + [0] * (t - total - empty_t)
    return x, y

def gen_pill(t):
    push_t = np.random.randint(1, 2)
    pull_t = np.random.randint(1, 2)
    use_t = np.random.randint(2, min(8,t-push_t-pull_t))
    total = push_t + pull_t + use_t
    if t > total:
        empty_t = np.random.randint(0, t - total)
    else:
        empty_t = 0
    x = [0] * empty_t + [9] * push_t + [0] * use_t + [10] * pull_t + [0] * (t - total - empty_t)
    y = [0] * empty_t + [22] * (push_t + pull_t + use_t) + [0] * (t - total - empty_t)

    return x, y

def gen_water_pill(t):
    if np.random.randint(2) == 0:
        t0 = np.random.randint(10, 15)
        x1, y1 = gen_filter(t0)
        x2, y2 = gen_pill(t - t0)
        x = x1 + x2
        y = y1 + y2
        n = [i for i in range(len(y)) if y[i] != 0]
        i = min(n)
        j = max(n) + 1
        for k in range(i, j):
            y[k] = 22
    else:
        t0 = np.random.randint(10, 15)
        x2, y2 = gen_filter(t0)
        x1, y1 = gen_pill(t - t0)
        x = x1 + x2
        y = y1 + y2
        n = [i for i in range(len(y)) if y[i] != 0]
        i = min(n)
        j = max(n) + 1
        for k in range(i, j):
            y[k] = 22
    return x, y

def wrap_cabinet(t):
    a = np.random.randint(3)
    b = np.random.randint(3)
    mid = t - a - b
    if np.random.randint(2) == 0:
        x1, y1 = gen_pill(mid)
    else:
        x1, y1 = gen_water_pill(mid)

    x = [15] * a + x1 + [16] * b
    y = [22] * t

    return x, y

def gen_medi(t):
    a = np.random.randint(3)
    if a % 3 == 0:
        x, y = gen_pill(t)
    elif a % 3 == 1:
        x, y = gen_water_pill(t)
    else:
        x, y = wrap_cabinet(t)
    return x, y

def gen_hyg(t):
    push_t = np.random.randint(1, 4)
    pull_t = np.random.randint(1, 4)
    use_t = np.random.randint(10, t - push_t - pull_t)
    total = push_t + pull_t + use_t
    empty_t = np.random.randint(0, t - total, 1).tolist()[0]
    x = [0] * empty_t + [19] * push_t + [0] * use_t + [20] * pull_t + [0] * (t - total - empty_t)
    y = [0] * empty_t + [23] * (push_t + pull_t + use_t) + [0] * (t - total - empty_t)

    return x, y

def wrap_filter(t):
    a = np.random.randint(3)
    b = np.random.randint(3)
    mid = t - a - b
    if np.random.randint(2) == 0:
        x1, y1 = gen_fridge(mid)
    else:
        x1, y1 = gen_fridge(mid)

    x = [5] * a + x1 + [6] * b
    y = [21] * t

    return x, y

def gen_fridge_sub(t):
    push_t = np.random.randint(1, 4)
    pull_t = np.random.randint(1, 4)
    if t - push_t - pull_t <= 3:
        return [0] * t, [0] * t
    else:
        use_t = np.random.randint(3, t - push_t - pull_t)
        total = push_t + pull_t + use_t
        empty_t = np.random.randint(0, t - total)
        x = [0] * empty_t + [3] * push_t + [0] * use_t + [4] * pull_t + [0] * (t - total - empty_t)
        y = [0] * empty_t + [21] * (push_t + pull_t + use_t) + [0] * (t - total - empty_t)
        return x, y

def gen_fridge(t):
    a = np.random.randint(3)
    if a % 3 == 0:
        x, y = gen_fridge_sub(t)
    elif a % 3 == 1:
        x1, y1 = gen_fridge_sub(int(t / 2))
        x2, y2 = gen_fridge_sub(t - int(t / 2))
        x = x1 + x2
        y = y1 + y2
        n = [i for i in range(len(y)) if y[i] != 0]
        if not len(n) == 0:
            i = min(n)
            j = max(n) + 1
            for k in range(i, j):
                y[k] = 21
    else:
        x1, y1 = gen_fridge_sub(int(t / 3))
        x2, y2 = gen_fridge_sub(int(t / 3))
        x3, y3 = gen_fridge_sub(t - 2 * int(t / 3))
        x = x1 + x2 + x3
        y = y1 + y2 + y3
        n = [i for i in range(len(y)) if y[i] != 0]
        if not len(n) == 0:
            i = min(n)
            j = max(n) + 1
            for k in range(i, j):
                y[k] = 21
    return x, y


def gen_food(t):
    a = np.random.randint(3)
    if a % 3 == 0:
        x, y = gen_filter(t)
    elif a % 3 == 1:
        x, y = gen_fridge(t)
    else:
        x, y = wrap_filter(t)
    return x, y

def gen_data():
    a = 0
    x = []
    y = []
    while a < 500:
        if 500 - a <= 20:
            b = 500 - a
            x += [0] * b
            y += [0] * b
            a = 500
        else:
            b = np.random.randint(20, 500-a)
            if b % 3 == 0:
                x1, y1 = gen_food(b)
            elif b % 3 == 1:
                x1, y1 = gen_medi(b)
            else:
                x1, y1 = gen_hyg(b)
            x += x1
            y += y1
            a += b
    return x, y

x = []
y = []
for i in range(1000):
    x1, y1 = gen_data()
    x.append(x1)
    y.append(y1)
f = open("x.txt", "wb")
g = open("y.txt", "wb")
pickle.dump(x, f)
pickle.dump(y, g)
f.close()
g.close()


