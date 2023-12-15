import subprocess
import platform

if platform.system() in ["Windows", "Darwin"]:
    try:
        subprocess.run(["pip", "install", "numpy", "pandas", "tk"])
    except:
        subprocess.run(["pip3", "install", "numpy", "pandas", "tk"])
    finally:
        try:
            subprocess.run(["python3", "temp.py"]) 
        except:
            subprocess.run(["python", "temp.py"])
elif platform.system() == "Linux":
    try:
        subprocess.run(["sudo", "apt-get", "install", "python3-pandas"])
    except:
        subprocess.run(["sudo", "pip", "install", "pandas"])
    try:
        subprocess.run(["sudo", "pip", "install", "numpy"])
    except:
        subprocess.run(["sudo", "apt-get", "install", "python-pip"])
        subprocess.run(["sudo", "pip", "install", "numpy"])
    try:
        subprocess.run(["sudo", "apt-get", "install", "python3-tk"])
    except:
        subprocess.run(["sudo", "apt-get", "install", "python-pip"])
        subprocess.run(["sudo", "pip", "install", "tk"])
    finally:
        try:
            subprocess.run(["python3", "temp.py"])
        except:   
            subprocess.run(["python", "temp.py"])
else:
    try:
        subprocess.run(["pip", "install", "numpy", "pandas", "tk"])
    except:
        subprocess.run(["pip3", "install", "numpy", "pandas", "tk"])
    finally:
        try:
            subprocess.run(["python3", "temp.py"]) 
        except:
            subprocess.run(["python", "temp.py"])