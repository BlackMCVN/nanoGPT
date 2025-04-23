import pickle
import os
from model import GPTConfig

config = GPTConfig(
    block_size=64,
    vocab_size=74,       # Match your meta.pkl
    n_layer=6,
    n_head=6,
    n_embd=384,
    dropout=0.1,
    bias=True
)

config.dataset = "neuro"  # needed for loading meta.pkl

out_dir = "out_neuro"
os.makedirs(out_dir, exist_ok=True)
with open(os.path.join(out_dir, "config.pkl"), "wb") as f:
    pickle.dump(config, f)

print("✅ config.pkl saved to", out_dir)
