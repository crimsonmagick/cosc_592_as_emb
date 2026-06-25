#!/usr/bin/env bash
set -e

CONTAINER=as-emb
IMAGE=cosc_592_as_emb
HF_CACHE="${HF_HOME:-$HOME/.cache/huggingface}"

if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "Starting existing container..."
    exec docker start -ai "$CONTAINER"
else
    echo "Creating new container..."
    exec docker run \
        --name "$CONTAINER" \
        --gpus all \
        -v "$(pwd)/out:/workspace/out" \
        -v "$HF_CACHE:/root/.cache/huggingface" \
        "$IMAGE" \
        python -m src.runner.main
fi