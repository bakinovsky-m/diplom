import random

PROB_B_T = 0.9

def prob_t(t):
    return (1/2) ** t
    # return 1/2

def prob(t, p_b_t):
    t = t + 1
    p_t = prob_t(t)
    p_b = p_b_t * p_t + (1 - p_b_t) * (1 - p_t)
    return p_b_t * p_t / p_b

a = {}

counter = 0
while counter <= 1000:
    for i in range(0, 10):
        try:
            a[i] == None
        except KeyError:
            a[i] = []
        a[i].append(prob(i, random.uniform(0.8, 0.99)))
    counter += 1

qwe = {}
for k, v in a.items():
    mean = 0
    for i in v:
        mean += i
    mean /= len(v)
    qwe[k] = mean

for k, v in qwe.items():
    print(k, ": ", v)