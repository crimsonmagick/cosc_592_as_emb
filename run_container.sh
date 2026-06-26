#!/usr/bin/env bash
set -e

CONTAINER=as-emb
IMAGE=cosc_592_as_emb
HOST_HF_CACHE="${HF_HOME:-$HOME/.cache/huggingface}" # re-use host cache if possible, cache across image builds and containers
VM_HF_CACHE=/workspace/.cache/huggingface

mkdir -p out
rm -rf out/*

if docker ps -a --format '{{.Names}}' | grep -qx "$CONTAINER"; then
    echo "Starting existing container..."
    exec docker start -ai "$CONTAINER"
else
    echo "Creating new container..."
    exec docker run \
        --user $(id -u):$(id -g) \
        --name "$CONTAINER" \
        -e HF_HOME=$VM_HF_CACHE \
        -v "$HOST_HF_CACHE:$VM_HF_CACHE" \
        -v "$(pwd)/config:/workspace/config" \
        -v "$(pwd)/out:/workspace/out" \
        --gpus all \
        "$IMAGE" \
        python -m src.runner.main
fi