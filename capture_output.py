import subprocess
import os

with open("out_capture.txt", "w") as f:
    f.write("Starting capture...\n")
    try:
        # Run main.py and capture everything
        result = subprocess.run(["python", "main.py"], capture_output=True, text=True, timeout=30)
        f.write("STDOUT:\n")
        f.write(result.stdout)
        f.write("\nSTDERR:\n")
        f.write(result.stderr)
    except subprocess.TimeoutExpired as e:
        f.write("Timeout expired!\n")
        f.write("STDOUT SO FAR:\n")
        f.write(e.stdout if e.stdout else "")
        f.write("\nSTDERR SO FAR:\n")
        f.write(e.stderr if e.stderr else "")
    except Exception as e:
        f.write(f"Error occurred: {str(e)}\n")
