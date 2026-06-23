import os.path, logging
from pathlib import Path

from src.runner.compiler import GnuCompilerCollection, OptimizationLevel

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def main():
    logger.setLevel(logging.INFO)
    out_dir = os.path.abspath('../../out')
    source_paths = get_source_paths()
    gcc = GnuCompilerCollection()
    try:
        object_files = []
        for source_path in source_paths:
            object_file = gcc.compile(source_path,
                                      out_dir, OptimizationLevel.OFF)
            object_files.append(object_file)
            logger.info(f"object_file={object_file}")
    except RuntimeError as e:
        logger.error("Failed to compile to object files", exc_info=e)


def get_source_paths():
    source_dir = os.path.abspath('../native/functions')
    return [Path(source_dir, file_name)
            for file_name in os.listdir(source_dir) if file_name.endswith(".c")]


if __name__ == "__main__":
    main()
