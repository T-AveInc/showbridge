from pathlib import Path

file_a = Path("test_sessions/ch1only_muted.ses")
file_b = Path("test_sessions/ch2only_muted.ses")

data_a = file_a.read_bytes()
data_b = file_b.read_bytes()

differences = []

block_size = 212

for i in range(min(len(data_a), len(data_b))):

    if data_a[i] != data_b[i]:

        block = i // block_size
        pos = i % block_size

        differences.append((i, block, pos, data_a[i], data_b[i]))

print()

target_block = 2161

for offset, block, pos, a, b in differences:

    if block == target_block:

        print(
            f"Offset {offset} | "
            f"Block {block} | "
            f"Pos {pos} | "
            f"{a} -> {b}"
        )
