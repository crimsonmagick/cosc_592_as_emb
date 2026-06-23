import os.path
import subprocess
from abc import ABC, abstractmethod
from enum import Enum
from pathlib import Path

from src.runner.validation import validate_response


class CompilerType(Enum):
    GCC = "gcc"
    CLANG = "clang"
    MSVC = "msvc"


class OptimizationLevel(Enum):
    OFF = 1
    MAX = 2
    SIZE = 3


class Compiler(ABC):

    def compile(self, file_path, out_dir, optimization_level: OptimizationLevel) -> Path:
        if not file_path or not out_dir or not optimization_level:
            raise TypeError("file_path, out_dir, and optimization_level are all required")
        file_name = os.path.basename(file_path)
        out_file_name = file_name.split('.')[0] + '.obj'
        out_path = Path(out_dir, out_file_name).resolve()
        os.makedirs(os.path.dirname(out_path), exist_ok=True)

        res = subprocess.run(self._compile_command(file_path, out_path, optimization_level), capture_output=True)
        validate_response(res)
        return out_path

    @abstractmethod
    def compiler_type(self):
        pass

    @abstractmethod
    def _compile_command(self, file_path, out_path, optimization_level):
        pass


class GnuCompilerCollection(Compiler):

    def compiler_type(self):
        return CompilerType.GCC

    def _compile_command(self, file_path, out_path, optimization_level):
        if optimization_level is OptimizationLevel.OFF:
            opt_literal = "-O0"
        elif optimization_level is OptimizationLevel.SIZE:
            opt_literal = "-Os"
        elif optimization_level is OptimizationLevel.MAX:
            opt_literal = "-O3"
        else:
            raise RuntimeError("Unsupported OptimizationLevel, optimizationLevel=" + optimization_level.name)
        return ["gcc", "-c", file_path, "-o", out_path, opt_literal, "-fno-builtin"]


class Msvc(Compiler):

    def compiler_type(self):
        return CompilerType.MSVC

    def _compile_command(self, file_path, out_path, optimization_level):
        if optimization_level is OptimizationLevel.OFF:
            opt_literal = "/Od"
        elif optimization_level is OptimizationLevel.SIZE:
            opt_literal = "/O1"
        elif optimization_level is OptimizationLevel.MAX:
            opt_literal = "/O2"
        else:
            raise RuntimeError("Unsupported OptimizationLevel, optimizationLevel=" + optimization_level.name)
        return ["cl", "/c", file_path, f"/Fo:{out_path}", opt_literal, "/Oi-", "/Ob0"]


class Clang(Compiler):

    def compiler_type(self):
        return CompilerType.CLANG

    def _compile_command(self, file_path, out_path, optimization_level):
        if optimization_level is OptimizationLevel.OFF:
            opt_literal = "-O0"
        elif optimization_level is OptimizationLevel.SIZE:
            opt_literal = "-Os"
        elif optimization_level is OptimizationLevel.MAX:
            opt_literal = "-Oz"
        else:
            raise RuntimeError("Unsupported OptimizationLevel, optimizationLevel=" + optimization_level.name)
        return ["clang", "-c", file_path, "-o", out_path, opt_literal, "-fno-builtin"]
