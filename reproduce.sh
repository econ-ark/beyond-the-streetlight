#!/bin/bash

SCPT_DIR=$(cd -- "$( dirname -- "${BASH_SOURCE[0]}" )" &> /dev/null && pwd)

cd "$SCPT_DIR"

mamba env update -f binder/environment.yml
source activate rs100_discussion

ipython *.ipynb

python code/main/reproduce.py



