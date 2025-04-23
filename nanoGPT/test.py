import sys
import os
import subprocess

python_path = os.path.join(os.environ["VIRTUAL_ENV"], "Scripts", "python.exe")
cmd = [
    python_path,
    "sample.py",
    "--device=cpu",
    "--out_dir=out_neuro",
    f"--start={prompt}",
    "--num_samples=1",
    "--max_new_tokens=100"
]


result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
print("OUTPUT:\n", result.stdout)
