import os
import sys
import subprocess

def bundle_script(script_path, output_directory="dist"): # to check if PyInstaller is installed
    try:
        import PyInstaller
    except ImportError:
        print("PyInstaller is not installed. Please run 'pip install pyinstaller' first.")
        sys.exit(1)

    
    if not os.path.isfile(script_path): # if script path present
        print(f"Script file '{script_path}' not found.")
        sys.exit(1)

    if not os.path.exists(output_directory): # if output directory exists
        os.makedirs(output_directory)

    
    command = [
        "pyinstaller",
        "--onefile", 
        f"--name={os.path.splitext(os.path.basename(script_path))[0]}",  
        f"--distpath={output_directory}", 
        script_path
    ]

    try:
        subprocess.run(command, check=True)
        print(f"Binary created successfully in the '{output_directory}' directory.")
    except subprocess.CalledProcessError:
        print("Failed to create the binary.")
        sys.exit(1)

if __name__ == "__main__":
    script_path = "compiler.py"  #your path
    bundle_script(script_path)
