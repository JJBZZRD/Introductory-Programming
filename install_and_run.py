import subprocess
import platform

try:
# Install NumPy and Pandas
    subprocess.run(["pip", "install", "numpy", "pandas"])

    # Install Tkinter based on the operating system
    if platform.system() == "Windows":
        subprocess.run(["pip", "install", "tk"])
        # On Windows, Tkinter is included with Python
    elif platform.system() == "Darwin":
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"])

    elif platform.system() == "Linux":
        # On Linux, install the Tkinter package (python3-tk)
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"])
    else:
        print("Unsupported operating system.")

    # Run the dms.py file
    subprocess.run(["python", "dms.py"])

except:
    subprocess.run(["pip3", "install", "numpy", "pandas"])

    # Install Tkinter based on the operating system
    if platform.system() == "Windows":
        subprocess.run(["pip3", "install", "tk"])
        # On Windows, Tkinter is included with Python
    elif platform.system() == "Darwin":
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"])

    elif platform.system() == "Linux":
        # On Linux, install the Tkinter package (python3-tk)
        subprocess.run(["sudo", "apt-get", "install", "-y", "python3-tk"])
    else:
        print("Unsupported operating system.")

    # Run the dms.py file
    subprocess.run(["python3", "dms.py"]) 