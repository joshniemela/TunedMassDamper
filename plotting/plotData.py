import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.optimize import curve_fit
import pandas as pd
from scipy.interpolate import UnivariateSpline
import matplotlib as mpl

mpl.use("pgf")

# stuff to make matplotlib return pgf plots to be used in latex
pgf_with_latex = {
    "text.usetex": True,
    "pgf.rcfonts": False,
    "legend.fontsize": "xx-small",
}
mpl.rcParams.update(pgf_with_latex)


def plus(n) -> str:
    """
    Add a plus sign to a number if it is positive.
    """
    if np.sign(n) == 1:
        return f"+{n}"
    else:
        return str(n)


def decay(t, r, w, p, A, d, B, r2, w2, p2):
    """
    Approximate the exponential decay of a coupled harmonic oscillator with two degrees of freedom.
    A and B are linear scaling factors, r and r2 are the decay rates, w and w2 are the angular frequencies, p and p2 are the phases, and d is vertical offset.
    """
    x = A * np.exp(r * t) * np.cos(w * t + p) + B * np.exp(r2 * t) * np.cos(w2 * t + p2)
    x = x + d
    return x


def num_diff(x, y, n):
    f = UnivariateSpline(x, y, s=2e-3).derivative(n)
    return f(x)

def rSquared(x, t, *params):
    return 1 - sum((x - [decay(i, *params) for i in t]) ** 2) / sum((x - x.mean()) ** 2)

def plotData(ax, t, x, index, *params):
    ax.plot(t, x - params[-1], ".-", label=f"Data, $x_{index}(t)$")
    ax.plot(
        t,
        [decay(i, *params1) for i in t] - params1[-1],
        "-r",
        label="$Model, \hat{x}_2(t) = A_1 e^{r_1t} \cos (\omega_1 t+\phi_1)+A_2 e^{r_2 t}\cos (\omega_2t+\phi_2$)"
        + f"\n $R^2=${round(rSquared(x, t, *params), 3)}",
    )

# file to read data from
fileName = "tmddataraw2.csv"


df = pd.read_csv(fileName, index_col=0)

df = df[7:10] # Seconds to slice data from, in this case 7 to 10 seconds

t = df.index - df.index[1]
x1 = df[df.columns[0]].values
x2 = df[df.columns[1]].values

params1 = curve_fit(decay, t, x1)[0]
params2 = curve_fit(decay, t, x2)[0]


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)

plotData(ax1, t, x1, 1, *params1)
plotData(ax2, t, x2, 2, *params2)

ax3.plot(t, x1 - [decay(i, *params1) for i in t], label="Residualplot, $x_1-\hat{x}_1$")
ax4.plot(t, x2 - [decay(i, *params2) for i in t], label="Residualplot, $x_2-\hat{x}_2$")

print("r-squared", r21, r22)
ax1.grid()
ax2.grid()
ax1.plot(t,params[3]*np.exp(params[0]*t), "g", label = f"Kuvert, $\pm${round(params[3],1)}$\cdot e^{{{round(params[0],3)}\cdot t}}$")
ax1.plot(t,-params[3]*np.exp(params[0]*t), "g")
ax1.legend(loc="upper right")
ax2.legend()
ax1.set_ylabel("Position[mm]")
ax3.set_ylabel("Afvigelse[mm]")

ax1.set_xlabel("Tid[s]")
ax2.set_xlabel("Tid[s]")
ax1.set_title("Dæmper")
ax2.set_title("Bygning")
ax3.legend()
ax4.legend()
plt.savefig("../PGFs/tunedTMDimprovedmodel.pgf", format="pgf")
