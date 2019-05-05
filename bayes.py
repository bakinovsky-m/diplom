import matplotlib.pyplot as plt

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

def gen_plot(rho, n, fig, delta, count):
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
        probs_bayes.append(bayes_p -0.01)
        # print(counter, "cursign:", bayes_p, cur_signal)
        if bayes_p <= 0.2:
            cur_signal = abs(1 - cur_signal)
            prev_p = 1 - prev_p
            print(counter, "new:", bayes_p, cur_signal)
        cur_signals.append(cur_signal + .01)
        counter += 1

    fig.clear()
    plt.xlabel("Время симуляции")
    plt.ylabel("Уверенность")
    plt.plot(probs, 'go-')
    plt.plot(probs_bayes, 'bo-')
    plt.plot(cur_signals, 'ro')
    plt.plot(signals, 'yo')
    plt.plot(realsignals, 'mo')

    # plt.show()
    fig.canvas.draw()