import shutil
import subprocess
import sys
from pathlib import Path
from time import sleep

# Set the current working dir to parent directory
sys.path.append(Path.cwd().parent.as_posix())

CATALOGS = ("build", "dist")
BUILD_CMD = "python -m setup sdist bdist_wheel".split()


if __name__ == "__main__":
    [shutil.rmtree(i) for i in CATALOGS if Path(i).exists()]
    sleep(1)
    subprocess.run(BUILD_CMD)
