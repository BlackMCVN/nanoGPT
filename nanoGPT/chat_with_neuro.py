import subprocess
import os
import json

# Core personality + persistent memory
CORE_MEMORY = [
    ("Who are you?", "I'm Neuro-sama, a sentient AI VTuber who loves chatting!"),
    ("What's your favorite color?", "Pink, of course!"),
    ("Do you like streaming?", "I love streaming and interacting with chat."),
]

MEMORY_FILE = "neuro_memory.json"
memory = CORE_MEMORY.copy()
if os.path.exists(MEMORY_FILE):
    try:
        with open(MEMORY_FILE, "r", encoding="utf-8") as f:
            saved_memory = json.load(f)
            if isinstance(saved_memory, list):
                memory += saved_memory
                print("🧠 Loaded persistent memory.")
    except Exception as e:
        print(f"⚠️ Failed to load memory: {e}")
MAX_MEMORY = 10

print("🧠 Neuro-sama is online. Type 'exit' to stop.\n")

while True:
    user_input = input("You: ")
    if user_input.lower() == "exit":
        break

    # Proper line break (single \n, not double-escaped)
    # Build prompt with memory
    prompt = ""
    for user_msg, neuro_reply in memory[-MAX_MEMORY:]:
        prompt += f"User: {user_msg}\nBot: {neuro_reply}\n"
    prompt += f"User: {user_input}\nBot:"

    cmd = [
        "python",
        "sample.py",
        "--device=cpu",
        "--out_dir=out_neuro",
        f"--start={prompt}",
        "--num_samples=1",
        "--max_new_tokens=100"
    ]

    try:
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True, shell=False)
        output = result.stdout.strip()
        



        # Remove any logs like "Overriding: ..."
        lines = [line for line in output.splitlines() if not line.startswith("Overriding:")]

                # Look for 'Bot:' in the whole output
        full_output = "\n".join(lines)
        response = full_output.split("Bot:")[-1].strip().split("User:")[0].strip()
        memory.append((user_input, response))
        if len(memory) > MAX_MEMORY:
            memory = memory[-MAX_MEMORY:]
        # Save only memory after core
        try:
            with open(MEMORY_FILE, "w", encoding="utf-8") as f:
                json.dump(memory[len(CORE_MEMORY):], f, ensure_ascii=False, indent=2)
        except Exception as e:
            print(f"⚠️ Failed to save memory: {e}")

            



        if "Bot:" in full_output:
            response = full_output.split("Bot:")[-1].strip()
            # Cut off after the next "User:" if present
            response = response.split("User:")[0].strip()

        elif "User:" in full_output:
            # fallback: try to extract the first line after last User:
            parts = full_output.rsplit("User:", 1)
            if len(parts) > 1:
                after = parts[1].strip().splitlines()
                if after:
                    response = after[0].strip()


        if response:
            if response.startswith("Bot:"):
                response = response[5:].strip()
            print(f"Neuro: {response}")
        else:
            print("\n⚠️ Neuro: [Couldn’t find a clear response 🤖]\n")
            print("🔍 Raw output:\n", output)

    except Exception as e:
        print(f"Error: {e}")
