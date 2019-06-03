from generator import Generator
from bayes import *
from tkinter import *
from PIL import Image, ImageTk
import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('TkAgg')
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from datetime import datetime

W_WIDTH = 900
W_HEIGHT = 900

RUNNING = False
DELAY = 5

N = 300

GREEN_L = None # PhotoImage(file='green_light.jpg')
RED_L = None # PhotoImage(file='red_light.jpg')

IMPORTANT_A = (0,)

IMP_WEIGHT = 2
NOT_IMP_WEIGHT = 1

def levenshteinDistance(s1, s2):
    if len(s1) > len(s2):
        s1, s2 = s2, s1

    distances = range(len(s1) + 1)
    for i2, c2 in enumerate(s2):
        distances_ = [i2+1]
        for i1, c1 in enumerate(s1):
            if c1 == c2:
                distances_.append(distances[i1])
            else:
                distances_.append(1 + min((distances[i1], distances[i1 + 1], distances_[-1])))
        distances = distances_
    return distances[-1]

def hemmingDist(a_list,b_list):
    res = 0
    for a,b in zip(a_list, b_list):
        if a!=b:
            res += 1
    return res

def wHemmingDist(a_list, b_list):
    res = 0
    for a,b in zip(a_list, b_list):
        if a!=b:
            # res += 1
            if a in IMPORTANT_A:
                res += IMP_WEIGHT
            else:
                res += NOT_IMP_WEIGHT
    return res    

class Observer:
    def __init__(self, small_delta, big_delta):
        self.small_delta = small_delta
        self.big_delta = big_delta
        self.cur_conf = 0.9
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

ITER = 0

scores = []
ma_signals = []
ma_scores = []

def ma(lis):
    res = sum(lis)/len(lis)
    # return 
    if res >= 0.8:
        return 1
    else:
        return 0

gen_signals = []

def run(root, obs, gen, pred_label, real_label, stats_label, real_signals, pred_signals):
    if RUNNING:
        signal = gen.next()
        gen_signals.append(signal)
        if gen.cur_signal == 1:
            real_label['text'] = "MOVE"
            real_label['image'] = GREEN_L
        else:
            real_label['text'] = "STOP"
            real_label['image'] = RED_L
        obs.process(signal)
        if obs.cur_signal == 1:
            pred_label['text'] = "MOVE"
            pred_label['image'] = GREEN_L
        else:
            pred_label['text'] = "STOP"
            pred_label['image'] = RED_L
        # print('{} {} {}'.format(signal, obs.cur_signal, obs.cur_conf))
        # print('----------')
        global ITER
        # print("ITER", ITER)
        # print("real_label",gen.cur_signal)
        # print("sign",signal)
        # print("pred",obs.cur_signal, obs.cur_conf)
        # print('----------')

        real_signals.append(gen.cur_signal)
        pred_signals.append(obs.cur_signal)
        ma_signals.append(ma(gen_signals[-100:]))

        if ITER % 10 == 0:
            stats_label['text'] = "iter: " + str(ITER) + "\n"
            # score = hemmingDist(real_signals[-10*N:],pred_signals[-10*N:])/len(real_signals)
            # score = hemmingDist(real_signals,pred_signals)/len(real_signals)
            score = wHemmingDist(real_signals, pred_signals)/len(real_signals)
            scores.append(score)
            # ma_scores.append(hemmingDist(real_signals, ma_signals)/len(real_signals))
            ma_score = wHemmingDist(real_signals, ma_signals)/len(real_signals)
            ma_scores.append(ma_score)
            # if ITER % 100 == 0:
            stats_label['text'] += "conf: {:0.3}\n".format(obs.cur_conf)
            stats_label['text'] += "score: {:0.3}\n".format(score)
            stats_label['text'] += "ma score: {:0.3}".format(ma_score)
        # real_signals = real_signals[-N*10:]
        # pred_signals = pred_signals[-N*10:]
        ITER += 1

    root.after(DELAY, run, root, obs, gen, pred_label, real_label, stats_label, real_signals, pred_signals)

def switch_running(label):
    global RUNNING
    if RUNNING == True:
        label['text'] = "Start"
    else:
        label['text'] = "Stop"
    RUNNING = not RUNNING

def draw_plot(root, fig):
    fig.clear()
    plt.plot(scores, 'b-', label="F error")
    plt.plot(ma_scores, 'r-', label="MA error")
    plt.xlabel("Время симуляции")
    plt.ylabel("Функция ошибки")
    # plt.plot(scores)
    # plt.draw()
    # plt.pause(0.01)
    plt.legend()

    fig.canvas.draw()
    root.after(DELAY*100, draw_plot, root, fig)

def save_plot():
    path = "images/{}_{}.png".format(datetime.now().strftime('%Y%m%d_%H%M%S'), ITER)
    print('saving to', path)
    plt.savefig(path)

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
    small_delta_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.05)
    small_delta_scale.set(0.5)
    small_delta_scale.grid(row=1, column=1)

    big_delta_label = Label(root, text="big delta")
    big_delta_label.grid(row=2, column=0)
    big_delta_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.05)
    big_delta_scale.set(0.9)
    big_delta_scale.grid(row=2, column=1)

    global GREEN_L, RED_L
    green_image = Image.open("green_light.jpg")
    GREEN_L = ImageTk.PhotoImage(green_image)
    red_image = Image.open("red_light.png")
    RED_L = ImageTk.PhotoImage(red_image)

    real_label = Label(root, text="real")
    real_label.grid(row=0, column=2)
    real_label2 = Label(root, image=RED_L, width=150)
    real_label2.grid(row=1, column=2, rowspan=2)

    pred_label = Label(root, text="pred")
    pred_label.grid(row=0, column=3)
    pred_label2 = Label(root, image=RED_L, width=150)
    pred_label2.grid(row=1, column=3, rowspan=2)


    obs = Observer(small_delta_scale.get(),big_delta_scale.get())
    gen = Generator(rho_scale.get(), N, (0,1))

    start_button = Button(root, text="Start", command=lambda:switch_running(start_button))
    start_button.grid(row=3, column=1)

    stats_label = Label(root, text="")
    stats_label.grid(row=3, column=2, columnspan=2)

    root.bind("<Return>", lambda ev: switch_running(start_button))
    root.bind("o", lambda ev: obs.update_deltas(small_delta_scale.get(), big_delta_scale.get()))
    root.bind('g', lambda ev: gen.update_rho(rho_scale.get()))
    root.bind('s', lambda ev: save_plot())

    fig = plt.figure(1, figsize=(10,6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=4, column=1, rowspan=4)
    root.after(0, draw_plot, root, fig)

    real_signals = []
    pred_signals = []

    root.after(0, run, root, obs, gen, pred_label2, real_label2, stats_label, real_signals, pred_signals)
    root.mainloop()

if __name__ == "__main__":
    main()
