# -*- coding: utf-8 -*-
"""
Created on Wed Jan  7 13:05:27 2026

@author: Alfauziyah
"""

import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# INPUT DASAR
# ==================================================
nama_sungai = "Cikapundung"
Q_dasar = 5.0     # m3/s
head = 10.0       # m

bulan = [
    "Jan", "Feb", "Mar", "Apr", "Mei", "Jun",
    "Jul", "Agt", "Sep", "Okt", "Nov", "Des"
]

bulan_full = [
    "Januari", "Februari", "Maret", "April", "Mei", "Juni",
    "Juli", "Agustus", "September", "Oktober", "November", "Desember"
]

# ==================================================
# DATA IKLIM
# ==================================================
curah_hujan = {
    "Januari": 300, "Februari": 280, "Maret": 250, "April": 220,
    "Mei": 180, "Juni": 120, "Juli": 100, "Agustus": 90,
    "September": 110, "Oktober": 180, "November": 240, "Desember": 290
}

suhu = {b: 27 for b in curah_hujan}
kelembaban = {b: 75 for b in curah_hujan}

# ==================================================
# KONSTANTA
# ==================================================
rho = 1000
g = 9.81

k_r = 0.001
k_t = 0.01
k_h = 0.002

seasonal_factor = {
    "Januari": 1.25, "Februari": 1.20, "Maret": 1.15, "April": 1.05,
    "Mei": 0.95, "Juni": 0.85, "Juli": 0.80, "Agustus": 0.78,
    "September": 0.82, "Oktober": 0.95, "November": 1.10, "Desember": 1.20
}

# ==================================================
# PERHITUNGAN DEBIT & DAYA
# ==================================================
debit_forecast = []
daya_forecast = []

for b in bulan_full:
    R = curah_hujan[b]
    T = suhu[b]
    H = kelembaban[b] / 100

    Q_iklim = Q_dasar * (
        1
        + k_r * (R / 100)
        - k_t * (T - 25)
        + k_h * (H - 0.7)
    )

    Q = Q_iklim * seasonal_factor[b]
    Q = max(0.3 * Q_dasar, min(Q, 2.5 * Q_dasar))

    P = rho * g * Q * head / 1000

    debit_forecast.append(Q)
    daya_forecast.append(P)

# ==================================================
# DATAFRAME
# ==================================================
df = pd.DataFrame({
    "Bulan": bulan,
    "Debit (m3/s)": debit_forecast,
    "Daya (kW)": daya_forecast
})

# ==================================================
# VISUALISASI DUAL AXIS (MIRIP CONTOH GAMBAR)
# ==================================================
fig, ax1 = plt.subplots(figsize=(11,5))

# Debit (kiri)
ax1.plot(
    df["Bulan"],
    df["Debit (m3/s)"],
    marker="o",
    linewidth=2.5,
    label="Debit Sungai",
    color="tab:blue"
)
ax1.set_xlabel("Bulan")
ax1.set_ylabel("Debit Sungai (m³/s)", color="tab:blue")
ax1.tick_params(axis="y", labelcolor="tab:blue")

# Garis debit minimum
Q_min = 0.4 * Q_dasar
ax1.axhline(
    Q_min,
    color="green",
    linestyle="--",
    linewidth=1.5,
    label="Debit Minimum Operasional"
)

# Daya (kanan)
ax2 = ax1.twinx()
ax2.plot(
    df["Bulan"],
    df["Daya (kW)"],
    marker="s",
    linestyle="--",
    linewidth=2.5,
    label="Daya PLTA",
    color="red"
)
ax2.set_ylabel("Daya PLTA (kW)", color="red")
ax2.tick_params(axis="y", labelcolor="red")

# Judul & legend
fig.suptitle(
    f"Forecast Debit dan Daya PLTA Tahunan\nSungai {nama_sungai}",
    fontsize=13
)

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines1 + lines2, labels1 + labels2, loc="upper left")

ax1.grid(True, linestyle="--", alpha=0.6)
plt.tight_layout()
plt.show()
