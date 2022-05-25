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
    "legend.fontsize": "xx-small",
}
mpl.rcParams.update(pgf_with_latex)


def plus(n):
    if np.sign(n) == 1:
        return f"+{n}"
    else:
        return str(n)


def decay(t, r, w, p, A, d, B, r2, w2, p2):
    x = A * np.exp(r * t) * np.cos(w * t + p) + B * np.exp(r2 * t) * np.cos(w2 * t + p2)
    x = x + d
    return x


def num_diff(x, y, n):
    f = UnivariateSpline(x, y, s=2e-3).derivative(n)
    return f(x)


df = pd.read_csv("tmddataraw2.csv", index_col=0)

# df = df[7:10]

x1 = df[df.columns[0]].values
x2 = df[df.columns[1]].values
t = df.index - df.index[1]

params1 = curve_fit(decay, t, x1)[0]
params2 = curve_fit(decay, t, x2)[0]


fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2)
r21 = 1 - sum((x1 - [decay(i, *params1) for i in t]) ** 2) / sum((x1 - x1.mean()) ** 2)
r22 = 1 - sum((x2 - [decay(i, *params2) for i in t]) ** 2) / sum((x2 - x2.mean()) ** 2)


ax1.plot(t, x1 - params1[-1], ".-", label="Data, $x_1(t)$")
ax2.plot(t, x2 - params2[-1], ".-", label="Data, $x_2(t)$")
ax1.plot(
    t,
    [decay(i, *params1) for i in t] - params1[-1],
    "-r",
    label="$Model, \hat{x}_2(t) = A_1 e^{r_1t} \cos (\omega_1 t+\phi_1)+A_2 e^{r_2 t}\cos (\omega_2t+\phi_2$)"
    + f"\n $R^2=${round(r21, 3)}",
)
ax2.plot(
    t,
    [decay(i, *params2) for i in t] - params2[-1],
    "-r",
    label="$Model, \hat{x}_2(t) = A_1 e^{r_1t}\cos (\omega_1 t+\phi_1)+A_2 e^{r_2t}\cos (\omega_2t+\phi_2$)"
    + f"\n $R^2=${round(r22, 3)}",
)


ax3.plot(t, x1 - [decay(i, *params1) for i in t], label="Residualplot, $x_1-\hat{x}_1$")
ax4.plot(t, x2 - [decay(i, *params2) for i in t], label="Residualplot, $x_2-\hat{x}_2$")

print("r-squared", r21, r22)
ax1.grid()
ax2.grid()
# ax1.plot(t,params[3]*np.exp(params[0]*t), "g", label = f"Kuvert, $\pm${round(params[3],1)}$\cdot e^{{{round(params[0],3)}\cdot t}}$")
# ax1.plot(t,-params[3]*np.exp(params[0]*t), "g")
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
