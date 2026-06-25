import logging
import os.path
from itertools import product
from pathlib import Path

from src.runner.disassembly import disassemble
from src.runner.embedding import generate_embeddings
from src.runner.heatmap import generate_heatmaps
from src.runner.compiler import GnuCompilerCollection, OptimizationLevel, Msvc, Clang

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)


def get_source_paths():
    source_dir = os.path.abspath('src/native/functions')
    return [Path(source_dir, file_name)
            for file_name in os.listdir(source_dir) if file_name.endswith(".c")]


def run_experiment():
    logger.setLevel(logging.INFO)

    out_dir = os.path.abspath('out')
    object_dir = Path(out_dir, 'objects')
    heatmap_dir = Path(out_dir, 'heatmaps')
    disassembly_dir = Path(out_dir, 'disassembly')
    os.makedirs(disassembly_dir, exist_ok=True)
    os.makedirs(object_dir, exist_ok=True)
    os.makedirs(heatmap_dir, exist_ok=True)

    source_paths = get_source_paths()
    function_names = [source_path.stem for source_path in source_paths]
    compilers = [GnuCompilerCollection(), Msvc(), Clang()]
    optimization_levels = [o for o in OptimizationLevel]

    disassemblies = []

    try:
        for source_path, compiler, optimization_level in product(source_paths, compilers, optimization_levels):
            object_file = compiler.compile(source_path,
                                           object_dir, optimization_level)
            disassembly = disassemble(object_file, strip=True)
            logger.debug(f"object_file={object_file}, disassembly={disassembly}")

            disassemblies.append(disassembly)

            # generate assembly files for debugging purposes
            disassembly_id = f"{object_file.stem}_{compiler.compiler_type().name.lower()}_{optimization_level.name}"
            asm_filename = f"{disassembly_id}.asm"
            disassembly_path = Path(disassembly_dir, asm_filename)
            disassembly_file = open(disassembly_path, 'w')
            disassembly_file.write(disassembly)
            disassembly_file.close()
            logger.info(f"asm file written, disassembly_path={disassembly_path}")

    except RuntimeError as e:
        logger.error("Failed to process source files", exc_info=e)
        raise e

    for model_name in ["mchochlov/codebert-base-cd-ft", "bigcode/starcoder2-7b", "Qwen/Qwen3-Embedding-0.6B",
                       "Qwen/Qwen3-Embedding-4B", "Qwen/Qwen3-Embedding-8B"]:
        embeddings = generate_embeddings(model_name, disassemblies, batch_size=4)
        group_size = len(compilers) * len(optimization_levels)
        generate_heatmaps(embeddings, model_name=model_name, function_names=function_names, group_size=group_size, out_dir=heatmap_dir)


if __name__ == "__main__":
    run_experiment()
