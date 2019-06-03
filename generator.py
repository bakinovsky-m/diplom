import random as rand
import itertools

RHO = 0.9
N = 10
SIGNALS = [0,1]

class Generator:
    def __init__(self, rho, n, signals):
        self.rho = rho
        self.n = n
        self.cur_n = 0
        self.signals = itertools.cycle(signals)
        self.cur_signal = next(self.signals)

    def next(self):
        if self.cur_n == self.n:
            self.cur_signal = next(self.signals)
            self.cur_n = 0
        x = rand.random()
        res = 0
        if x <= self.rho:
            res = self.cur_signal
        else :
            res = abs(self.cur_signal-1)

        self.cur_n += 1
        return res

    def update_rho(self, new_rho):
        print('updated rho, new rho:', new_rho)
        self.rho = new_rho


if __name__ == '__main__':
    g = Generator(RHO, N, SIGNALS)
    for _ in range(20):
        print(g.next())