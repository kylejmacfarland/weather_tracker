import matplotlib.pyplot as plt
from scipy.interpolate import make_interp_spline
import numpy as np
from datetime import datetime

def render_plot(x_axis, y_axis, x_label="", y_label="", title=""):
    RESOLUTION = 300
    int_x = [d.timestamp() for d in x_axis]
    new_x = np.linspace(min(int_x), max(int_x), RESOLUTION)
    spl = make_interp_spline(int_x, y_axis, k=3)
    new_y = spl(new_x)
    new_x = [datetime.fromtimestamp(t) for t in new_x]
    plt.plot(new_x, new_y)
    plt.xlabel(x_label)
    plt.ylabel(y_label)
    plt.title(title)
    plt.show()
