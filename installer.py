import subprocess
from os import system, path


if __name__ == "__main__":
    print("\nBefore downloading program files, make sure git is accessible from command line\n")

    system('pause')

    if not path.exists("tic-tac-toe-ai") and not path.exists("../tic-tac-toe-ai"):
        print("Downloading program files...")
        dl_program = subprocess.Popen("git clone https://github.com/Miguel-Antoons/Python_project.git", shell=True)
        dl_program.wait()
        print("\nDone")

    else:
        print("program files already exist")

    system("python ./tic-tac-toe-ai/installation.py 1")
