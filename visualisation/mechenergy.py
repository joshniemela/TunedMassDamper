import matplotlib.pyplot as plt
import numpy as np
from scipy import integrate
from scipy.optimize import curve_fit
import pandas as pd
from scipy.interpolate import UnivariateSpline
import matplotlib as mpl

# mpl.use("pgf")


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


def decay(t, r, w, p, A, d):
    x = A * np.exp(r * t) * np.cos(w * t + p)
    x = x + d
    return x


def num_diff(x, y, n):
    f = UnivariateSpline(x, y, s=5e-4).derivative(n)
    return f(x)


df = pd.read_csv("tmddata.csv", index_col=0)
df = df[7:]

x1 = df[df.columns[0]].values  # /1000
x2 = df[df.columns[1]].values  # /1000
t = df.index - df.index[1]

x2 = -(x2 - 120) / 1000
x1 = (x1 - 46) / 1000
x1 = num_diff(t, x1, 0)
x2 = num_diff(t, x2, 0)
v1 = num_diff(t, x1, 1)
v2 = num_diff(t, x2, 1)


m2 = 1.14
k2 = 38.62

m1 = 0.225
k1 = 9.588

KE1 = 1 / 2 * m1 * v1**2
PE1 = 1 / 2 * k1 * x1**2
ME1 = KE1 + PE1

c1 = 2 * m2 * 5.84336233568
c2 = 2 * m2 * 5.654866776468

fig, (ax1, ax2, ax3, ax4) = plt.subplots(4)

ax3.plot(t, KE1, label="Kin. energi")
ax3.plot(t, PE1, label="Pot. energi")
ax3.plot(t, ME1, label="Mek. energi")

# diss energy
ax4.plot(t, 1 / 2 * c1 * v1**2, label="dæmper")
ax4.plot(t, 1 / 2 * c2 * v2**2, label="bygnung")


KE2 = 1 / 2 * m2 * (v2**2)
PE2 = 1 / 2 * k2 * (x2**2)
ME2 = KE2 + PE2
ax2.plot(t, KE2, label="Kin. energi")
ax2.plot(t, PE2, label="Pot. energi")
ax2.plot(t, ME2, label="Mek. energi")

ax1.plot(t, x1, label="Dæmper")
ax1.plot(t, x2, label="Bygning")

ax1.set_title("Positioner af dæmper og bygning over tid")
ax2.set_title("Kinetisk, potentiel og mekanisk energi af bygning")
ax3.set_title("Kinetisk, potentiel og mekanisk energi af dæmper")


ax3.set_xlabel("Tid[s]")
ax1.set_ylabel("Position[m]")
ax2.set_ylabel("Energi[J]")
ax3.set_ylabel("Energi[J]")

ax4.legend()
ax1.legend()

ax2.legend()
ax3.legend()
# plt.savefig("Energi.pgf")
