@echo off

conda activate python38 && python -m build --wheel && ^
conda activate python39 && python -m build --wheel && ^
conda activate python310 && python -m build --wheel && ^
conda activate python311 && python -m build --wheel && ^
conda activate python312 && python -m build --wheel && ^
conda activate python313 && python -m build --wheel

pause

conda activate python38 && python -m build --wheel && \
conda activate python39 && python -m build --wheel && \
conda activate python310 && python -m build --wheel && \
conda activate python311 && python -m build --wheel && \
conda activate python312 && python -m build  --wheel && \
conda activate python313 && python -m build

