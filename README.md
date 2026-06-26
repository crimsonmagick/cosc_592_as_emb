# Semantic Proximity of  Disassembly Artifact Embeddings

## Project Description

This project measures cosine similarity across diassembly embeddings from 10 C files compiled using GCC, Clang, and MSVC.

Embedding models:

- [mchochlov/codebert-base-cd-ft](https://huggingface.co/mchochlov/codebert-base-cd-ft)
- [bigcode/starcoder2-7b](https://huggingface.co/bigcode/starcoder2-7b)
- [Qwen/Qwen3-Embedding-0.6B](https://huggingface.co/Qwen/Qwen3-Embedding-0.6B)
- [Qwen/Qwen3-Embedding-4B](https://huggingface.co/Qwen/Qwen3-Embedding-4B)
- [Qwen/Qwen3-Embedding-8B](https://huggingface.co/Qwen/Qwen3-Embedding-8B)

Codebert and StarCoder2 were selected as models specifically trained for code. StarCoder2 is not specifically an embedding model which may partially explain some less-than-stellar performance. A pooling layer was added to produce the embeddings, but the model wasn't fine-tuned with the pooled embedding vector as an objective.

The Qwen3 Embedding models were selected to demonstrate the effect of increasing parameter count of a generalized modern embedding model.

A Dockerfile and management scripts are provided to facilitate setting up and running the project.

## Project Anatomy

- Native and Python source code can be found under `src`
  - Native code used for the disassembly experiment is under `src/native/functions`
  - Python code running the experiment and loading the models can be found under `src/runner`
    - Main entrance point can be found in `src/runner/main.py`
- Configuration can be found under `config/config.yml`. Models under test and the forward-pass batch-size can be configured there.
- `build_image.sh`, `run_container.sh`, and `remove_container.sh` are provided as management scripts for the Dockerfile build process and the container life cycle.

## Running the Project

### Prerequisites

1. An Nvidia GPU. The project assumes the Cuda runtime. It will not run on CPU or non-Nvidia GPUs without modification.
2. Linux. The project will not run on Windows (outside of WSL) and is not configured to use MPS on Mac.
3. [Docker](https://docs.docker.com/engine/install/)
4. [Nvidia Container Toolkit](https://docs.nvidia.com/datacenter/cloud-native/container-toolkit/latest/install-guide.html)
5. Optional: configure [HF_HOME](https://huggingface.co/docs/huggingface_hub/package_reference/environment_variables#HF_HOME) env variable for a custom model cache directory. The Docker container will otherwise fall back to `~/.cache/huggingface` for caching host-side.

## Building the Docker Image

Run `./build_image.sh`. This will create a Docker image with name `cosc_592_as_emb`. If you make any changes to the code or requirements, you'll need to re-build the image (don't worry, it's an incremental build so it won't be too long.)

The docker image can be removed with the command `docker image rm cosc_592_as_emb` if need be. Note that if you've built a container for the project, you'll need to remove that first.

## Building and Running the Container

Run `./run_container`. This is a convenience script for both building and running the container. The container name is `as-emb`. On initial run the Docker container will be built and the Python application will be run (`python -m src.runner.main.py`).

There are 3 mounted directories:

1. The Huggingface cache directory will be mounted and configured as an environment variable in the container. `HF_HOME` will be mounted if configured host-side, otherwise `~/.cache/huggingface` will be mounted instead.
2. `config`. You can update the configuration in `config/config.yml` without having to rebuild the image.
3. `out`. This is where the generated files are output to.
   - Diassemblies/assembly files: `out/disassembly`
   - Heatmaps: `out/heatmaps`
   - Object files (not intended as a final produced artifact): `out/objects`

**TLDR**: run `./run_container` and if it doesn't explode you should have heatmap png files in `out/heatmaps`.

If you run out of memory while running the container, try reducing batch size to 1 in `config/config.yml` or remove/comment out the larger models.

## Removing the Container
Simply run `./remove_container` or manually run `docker rm as-emb`.
