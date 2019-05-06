import matplotlib.pyplot as plt
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

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

# signals = [1,0,0,0,0,1,1,0,0,1]
# signals = [1,1,1,1,1,1,1,1,1,1]
# signals += [1,1,1,1,1,1,1,1,1,1]
# signals += [0,0,0,0,0,0,0,0,0,0]
# signals += [0,0,0,0,0,0,0,0,0,0]
# signals += [1,1,1,1,1,1,1,1,1,1]
# signals += [1,1,1,1,1,1,1,1,1,1]
# signals += [1,1,1,1,1,1,1,1,1,1]
# signals += [0,0,0,0,0,0,0,0,0,0]
# signals += [0,0,0,0,0,0,0,0,0,0]
# signals += [1,1]
# signals += [0,0,0,0,0,0,0,0,0,0]
# signals += [0,0,0,0,0,0,0,0,0,0]
# signals += [1,1,1,1,1,1]
# signals += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
# signals += [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# signals += [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
# signals += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
from generator import Generator

def gen_plot(rho, n, fig, delta, count, res_label):
    print('rho', rho)
    print('n', n)
    print('delta', delta)
    g = Generator(rho, n, (0,1))

    signals = []
    realsignals = []
    for _ in range(count):
        signals.append(g.next())
        realsignals.append(g.cur_signal)

    prev_p = 0.1

    probs = []
    probs_bayes = []
    # diffs = []

    cur_signals = []
    cur_signal = 1
    counter = 0

    for s in signals:
        if s == cur_signal:
            tmp_p = prob_up(prev_p, delta)
        elif s != cur_signal:
            tmp_p = prob_down(prev_p, delta)
        bayes_p = prob(tmp_p, rho)
        # diffs.append(abs(tmp_p - prev_p))
        prev_p = tmp_p
        probs.append(prev_p)
        probs_bayes.append(bayes_p)
        # print(counter, "cursign:", bayes_p, cur_signal)
        if bayes_p <= 0.2:
            cur_signal = abs(1 - cur_signal)
            prev_p = 1 - prev_p
            # print(counter, "new:", bayes_p, cur_signal)
        cur_signals.append(cur_signal)
        counter += 1

    fig.clear()
    plt.xlabel("Время симуляции")
    plt.ylabel("Уверенность")
    plt.plot(probs, 'go-', label='confidence')
    plt.plot(probs_bayes, 'bo-', label='confidence corrected')
    plt.plot([x+0.01 for x in cur_signals], 'ro', label='current signal')
    plt.plot([x-0.01 for x in signals], 'yo', label='generated signal')
    plt.plot(realsignals, 'mo', label='real signal')
    plt.legend()

    fig.canvas.draw()

    accuracy = accuracy_score(realsignals, cur_signals)
    precision = precision_score(realsignals, cur_signals)
    recall = recall_score(realsignals, cur_signals)
    f1 = f1_score(realsignals, cur_signals)

    res_label['text'] = 'accuracy: {:.3}'.format(accuracy) + "\nprecision: {:.3}".format(precision) + '\nrecall: {:.3}'.format(recall) + '\nf1: {:.3}'.format(f1)