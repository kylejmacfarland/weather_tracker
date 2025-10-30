import matplotlib.pyplot as plt

def render_plot(x_axis, y_axis, x_label="", y_label="", title=""):
    plt.plot(x_axis, y_axis)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
