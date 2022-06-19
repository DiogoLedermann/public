import numpy as np
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.animation import FuncAnimation, writers


def F(x, y):

    fx = y
    fy = -x

    return fx, fy


def curve_coordinates():

    # C
    theta = np.linspace(0, 2*np.pi, 360)
    x = 2*np.cos(theta)
    y = np.sin(theta)
    # z = t

    return x, y


def velocity(x_size, y_size):

    theta = np.linspace(0, 2*np.pi, 360)
    vx = -np.sin(theta)
    vy = np.cos(theta)
    return vx, vy


def main(save_animation=False, title='untitled', option='quiver'):

    def get_values():

        values = []

        for t in range(frames):

            if case == '2D':

                fx, fy = F(x[t], y[t])
                value = fx * vx[t] + fy * vy[t]

            # if case == '3D':
            #
            #     fx, fy, fz = F(x[t], y[t], z[t])
            #     value = fx * vx[t] + fy * vy[t] + fz * vz[t]
            
            values.append(value)

        return values

    def set_figure():

        def set_ax1():

            def set_ax1_axis(margin=0):

                limits = min(x) - margin, max(x) + margin, min(y) - margin, max(y) + margin

                return limits

            def plot_vector_field(ax, domain, density=3):

                xmin, xmax, ymin, ymax = domain

                nx = int(round((xmax - xmin) * density))
                ny = int(round((ymax - ymin) * density))

                x_axis = np.linspace(xmin, xmax, nx)
                y_axis = np.linspace(ymin, ymax, ny)

                x0, y0 = np.meshgrid(x_axis, y_axis)

                Vx, Vy = F(x0, y0)

                Vres = np.sqrt(Vx ** 2 + Vy ** 2)

                if option == 'quiver':
                    vector_field = ax.quiver(x0, y0, Vx, Vy, Vres)

                if option == 'streamplot':
                    vector_field = ax.streamplot(x0, y0, Vx, Vy, color=Vres)

                return vector_field

            def plot_curve(ax):

                ax.plot(x, y, color='black', lw=2)

            ax1 = fig.add_subplot(gs[0, 0])
            ax1.set_title('C')
            ax1.set_xlabel('X coordinates')
            ax1.set_ylabel('Y coordinates')
            ax1.grid()
            ax1_axis = set_ax1_axis(margin=0.2)
            ax1.axis(ax1_axis)
            vector_field = plot_vector_field(ax1, ax1_axis)
            plot_curve(ax1)
            dot, = ax1.plot(x[0], y[0], 'ro', ms=10)

            return vector_field, ax1, dot,

        def set_ax2():

            def set_ax2_axis(margin=0):

                limits = 0, frames, min(dot_products) - margin, max(dot_products) + margin

                return limits

            ax2 = fig.add_subplot(gs[1, 0])
            ax2.set_title('Line Integral')
            ax2.set_xlabel('T')
            ax2.set_ylabel('Dot Product')
            ax2.grid()
            ax2_axis = set_ax2_axis(margin=1)
            ax2.axis(ax2_axis)
            ax2.axhline(color='black')
            line, = ax2.plot([], [])

            return ax2, line,

        fig = plt.figure(figsize=(15, 9), tight_layout=True)
        gs = gridspec.GridSpec(nrows=2, ncols=1)

        vector_field, ax1, dot, = set_ax1()
        ax2, line, = set_ax2()

        fig.colorbar(vector_field, ax=ax1)
        fig.colorbar(vector_field, ax=ax2).ax.set_visible(False)

        return fig, dot, line,

    def update_figure(t):

        dot.set_data(x[t], y[t])

        if dot_products[t] < 0:
            line.set_color('red')
        else:
            line.set_color('blue')

        line.set_data(range(t), dot_products[:t])

        return dot, line,

    def save():

        white, green, blue = '\033[30m', '\033[32m', '\033[34m'

        print(f'{blue}Rendering...{white}')
        Writer = writers['ffmpeg']
        writer = Writer(fps=90, metadata=dict(artist='Me'), bitrate=1800)
        animation.save(f'{title}.gif', writer='ffmpeg', dpi=200)
        print(f'{green}Done!{white}')

    if len(curve_coordinates()) == 2:
        case = '2D'
        x, y = curve_coordinates()
        vx, vy = velocity(len(x), len(y))
    
    # if len(curve_coordinates()) == 3:
    #     case = '3D'
    #     x, y, z = curve_coordinates()
    #     vx, vy, vz = velocity(len(x), len(y), len(z))

    frames = len(x)

    dot_products = get_values()

    fig, dot, line, = set_figure()
    animation = FuncAnimation(fig, update_figure, frames=frames, interval=1, blit=True)

    if save_animation:

        save()

    plt.show()


main()
