FROM nvcr.io/nvidia/pytorch@sha256:b5541f591b87e68d3883040bfdbf89707bd6f80e2e38b95411c9ff3e1cb63eeb
RUN python -m pip install --no-cache-dir yacs==0.1.8 tensorboardX==2.6.4 swanlab==0.6.8 gdown==5.2.0
ENV PYTHONPATH=/workspace/EKD OMP_NUM_THREADS=8 SWANLAB_MODE=disabled
WORKDIR /workspace/EKD
CMD ["sleep", "infinity"]
