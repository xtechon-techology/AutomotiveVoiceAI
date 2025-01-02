#!/bin/bash

echo "Installing required libraries..."

apt-get update && apt-get install -y \
    libasound2 \
    libstdc++6 \
    libgcc1 \
    libffi7

echo "Starting the application..."

python -m streamlit run UI/demo_v3.py --server.port=8000 --server.address=0.0.0.0
