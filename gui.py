from tkinter import *
import matplotlib
matplotlib.use('TkAgg')

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt

from bayes import gen_plot

W_WIDTH = 900
W_HEIGHT = 900

def print_gen_params(rho, n):
    print('rho',rho.get())
    print('n', n.get())

def main():
    root = Tk()
    root.title('Figure 1')
    root.protocol('WM_DELETE_WINDOW', lambda: root.quit()) # обработчик закрытия окна
    root.resizable(False, False)

    rho_label = Label(root, text='Choose the rho')

    rho_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.1)
    rho_scale.set(0.9)
    rho_label.grid(row=0, column=0)
    rho_scale.grid(row=1, column=0)

    n_label = Label(root, text='Choose the n')
    n_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=100, tickinterval=10, resolution=1)
    n_scale.set(80)
    n_label.grid(row=2, column=0)
    n_scale.grid(row=3, column=0)

    delta_label = Label(root, text='Choose the delta')
    delta_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.05)
    delta_scale.set(0.9)
    delta_label.grid(row=4, column=0)
    delta_scale.grid(row=5, column=0)

    count_label = Label(root, text='Choose the count')
    count_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=10, to=300, tickinterval=10, resolution=1)
    count_scale.set(300)
    count_label.grid(row=6, column=0)
    count_scale.grid(row=7, column=0)

    res_label = Label(root, text='accuracy\nprecision\nrecall')
    res_label.grid(row=7, column=1)

    fig = plt.figure(1, figsize=(10,6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=0, column=1, rowspan=6)
    button2 = Button(root, text='Generate', command=lambda:gen_plot(rho_scale.get(),n_scale.get(),fig,delta_scale.get(),count_scale.get(), res_label))
    button2.grid(row=6, column=1)


    root.bind("<Return>", lambda ev:gen_plot(rho_scale.get(),n_scale.get(),fig,delta_scale.get(),count_scale.get(), res_label))
    root.mainloop()


if __name__ == '__main__':
    main()