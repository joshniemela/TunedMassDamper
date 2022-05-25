import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.optimize import curve_fit
import pandas as pd
from scipy.interpolate import UnivariateSpline
import matplotlib as mpl

mpl.use("pgf")


pgf_with_latex = {
    "text.usetex": True,
    "pgf.rcfonts": False,
    "legend.fontsize": "x-small",
}
mpl.rcParams.update(pgf_with_latex)


def plus(n):
    if np.sign(n) == 1:
        return f"+{n}"
    else:
        return str(n)


def decay(t, r, w, p, A, d):
    x = A * np.exp(r * t) * np.cos(w * t + p)
    x = x + d
    return x


def num_diff(x, y, n):
    f = UnivariateSpline(x, y, s=2e-3).derivative(n)
    return f(x)


df = pd.read_csv("bygningdatatuned.csv", index_col=0)

df = df[7:14]  # Bruges til at vælge intervallet i datafilen

x1 = df[df.columns[1]].values  # Bruges til at vælge den specifikke sensor.

t = df.index - df.index[1]

params = curve_fit(decay, t, x1)[0]
r2 = 1 - sum((x1 - [decay(i, *params) for i in t]) ** 2) / sum(
    (x1 - x1.mean()) ** 2
)  # genererer R² score


fig, (ax1, ax2) = plt.subplots(2)

function = f"{round(params[3],1)}$\cdot e^{{{round(params[0],3)}\cdot t}} \cdot \cos({{{round(params[1],3)}}} \cdot t {{{plus(round(params[2], 3))}}})$\n $r^2=${round(r2,3)}"
ax1.plot(t, x1 - params[-1], ".-", label="Data, x(t)")
ax1.plot(
    t,
    [decay(i, *params) for i in t] - params[-1],
    "-r",
    label="$Model, \hat{x}(t)$ = " + function,
)

print("r-squared", r2)  # til debugging
print(params)  # til debugging

ax1.grid()
ax1.plot(
    t,
    params[3] * np.exp(params[0] * t),
    "g",
    label=f"Kuvert, $\pm${round(params[3],1)}$\cdot e^{{{plus(round(params[0],3))}\cdot t}}$",
)
ax1.plot(t, -params[3] * np.exp(params[0] * t), "g")
ax1.legend(loc="upper right")
ax1.set_ylabel("Position[mm]")
ax1.set_title("Målinger og model af svingninger fra bygning")

ax2.plot(t, x1 - [decay(i, *params) for i in t], label="Residualplot, x-$\hat{x}$")
ax2.legend()
ax2.set_xlabel("Tid[s]")
ax2.grid()
plt.savefig("../PGFs/bygningtuned.pgf", format="pgf")
