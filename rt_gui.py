from generator import Generator
from bayes import *
from tkinter import *
import time

W_WIDTH = 900
W_HEIGHT = 900

RUNNING = True
DELAY = 50

class Observer:
    def __init__(self, small_delta, big_delta):
        self.pred_signal = 0
        self.small_delta = small_delta
        self.big_delta = big_delta
        self.cur_conf = 0.5
        self.cur_signal = 0

    def process(self, signal):
        delta = {}
        if self.cur_signal == 0:
            delta = {"up":self.big_delta, "down": self.small_delta}
        else:
            delta = {"up":self.small_delta, "down": self.big_delta}
        if signal == self.cur_signal:
            tmp_p = prob_up(self.cur_conf, delta["up"])
        elif signal != self.cur_signal:
            tmp_p = prob_down(self.cur_conf, delta["down"])

        self.cur_conf = tmp_p

        if abs(self.cur_conf)<=0.1:
            self.cur_signal = abs(1 - self.cur_signal)
            self.cur_conf = 1.0

    def update_deltas(self, small_delta, big_delta):
        self.small_delta = small_delta
        self.big_delta = big_delta

def run(root, obs, gen, pred, real):
    if RUNNING:
        signal = gen.next()
        print('{} {} {}'.format(signal, obs.cur_signal, obs.cur_conf))
        if gen.cur_signal >= 0.9:
            real['text'] = "MOVE"
        else:
            real['text'] = "STOP"
        obs.process(signal)
        pred['text'] = obs.cur_signal
        if obs.cur_signal == 1:
            pred['text'] = "MOVE"
        else:
            pred['text'] = "STOP"
    root.after(DELAY, run, root, obs, gen, pred, real)

def switch_running():
    global RUNNING
    RUNNING = not RUNNING

def main():
    root = Tk()
    root.title('Figure 1')
    root.protocol('WM_DELETE_WINDOW', lambda: root.quit()) # обработчик закрытия окна
    # root.resizable(False, False)

    rho_label = Label(root, text="rho")
    rho_label.grid(row=0, column=0)
    rho_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.1)
    rho_scale.set(0.9)
    rho_scale.grid(row=0, column=1)

    small_delta_label = Label(root, text="small delta")
    small_delta_label.grid(row=1, column=0)
    small_delta_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.1)
    small_delta_scale.set(0.5)
    small_delta_scale.grid(row=1, column=1)

    big_delta_label = Label(root, text="big delta")
    big_delta_label.grid(row=2, column=0)
    big_delta_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.1)
    big_delta_scale.set(0.9)
    big_delta_scale.grid(row=2, column=1)

    real_label = Label(root, text="real")
    real_label.grid(row=0, column=2)
    real_label2 = Label(root, text="MOVE", width=50)
    real_label2.grid(row=1, column=2, rowspan=2)

    pred_label = Label(root, text="pred")
    pred_label.grid(row=0, column=3)
    pred_label2 = Label(root, text="STOP", width=50)
    pred_label2.grid(row=1, column=3, rowspan=2)

    obs = Observer(small_delta_scale.get(),big_delta_scale.get())
    gen = Generator(rho_scale.get(), 50, (0,1))

    start_button = Button(root, text="Start", command=lambda:switch_running())
    start_button.grid(row=3, column=1)

    root.bind("<Return>", lambda ev: switch_running())
    root.bind("r", lambda ev: obs.update_deltas(small_delta_scale.get(), big_delta_scale.get()))

    root.after(0, run, root, obs, gen, pred_label2, real_label2)
    root.mainloop()

if __name__ == "__main__":
    main()