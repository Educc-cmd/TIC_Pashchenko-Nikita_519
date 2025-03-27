import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal, fft
import scipy.fft

# Задаем параметры
n = 500  # Количество точек сигнала
Fs = 1000  # Частота дискретизации (Гц)
F_max = 7  # Максимальная частота сигнала (Гц)
F_filter = 14  # Полоса пропуску фільтру, Гц

'''
# Генерируем случайный сигнал (нормальное распределение)
signal_data = np.random.normal(0, 10, n)  # Среднее = 0, стандартное отклонение = 10

# Создаем временную ось (моменты времени)
time = np.arange(n) / Fs

# Настраиваем фильтр низких частот (ФНЧ)
w = F_max / (Fs / 2)  # Нормированная частота
sos = signal.butter(3, w, 'low', output='sos')

# Применяем фильтр к сигналу
filtered_signal = signal.sosfiltfilt(sos, signal_data)

# Рассчитываем спектр сигнала
spectrum = fft.fft(filtered_signal)
shifted_spectrum = np.abs(fft.fftshift(spectrum))
frequencies = fft.fftshift(fft.fftfreq(n, 1 / Fs))

# Создаем папку для сохранения графиков
os.makedirs("SignalProcessing/figures", exist_ok=True)

# Строим график сигнала
plt.figure(figsize=(8, 5))
plt.plot(time, filtered_signal, linewidth=1)
plt.xlabel("Time (s)", fontsize=12)
plt.ylabel("Amplitude", fontsize=12)
plt.title("Filtered Signal", fontsize=12)
plt.grid()
plt.savefig("SignalProcessing/figures/filtered_signal.png", dpi=300)
plt.show()

# Строим график спектра
plt.figure(figsize=(8, 5))
plt.plot(frequencies, shifted_spectrum, linewidth=1)
plt.xlabel("Frequency (Hz)", fontsize=12)
plt.ylabel("Magnitude", fontsize=12)
plt.title("Signal Spectrum", fontsize=12)
plt.grid()
plt.savefig("SignalProcessing/figures/signal_spectrum.png", dpi=300)
plt.show()
'''

# Дискретизація сигналу

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
