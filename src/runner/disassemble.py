import gc
import logging
import os.path
import subprocess
from itertools import product
from pathlib import Path

import matplotlib.pyplot as plt
import seaborn as sns
import torch
from sentence_transformers import SentenceTransformer
from sentence_transformers.sentence_transformer import modules
from sklearn.metrics.pairwise import cosine_similarity

from src.runner.compiler import GnuCompilerCollection, OptimizationLevel, Msvc, Clang

logging.basicConfig(level=logging.ERROR)
logger = logging.getLogger(__name__)
from src.runner.validation import validate_response


def disassemble(source_path, *, strip: bool) -> str:
    if strip:
        validate_response(subprocess.run(["strip", source_path], capture_output=True))
    res = subprocess.run(["objdump", "--no-addresses", "--no-show-raw-insn", "-M intel", "-d", source_path],
                         capture_output=True)
    validate_response(res)
    raw_output_lines = res.stdout.decode().split('\n')
    idx = 0
    # assumes we'll always have .text in the diassembly
    for idx, line in enumerate(raw_output_lines):
        if '.text' in line:
            break
    normalized_output = '\n'.join(raw_output_lines[idx + 1:])
    return normalized_output


def get_source_paths():
    source_dir = os.path.abspath('../native/functions')
    return [Path(source_dir, file_name)
            for file_name in os.listdir(source_dir) if file_name.endswith(".c")]


def get_model(model_name: str):
    if "starcoder" in model_name:
        word_embedding_model = modules.Transformer(
            model_name,
            max_seq_length=2048
        )
        if word_embedding_model.tokenizer.pad_token is None:
            word_embedding_model.tokenizer.pad_token = word_embedding_model.tokenizer.eos_token
        pooling_model = modules.Pooling(
            word_embedding_model.get_word_embedding_dimension(),
            pooling_mode_mean_tokens=True
        )

        return SentenceTransformer(modules=[word_embedding_model, pooling_model], device="cuda",
                                   model_kwargs={"torch_dtype": torch.bfloat16})
    return SentenceTransformer(model_name, device="cuda", model_kwargs={"torch_dtype": torch.bfloat16})


def produce_diassemblies():
    logger.setLevel(logging.INFO)

    out_dir = os.path.abspath('../../out')
    object_dir = Path(out_dir, 'objects')
    disassembly_dir = Path(out_dir, 'disassembly')
    os.makedirs(disassembly_dir, exist_ok=True)
    os.makedirs(object_dir, exist_ok=True)

    source_paths = get_source_paths()
    function_names = [os.path.basename(source_path).split(".")[0] for source_path in source_paths]
    compilers = [GnuCompilerCollection(), Msvc(), Clang()]

    diassembly_labels = []
    disassemblies = []

    try:
        for source_path, compiler, optimization_level in product(source_paths, compilers,
                                                                 [o for o in OptimizationLevel]):

            object_file = compiler.compile(source_path,
                                           object_dir, optimization_level)
            logger.debug(f"object_file={object_file}")
            disassembly = disassemble(object_file, strip=True)
            logger.debug(f"object_file={object_file}, disassembly={disassembly}")
            base_filename = os.path.basename(object_file).split(".")[0]

            disassembly_id = f"{base_filename}_{compiler.compiler_type().name.lower()}_{optimization_level.name}"
            diassembly_labels.append(disassembly_id)
            disassemblies.append(disassembly)

            asm_filename = f"{disassembly_id}.asm"
            disassembly_path = Path(disassembly_dir, asm_filename)
            logger.debug(f"disassembly_path={disassembly_path}")
            disassembly_file = open(disassembly_path, 'w')
            disassembly_file.write(disassembly)
            disassembly_file.close()
    except RuntimeError as e:
        logger.error("Failed to process source files", exc_info=e)
        raise e

    for model_name in ["mchochlov/codebert-base-cd-ft", "bigcode/starcoder2-7b", "Qwen/Qwen3-Embedding-0.6B",
                       "Qwen/Qwen3-Embedding-4B", "Qwen/Qwen3-Embedding-8B"]:
        if "8B" in model_name:
            batch_size = 4
        else:
            batch_size = 8
        logger.info(f"BEGIN Generating embeddings for {model_name}")
        model = get_model(model_name)
        embeddings = model.encode(disassemblies, batch_size=batch_size)
        logger.info(f"END Generating embeddings for {model_name}, embedding_dim")
        similarities = cosine_similarity(embeddings)

        plt.figure(figsize=(12, 10))

        dis_hm = sns.heatmap(
            similarities,
            cmap="magma",
            xticklabels=False,
            yticklabels=False,
            square=True
        )

        group_size = 9

        for i in range(0, len(similarities) + 1, group_size):
            dis_hm.axhline(i, color="white", linewidth=2)
            dis_hm.axvline(i, color="white", linewidth=2)

        centers = [i * 9 + 4 for i in range(len(function_names))]

        dis_hm.set_xticks(centers)
        dis_hm.set_yticks(centers)

        dis_hm.set_xticklabels(function_names, rotation=45, ha="right")
        dis_hm.set_yticklabels(function_names)

        plt.title(model_name)
        plt.tight_layout()
        plt.show()

        del model
        gc.collect()
        torch.cuda.empty_cache()


if __name__ == "__main__":
    produce_diassemblies()
