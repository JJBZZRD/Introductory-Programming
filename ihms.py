import subprocess
import platform

if platform.system() in ["Windows", "Darwin"]:
    try:
        subprocess.run(["pip", "install", "numpy"])
    except:
        subprocess.run(["pip3", "install", "numpy"])
    finally:
        subprocess.run(["pip3", "install", "numpy"])
    try:
        subprocess.run(["pip", "install", "pandas"])
    except:
        subprocess.run(["pip3", "install", "pandas"])
    finally:
        subprocess.run(["pip3", "install", "pandas"])
    try:
        subprocess.run(["pip", "install", "tk"])
    except:
        subprocess.run(["pip3", "install", "tk"])
    finally:
        subprocess.run(["pip3", "install", "tk"])
    try:
        subprocess.run(["python3", "temp.py"]) 
    except:
        subprocess.run(["python", "temp.py"])
    finally:
        subprocess.run(["python", "temp.py"])

elif platform.system() == "Linux":
    try:
        subprocess.run(["sudo", "apt", "update"])
    except:
        print("Looks like your system is faulty. Please use a proper Linux distro.")
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
            print("Trying Python 3")
            subprocess.run(["python3", "temp.py"])
        except Exception as e:
            print(e)
            print("Trying Python in except")
            subprocess.run(["python", "temp.py"])
        finally:
            print("Trying Python in finally")
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
            try:
                subprocess.run(["python", "temp.py"])
            except:
                print("Looks like your system is faulty. Please use a proper Linux distro.")
            finally:
                subprocess.run(["python", "temp.py"])