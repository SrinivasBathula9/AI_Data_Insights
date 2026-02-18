import subprocess
import os

def run_git(cmd):
    print(f"Running: {cmd}")
    try:
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True, cwd=os.getcwd())
        print(f"STDOUT: {result.stdout}")
        print(f"STDERR: {result.stderr}")
        return result.stdout + result.stderr
    except Exception as e:
        print(f"Exception: {str(e)}")
        return str(e)

commands = [
    "git status",
    "git remote -v",
    "git add .",
    "git commit -m \"Final attempt: Add all files\"",
    "git push -u origin main"
]

output = ""
for cmd in commands:
    output += f"\n--- {cmd} ---\n"
    output += run_git(cmd)

with open("git_output.txt", "w") as f:
    f.write(output)
