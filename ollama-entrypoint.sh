#!/bin/bash

# Run in terminal for executable permissions:
# chmod +x ./ollama-entrypoint.sh

MODEL="LLaVA-LLaMA3:8b"

ollama serve

sleep 5

# Pull the desired model if not already present
if ! ollama list | grep -q "$MODEL"; then
    echo "Pulling model $MODEL..."
    ollama pull "$MODEL"
else
    echo "Model $MODEL already exists."
fi

