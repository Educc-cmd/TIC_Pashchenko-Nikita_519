import numpy as np
import scipy.signal
import scipy.fft
import matplotlib.pyplot as plt

# Ініціалізація даних
n = 500  # Довжина сигналу у відліках
Fs = 1000  # Частота дискретизації, Гц
F_max = 7  # Максимальна частота сигналу, Гц
F_filter = 14  # Полоса пропуску фільтру, Гц

t = np.linspace(0, n / Fs, n, endpoint=False)  # Временная шкала
y = np.sin(2 * np.pi * F_max * t)  # Синусоидальний сигнал
x = t  # Ось часу

discrete_signals = []
discrete_spectrums = []
signal_after_filters = []
dispersion = []
variance_dif = []

for Dt in [2, 4, 8, 16]:
    discrete_signal = np.zeros(n)
    for i in range(0, round(n / Dt)):
        discrete_signal[i * Dt] = y[i * Dt]
    discrete_signals.append(discrete_signal.tolist())

    # Розрахунок спектру сигналів
    y_s = np.abs(scipy.fft.fftshift(scipy.fft.fft(discrete_signal)))
    discrete_spectrums.append(y_s.tolist())

    # Відновлення аналогового сигналу з дискретного
    w = F_filter / (Fs / 2)
    sos = scipy.signal.butter(3, w, 'low', output='sos')
    discrete_signal_after_filter = scipy.signal.sosfiltfilt(sos, discrete_signal)
    signal_after_filters.append(discrete_signal_after_filter.tolist())

    # Розрахунок дисперсії
    E1 = discrete_signal_after_filter - y
    dispersion.append(np.var(E1))

    # Розрахунок співвідношення сигнал - шум
    variance_dif.append(np.var(y) / np.var(E1))

# Графіки
fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(x, discrete_signals[s], linewidth=1)
        s += 1
fig.supxlabel('Час (секунди)', fontsize=14)
fig.supylabel('Амплітуда сигналу', fontsize=14)
fig.suptitle('Сигнал з кроком дискретизації Dt = (2, 4, 8, 16)', fontsize=14)
fig.savefig('./figures/discrete_signals.png', dpi=600)
plt.close(fig)

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(x, discrete_spectrums[s], linewidth=1)
        s += 1
fig.supxlabel('Частота (Гц)', fontsize=14)
fig.supylabel('Амплітуда сигналу', fontsize=14)
fig.suptitle('Спектри сигналів з кроком дискретизації Dt = (2, 4, 8, 16)', fontsize=14)
fig.savefig('./figures/discrete_spectrums.png', dpi=600)
plt.close(fig)

fig, ax = plt.subplots(2, 2, figsize=(21 / 2.54, 14 / 2.54))
s = 0
for i in range(2):
    for j in range(2):
        ax[i, j].plot(x, signal_after_filters[s], linewidth=1)
        s += 1
fig.supxlabel('Час (секунди)', fontsize=14)
fig.supylabel('Амплітуда сигналу', fontsize=14)
fig.suptitle('Відновлені аналогові сигнали з кроком дискретизації Dt = (2, 4, 8, 16)', fontsize=14)
fig.savefig('./figures/reconstructed_signals.png', dpi=600)
plt.close(fig)

fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot([2, 4, 8, 16], dispersion, linewidth=1)
fig.supxlabel('Крок дискретизації', fontsize=14)
fig.supylabel('Дисперсія', fontsize=14)
fig.suptitle('Залежність дисперсії від кроку дискретизації', fontsize=14)
fig.savefig('./figures/dispersion_vs_dt.png', dpi=600)
plt.close(fig)

fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
ax.plot([2, 4, 8, 16], variance_dif, linewidth=1)
fig.supxlabel('Крок дискретизації', fontsize=14)
fig.supylabel('ССШ', fontsize=14)
fig.suptitle('Залежність співвідношення сигнал-шум від кроку дискретизації', fontsize=14)
fig.savefig('./figures/snr_vs_dt.png', dpi=600)
plt.close(fig)
