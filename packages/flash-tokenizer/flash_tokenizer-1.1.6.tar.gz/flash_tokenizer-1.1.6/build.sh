#!/bin/bash
environments=("python39:3.9" "python310:3.10" "python311:3.11" "python312:3.12")

for env in "${environments[@]}"; do
  IFS=":" read name version <<< "$env"
  conda create -n "$name" python="$version" -y
done

for env in python39 python310 python311 python312; do
  conda activate "$env"
done

pip install build twine pybind11 numpy==1.26.4 setuptools wheel --no-warn-script-location
python -m build
