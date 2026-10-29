# Docker 环境

- 系统检查：4 张 RTX 6000D，单卡约 84 GiB，compute capability 12.0；驱动 595.91.07。
- Docker 29.1.3，无需在宿主安装 Python 库。
- 复用本机 NVIDIA NGC 25.12 PyTorch 镜像，digest 固定在 Dockerfile；支持该 Blackwell GPU，矩阵乘法实测通过。
- 实际：Python 3.12 / torch 2.10.0a0+b4e4ee81d3.nv25.12 / torchvision 0.25.0a0+ca221243。
- 作者：Python 3.10 / torch 2.8.0。README 明确允许使用与硬件匹配的 PyTorch。本次是硬件兼容复现，非逐包相同环境。
- 作者 requirements.txt 包含 SSH editable 自安装和全部 CUDA 包，未直接照抄覆盖 NGC；只补充入口所需的 yacs、tensorboardX、swanlab，gdown 用于作者权重下载。
- 完整环境冻结：artifacts/pip-freeze.txt；安装日志：logs/install.log。
- 当前容器：ekd-reproduction，bind mount 项目到 /workspace，宿主 GPU 1，8 GiB shared memory，8 OpenMP 线程。
- 远程实验日志关闭（LOG.WANDB False），输出保存本地。

重建：
```bash
cd /home/gyf/ekd-reproduction
docker build -t ekd-reproduction:ngc25.12 .
docker run -d --name ekd-reproduction-new --gpus device=1 --shm-size 8g \
  -v "$PWD:/workspace" ekd-reproduction:ngc25.12
```
代码通过 PYTHONPATH 加载，无需重复从 SSH 安装。
