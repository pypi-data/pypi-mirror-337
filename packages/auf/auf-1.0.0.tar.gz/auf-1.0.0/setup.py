import sys
import subprocess
from setuptools import setup, find_packages

if __name__ == '__main__':
    # Предустановка lightgbm перед основной установкой
    subprocess.check_call([
        sys.executable, "-m", "pip", "install",
        "lightgbm>=3.3.5",
        "--config-settings=cmake.define.USE_OPENMP=OFF"
    ])
    setup()
