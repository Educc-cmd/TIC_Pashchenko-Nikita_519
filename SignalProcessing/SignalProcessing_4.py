import numpy as np
import matplotlib.pyplot as plt
import os

# === Налаштування ===
n = 500  # довжина сигналу
Fs = 1000  # частота дискретизації
f_max = 7  # максимальна частота сигналу (варіант 3)
t = np.linspace(0, 1, n)  # часовий масив
signal = np.sin(2 * np.pi * f_max * t)  # синусоїдальний сигнал

# Створення директорії для збереження графіків
os.makedirs('figures', exist_ok=True)

# Масиви для збереження результатів
quantized_signals = []
noise_powers = []
snr_values = []

# === Основний цикл ===
for M in [4, 16, 64, 256]:
    delta = (np.max(signal) - np.min(signal)) / (M - 1)
    quantized_signal = delta * np.round(signal / delta)
    quantized_signals.append(quantized_signal)

    quantize_levels = np.arange(np.min(quantized_signal), np.max(quantized_signal) + delta, delta)
    quantize_bit = [format(bits, f'0{int(np.log2(M))}b') for bits in range(M)]

    quantize_table = np.c_[quantize_levels[:M], quantize_bit[:M]]

    # Таблиця квантування
    fig, ax = plt.subplots(figsize=(14 / 2.54, M / 2.54))
    table = ax.table(cellText=quantize_table, colLabels=['Значення сигналу', 'Кодова послідовність'], loc='center')
    table.set_fontsize(14)
    table.scale(1, 2)
    ax.axis('off')
    fig.savefig(f'figures/Таблиця_квантування_{M}.png', dpi=600)
    plt.close(fig)

    # Бітове кодування сигналу
    bits = []
    for signal_value in quantized_signal:
        for index, value in enumerate(quantize_levels[:M]):
            if np.round(np.abs(signal_value - value), 0) == 0:
                bits.append(quantize_bit[index])
                break

    # Розгортання бітів у послідовність
    bit_string = ''.join(bits)
    bits_array = [int(b) for b in bit_string]

    # Побудова графіку бітової послідовності
    x = np.arange(0, len(bits_array))
    y = bits_array
    fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
    ax.step(x, y, linewidth=0.1)
    ax.set_xlabel("Час (відлік)")
    ax.set_ylabel("Біт")
    ax.set_title(f"Кодова послідовність для M={M}")
    fig.savefig(f'figures/Кодова_послідовність_{M}.png', dpi=600)
    plt.close(fig)

    # Визначення дисперсії шуму та SNR
    noise = signal - quantized_signal
    noise_power = np.var(noise)
    signal_power = np.var(signal)
    snr = 10 * np.log10(signal_power / noise_power)

    noise_powers.append(noise_power)
    snr_values.append(snr)

# === Побудова графіків ===

# Графік усіх цифрових сигналів
fig, ax = plt.subplots(figsize=(21 / 2.54, 14 / 2.54))
for i, q_signal in enumerate(quantized_signals):
    ax.plot(t, q_signal, label=f'M={ [4,16,64,256][i] }')
ax.set_title("Цифрові сигнали для різних рівнів квантування")
ax.set_xlabel("Час (с)")
ax.set_ylabel("Амплітуда")
ax.legend()
fig.savefig("figures/Цифрові_сигнали.png", dpi=600)
plt.close(fig)

# Графік дисперсії
fig, ax = plt.subplots()
ax.plot([4, 16, 64, 256], noise_powers, marker='o')
ax.set_title("Залежність дисперсії шуму від M")
ax.set_xlabel("Кількість рівнів квантування (M)")
ax.set_ylabel("Дисперсія")
fig.savefig("figures/Дисперсія_від_M.png", dpi=600)
plt.close(fig)

# Графік SNR
fig, ax = plt.subplots()
ax.plot([4, 16, 64, 256], snr_values, marker='o')
ax.set_title("Залежність SNR від M")
ax.set_xlabel("Кількість рівнів квантування (M)")
ax.set_ylabel("SNR (дБ)")
fig.savefig("figures/SNR_від_M.png", dpi=600)
plt.close(fig)