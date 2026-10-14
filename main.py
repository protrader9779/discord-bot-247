import subprocess
import sys

# Teeno selfbot scripts ki list jo ek sath chalengi
scripts = ["selfbot.py", "selfbot2.py", "selfbot3.py"]

processes = []
for script in scripts:
    p = subprocess.Popen([sys.executable, script])
    processes.append(p)

for p in processes:
    p.wait()
