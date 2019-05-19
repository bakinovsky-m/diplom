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

    rho_label = Label(root, text='Choose the rho (gen goodness)')
    rho_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.1)
    rho_scale.set(0.9)
    rho_label.grid(row=0, column=0, columnspan=2)
    rho_scale.grid(row=1, column=0, columnspan=2)

    n_label = Label(root, text='Choose the signal length')
    n_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=100, tickinterval=10, resolution=1)
    n_scale.set(80)
    n_label.grid(row=2, column=0, columnspan=2)
    n_scale.grid(row=3, column=0, columnspan=2)

    delta1_label = Label(root, text='Choose the small delta')
    delta1_scale = Scale(root, orient=HORIZONTAL, length=(W_WIDTH-100)/2, from_=0, to=1, tickinterval=0.1, resolution=0.05)
    delta1_scale.set(0.9)
    delta1_label.grid(row=4, column=0, columnspan=1)
    delta1_scale.grid(row=5, column=0, columnspan=1)
    delta2_label = Label(root, text='Choose the big delta')
    delta2_scale = Scale(root, orient=HORIZONTAL, length=(W_WIDTH-100)/2, from_=0, to=1, tickinterval=0.1, resolution=0.05)
    delta2_scale.set(0.9)
    delta2_label.grid(row=4, column=1, columnspan=1)
    delta2_scale.grid(row=5, column=1, columnspan=1)

    count_label = Label(root, text='Choose the count of signals')
    count_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=10, to=3000, tickinterval=300, resolution=1)
    count_scale.set(3000)
    count_label.grid(row=6, column=0, columnspan=2)
    count_scale.grid(row=7, column=0, columnspan=2)

    res_label = Label(root, text='')
    res_label.grid(row=7, column=2)

    fig = plt.figure(1, figsize=(10,6))
    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.grid(row=0, column=2, rowspan=6)
    button2 = Button(root, text='Generate', command=lambda:gen_plot(rho_scale.get(),n_scale.get(),fig,delta_scale.get(),count_scale.get(), res_label))
    button2.grid(row=6, column=2)


    root.bind("<Return>", lambda ev:gen_plot(rho_scale.get(),n_scale.get(),fig,delta1_scale.get(),delta2_scale.get(),count_scale.get(), res_label))
    root.mainloop()


if __name__ == '__main__':
    main()