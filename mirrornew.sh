#!/bin/bash
sleep 2
# Activate Python virtual environment
source /home/hitech/smart-mirror/.venv/bin/activate
export DISPLAY=:0
# Start Magic Mirror
npm start -- --no-sandbox --prefix /home/hitech/MagicMirrornew


