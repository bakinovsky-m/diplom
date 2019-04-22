import matplotlib.pyplot as plt

DELTA = 0.3

def prob_up(prev):
    res = abs(prev + abs(prev) * DELTA)
    # res = abs(prev + abs(prev) * DELTA)
    if res >= 1:
        return 0.99
    # return abs(prev + abs(prev) * DELTA)
    return res

def prob_down(prev):
    res = abs(prev - (1 - abs(prev)) * DELTA)
    if res >= 1:
        return 0.99
    # return abs(prev - (1 - abs(prev)) * DELTA)
    return res

PROB_B_T = 0.9


def prob(p_t):
    p_b = PROB_B_T * p_t + (1 - PROB_B_T) * (1 - p_t)
    return PROB_B_T * p_t / p_b

signals = [1,0,0,0,0,1,1,0,0,0,0,0,0]
signals += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
signals += [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]

prev_p = 0.1

probs = []
probs_bayes = []
diffs = []

for s in signals:
    if s == 1:
        tmp_p = prob_up(prev_p)
    elif s == 0:
        tmp_p = prob_down(prev_p)
    bayes_p = prob(tmp_p)
    diffs.append(abs(tmp_p - prev_p))
    prev_p = tmp_p
    probs.append(prev_p)
    probs_bayes.append(bayes_p)


plt.plot(probs, 'go-')
plt.plot(probs_bayes, 'bo-')
plt.plot(diffs, 'ro-')

plt.show()
# a = {}

# counter = 0
# while counter <= 1000:
#     for i in range(0, 10):
#         try:
#             a[i] == None
#         except KeyError:
#             a[i] = []
#         a[i].append(prob(i, random.uniform(0.8, 0.99)))
#     counter += 1

# qwe = {}
# for k, v in a.items():
#     mean = 0
#     for i in v:
#         mean += i
#     mean /= len(v)
#     qwe[k] = mean

# for k, v in qwe.items():
#     print(k, ": ", v)