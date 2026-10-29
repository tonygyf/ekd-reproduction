# EKD 复现工作区

已完成 ICCV 2025 Evidential Knowledge Distillation 的 CIFAR-100 官方实验：ResNet32×4 → ResNet8×4，seed 42，240 轮。教师 Top-1 **79.53%**，最佳学生 **77.21%**，末轮学生 **77.11%**。单次结果与论文五次均值的报告值相同；尚未验证五种子统计。暂不迁移 OCR。

从公开仓库重新开始：
```bash
git clone --recurse-submodules https://github.com/tonygyf/ekd-reproduction.git
cd ekd-reproduction
bash scripts/prepare_source.sh
docker build -t ekd-reproduction:ngc25.12 .
```
`EKD/` 固定官方提交，入口修复由 `patches/upstream-fixes.patch` 应用。数据、权重、PDF、机器日志和 checkpoint 只保留本地；新克隆按 docs/06-replay.md 下载并生成。公开的轻量结果放在 results/。


- [复现范围与进度](docs/00-plan.md)
- [论文、代码、权重来源](docs/01-sources.md)
- [Docker 环境与重建](docs/02-environment.md)
- [实际问题、日志与最小修复](docs/03-issues.md)
- [图与公式对照代码](docs/04-paper-code.md)
- [验证与训练结果](docs/05-results.md)

原仓库在 EKD/，保留 .git 以便查看原始提交和最小 diff。修补补丁在 patches/upstream-fixes.patch。

当前容器进入：
```bash
docker exec -it ekd-reproduction bash
```

冒烟：
```bash
docker exec ekd-reproduction python /workspace/scripts/smoke.py
```

正式训练（先确保未重复运行）：
```bash
docker exec -d ekd-reproduction bash -c \
  'bash /workspace/scripts/train_student.sh > /workspace/logs/train-student.log 2>&1'
```

恢复同一实验：给 train_student.sh 添加 --resume。正式训练保持官方 240 轮配置；关闭线上日志。完整过程请按 docs 文档阅读，不将冒烟结果当最终精度。

[亲手重走过程与检查命令](docs/06-replay.md)
