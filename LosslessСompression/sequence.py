import os
import random
import string
import collections
import math
import matplotlib.pyplot as plt

# === Дані ===
surname = "Пащенко"
group_number = "519"
N_sequence = 100
student_number = 3

# === Послідовність 1 ===
list1 = ['1'] * student_number
list0 = ['0'] * (N_sequence - student_number)
sequence1 = list1 + list0
random.shuffle(sequence1)
original_sequence_1 = ''.join(sequence1)

sequence_alphabet_size = len(set(original_sequence_1))
Original_sequence_size = len(original_sequence_1)

# === Послідовність 2 ===
surname_letters = list(surname)
list0 = ['0'] * (N_sequence - len(surname_letters))
original_sequence_2 = ''.join(surname_letters + list0)

# === Послідовність 3 ===
sequence3 = surname_letters + ['0'] * (N_sequence - len(surname_letters))
random.shuffle(sequence3)
original_sequence_3 = ''.join(sequence3)

# === Послідовність 4 ===
group_digits = list(group_number)
letters_and_digits = surname_letters + group_digits
repeats = N_sequence // len(letters_and_digits)
remainder = N_sequence % len(letters_and_digits)
sequence4 = letters_and_digits * repeats + letters_and_digits[:remainder]
original_sequence_4 = ''.join(sequence4)

# === Послідовність 5 ===
letters2 = list(surname[:2].lower())
alphabet5 = letters2 + group_digits
original_sequence_5_list = []

for symbol in alphabet5:
    original_sequence_5_list.extend([symbol] * 20)

random.shuffle(original_sequence_5_list)
original_sequence_5 = ''.join(original_sequence_5_list)

# === Послідовність 6 ===
n_letters = int(0.7 * N_sequence)
n_digits = N_sequence - n_letters
letters_part = [random.choice(letters2) for _ in range(n_letters)]
digits_part = [random.choice(group_digits) for _ in range(n_digits)]
sequence6 = letters_part + digits_part
random.shuffle(sequence6)
original_sequence_6 = ''.join(sequence6)

# === Послідовність 7 ===
elements = string.ascii_lowercase + string.digits
original_sequence_7 = ''.join(random.choice(elements) for _ in range(N_sequence))

# === Послідовність 8 ===
original_sequence_8 = '1' * N_sequence

# === Список всіх послідовностей ===
original_sequences = [
    original_sequence_1,
    original_sequence_2,
    original_sequence_3,
    original_sequence_4,
    original_sequence_5,
    original_sequence_6,
    original_sequence_7,
    original_sequence_8
]

# === Збереження у sequence.txt ===
sequence_file_path = os.path.join("sequence.txt")
with open(sequence_file_path, "w", encoding="utf-8") as file:
    for seq in original_sequences:
        file.write(seq + "\n")

print(f"Усі послідовності збережено у файл: {sequence_file_path}")

# === Перевірити відповідність характеристик згенерованих послідовностей ===
counts = collections.Counter(sequence1)
probability = {symbol: count / N_sequence for symbol, count in counts.items()}
mean_probability = sum(probability.values()) / len(probability)
equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
if equal:
    uniformity = "рівна"
else:
    uniformity = "нерівна"

entropy = -sum(p * math.log2(p) for p in probability.values())
if sequence_alphabet_size > 1:
    source_excess = 1 - entropy / math.log2(sequence_alphabet_size)
else:
    source_excess = 1

probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])

# === Створення таблиці ===
results = []
for i, seq in enumerate(original_sequences):
    counts = collections.Counter(seq)
    probability = {symbol: count / N_sequence for symbol, count in counts.items()}
    mean_probability = sum(probability.values()) / len(probability)
    equal = all(abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values())
    if equal:
        uniformity = "рівна"
    else:
        uniformity = "нерівна"

    entropy = -sum(p * math.log2(p) for p in probability.values())
    if len(set(seq)) > 1:
        source_excess = 1 - entropy / math.log2(len(set(seq)))
    else:
        source_excess = 1

    results.append([len(set(seq)), round(entropy, 2), round(source_excess, 2), uniformity])

fig, ax = plt.subplots(figsize=(14/1.54, 8/1.54))
headers = ['Розмір алфавіту', 'Ентропія', 'Надмірність', 'Ймовірність']
row = ['Послідовність 1', 'Послідовність 2', 'Послідовність 3', 'Послідовність 4', 'Послідовність 5', 'Послідовність 6', 'Послідовність 7', 'Послідовність 8']
ax.axis('off')
table = ax.table(cellText=results, colLabels=headers, rowLabels=row, loc='center', cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)
fig.savefig(f'Характеристики сформованих послідовностей.png')

print("Таблиця характеристик сформованих послідовностей збережена у файл: Характеристики сформованих послідовностей.png")

# === Запис результатів у файл results_sequence.txt ===
with open("results_sequence.txt", "w", encoding="utf-8") as f:
    for i, seq in enumerate(original_sequences):
        counts = collections.Counter(seq)
        probability = {symbol: count / N_sequence for symbol, count in counts.items()}
        mean_probability = sum(probability.values()) / len(probability)
        uniformity = "рівна" if all(
            abs(prob - mean_probability) < 0.05 * mean_probability for prob in probability.values()) else "нерівна"
        entropy = -sum(p * math.log2(p) for p in probability.values())
        alphabet_size = len(set(seq))
        source_excess = 1 - entropy / math.log2(alphabet_size) if alphabet_size > 1 else 1
        probability_str = ', '.join([f"{symbol}={prob:.4f}" for symbol, prob in probability.items()])

        f.write(f"Оригінальна послідовність {i + 1}:\n")
        f.write(f"Послідовність: {seq}\n")
        f.write(f"Розмір алфавіту: {alphabet_size}\n")
        f.write(f"Ентропія: {entropy:.4f}\n")
        f.write(f"Надмірність: {source_excess:.4f}\n")
        f.write(f"Ймовірності: {probability_str}\n")
        f.write(f"Тип розподілу ймовірностей: {uniformity}\n")
        f.write("=" * 50 + "\n")

print("Результати характеристик послідовностей збережено у файл: results_sequence.txt")