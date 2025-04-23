import os
import pickle
import numpy as np
from tqdm import tqdm

input_file_path = "data/neuro/input.txt"
with open(input_file_path, "r", encoding="utf-8") as f:
    data = f.read()

# get all the unique characters in the dataset
chars = sorted(list(set(data)))
vocab_size = len(chars)
print("Unique chars:", "".join(chars))
print("Vocab size:", vocab_size)

# create a mapping from characters to integers
stoi = {ch: i for i, ch in enumerate(chars)}
itos = {i: ch for ch, i in stoi.items()}
encode = lambda s: [stoi[c] for c in s]
decode = lambda l: "".join([itos[i] for i in l])

# create the train and test splits
n = len(data)
train_data = data[:int(n * 0.9)]
val_data = data[int(n * 0.9):]

train_ids = encode(train_data)
val_ids = encode(val_data)
print(f"Train has {len(train_ids)} tokens")
print(f"Val has {len(val_ids)} tokens")

# export to bin files
train_ids = np.array(train_ids, dtype=np.uint16)
val_ids = np.array(val_ids, dtype=np.uint16)
train_ids.tofile("data/neuro/train.bin")
val_ids.tofile("data/neuro/val.bin")

# save meta info
meta = {
    "vocab_size": vocab_size,
    "itos": itos,
    "stoi": stoi,
}
with open("data/neuro/meta.pkl", "wb") as f:
    pickle.dump(meta, f)

print("✅ Preprocessing complete.")
