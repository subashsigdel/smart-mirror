#!/bin/bash
cd /home/hitech/MagicMirrornew/smolvlm-VisionLanguageModel/llama.cpp/build/bin



# Start the server and let systemd track it
./llama-server -hf ggml-org/smolVLM-500M-Instruct-GGUF --port 9090

