from generator import Generator
from bayes import *
import time
import scipy.signal as scs

class Observer:
    def __init__(self, low_delta, high_delta):
        self.low_delta = low_delta
        self.high_delta = high_delta
        self.cur_conf = 0.9
        self.cur_signal = 0
        self.border = 0.1

    def process(self, signal):
        delta = {}
        if self.cur_signal == 0:
            delta = {"up":self.high_delta, "down": self.low_delta}
        else:
            delta = {"up":self.low_delta, "down": self.high_delta}
        if signal == self.cur_signal:
            tmp_p = conf_up(self.cur_conf, delta["up"])
        elif signal != self.cur_signal:
            tmp_p = conf_down(self.cur_conf, delta["down"])

        self.cur_conf = tmp_p

        if abs(self.cur_conf)<=self.border:
            self.cur_signal = abs(1 - self.cur_signal)
            self.cur_conf = 1.0

IMP_WEIGHT = 1
NOT_IMP_WEIGHT = 0.5
IMPORTANT_A = (0,)
MONOTON_CONST = 1.0
MONOTON_PLUS = 0.1


def wHemmingDist(a_list, b_list):
    res = 0
    monotonic = 0
    prev = 0
    for a,b in zip(a_list, b_list):
        if prev == a:
            monotonic += MONOTON_PLUS
        else:
            monotonic = MONOTON_CONST

        if a!=b:
            if a in IMPORTANT_A:
                res += IMP_WEIGHT * monotonic
            else:
                res += NOT_IMP_WEIGHT * monotonic
        prev = a
    return res  


rho = 0.9
N = 300
SIGNALS = (0,1)

# best_score = {'small':0, 'big':0, 'score':100}

window = scs.exponential(15)

start = time.time()

rho_num = True

for rho in range(50,100,5):
    rho = rho/100
    smalls = []
    bigs = []
    scores = []
    # ex_scores = []
    for _ in range(10):
        rho_num = True
        best_score = {'small':0, 'big':0, 'score':100}
        for sm in range(50,100,2):
            small = sm / 100
            for b in range(50,100,2):
                big = b / 100
                small_to_gen = small
                big_to_gen = big
                if small > big:
                    small_to_gen, big_to_gen = big_to_gen, small_to_gen


                t = []
                q = []
                exx = []
                signals = []
                g = Generator(rho, N, SIGNALS)
                obs = Observer(small_to_gen, big_to_gen)
                for i in range(5000):
                    signal = g.next()
                    signals.append(signal)
                    obs.process(signal)
                    t.append(g.cur_signal)
                    q.append(obs.cur_signal)
                        

                score = wHemmingDist(t,q) / len(t)
                if score < best_score['score']:
                    best_score['small'] = small_to_gen
                    best_score['big'] = big_to_gen
                    best_score['score'] = score
            
        # print("small:", best_score['small'], 'big:', best_score['big'], 'score:', best_score['score'])
        smalls.append(best_score['small'])
        bigs.append(best_score['big'])
        scores.append(best_score['score'])
        # ex_scores.append(best_score['ex_score'])

    av_big = sum(bigs) / len(bigs)
    av_small = sum(smalls) / len(smalls)
    av_score = sum(scores) / len(scores)
    # print(ex_scores)
    # av_ex_score = sum(ex_scores) / len(ex_scores)
    # print("average big:", av_big, "average small:", av_small)
    print('rho: {:0.3}, average small: {:0.3}, average big: {:0.3}, average score: {:0.4}'.format(rho, av_small, av_big, av_score))
    # print('ex:', av_ex_score)


end = time.time()

print('time elapsed: {} sec'.format(end - start))