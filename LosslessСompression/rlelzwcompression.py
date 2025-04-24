import collections
import math
import matplotlib.pyplot as plt

# === Дані ===
N_sequence = 100
BIT_PER_SYMBOL = 16
ORIGINAL_BIT_SIZE = N_sequence * BIT_PER_SYMBOL

# === Зчитування з файла ===
with open("sequence.txt", "r", encoding="utf-8") as file:
    original_sequences = [line.strip() for line in file.readlines()]

# === Обчислення ентропії ===
def calculate_entropy(probabilities):
    return -sum(p * math.log2(p) for p in probabilities.values())

# === RLE Кодування ===
def encode_rle(sequence):
    result = []
    count = 1
    for i in range(1, len(sequence)):
        if sequence[i] == sequence[i - 1]:
            count += 1
        else:
            result.append((sequence[i - 1], count))
            count = 1
    result.append((sequence[-1], count))
    encoded = ''.join(f"{count}{char}" for char, count in result)
    return encoded, result

# === RLE Декодування ===
def decode_rle(encoded_tuples):
    return ''.join(char * count for char, count in encoded_tuples)

# === LZW Кодування ===
def encode_lzw(sequence):
    dictionary = {chr(i): i for i in range(65536)}
    current = ""
    result = []
    total_bits = 0
    entries = []

    for char in sequence:
        new_str = current + char
        if new_str in dictionary:
            current = new_str
        else:
            code = dictionary[current]
            bits = 16 if code < 65536 else math.ceil(math.log2(len(dictionary)))
            total_bits += bits
            result.append(code)
            entries.append((code, current, bits))
            dictionary[new_str] = len(dictionary)
            current = char

    if current:
        code = dictionary[current]
        bits = 16 if code < 65536 else math.ceil(math.log2(len(dictionary)))
        total_bits += bits
        result.append(code)
        entries.append((code, current, bits))

    return result, total_bits, entries

# === LZW Декодування ===
def decode_lzw(encoded):
    dictionary = {i: chr(i) for i in range(65536)}
    result = []

    prev_code = encoded[0]
    result.append(dictionary[prev_code])
    next_code = 65536

    for code in encoded[1:]:
        if code in dictionary:
            entry = dictionary[code]
        elif code == next_code:
            entry = dictionary[prev_code] + dictionary[prev_code][0]
        else:
            entry = '?'

        result.append(entry)
        dictionary[next_code] = dictionary[prev_code] + entry[0]
        next_code += 1
        prev_code = code

    return ''.join(result)

results = []

# === Формування звіту ===
with open("results_rle_lzw.txt", "w", encoding="utf-8") as f:
    for idx, sequence in enumerate(original_sequences):
        f.write("Приклад реалізації:\n")
        f.write("/" * 80 + "\n")
        f.write(f"Оригінальна послідовність: {sequence}\n")
        f.write(f"Розмір оригінальної послідовності: {ORIGINAL_BIT_SIZE} bits\n")

        counts = collections.Counter(sequence)
        probabilities = {char: count / N_sequence for char, count in counts.items()}
        entropy = calculate_entropy(probabilities)
        f.write(f"Ентропія: {entropy:.4f}\n\n")

        # --- RLE ---
        f.write("__________Кодування RLE__________\n")
        encoded_rle, encoded_tuples = encode_rle(sequence)
        decoded_rle = decode_rle(encoded_tuples)
        encoded_rle_bits = len(encoded_rle) * 16
        cr_rle = round(ORIGINAL_BIT_SIZE / encoded_rle_bits, 2) if encoded_rle_bits > 0 else "-"
        if cr_rle != "-" and cr_rle < 1:
            cr_rle = "-"

        f.write(f"Закодована RLE послідовність: {encoded_rle}\n")
        f.write(f"Розмір закодованої RLE послідовності: {encoded_rle_bits} bits\n")
        f.write(f"Коефіцієнт стиснення RLE: {cr_rle}\n")
        f.write(f"Декодована RLE послідовність: {decoded_rle}\n")
        f.write(f"Розмір декодованої RLE послідовності: {ORIGINAL_BIT_SIZE} bits\n\n")

        # --- LZW ---
        f.write("__________Кодування LZW__________\n")
        f.write("Словник:\n")
        encoded_lzw, total_bits_lzw, entries = encode_lzw(sequence)

        for code, text, bits in entries:
            f.write(f"Code: {code}, Element: {text}, Bits: {bits}\n")

        cr_lzw = round(ORIGINAL_BIT_SIZE / total_bits_lzw, 2) if total_bits_lzw > 0 else "-"
        if cr_lzw != "-" and cr_lzw < 1:
            cr_lzw = "-"

        decoded_lzw = decode_lzw(encoded_lzw)
        lzw_encoded_str = ''.join(str(code) for code in encoded_lzw)

        f.write(f"\nЗакодована LZW послідовність: {lzw_encoded_str}\n")
        f.write(f"Розмір закодованої LZW послідовності: {total_bits_lzw} bits\n")
        f.write(f"Коефіцієнт стиснення LZW: {cr_lzw}\n")
        f.write(f"Декодована LZW послідовність: {decoded_lzw}\n")
        f.write(f"Розмір декодованої LZW послідовності: {ORIGINAL_BIT_SIZE} bits\n")
        f.write("/" * 80 + "\n\n")

        results.append([
            round(entropy, 2),
            cr_rle if cr_rle != "-" else 0,
            cr_lzw if cr_lzw != "-" else 0
        ])

# === Побудова таблиці з результатами ===
fig, ax = plt.subplots(figsize=(14 / 1.54, len(results) / 1.54))
headers = ['Ентропія', 'КС RLE', 'КС LZW']
rows = [f"Послідовність {i+1}" for i in range(len(results))]

ax.axis('off')
table = ax.table(cellText=results, colLabels=headers, rowLabels=rows, loc='center', cellLoc='center')
table.set_fontsize(14)
table.scale(0.8, 2)
fig.savefig("Результати стиснення методами RLE та LZW.png")

print("Усі результати збережено у 'results_rle_lzw.txt'")
print("Таблиця збережена у 'Результати стиснення методами RLE та LZW.png'")