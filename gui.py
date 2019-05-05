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

def enter_callback(e, rho, n, fig, delta):
    gen_plot(rho,n,fig,delta)

def main():
    root = Tk()
    root.title('Figure 1')
    # geom = str(W_WIDTH) + 'x' + str(W_HEIGHT)
    # root.geometry(geom)
    root.protocol('WM_DELETE_WINDOW', lambda: root.quit()) # обработчик закрытия окна
    root.resizable(False, False)

    rho_label = Label(root, text='Choose the rho')
    rho_label.pack()

    rho_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.1)
    rho_scale.set(0.9)
    rho_scale.pack()

    n_label = Label(root, text='Choose the n')
    n_label.pack()
    n_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=100, tickinterval=10, resolution=1)
    n_scale.set(30)
    n_scale.pack()

    delta_label = Label(root, text='Choose the delta')
    delta_label.pack()
    delta_scale = Scale(root, orient=HORIZONTAL, length=W_WIDTH-100, from_=0, to=1, tickinterval=0.1, resolution=0.05)
    delta_scale.set(0.9)
    delta_scale.pack()

    fig = plt.figure(1, figsize=(9,8))
    # plt.ion()

    canvas = FigureCanvasTkAgg(fig, master=root)
    plot_widget = canvas.get_tk_widget()
    plot_widget.pack()
    button2 = Button(root, text='Generate', command=lambda:gen_plot(rho_scale.get(),n_scale.get(),fig,delta_scale.get()))
    button2.pack()

    root.bind("<Return>", lambda ev, rho=rho_scale.get(), n=n_scale.get(), fig=fig:gen_plot(rho_scale.get(),n_scale.get(),fig,delta_scale.get()))
    root.mainloop()


if __name__ == '__main__':
    main()