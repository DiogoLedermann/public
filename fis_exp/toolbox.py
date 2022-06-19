import numpy as np
import numpy.polynomial.polynomial as poly
import matplotlib.pyplot as plt


def generalForm(a, sA, mult=1, symbol='a', unit='um', precision=2):
    print(f'{symbol} = ({a * mult:.{precision}f} ± {sA:.{precision}f}) {unit}')


def polyplot(X, Y, deg, c=None, lw=3, label=None):

    p = poly.polyfit(X, Y, deg)

    d = X[-1] - X[0]
    i = X[0] - d
    f = X[-1] + d

    xvalues = np.arange(i, f, d / 1000)
    yvalues = poly.polyval(xvalues, p)

    plt.plot(xvalues, yvalues, color=c, linewidth=lw, label=label)


def getTicks(data, gridscale):

    X, Y = data
    dx, dy = gridscale

    xti, xtf = X[0] - (X[0] % dx), X[-1] - (X[-1] % dx)
    if X[0] > X[-1]:
        xti, xtf = xtf, xti
    lx = xtf - xti

    yti, ytf = Y[0] - (Y[0] % dy), Y[-1] - (Y[-1] % dy)
    if Y[0] > Y[-1]:
        yti, ytf = ytf, yti
    ly = ytf - yti

    return [i for i in np.arange(xti-lx, xtf+lx, dx)], [i for i in np.arange(0, 90, 5)]


def graph(data, variables, gridscale, deg=1, label=None, title=None, xlabel=None, ylabel=None):

    X, Y = data
    if X[0] > X[-1]:
        X = X[::-1]
        Y = Y[::-1]
    (xvariable, xunit), (yvariable, yunit) = variables

    xticks, yticks = getTicks(data, gridscale)

    if title is None:
        title = f'{yvariable} Versus {xvariable}'
    if xlabel is None:
        xlabel = f'{xvariable} ({xunit})'
    if ylabel is None:
        ylabel = f'{yvariable} ({yunit})'

    fs = 30
    plt.subplots(constrained_layout=True)
    plt.title(title, fontsize=fs+10)
    plt.xlabel(xlabel, fontsize=fs)
    plt.ylabel(ylabel, fontsize=fs)
    plt.xticks(xticks, fontsize=fs)
    plt.yticks(yticks, fontsize=fs)
    plt.grid()
    plt.scatter(X, Y, color='black', s=80)
    polyplot(X, Y, deg, label=label)
    plt.legend(loc='best', fontsize=fs-5)
    plt.show()


def linearRegression(X, Y):

    n = len(X)

    X2 = [x ** 2 for x in X]
    XY = [x * y for x, y, in zip(X, Y)]

    a = (n * sum(XY) - sum(X) * sum(Y)) / (n * sum(X2) - sum(X) ** 2)
    b = (sum(Y) * sum(X2) - sum(X) * sum(XY)) / (n * sum(X2) - sum(X) ** 2)

    estimatedY = [a * x + b for x in X]
    deltaY = [y - ey for y, ey in zip(Y, estimatedY)]
    deltaY2 = [dy ** 2 for dy in deltaY]

    aux = (sum(deltaY2)) / (n - 2)

    sA = np.sqrt((n * aux) / (n * sum(X2) - sum(X) ** 2))

    return a, b, sA
