#!/usr/bin/env bash
set -e

CONTAINER=as-emb
IMAGE=cosc_592_as_emb
HOST_HF_CACHE="${HF_HOME:-$HOME/.cache/huggingface}"


mkdir -p out
rm -rf out/*

if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "Starting existing container..."
    exec docker start -ai "$CONTAINER"
else
    echo "Creating new container..."
    exec docker run \
        -e HF_HOME=/workspace/.cache/huggingface \
        --user $(id -u):$(id -g) \
        --name "$CONTAINER" \
        --gpus all \
        -v "$(pwd)/out:/workspace/out" \
        -v "$HOST_HF_CACHE:/workspace/.cache/huggingface" \
        -v "$(pwd)/config:/workspace/config" \
        "$IMAGE" \
        python -m src.runner.main
fi