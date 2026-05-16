from pathlib import Path

# Master routing
file_a = Path("test_sessions/routing_master_on.ses")
file_b = Path("test_sessions/routing_master_off.ses")

block_size = 212

data_a = file_a.read_bytes()
data_b = file_b.read_bytes()

differences = []

for i in range(min(len(data_a), len(data_b))):
    if data_a[i] != data_b[i]:
        block = i // block_size
        pos = i % block_size
        differences.append((i, block, pos, data_a[i], data_b[i]))

print("ShowBridge Test Diff")
print("File A:", file_a.name)
print("File B:", file_b.name)
print("Total differences:", len(differences))
print()

for offset, block, pos, a, b in differences[:300]:
    print(f"Offset {offset} | Block {block} | Pos {pos} | {a} -> {b}")