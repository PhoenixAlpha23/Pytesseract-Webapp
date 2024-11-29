import subprocess

subprocess.run(["pip", "install", "--upgrade", "pip", "setuptools", "wheel"])
subprocess.run(["pip", "install", "-r", "requirements.txt"])
