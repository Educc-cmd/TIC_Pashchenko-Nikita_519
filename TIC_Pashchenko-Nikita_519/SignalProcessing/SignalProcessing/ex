import numpy as np
import matplotlib.pyplot as plt
import os
from scipy import signal, fft

# Задаем параметры
n = 500  # Количество точек сигнала
Fs = 1000  # Частота дискретизации (Гц)
F_max = 7  # Максимальная частота сигнала (Гц)

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