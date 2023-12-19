import subprocess
import platform

if platform.system() in ["Windows", "Darwin"]:
    try:
        print("Trying pip install --upgrade numpy")
        subprocess.run(["pip", "install", "--upgrade", "numpy"])
    except:
        print("Except Trying pip3 install --upgrade numpy")
        subprocess.run(["pip3", "install", "--upgrade", "numpy"])
    finally:
        print("Finally Trying pip3 install --upgrade numpy")
        subprocess.run(["pip3", "install", "--upgrade", "numpy"])
    try:
        print("Trying pip install --upgrade pandas")
        subprocess.run(["pip", "install", "--upgrade", "pandas"])
    except:
        print("Except Trying pip3 install --upgrade pandas")
        subprocess.run(["pip3", "install", "--upgrade", "pandas"])
    finally:
        print("Finally Trying pip3 install --upgrade pandas")
        subprocess.run(["pip3", "install", "--upgrade", "pandas"])
    try: 
        print("Trying pip install tk")
        subprocess.run(["pip", "install", "tk"])
    except:
        print("Except Trying pip3 install tk")
        subprocess.run(["pip3", "install", "tk"])
    finally:
        print("Finally Trying pip3 install tk")
        subprocess.run(["pip3", "install", "tk"])
    try:
        print("Trying Python 3")
        subprocess.run(["python3", "app.py"]) 
    except Exception as e:
        print(e)
        print("Trying Python in except")
        subprocess.run(["python", "app.py"])
    finally:
        try:
            print("Trying Python in finally")
            subprocess.run(["python", "app.py"])
        except:
            pass

elif platform.system() == "Linux":
    try:
        subprocess.run(["sudo", "apt", "update"])
    except:
        print("Looks like your system is faulty. Please use a proper Linux distro.")
    try:
        subprocess.run(["sudo", "apt-get", "install", "python3-pandas"])
    except:
        subprocess.run(["sudo", "pip", "install", "--upgrade", "pandas"])
    try:
        subprocess.run(["sudo", "pip", "install", "--upgrade", "numpy"])
    except:
        subprocess.run(["sudo", "apt-get", "install", "python-pip"])
        subprocess.run(["sudo", "pip", "install", "--upgrade", "numpy"])
    try:
        subprocess.run(["sudo", "apt-get", "install", "python3-tk"])
    except:
        subprocess.run(["sudo", "apt-get", "install", "python-pip"])
        subprocess.run(["sudo", "pip", "install", "tk"])
    finally:
        try:
            print("Trying Python 3")
            subprocess.run(["python3", "app.py"])
        except Exception as e:
            print(e)
            print("Trying Python in except")
            subprocess.run(["python", "app.py"])
        finally:
            print("Trying Python in finally")
            subprocess.run(["python", "app.py"])
else:
    try:
        subprocess.run(["pip", "install", "--upgrade", "numpy", "pandas", "tk"])
    except:
        subprocess.run(["pip3", "install", "--upgrade", "numpy", "pandas", "tk"])
    finally:
        try:
            subprocess.run(["python3", "app.py"]) 
        except:
            try:
                subprocess.run(["python", "app.py"])
            except:
                print("Looks like your system is faulty. Please use a proper Linux distro.")
            finally:
                subprocess.run(["python", "app.py"])