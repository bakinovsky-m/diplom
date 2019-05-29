import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_auc_score
import numpy as np

DELTA = 0.8

def prob_up(prev, delta):
    res = prev + prev * delta
    if res >= 1:
        return 0.99
    return res

def prob_down(prev, delta):
    res = prev - (1 - prev) * delta
    if res <= 0:
        return 0.01
    return res

def prob(p_t, rho):
    p_b = rho * p_t + (1 - rho) * (1 - p_t)
    return rho * p_t / p_b

from generator import Generator

def trail_ma(t):
    return np.mean(t)

def gen_plot(rho, n, fig, delta_small, delta_big, count, res_label):
    g = Generator(rho, n, (0,1))

    signals = []
    realsignals = []
    for _ in range(count):
        signals.append(g.next())
        realsignals.append(g.cur_signal)

    prev_p = 0.1

    probs = []
    probs_bayes = []

    cur_signals = []
    cur_signal = 1
    counter = 0
    trail_mas = []

    for s in signals:
        delta = {}
        if cur_signal == 0:
            delta = {"up":delta_big, "down": delta_small}
        else:
            delta = {"up":delta_small, "down": delta_big}
        if s == cur_signal:
            tmp_p = prob_up(prev_p, delta["up"])
        elif s != cur_signal:
            tmp_p = prob_down(prev_p, delta["down"])
        bayes_p = prob(tmp_p, rho)
        prev_p = tmp_p
        probs.append(prev_p)
        probs_bayes.append(bayes_p)
        if bayes_p <= 0.2:
            cur_signal = abs(1 - cur_signal)
            prev_p = 1 - prev_p
        cur_signals.append(cur_signal)

        ma = 0
        if counter == 0:
            ma = trail_ma(s)
        elif counter == 1:
            ma = trail_ma((s, signals[counter-1]))
        elif counter == 2:
            ma = trail_ma((s, signals[counter-1], signals[counter-2]))
        else:
            ma = trail_ma(signals[counter - 3:counter])
        trail_mas.append(ma)

        counter +=1

    fig.clear()
    plt.xlabel("Время симуляции")
    plt.ylabel("Уверенность")
    plt.plot(probs, 'go-', label='confidence')
    # plt.plot(probs_bayes, 'bo-', label='confidence corrected')
    plt.plot([x+0.01 for x in cur_signals], 'ro', label='current signal')
    plt.plot([x-0.01 for x in signals], 'yo', label='generated signal')
    plt.plot(realsignals, 'mo', label='real signal')


    # qwe = [math.floor(t+0.5) for t in trail_mas]
    # plt.plot(qwe, 'o-', label='MA')
    # print(precision_score(realsignals, qwe))
    # print(recall_score(realsignals, qwe))
    # print(f1_score(realsignals, qwe))

    plt.legend()

    fig.canvas.draw()

    accuracy = accuracy_score(realsignals, cur_signals)
    precision = precision_score(realsignals, cur_signals)
    recall = recall_score(realsignals, cur_signals)
    f1 = f1_score(realsignals, cur_signals)
    roc_auc = roc_auc_score(realsignals, cur_signals)

    res_label['text'] = 'accuracy: {:.3}'.format(accuracy) + "\nprecision: {:.3}".format(precision) + '\nrecall: {:.3}'.format(recall) + '\nf1: {:.3}'.format(f1) + '\nroc_auc: {:.3}'.format(roc_auc)