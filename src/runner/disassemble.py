import os.path, logging, subprocess
from itertools import product
from pathlib import Path

from src.runner.compiler import GnuCompilerCollection, OptimizationLevel, Msvc, Clang

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)
from src.runner.validation import validate_response


def disassemble(source_path) -> str:
    validate_response(subprocess.run(["strip", source_path], capture_output=True))
    res = subprocess.run(["objdump", "--no-addresses", "--no-show-raw-insn", "-M intel", "-d", source_path],
                         capture_output=True)
    validate_response(res)
    raw_output_lines = res.stdout.decode().split('\n')
    idx = 0
    # assumes we'll always have <.text in the diassembly
    for idx, line in enumerate(raw_output_lines):
        if '<.text' in line:
            break
    normalized_output = '\n'.join(raw_output_lines[idx + 1:])
    return normalized_output


def get_source_paths():
    source_dir = os.path.abspath('../native/functions')
    return [Path(source_dir, file_name)
            for file_name in os.listdir(source_dir) if file_name.endswith(".c")]


def produce_diassemblies():
    logger.setLevel(logging.INFO)

    out_dir = os.path.abspath('../../out')
    object_dir = Path(out_dir, 'objects')
    disassembly_dir = Path(out_dir, 'disassembly')
    os.makedirs(disassembly_dir, exist_ok=True)
    os.makedirs(object_dir, exist_ok=True)
    source_paths = get_source_paths()

    compilers = [GnuCompilerCollection(), Msvc(), Clang()]

    try:
        for source_path, optimization_level, compiler in product(source_paths, [o for o in OptimizationLevel], compilers):
            object_file = compiler.compile(source_path,
                                      object_dir, optimization_level)
            logger.info(f"object_file={object_file}")
            disassembly = disassemble(object_file)
            logger.info(f"object_file={object_file}, disassembly={disassembly}")
            base_filename = os.path.basename(object_file).split(".")[0]
            asm_filename = f"{base_filename}_{compiler.compiler_type().name.lower()}_{optimization_level.name}.asm"
            disassembly_path = Path(disassembly_dir, asm_filename)
            logger.info(f"disassembly_path={disassembly_path}")
            disassembly_file = open(disassembly_path, 'w')
            disassembly_file.write(disassembly)
            disassembly_file.close()


    except RuntimeError as e:
        logger.error("Failed to process source files", exc_info=e)


if __name__ == "__main__":
    produce_diassemblies()
