import subprocess
import os

def grant_execute_permission(binary_file_path):
    # Check if the binary file exists
    if not os.path.exists(binary_file_path):
        print(f"Error: The binary file '{binary_file_path}' does not exist.")
        return

    # Create a shell script content to grant execute permission
    script_content = f"#!/bin/bash\nchmod +x {binary_file_path}\n"

    # Create a temporary shell script file
    script_file_path = "/tmp/grant_execute_permission_script.sh"
    with open(script_file_path, "w") as script_file:
        script_file.write(script_content)

    # Make the shell script executable
    # subprocess.run(["chmod", "+x", script_file_path])

    subprocess.run(["pip3 install pandas"])
    subprocess.run(["pip3 install np"])

    # Execute the shell script
    # subprocess.run(["/bin/bash", script_file_path])

    # Remove the temporary script file
    os.remove(script_file_path)

if __name__ == "__main__":
    # Replace 'your_binary_file' with the path to your binary file
    binary_file_path = "dms"
    grant_execute_permission(binary_file_path)