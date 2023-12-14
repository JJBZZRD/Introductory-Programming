import subprocess
import platform

try:
    subprocess.run(["pip", "install", "numpy", "pandas"])

    if platform.system() == "Windows":
        subprocess.run(["pip", "install", "tk"])
    elif platform.system() == "Darwin":
        subprocess.run(["pip", "install", "tk"])
    elif platform.system() == "Linux":
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"])

    subprocess.run(["python", "temp.py"])
except:
    subprocess.run(["pip3", "install", "numpy", "pandas"])
    if platform.system() == "Windows":
        subprocess.run(["pip3", "install", "tk"])
    elif platform.system() == "Darwin":
        subprocess.run(["pip3", "install", "tk"])
    elif platform.system() == "Linux":
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"])

    subprocess.run(["python3", "temp.py"]) 