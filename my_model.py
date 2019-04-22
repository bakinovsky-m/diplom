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

# signals = [1,1,-1,1,1,1,-1,1,-1,1,1,1,1,1,-1,1,1,1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]
# signals = [0,0,0,0,0,0,0,1,0,1,0,0,0,1,1,1,1,1,0,1,1,1,1,1,1,1,1,1]
# signals = [0,0,0,0,0,1,0,0,1,0,0,1,0,0,0,0,1,1,1,0,0,0,1,0,0,0,1,1,0,0]
# signals = [1,1,1,1,0,0,1,1,0,1,1,1,1,1]
# signals = [1,2,3,2,2,2,2,2,4,2,2,4,5,2,2,2,2,3,4,3,2,2,2,2,2,2,2,2,2,]
# signals = [1,2,3]
if __name__ == "__main__":
# signals += [0,0,0,0,0,0,0,0,0,0,0,0]
# signals += [0,0,0,0,0,0,0,0,0,0,0,0]
# signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    signals = [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    signals += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    signals += [1,1,1,1,0,0,0,0,0,0,1,1,1,1,1,1,1,1,1,1]
    signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    # signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    # signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    # signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    # signals += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    # signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    # signals += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    signals += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    # signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    # signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    # signals += [0,0,0,0,0,0,0,0,0,0,0,0]
    # signals += [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
    # signals += [0,0,0,0,0,0,0,0,0,0,0,0]

    probs = []
    # probs2 = []
    diffs = []

    first_signal = True
    # prev_p = 0.0000000001
    prev_p = 0.1

    for signal in signals:
        if signal == 1:
            tmp_p = prob_up(prev_p)
        elif signal == 0:
            tmp_p = prob_down(prev_p)

        diffs.append(abs(tmp_p - prev_p))
        prev_p = tmp_p
        probs.append(prev_p)
        # print(prev_p)

    plt.plot(probs, 'go-')
    plt.plot(diffs, 'ro-')

    plt.show()