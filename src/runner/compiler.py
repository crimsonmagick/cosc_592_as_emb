import os.path
import subprocess
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path


class CompilerType(Enum):
    GCC = "gcc"
    CLANG = "clang"
    MINGW = "mingw"


class OptimizationLevel(Enum):
    OFF = 1
    MAX = 2
    SIZE = 3


class Compiler(ABC):

    @abstractmethod
    def compile(self, file_path, out_dir, optimization_level) -> str:
        pass


class GnuCompilerCollection(Compiler):

    def compile(self, file_path, out_dir, optimization_level) -> Path:
        if not file_path or not out_dir or not optimization_level:
            raise TypeError("file_path, out_dir, and optimization_level are all required")
        file_name = os.path.basename(file_path)
        out_file_name = file_name.split('.')[0] + '.o'
        out_path = Path(out_dir, out_file_name)
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        res = subprocess.run(["gcc", "-c", file_path, "-o", out_path])
        if res.returncode != 0:
            raise RuntimeError(f"GCC returned code {res.returncode}")
        return out_path
